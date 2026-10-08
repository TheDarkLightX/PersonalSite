// Generated declarative data. Review v2/policy.json and project.zeno.
// Regenerate or check with `zeno-fcis generate contract`; no runtime mapper.
extern crate alloc;
use alloc::{vec, vec::Vec};
use zeno_fcis_synthesis::finite::{Domain as ScalarDomain, Op, V2ScalarProgram};
use zeno_fcis_synthesis::finite::{
    V2InputField as InputField, V2InputLeaf as InputLeaf, V2InputVariant as InputVariant,
    V2Resource as Resource, canonical_v2::schema as s, v2_authority as authority,
    v2_catalog as catalog, v2_composition as c, v2_laws as l, v2_zero_limits,
};
/// Exact actual original schema bytes.
pub const ORIGINAL_SCHEMA: &[u8] = include_bytes!("../v2/schema.zcve");
/// Complete reviewed library-encoded policy.
pub const ORIGINAL_POLICY: &[u8] = include_bytes!("../v2/policy.zcve");
/// Complete original named schema description.
pub const DESCRIPTION: s::Description<'static> = s::Description {
    profile: b"two_key_release",
    version: 1,
    root: 100,
    definitions: &[
        s::Definition {
            id: 100,
            name: b"Request",
            kind: s::Kind::Record(&[
                s::Field {
                    id: 110,
                    name: b"status",
                    type_id: 105,
                },
                s::Field {
                    id: 111,
                    name: b"first_approval",
                    type_id: 106,
                },
                s::Field {
                    id: 112,
                    name: b"second_approval",
                    type_id: 106,
                },
            ]),
        },
        s::Definition {
            id: 101,
            name: b"RequestCommand",
            kind: s::Kind::Sum(&[
                s::Variant {
                    id: 140,
                    name: b"Approve",
                },
                s::Variant {
                    id: 141,
                    name: b"Cancel",
                },
            ]),
        },
        s::Definition {
            id: 102,
            name: b"Caller",
            kind: s::Kind::Record(&[s::Field {
                id: 120,
                name: b"officer",
                type_id: 106,
            }]),
        },
        s::Definition {
            id: 103,
            name: b"ReleaseDesk",
            kind: s::Kind::Text { min: 1, max: 32 },
        },
        s::Definition {
            id: 104,
            name: b"Release",
            kind: s::Kind::Record(&[
                s::Field {
                    id: 130,
                    name: b"approved_by",
                    type_id: 106,
                },
                s::Field {
                    id: 131,
                    name: b"first_approved_by",
                    type_id: 106,
                },
            ]),
        },
        s::Definition {
            id: 105,
            name: b"Status",
            kind: s::Kind::Sum(&[
                s::Variant {
                    id: 150,
                    name: b"Pending",
                },
                s::Variant {
                    id: 151,
                    name: b"Approved",
                },
                s::Variant {
                    id: 152,
                    name: b"Cancelled",
                },
            ]),
        },
        s::Definition {
            id: 106,
            name: b"Officer",
            kind: s::Kind::Sum(&[
                s::Variant {
                    id: 160,
                    name: b"Nobody",
                },
                s::Variant {
                    id: 161,
                    name: b"Alice",
                },
                s::Variant {
                    id: 162,
                    name: b"Bob",
                },
                s::Variant {
                    id: 163,
                    name: b"Carol",
                },
            ]),
        },
    ],
};
/// Original root and schema commitments and complete wire-size limits.
pub const FRAMING: c::Framing = c::Framing {
    state: c::FrameBinding {
        root: 100,
        schema: [
            230, 110, 238, 40, 85, 113, 32, 195, 206, 153, 146, 181, 225, 47, 14, 84, 236, 82, 101,
            142, 200, 9, 60, 201, 58, 45, 39, 190, 45, 120, 23, 255,
        ],
        max_bytes: 83,
    },
    command: c::FrameBinding {
        root: 101,
        schema: [
            230, 110, 238, 40, 85, 113, 32, 195, 206, 153, 146, 181, 225, 47, 14, 84, 236, 82, 101,
            142, 200, 9, 60, 201, 58, 45, 39, 190, 45, 120, 23, 255,
        ],
        max_bytes: 56,
    },
    context: c::FrameBinding {
        root: 102,
        schema: [
            230, 110, 238, 40, 85, 113, 32, 195, 206, 153, 146, 181, 225, 47, 14, 84, 236, 82, 101,
            142, 200, 9, 60, 201, 58, 45, 39, 190, 45, 120, 23, 255,
        ],
        max_bytes: 63,
    },
};
/// Exact channel to original destination and payload type links.
pub const CHANNEL_ROOTS: &[(u32, u32, u32)] = &[(300, 103, 104)];
/// The genesis state law 990 requires, field by field.
pub const GENESIS: &[c::Field<'static>] = &[
    c::Field {
        id: 110,
        value: c::Atom::Sum {
            type_id: 105,
            variant: 150,
        },
    },
    c::Field {
        id: 111,
        value: c::Atom::Sum {
            type_id: 106,
            variant: 160,
        },
    },
    c::Field {
        id: 112,
        value: c::Atom::Sum {
            type_id: 106,
            variant: 160,
        },
    },
];
/// Complete ordered decisions selected only by actual graph output.
pub const BRANCHES: &[c::Branch<'static>] = &[
    c::Branch {
        code: 0,
        class: c::Class::Reject,
        reason: Some(200),
        assignments: &[],
        effects: &[],
        outbox: &[],
    },
    c::Branch {
        code: 1,
        class: c::Class::Reject,
        reason: Some(201),
        assignments: &[],
        effects: &[],
        outbox: &[],
    },
    c::Branch {
        code: 2,
        class: c::Class::CommittedFailure,
        reason: Some(202),
        assignments: &[
            c::Assignment {
                field: 110,
                value: c::Expr::Constant(c::Atom::Sum {
                    type_id: 105,
                    variant: 152,
                }),
                domain: c::Domain::Sum {
                    type_id: 105,
                    variants: &[150, 151, 152],
                },
            },
            c::Assignment {
                field: 111,
                value: c::Expr::Input(c::Source::State, 111),
                domain: c::Domain::Sum {
                    type_id: 106,
                    variants: &[160, 161, 162, 163],
                },
            },
            c::Assignment {
                field: 112,
                value: c::Expr::Input(c::Source::State, 112),
                domain: c::Domain::Sum {
                    type_id: 106,
                    variants: &[160, 161, 162, 163],
                },
            },
        ],
        effects: &[],
        outbox: &[],
    },
    c::Branch {
        code: 3,
        class: c::Class::Reject,
        reason: Some(203),
        assignments: &[],
        effects: &[],
        outbox: &[],
    },
    c::Branch {
        code: 4,
        class: c::Class::Accept,
        reason: None,
        assignments: &[
            c::Assignment {
                field: 110,
                value: c::Expr::Constant(c::Atom::Sum {
                    type_id: 105,
                    variant: 150,
                }),
                domain: c::Domain::Sum {
                    type_id: 105,
                    variants: &[150, 151, 152],
                },
            },
            c::Assignment {
                field: 111,
                value: c::Expr::Input(c::Source::Context, 120),
                domain: c::Domain::Sum {
                    type_id: 106,
                    variants: &[160, 161, 162, 163],
                },
            },
            c::Assignment {
                field: 112,
                value: c::Expr::Input(c::Source::State, 112),
                domain: c::Domain::Sum {
                    type_id: 106,
                    variants: &[160, 161, 162, 163],
                },
            },
        ],
        effects: &[],
        outbox: &[],
    },
    c::Branch {
        code: 5,
        class: c::Class::Accept,
        reason: None,
        assignments: &[
            c::Assignment {
                field: 110,
                value: c::Expr::Constant(c::Atom::Sum {
                    type_id: 105,
                    variant: 151,
                }),
                domain: c::Domain::Sum {
                    type_id: 105,
                    variants: &[150, 151, 152],
                },
            },
            c::Assignment {
                field: 111,
                value: c::Expr::Input(c::Source::State, 111),
                domain: c::Domain::Sum {
                    type_id: 106,
                    variants: &[160, 161, 162, 163],
                },
            },
            c::Assignment {
                field: 112,
                value: c::Expr::Input(c::Source::Context, 120),
                domain: c::Domain::Sum {
                    type_id: 106,
                    variants: &[160, 161, 162, 163],
                },
            },
        ],
        effects: &[],
        outbox: &[c::DeliveryPlan {
            ordinal: 0,
            channel: 300,
            when: c::Expr::Constant(c::Atom::Bool(true)),
            destination: c::Expr::Constant(c::Atom::Text(b"release-desk")),
            payload: &[
                c::PayloadField {
                    field: 130,
                    value: c::Expr::Input(c::Source::Context, 120),
                },
                c::PayloadField {
                    field: 131,
                    value: c::Expr::Input(c::Source::State, 111),
                },
            ],
            idempotency: c::Expr::Constant(c::Atom::U128(0)),
        }],
    },
];
const LAW_500: &[l::Op<'static>] = &[
    l::Op::Observe(l::Observation::Post(110)),
    l::Op::ToI128(0),
    l::Op::Literal(l::Atom::I128(151)),
    l::Op::Eq(1, 2),
    l::Op::Observe(l::Observation::Post(111)),
    l::Op::ToI128(4),
    l::Op::Literal(l::Atom::I128(160)),
    l::Op::Eq(5, 6),
    l::Op::Not(7),
    l::Op::Observe(l::Observation::Post(112)),
    l::Op::ToI128(9),
    l::Op::Eq(10, 6),
    l::Op::Not(11),
    l::Op::And(8, 12),
    l::Op::Eq(5, 10),
    l::Op::Not(14),
    l::Op::And(13, 15),
    l::Op::Not(3),
    l::Op::Not(17),
    l::Op::Not(16),
    l::Op::And(18, 19),
    l::Op::Not(20),
];
const LAW_501: &[l::Op<'static>] = &[
    l::Op::Observe(l::Observation::Pre(110)),
    l::Op::ToI128(0),
    l::Op::Literal(l::Atom::I128(150)),
    l::Op::Eq(1, 2),
    l::Op::Observe(l::Observation::Post(110)),
    l::Op::ToI128(4),
    l::Op::Literal(l::Atom::I128(152)),
    l::Op::Eq(5, 6),
    l::Op::Not(7),
    l::Op::And(3, 8),
    l::Op::Observe(l::Observation::Post(111)),
    l::Op::ToI128(10),
    l::Op::Observe(l::Observation::Context(120)),
    l::Op::ToI128(12),
    l::Op::Eq(11, 13),
    l::Op::Observe(l::Observation::Post(112)),
    l::Op::ToI128(15),
    l::Op::Eq(16, 13),
    l::Op::Not(14),
    l::Op::Not(17),
    l::Op::And(18, 19),
    l::Op::Not(20),
    l::Op::And(9, 21),
];
const LAW_502: &[l::Op<'static>] = &[
    l::Op::Observe(l::Observation::CommandRoot),
    l::Op::ToI128(0),
    l::Op::Literal(l::Atom::I128(141)),
    l::Op::Eq(1, 2),
    l::Op::Observe(l::Observation::Post(110)),
    l::Op::ToI128(4),
    l::Op::Literal(l::Atom::I128(152)),
    l::Op::Eq(5, 6),
    l::Op::And(3, 7),
    l::Op::Observe(l::Observation::Post(111)),
    l::Op::ToI128(9),
    l::Op::Observe(l::Observation::Pre(111)),
    l::Op::ToI128(11),
    l::Op::Eq(10, 12),
    l::Op::And(8, 13),
    l::Op::Observe(l::Observation::Post(112)),
    l::Op::ToI128(15),
    l::Op::Observe(l::Observation::Pre(112)),
    l::Op::ToI128(17),
    l::Op::Eq(16, 18),
    l::Op::And(14, 19),
];
const LAW_503: &[l::Op<'static>] = &[
    l::Op::Observe(l::Observation::Post(110)),
    l::Op::ToI128(0),
    l::Op::Literal(l::Atom::I128(151)),
    l::Op::Eq(1, 2),
    l::Op::Not(3),
    l::Op::Observe(l::Observation::Post(112)),
    l::Op::ToI128(5),
    l::Op::Literal(l::Atom::I128(160)),
    l::Op::Eq(6, 7),
    l::Op::Not(4),
    l::Op::Not(9),
    l::Op::Not(8),
    l::Op::And(10, 11),
    l::Op::Not(12),
];
const LAW_509: &[l::Op<'static>] = &[
    l::Op::Observe(l::Observation::PostLength),
    l::Op::ToI128(0),
    l::Op::Literal(l::Atom::I128(0)),
    l::Op::Eq(1, 2),
    l::Op::Observe(l::Observation::PatchLength),
    l::Op::ToI128(4),
    l::Op::Eq(5, 2),
    l::Op::Observe(l::Observation::EffectLength),
    l::Op::ToI128(7),
    l::Op::Eq(8, 2),
    l::Op::Observe(l::Observation::OutboxLength),
    l::Op::ToI128(10),
    l::Op::Eq(11, 2),
    l::Op::Literal(l::Atom::Bool(true)),
    l::Op::And(13, 3),
    l::Op::And(14, 6),
    l::Op::And(15, 9),
    l::Op::And(16, 12),
];
const LAW_990: &[l::Op<'static>] = &[
    l::Op::Observe(l::Observation::Initial(110)),
    l::Op::Literal(l::Atom::Sum {
        type_id: 105,
        variant: 150,
    }),
    l::Op::Eq(0, 1),
    l::Op::Observe(l::Observation::Initial(111)),
    l::Op::Literal(l::Atom::Sum {
        type_id: 106,
        variant: 160,
    }),
    l::Op::Eq(3, 4),
    l::Op::Observe(l::Observation::Initial(112)),
    l::Op::Eq(6, 4),
    l::Op::Literal(l::Atom::Bool(true)),
    l::Op::And(8, 2),
    l::Op::And(9, 5),
    l::Op::And(10, 7),
];
const LAW_991: &[l::Op<'static>] = &[
    l::Op::Literal(l::Atom::Bool(true)),
    l::Op::Observe(l::Observation::Pre(110)),
    l::Op::ToI128(1),
    l::Op::Literal(l::Atom::I128(150)),
    l::Op::Eq(2, 3),
    l::Op::Not(4),
    l::Op::And(0, 5),
    l::Op::Not(5),
    l::Op::And(0, 7),
    l::Op::Observe(l::Observation::Class),
    l::Op::ToI128(9),
    l::Op::Literal(l::Atom::I128(1)),
    l::Op::Eq(10, 11),
    l::Op::Observe(l::Observation::HasReason),
    l::Op::ObserveWhen(6, l::Observation::Reason, l::Atom::I128(0)),
    l::Op::ToI128(14),
    l::Op::Literal(l::Atom::I128(200)),
    l::Op::Eq(15, 16),
    l::Op::Observe(l::Observation::EffectLength),
    l::Op::ToI128(18),
    l::Op::Literal(l::Atom::I128(0)),
    l::Op::Eq(19, 20),
    l::Op::Observe(l::Observation::OutboxLength),
    l::Op::ToI128(22),
    l::Op::Eq(23, 20),
    l::Op::Observe(l::Observation::PostLength),
    l::Op::ToI128(25),
    l::Op::Eq(26, 20),
    l::Op::And(0, 12),
    l::Op::And(28, 13),
    l::Op::And(29, 17),
    l::Op::And(30, 21),
    l::Op::And(31, 24),
    l::Op::And(32, 27),
    l::Op::Select(6, 33, 0),
    l::Op::Observe(l::Observation::Context(120)),
    l::Op::ToI128(35),
    l::Op::Literal(l::Atom::I128(160)),
    l::Op::Eq(36, 37),
    l::Op::And(8, 38),
    l::Op::Not(38),
    l::Op::And(8, 40),
    l::Op::ObserveWhen(39, l::Observation::Reason, l::Atom::I128(0)),
    l::Op::ToI128(42),
    l::Op::Literal(l::Atom::I128(201)),
    l::Op::Eq(43, 44),
    l::Op::And(29, 45),
    l::Op::And(46, 21),
    l::Op::And(47, 24),
    l::Op::And(48, 27),
    l::Op::Select(39, 49, 0),
    l::Op::Observe(l::Observation::CommandRoot),
    l::Op::ToI128(51),
    l::Op::Literal(l::Atom::I128(141)),
    l::Op::Eq(52, 53),
    l::Op::And(41, 54),
    l::Op::Not(54),
    l::Op::And(41, 56),
    l::Op::Literal(l::Atom::I128(2)),
    l::Op::Eq(10, 58),
    l::Op::ObserveWhen(55, l::Observation::Reason, l::Atom::I128(0)),
    l::Op::ToI128(60),
    l::Op::Literal(l::Atom::I128(202)),
    l::Op::Eq(61, 62),
    l::Op::Literal(l::Atom::I128(3)),
    l::Op::Eq(26, 64),
    l::Op::ObserveWhen(
        55,
        l::Observation::Post(110),
        l::Atom::Sum {
            type_id: 105,
            variant: 150,
        },
    ),
    l::Op::Literal(l::Atom::Sum {
        type_id: 105,
        variant: 152,
    }),
    l::Op::Eq(66, 67),
    l::Op::Select(55, 68, 0),
    l::Op::ObserveWhen(
        55,
        l::Observation::Post(111),
        l::Atom::Sum {
            type_id: 106,
            variant: 160,
        },
    ),
    l::Op::ToI128(70),
    l::Op::Observe(l::Observation::Pre(111)),
    l::Op::ToI128(72),
    l::Op::Eq(71, 73),
    l::Op::Select(55, 74, 0),
    l::Op::ObserveWhen(
        55,
        l::Observation::Post(112),
        l::Atom::Sum {
            type_id: 106,
            variant: 160,
        },
    ),
    l::Op::ToI128(76),
    l::Op::Observe(l::Observation::Pre(112)),
    l::Op::ToI128(78),
    l::Op::Eq(77, 79),
    l::Op::Select(55, 80, 0),
    l::Op::And(0, 59),
    l::Op::And(82, 13),
    l::Op::And(83, 63),
    l::Op::And(84, 21),
    l::Op::And(85, 24),
    l::Op::And(86, 65),
    l::Op::And(87, 69),
    l::Op::And(88, 75),
    l::Op::And(89, 81),
    l::Op::Select(55, 90, 0),
    l::Op::Eq(36, 73),
    l::Op::And(57, 92),
    l::Op::Not(92),
    l::Op::And(57, 94),
    l::Op::ObserveWhen(93, l::Observation::Reason, l::Atom::I128(0)),
    l::Op::ToI128(96),
    l::Op::Literal(l::Atom::I128(203)),
    l::Op::Eq(97, 98),
    l::Op::And(29, 99),
    l::Op::And(100, 21),
    l::Op::And(101, 24),
    l::Op::And(102, 27),
    l::Op::Select(93, 103, 0),
    l::Op::Eq(73, 37),
    l::Op::And(95, 105),
    l::Op::Not(105),
    l::Op::And(95, 107),
    l::Op::Eq(10, 20),
    l::Op::Not(13),
    l::Op::ObserveWhen(
        106,
        l::Observation::Post(110),
        l::Atom::Sum {
            type_id: 105,
            variant: 150,
        },
    ),
    l::Op::Literal(l::Atom::Sum {
        type_id: 105,
        variant: 150,
    }),
    l::Op::Eq(111, 112),
    l::Op::Select(106, 113, 0),
    l::Op::ObserveWhen(
        106,
        l::Observation::Post(111),
        l::Atom::Sum {
            type_id: 106,
            variant: 160,
        },
    ),
    l::Op::ToI128(115),
    l::Op::Eq(116, 36),
    l::Op::Select(106, 117, 0),
    l::Op::ObserveWhen(
        106,
        l::Observation::Post(112),
        l::Atom::Sum {
            type_id: 106,
            variant: 160,
        },
    ),
    l::Op::ToI128(119),
    l::Op::Eq(120, 79),
    l::Op::Select(106, 121, 0),
    l::Op::And(0, 109),
    l::Op::And(123, 110),
    l::Op::And(124, 21),
    l::Op::And(125, 24),
    l::Op::And(126, 65),
    l::Op::And(127, 114),
    l::Op::And(128, 118),
    l::Op::And(129, 122),
    l::Op::Select(106, 130, 0),
    l::Op::And(108, 0),
    l::Op::Not(0),
    l::Op::And(108, 133),
    l::Op::Eq(23, 11),
    l::Op::ObserveWhen(
        132,
        l::Observation::Post(110),
        l::Atom::Sum {
            type_id: 105,
            variant: 150,
        },
    ),
    l::Op::Literal(l::Atom::Sum {
        type_id: 105,
        variant: 151,
    }),
    l::Op::Eq(136, 137),
    l::Op::Select(132, 138, 0),
    l::Op::ObserveWhen(
        132,
        l::Observation::Post(111),
        l::Atom::Sum {
            type_id: 106,
            variant: 160,
        },
    ),
    l::Op::ToI128(140),
    l::Op::Eq(141, 73),
    l::Op::Select(132, 142, 0),
    l::Op::ObserveWhen(
        132,
        l::Observation::Post(112),
        l::Atom::Sum {
            type_id: 106,
            variant: 160,
        },
    ),
    l::Op::ToI128(144),
    l::Op::Eq(145, 36),
    l::Op::Select(132, 146, 0),
    l::Op::ObserveWhen(132, l::Observation::OutboxOrdinal(0), l::Atom::I128(0)),
    l::Op::ToI128(148),
    l::Op::Eq(149, 20),
    l::Op::ObserveWhen(132, l::Observation::OutboxChannel(0), l::Atom::I128(0)),
    l::Op::ToI128(151),
    l::Op::Literal(l::Atom::I128(300)),
    l::Op::Eq(152, 153),
    l::Op::ObserveWhen(
        132,
        l::Observation::OutboxDestination(0),
        l::Atom::Text(b"release-desk"),
    ),
    l::Op::Literal(l::Atom::Text(b"release-desk")),
    l::Op::Eq(155, 156),
    l::Op::ObserveWhen(132, l::Observation::OutboxIdempotency(0), l::Atom::U128(0)),
    l::Op::Literal(l::Atom::U128(0)),
    l::Op::Eq(158, 159),
    l::Op::ObserveWhen(
        132,
        l::Observation::OutboxPayload(0, 130),
        l::Atom::Sum {
            type_id: 106,
            variant: 160,
        },
    ),
    l::Op::ToI128(161),
    l::Op::Eq(162, 36),
    l::Op::Select(132, 163, 0),
    l::Op::ObserveWhen(
        132,
        l::Observation::OutboxPayload(0, 131),
        l::Atom::Sum {
            type_id: 106,
            variant: 160,
        },
    ),
    l::Op::ToI128(165),
    l::Op::Eq(166, 73),
    l::Op::Select(132, 167, 0),
    l::Op::And(125, 135),
    l::Op::And(169, 65),
    l::Op::And(170, 139),
    l::Op::And(171, 143),
    l::Op::And(172, 147),
    l::Op::And(173, 150),
    l::Op::And(174, 154),
    l::Op::And(175, 157),
    l::Op::And(176, 160),
    l::Op::And(177, 164),
    l::Op::And(178, 168),
    l::Op::Select(132, 179, 0),
    l::Op::Not(134),
    l::Op::And(0, 34),
    l::Op::And(182, 50),
    l::Op::And(183, 91),
    l::Op::And(184, 104),
    l::Op::And(185, 131),
    l::Op::And(186, 180),
    l::Op::And(187, 181),
];
/// Original scoped laws plus independent structural requirements.
pub const LAWS: &[l::Law<'static>] = &[
    l::Law {
        id: 500,
        kind: l::Kind::StateInvariant,
        scope: l::Scope::Committing,
        genesis: true,
        program: l::Program {
            nodes: LAW_500,
            root: 21,
        },
    },
    l::Law {
        id: 501,
        kind: l::Kind::AuthoritySubjectRecipient,
        scope: l::Scope::Accept,
        genesis: false,
        program: l::Program {
            nodes: LAW_501,
            root: 22,
        },
    },
    l::Law {
        id: 502,
        kind: l::Kind::CommittedFailureEffects,
        scope: l::Scope::CommittedFailure,
        genesis: false,
        program: l::Program {
            nodes: LAW_502,
            root: 20,
        },
    },
    l::Law {
        id: 503,
        kind: l::Kind::StateInvariant,
        scope: l::Scope::Committing,
        genesis: true,
        program: l::Program {
            nodes: LAW_503,
            root: 13,
        },
    },
    l::Law {
        id: 509,
        kind: l::Kind::RejectNoAuthority,
        scope: l::Scope::Reject,
        genesis: false,
        program: l::Program {
            nodes: LAW_509,
            root: 17,
        },
    },
    l::Law {
        id: 990,
        kind: l::Kind::InitialCondition,
        scope: l::Scope::Always,
        genesis: true,
        program: l::Program {
            nodes: LAW_990,
            root: 11,
        },
    },
    l::Law {
        id: 991,
        kind: l::Kind::DecisionConformance,
        scope: l::Scope::Always,
        genesis: false,
        program: l::Program {
            nodes: LAW_991,
            root: 188,
        },
    },
];
/// No declared law is optional at descriptor admission.
pub const REQUIRED: &[u32] = &[500, 501, 502, 503, 509, 990, 991];
/// Owns declarative input/output type tables; evaluation stays in the library.
pub struct Contract {
    state: Vec<InputField>,
    command: InputLeaf,
    context: Vec<InputField>,
    output_types: Vec<InputLeaf>,
}
impl Default for Contract {
    fn default() -> Self {
        Self::new()
    }
}
impl Contract {
    /// Allocate only fixed declarative type tables.
    #[must_use]
    pub fn new() -> Self {
        Self {
            state: vec![
                InputField {
                    id: 110,
                    leaf: InputLeaf::Sum {
                        type_id: 105,
                        min: 150,
                        max: 152,
                        variants: vec![
                            InputVariant { id: 150, code: 150 },
                            InputVariant { id: 151, code: 151 },
                            InputVariant { id: 152, code: 152 },
                        ],
                    },
                },
                InputField {
                    id: 111,
                    leaf: InputLeaf::Sum {
                        type_id: 106,
                        min: 160,
                        max: 163,
                        variants: vec![
                            InputVariant { id: 160, code: 160 },
                            InputVariant { id: 161, code: 161 },
                            InputVariant { id: 162, code: 162 },
                            InputVariant { id: 163, code: 163 },
                        ],
                    },
                },
                InputField {
                    id: 112,
                    leaf: InputLeaf::Sum {
                        type_id: 106,
                        min: 160,
                        max: 163,
                        variants: vec![
                            InputVariant { id: 160, code: 160 },
                            InputVariant { id: 161, code: 161 },
                            InputVariant { id: 162, code: 162 },
                            InputVariant { id: 163, code: 163 },
                        ],
                    },
                },
            ],
            command: InputLeaf::Sum {
                type_id: 101,
                min: 140,
                max: 141,
                variants: vec![
                    InputVariant { id: 140, code: 140 },
                    InputVariant { id: 141, code: 141 },
                ],
            },
            context: vec![InputField {
                id: 120,
                leaf: InputLeaf::Sum {
                    type_id: 106,
                    min: 160,
                    max: 163,
                    variants: vec![
                        InputVariant { id: 160, code: 160 },
                        InputVariant { id: 161, code: 161 },
                        InputVariant { id: 162, code: 162 },
                        InputVariant { id: 163, code: 163 },
                    ],
                },
            }],
            output_types: vec![InputLeaf::I128 { min: 0, max: 5 }],
        }
    }
    /// Borrow the full raw-input, complete-decision and law contract.
    #[must_use]
    pub fn descriptor(&self) -> c::Descriptor<'_> {
        c::Descriptor {
            state: c::Schema::Record(&self.state),
            command: c::Schema::Leaf(&self.command),
            context: c::Schema::Record(&self.context),
            program: V2ScalarProgram {
                inputs: &[
                    ScalarDomain::Int { min: 150, max: 152 },
                    ScalarDomain::Int { min: 160, max: 163 },
                    ScalarDomain::Int { min: 160, max: 163 },
                    ScalarDomain::Int { min: 140, max: 141 },
                    ScalarDomain::Int { min: 160, max: 163 },
                ],
                outputs: &[ScalarDomain::Int { min: 0, max: 5 }],
                nodes: &[
                    Op::Input(0),
                    Op::Int(150),
                    Op::Eq(0, 1),
                    Op::Not(2),
                    Op::Int(0),
                    Op::Input(4),
                    Op::Int(160),
                    Op::Eq(5, 6),
                    Op::Int(1),
                    Op::Input(3),
                    Op::Int(141),
                    Op::Eq(9, 10),
                    Op::Int(2),
                    Op::Input(1),
                    Op::Eq(5, 13),
                    Op::Int(3),
                    Op::Eq(13, 6),
                    Op::Int(4),
                    Op::Int(5),
                    Op::Select(16, 17, 18),
                    Op::Select(14, 15, 19),
                    Op::Select(11, 12, 20),
                    Op::Select(7, 8, 21),
                    Op::Select(3, 4, 22),
                ],
                roots: &[23],
            },
            bindings: &[
                c::Binding {
                    source: c::Source::State,
                    selector: c::Selector::Field(110),
                },
                c::Binding {
                    source: c::Source::State,
                    selector: c::Selector::Field(111),
                },
                c::Binding {
                    source: c::Source::State,
                    selector: c::Selector::Field(112),
                },
                c::Binding {
                    source: c::Source::Command,
                    selector: c::Selector::Root,
                },
                c::Binding {
                    source: c::Source::Context,
                    selector: c::Selector::Field(120),
                },
            ],
            output_types: &self.output_types,
            decision_output: 0,
            branches: BRANCHES,
            reasons: &[
                c::Reason {
                    id: 200,
                    class: c::Class::Reject,
                },
                c::Reason {
                    id: 201,
                    class: c::Class::Reject,
                },
                c::Reason {
                    id: 202,
                    class: c::Class::CommittedFailure,
                },
                c::Reason {
                    id: 203,
                    class: c::Class::Reject,
                },
            ],
            channels: &[c::Channel {
                id: 300,
                destination: c::Domain::Text,
                payload: &[
                    c::TypedField {
                        field: 130,
                        domain: c::Domain::Sum {
                            type_id: 106,
                            variants: &[160, 161, 162, 163],
                        },
                    },
                    c::TypedField {
                        field: 131,
                        domain: c::Domain::Sum {
                            type_id: 106,
                            variants: &[160, 161, 162, 163],
                        },
                    },
                ],
                idempotency: c::Domain::U128 { min: 0, max: 0 },
            }],
            laws: LAWS,
            required: REQUIRED,
            limits: v2_zero_limits()
                .with_limit(Resource::Read, 131)
                .with_limit(Resource::Write, 3)
                .with_limit(Resource::Candidate, 1)
                .with_limit(Resource::Effect, 1)
                .with_limit(Resource::Byte, 202)
                .with_limit(Resource::WitnessByte, 0)
                .with_limit(Resource::Depth, 0)
                .with_limit(Resource::Step, 328),
        }
    }
}
/// Exact complete schema/policy correspondence precedes Authority construction.
pub fn checked_catalog<'a>(
    descriptor: &'a c::Descriptor<'a>,
) -> Result<catalog::BoundCatalog<'a>, catalog::Failure> {
    catalog::bind_original(
        ORIGINAL_SCHEMA,
        &DESCRIPTION,
        catalog::Limits {
            schema: s::Limits {
                bytes: ORIGINAL_SCHEMA.len() as u64,
                types: 7,
                fields: 3,
                variants: 4,
            },
            contract_bytes: ORIGINAL_POLICY.len() as u64,
        },
        ORIGINAL_POLICY,
        descriptor,
        &FRAMING,
        CHANNEL_ROOTS,
    )
}
/// Ordered refusal at checked catalog or private Authority construction.
#[derive(Debug)]
#[non_exhaustive]
pub enum BindFailure {
    /// Complete original schema/policy correspondence refused.
    Catalog(catalog::Failure),
    /// Private library source binding refused.
    Authority(authority::Refusal),
}
/// Sole supplied production constructor; identity comes from the checked library.
pub fn checked_authority<'a>(
    descriptor: &'a c::Descriptor<'a>,
) -> Result<authority::Authority<'a>, BindFailure> {
    let catalog = checked_catalog(descriptor).map_err(BindFailure::Catalog)?;
    authority::bind(&catalog).map_err(BindFailure::Authority)
}
/// Position in this application's contract lineage: 1 before any adoption.
pub const VERSION: u32 = 1;
/// Every contract version's checked catalog, oldest first and this one last,
/// for a store upgrade or a lineage open. Each binding checks that version's
/// complete retained schema and policy bytes.
pub fn with_lineage<R>(
    f: impl FnOnce(&[&catalog::BoundCatalog<'_>]) -> R,
) -> Result<R, catalog::Failure> {
    let contract = Contract::new();
    let descriptor = contract.descriptor();
    let catalog = checked_catalog(&descriptor)?;
    Ok(f(&[&catalog]))
}
