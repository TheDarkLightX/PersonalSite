//! Case-study tests added after generation. They do not change the app core.
use application::{authority, v2_contract, wire};
use zeno_fcis_synthesis::finite::v2_composition as c;

fn atom(type_id: u32, variant: i128) -> c::Atom<'static> {
    c::Atom::Sum { type_id, variant: variant as u16 }
}

#[test]
fn all_384_complete_decisions_match_a_separate_policy_model() {
    let contract = v2_contract::Contract::new();
    let descriptor = contract.descriptor();
    let auth = authority(&descriptor).unwrap();
    let mut refused = 0;
    for status in 150..=152 { for first in 160..=163 { for second in 160..=163 {
        for command in 140..=141 { for officer in 160..=163 {
            let inputs = [status, first, second, command, officer];
            let frames = wire(&descriptor, &inputs).unwrap();
            let result = auth.evaluate(c::Raw { state: &frames[0], command: &frames[1], context: &frames[2] });
            let (class, reason, post, release) = if status != 150 {
                (c::Class::Reject, Some(200), [status, first, second], false)
            } else if officer == 160 {
                (c::Class::Reject, Some(201), [status, first, second], false)
            } else if command == 141 {
                (c::Class::CommittedFailure, Some(202), [152, first, second], false)
            } else if officer == first {
                (c::Class::Reject, Some(203), [status, first, second], false)
            } else if first == 160 {
                (c::Class::Accept, None, [150, officer, second], false)
            } else {
                (c::Class::Accept, None, [151, first, officer], true)
            };
            if class != c::Class::Reject && post[0] != 151 && post[2] != 160 {
                assert!(result.result().is_err(), "{inputs:?}");
                refused += 1;
                continue;
            }
            let d = result.result().unwrap_or_else(|e| panic!("{inputs:?}: {e:?}"));
            assert_eq!((d.class(), d.reason()), (class, reason), "{inputs:?}");
            let pre: Vec<_> = (0..3).map(|i| c::Field {
                id: 110 + i as u16, value: atom(if i == 0 { 105 } else { 106 }, inputs[i])
            }).collect();
            assert_eq!(d.pre(), pre);
            assert!(d.effects().is_empty());
            if class == c::Class::Reject {
                assert!(d.post().is_empty() && d.patch().is_empty() && d.outbox().is_empty());
                continue;
            }
            let expected: Vec<_> = (0..3).map(|i| c::Field {
                id: 110 + i as u16, value: atom(if i == 0 { 105 } else { 106 }, post[i])
            }).collect();
            assert_eq!(d.post(), expected);
            let changes: Vec<_> = pre.iter().zip(&expected).filter(|(a,b)| a != b).collect();
            assert_eq!(d.patch().len(), changes.len());
            for (patch, (before, after)) in d.patch().iter().zip(changes) {
                assert_eq!((patch.field, patch.before, patch.after), (before.id, before.value, after.value));
            }
            assert_eq!(d.outbox().len(), usize::from(release));
            if release {
                let out = &d.outbox()[0];
                assert_eq!((out.ordinal, out.channel), (0, 300));
                assert_eq!(out.destination, c::Atom::Text(b"release-desk"));
                assert_eq!(out.idempotency, c::Atom::U128(0));
                assert_eq!(out.payload, vec![
                    c::Field { id: 130, value: atom(106, officer) },
                    c::Field { id: 131, value: atom(106, first) }
                ]);
            }
        }}
    }}}
    assert_eq!(refused, 45);
}

#[test]
fn truncation_trailing_bytes_and_foreign_variants_fail_closed() {
    let contract = v2_contract::Contract::new();
    let descriptor = contract.descriptor();
    let auth = authority(&descriptor).unwrap();
    let original = wire(&descriptor, &[150,160,160,140,161]).unwrap();
    for slot in 0..3 {
        for length in 0..original[slot].len() {
            let mut frames = original.clone();
            frames[slot].truncate(length);
            assert!(auth.evaluate(c::Raw { state: &frames[0], command: &frames[1], context: &frames[2] }).result().is_err());
        }
        let mut frames = original.clone(); frames[slot].push(0);
        assert!(auth.evaluate(c::Raw { state: &frames[0], command: &frames[1], context: &frames[2] }).result().is_err());
    }
    for value in [159, 164, 65535] {
        let frames = wire(&descriptor, &[150,160,160,140,value]).unwrap();
        assert!(auth.evaluate(c::Raw { state: &frames[0], command: &frames[1], context: &frames[2] }).result().is_err());
    }
}
