import Std

/-!
Companion to “Abstraction Is Compression”. Elementary logical facts, not
a proof that any physical AI containment system is secure. Concrete-to-abstract
transition coverage and bad-state coverage are hypotheses, not conclusions.
-/

set_option autoImplicit false
set_option warningAsError true

namespace Abstraction

universe u v w

/-- A summary preserves a question if the answer can be read from the summary. -/
theorem compression_preserves_decision {S : Type u} {A : Type v} {D : Type w}
    (summarize : S → A) (answer : S → D) (readout : A → D)
    (preserves : ∀ s, readout (summarize s) = answer s)
    (x y : S) (same : summarize x = summarize y) : answer x = answer y := by
  rw [← preserves x, ← preserves y, same]

/-- Any finite execution prefix, with no restriction on the search strategy. -/
inductive Reach {S : Type u} (step : S → S → Prop) (start : S) : S → Prop
  | initial : Reach step start start
  | advance {x y : S} : Reach step start x → step x y → Reach step start y

/-- Every path stays inside a region closed under ALL modeled steps. -/
theorem reachable_invariant {S : Type u} (step : S → S → Prop)
    (inside : S → Prop) (start : S)
    (initial : inside start)
    (closed : ∀ x y, inside x → step x y → inside y)
    {finish : S} (path : Reach step start finish) : inside finish := by
  induction path with
  | initial => exact initial
  | advance prior transition ih => exact closed _ _ ih transition

/-- Sound transition abstraction maps every concrete path to an abstract path.
Abstract steps must include stuttering when a concrete change is compressed away. -/
theorem reachability_maps {S : Type u} {A : Type v}
    (concreteStep : S → S → Prop) (abstractStep : A → A → Prop)
    (summarize : S → A)
    (coversStep : ∀ x y, concreteStep x y → abstractStep (summarize x) (summarize y))
    (start : S) {finish : S} (path : Reach concreteStep start finish) :
    Reach abstractStep (summarize start) (summarize finish) := by
  induction path with
  | initial => exact Reach.initial
  | advance prior transition ih => exact Reach.advance ih (coversStep _ _ transition)

/-- Abstract unreachability transfers only if both transitions and bad states
are covered. This does not establish either premise for physical hardware. -/
theorem abstract_safety_transfers {S : Type u} {A : Type v}
    (concreteStep : S → S → Prop) (abstractStep : A → A → Prop)
    (summarize : S → A) (bad : S → Prop) (abstractBad : A → Prop)
    (coversStep : ∀ x y, concreteStep x y → abstractStep (summarize x) (summarize y))
    (coversBad : ∀ s, bad s → abstractBad (summarize s))
    (start : S)
    (abstractSafe : ∀ a, Reach abstractStep (summarize start) a → ¬abstractBad a) :
    ∀ s, Reach concreteStep start s → ¬bad s := by
  intro s path forbidden
  exact abstractSafe (summarize s)
    (reachability_maps concreteStep abstractStep summarize coversStep start path)
    (coversBad s forbidden)

/-- One admissible configuration that defeats every modeled attack refutes
the claim that every admissible configuration has a successful modeled attack. -/
theorem witness_refutes_universal_escape {C : Type u} {P : Type v}
    (admissible : C → Prop) (escapes : C → P → Prop)
    (witness : ∃ c, admissible c ∧ ∀ p, ¬escapes c p) :
    ¬(∀ c, admissible c → ∃ p, escapes c p) := by
  intro everyConfig
  obtain ⟨c, valid, safe⟩ := witness
  obtain ⟨p, escape⟩ := everyConfig c valid
  exact safe p escape

/-- Choosing a different design after each attack is weaker than finding one
design that handles all attacks. Equality is just a finite logical example. -/
theorem quantifier_order_matters :
    (∀ attack : Bool, ∃ config : Bool, config ≠ attack) ∧
    ¬(∃ config : Bool, ∀ attack : Bool, config ≠ attack) := by
  constructor
  · intro attack
    cases attack <;> decide
  · intro candidate
    obtain ⟨config, protects⟩ := candidate
    exact protects config rfl

/-- An omitted transition can change the answer despite a correct proof about
the smaller graph. Here the extra edge goes from false to true. -/
theorem omitted_edge_changes_answer :
    (¬Reach (fun x y : Bool => y = x) false true) ∧
    Reach (fun _ _ : Bool => True) false true := by
  constructor
  · intro path
    have impossible : true = false := reachable_invariant
      (fun x y : Bool => y = x) (fun x => x = false) false rfl
      (by intro x y hx hxy; exact hxy.trans hx) path
    cases impossible
  · exact Reach.advance Reach.initial True.intro

#print axioms compression_preserves_decision
#print axioms reachable_invariant
#print axioms reachability_maps
#print axioms abstract_safety_transfers
#print axioms witness_refutes_universal_escape
#print axioms quantifier_order_matters
#print axioms omitted_edge_changes_answer

end Abstraction
