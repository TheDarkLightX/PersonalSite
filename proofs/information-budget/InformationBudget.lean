import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fin.VecNotation
import Mathlib.Tactic

/- A reduced answer must work without rereading the original input.
   Existence preservation is required only where the source has an answer. -/
namespace InformationBudget

def ExactReduction {X Y A B : Type*} (P : X → Y → Prop) (Q : A → B → Prop)
    (encode : X → A) (decode : B → Y) : Prop :=
  (∀ x b, Q (encode x) b → P x (decode b)) ∧
  (∀ x, (∃ y, P x y) → ∃ b, Q (encode x) b)

def Task (n : ℕ) : Option (Fin n) → Fin n → Prop
  | none, _ => False
  | some a, y => y = a

theorem task_encoder_injective {n : ℕ} {A B : Type*}
    {Q : A → B → Prop} {encode : Option (Fin n) → A} {decode : B → Fin n}
    (h : ExactReduction (Task n) Q encode decode) : Function.Injective encode := by
  rcases h with ⟨sound, complete⟩
  intro i j same
  cases i with
  | none =>
    cases j with
    | none => rfl
    | some b =>
      obtain ⟨z, hz⟩ := complete (some b) ⟨b, rfl⟩
      have hz' : Q (encode none) z := by rw [same]; exact hz
      exact False.elim (sound none z hz')
  | some a =>
    obtain ⟨z, hz⟩ := complete (some a) ⟨a, rfl⟩
    have hz' : Q (encode j) z := by rw [← same]; exact hz
    cases j with
    | none => exact False.elim (sound none z hz')
    | some b =>
      have ha : decode z = a := sound (some a) z hz
      have hb : decode z = b := sound (some b) z hz'
      exact congrArg some (ha.symm.trans hb)

theorem task_labels_lower_bound {n : ℕ} {A B : Type*} [Fintype A]
    {Q : A → B → Prop} {encode : Option (Fin n) → A} {decode : B → Fin n}
    (h : ExactReduction (Task n) Q encode decode) : n + 1 ≤ Fintype.card A := by
  have bound := Fintype.card_le_of_injective encode (task_encoder_injective h)
  simpa using bound

def mask : Fin 8 → Fin 16 := ![0, 3, 5, 6, 9, 10, 12, 15]
def Source (x : Fin 16) (h : Fin 8) : Prop := Nat.xor x.val (mask h).val = 1

instance (x : Fin 16) (h : Fin 8) : Decidable (Source x h) :=
  inferInstanceAs (Decidable (Nat.xor x.val (mask h).val = 1))
instance (n : ℕ) (x : Option (Fin n)) (y : Fin n) : Decidable (Task n x y) := by
  cases x <;> unfold Task <;> infer_instance

def classify : Fin 16 → Option (Fin 8) :=
  ![none, some 0, some 1, none, some 2, none, none, some 3,
    some 4, none, none, some 5, none, some 6, some 7, none]
def representative : Option (Fin 8) → Fin 16
  | none => 0
  | some i => ![1, 2, 4, 7, 8, 11, 13, 14] i

theorem source_iff (x : Fin 16) (h : Fin 8) : Source x h ↔ Task 8 (classify x) h := by
  revert x h
  decide

theorem classify_representative (x : Option (Fin 8)) : classify (representative x) = x := by
  revert x
  decide

theorem nine_labels_necessary {A B : Type*} [Fintype A]
    {Q : A → B → Prop} {encode : Fin 16 → A} {decode : B → Fin 8}
    (h : ExactReduction Source Q encode decode) : 9 ≤ Fintype.card A := by
  have ht : ExactReduction (Task 8) Q (encode ∘ representative) decode := by
    constructor
    · intro x b hb
      have hs := (source_iff (representative x) (decode b)).1 (h.1 (representative x) b hb)
      simpa only [classify_representative] using hs
    · intro x hx
      obtain ⟨y, hy⟩ := hx
      apply h.2 (representative x)
      refine ⟨y, (source_iff (representative x) y).2 ?_⟩
      simpa only [classify_representative] using hy
  exact task_labels_lower_bound ht

theorem nine_labels_sufficient : ExactReduction Source (Task 8) classify id := by
  constructor
  · intro x b hb
    exact (source_iff x b).2 hb
  · intro x hx
    obtain ⟨y, hy⟩ := hx
    exact ⟨y, (source_iff x y).1 hy⟩

theorem nine_label_count : Fintype.card (Option (Fin 8)) = 9 := by decide

def CanReach (x : Fin 16) : Bool := (classify x).isSome
theorem decision_correct (x : Fin 16) : CanReach x = true ↔ ∃ h, Source x h := by
  revert x
  decide

theorem decision_two_labels_necessary {A : Type*} [Fintype A]
    (encode : Fin 16 → A) (decode : A → Bool)
    (correct : ∀ x, decode (encode x) = CanReach x) : 2 ≤ Fintype.card A := by
  have distinct : encode 0 ≠ encode 1 := by
    intro h
    have same := congrArg decode h
    rw [correct 0, correct 1] at same
    norm_num [CanReach, classify] at same
  have inject : Function.Injective (fun b : Bool => if b then encode 1 else encode 0) := by
    intro a b h
    cases a <;> cases b <;> simp_all
  have bound := Fintype.card_le_of_injective _ inject
  simpa using bound

#print axioms task_encoder_injective
#print axioms task_labels_lower_bound
#print axioms nine_labels_necessary
#print axioms nine_labels_sufficient
#print axioms decision_correct
#print axioms decision_two_labels_necessary

end InformationBudget
