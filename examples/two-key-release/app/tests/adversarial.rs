//! Adversarial reviewer-authored native probes; added after factory generation.
#![cfg(feature = "sqlite")]
use application::{authority,genesis,v2_contract,wire};
use zeno_fcis_synthesis::finite::{v2_authority::{Authority,Publication,PublicationOutcome},v2_composition as c};
use zeno_fcis_shell_sqlite::{v2::{V2SqliteShell,Error},MemoryDestination};
use zeno_fcis_codec::Hash32;
use zeno_fcis_shell::CommitStatus;

fn raw(w:&[Vec<u8>;3])->c::Raw<'_>{ c::Raw{state:&w[0],command:&w[1],context:&w[2]} }
fn publication<'a>(a:&'a Authority<'_>,w:&'a [Vec<u8>;3])->Publication<'a>{
 match a.publish(raw(w)){PublicationOutcome::Commit(p)=>p,other=>panic!("{other:?}")}
}
#[test]
fn replay_state_and_delivery_boundaries(){
 let contract=v2_contract::Contract::new();let descriptor=contract.descriptor();
 let a=authority(&descriptor).unwrap();let g=genesis().unwrap();
 let gp=match a.publish_genesis(&g){PublicationOutcome::Commit(p)=>p,other=>panic!("{other:?}")};
 let mut db=V2SqliteShell::create_in_memory(&a,gp).unwrap();
 let alice=wire(&descriptor,&[150,160,160,140,161]).unwrap();
 let same=wire(&descriptor,&[150,161,160,140,161]).unwrap();
 let bob=wire(&descriptor,&[150,161,160,140,162]).unwrap();
 let carol_at_genesis=wire(&descriptor,&[150,160,160,140,163]).unwrap();
 let k1=Hash32::new([1;32]);let k2=Hash32::new([2;32]);
 assert_eq!(db.commit(k1,publication(&a,&alice)).unwrap().status(),CommitStatus::Committed);
 let before=db.snapshot().unwrap();
 assert!(matches!(a.publish(raw(&same)),PublicationOutcome::Reject(_)));
 assert!(matches!(db.commit(k1,publication(&a,&carol_at_genesis)),Err(Error::Replay)));
 assert!(matches!(db.commit(k2,publication(&a,&carol_at_genesis)),Err(Error::PreState)));
 assert_eq!(db.snapshot().unwrap(),before);
 assert_eq!(db.commit(k1,publication(&a,&alice)).unwrap().status(),CommitStatus::IdempotentReplay);
 db.commit(k2,publication(&a,&bob)).unwrap();
 let before=db.snapshot().unwrap();
 assert_eq!(before.pending(),1);assert_eq!(before.version(),2);
 assert!(matches!(db.commit(Hash32::new([3;32]),publication(&a,&bob)),Err(Error::PreState)));
 assert_eq!(db.snapshot().unwrap(),before);
 let pending=db.next_pending().unwrap().unwrap();
 assert!(matches!(db.acknowledge(pending.delivery_id(),Hash32::ZERO),Err(Error::Delivery)));
 assert_eq!(db.snapshot().unwrap(),before);
 let mut sink1=MemoryDestination::default();let mut sink2=MemoryDestination::default();
 let first=db.deliver_next_memory_unacknowledged(&mut sink1).unwrap().unwrap();
 let repeated=db.deliver_next_memory_unacknowledged(&mut sink1).unwrap().unwrap();
 let restarted=db.deliver_next_memory_unacknowledged(&mut sink2).unwrap().unwrap();
 assert_eq!(first,repeated);assert_eq!(first,restarted);
 assert_eq!(sink1.delivered_count(),1);assert_eq!(sink2.delivered_count(),1);
 println!("PASS: duplicate officer rejection, changed-command replay rejection, stale pre-state rejection, exact replay idempotence, duplicate publication rejection, wrong acknowledgement rejection");
 println!("CONFIRMED SCOPE: pending delivery is recorded once by each fresh MemoryDestination; destination deduplication is not persisted across destination restarts");
 for n in [159,164,65535] { let w=wire(&descriptor,&[150,160,160,140,n]).unwrap();assert!(matches!(a.publish(raw(&w)),PublicationOutcome::Refused{..})); }
 let invalid=wire(&descriptor,&[150,161,163,140,162]).unwrap();
 assert!(matches!(a.publish(raw(&invalid)),PublicationOutcome::Commit(_)));
 assert!(matches!(db.commit(Hash32::new([4;32]),publication(&a,&invalid)),Err(Error::PreState)));
 println!("PASS: out-of-domain officer input refused; law-inconsistent supplied pre-state cannot replace shell history even when its proposed successor is valid");
}
