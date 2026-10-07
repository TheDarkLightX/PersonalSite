import Std

/-!
Finite, independent, unit-cost checks on a fixed revision.
Candidate indices are allocated by (round, worker) = (i / k, i % k).
These elementary scheduling facts do not prove an empirical scaling law for LLMs.
-/
namespace FiniteSearch

/-- Ceiling division for positive worker counts, including an empty workload. -/
def rounds (n k : Nat) : Nat :=
  if n = 0 then 0 else (n - 1) / k + 1

/-- Completing by round r is exactly the capacity condition n ≤ r*k. -/
theorem rounds_le_iff_capacity (n k r : Nat) (hk : 0 < k) :
    rounds n k ≤ r ↔ n ≤ r * k := by
  by_cases hn : n = 0
  · subst n
    simp [rounds]
  · simp only [rounds, if_neg hn]
    have hdiv := Nat.div_lt_iff_lt_mul (x := n - 1) (y := r) hk
    omega

/-- More workers cannot increase the completion round under this cost model. -/
theorem more_workers (n k₁ k₂ : Nat) (hk₁ : 0 < k₁) (h : k₁ ≤ k₂) :
    rounds n k₂ ≤ rounds n k₁ := by
  have hk₂ : 0 < k₂ := Nat.lt_of_lt_of_le hk₁ h
  apply (rounds_le_iff_capacity n k₂ (rounds n k₁) hk₂).mpr
  have hc := (rounds_le_iff_capacity n k₁ (rounds n k₁) hk₁).mp (Nat.le_refl _)
  exact Nat.le_trans hc (Nat.mul_le_mul_left _ h)

/-- A smaller workload cannot require more rounds at the same worker count. -/
theorem less_work (m n k : Nat) (hmn : m ≤ n) (hk : 0 < k) :
    rounds m k ≤ rounds n k := by
  apply (rounds_le_iff_capacity m k (rounds n k) hk).mpr
  exact Nat.le_trans hmn
    ((rounds_le_iff_capacity n k (rounds n k) hk).mp (Nat.le_refl _))

/-- Every candidate has an in-range worker and is scheduled before completion. -/
theorem candidate_covered (n k i : Nat) (hk : 0 < k) (hi : i < n) :
    i / k < rounds n k ∧ i % k < k ∧ k * (i / k) + i % k = i := by
  have hc := (rounds_le_iff_capacity n k (rounds n k) hk).mp (Nat.le_refl _)
  exact ⟨(Nat.div_lt_iff_lt_mul hk).mpr (Nat.lt_of_lt_of_le hi hc),
    Nat.mod_lt i hk, Nat.div_add_mod i k⟩

/-- Two candidates assigned the same round and worker are the same candidate. -/
theorem assignment_injective (k i j : Nat)
    (hr : i / k = j / k) (hw : i % k = j % k) : i = j := by
  calc
    i = k * (i / k) + i % k := (Nat.div_add_mod i k).symm
    _ = k * (j / k) + j % k := by rw [hr, hw]
    _ = j := Nat.div_add_mod j k

/-- Negative memory removes only candidates that cannot satisfy this predicate. -/
def SoundRejections {α : Type} (good : α → Prop) (rejected : α → Bool) : Prop :=
  ∀ x, rejected x = true → ¬good x

def remaining {α : Type} (candidates : List α) (rejected : α → Bool) : List α :=
  candidates.filter (fun x => !rejected x)

/-- Sound rejection preserves every solution, not merely existence of one. -/
theorem pruning_preserves_solutions {α : Type} (candidates : List α)
    (good : α → Prop) (rejected : α → Bool) (hs : SoundRejections good rejected)
    (x : α) :
    (x ∈ remaining candidates rejected ∧ good x) ↔ (x ∈ candidates ∧ good x) := by
  constructor
  · intro ⟨hm, hg⟩
    exact ⟨(List.mem_filter.mp hm).1, hg⟩
  · intro ⟨hm, hg⟩
    refine ⟨List.mem_filter.mpr ⟨hm, ?_⟩, hg⟩
    have hn : rejected x ≠ true := fun hx => hs x hx hg
    cases h : rejected x <;> simp_all

/-- Pruning reduces or preserves the number of remaining check rounds.
This arithmetic fact alone does NOT establish that the pruning was sound. -/
theorem pruning_reduces_rounds {α : Type} (candidates : List α)
    (rejected : α → Bool) (k : Nat) (hk : 0 < k) :
    rounds (remaining candidates rejected).length k ≤ rounds candidates.length k := by
  exact less_work _ _ k (List.length_filter_le _ _) hk

/-- Combined result: sound memory keeps all solutions; more workers and the
smaller remaining workload do not increase the ideal completion round. -/
theorem memory_and_workers {α : Type} (candidates : List α)
    (good : α → Prop) (rejected : α → Bool) (hs : SoundRejections good rejected)
    (k₁ k₂ : Nat) (hk₁ : 0 < k₁) (h : k₁ ≤ k₂) :
    (∀ x, (x ∈ remaining candidates rejected ∧ good x) ↔
      (x ∈ candidates ∧ good x)) ∧
    rounds (remaining candidates rejected).length k₂ ≤ rounds candidates.length k₁ := by
  refine ⟨pruning_preserves_solutions candidates good rejected hs, ?_⟩
  exact Nat.le_trans (more_workers _ k₁ k₂ hk₁ h)
    (pruning_reduces_rounds candidates rejected k₁ hk₁)

-- Concrete edge cases are checks alongside the general theorems above.
example : rounds 0 4 = 0 := by decide
example : rounds 32 1 = 32 := by decide
example : rounds 32 4 = 8 := by decide
example : rounds 32 8 = 4 := by decide
example : rounds 33 8 = 5 := by decide
example : rounds 3 8 = 1 := by decide

#print axioms rounds_le_iff_capacity
#print axioms more_workers
#print axioms less_work
#print axioms candidate_covered
#print axioms assignment_injective
#print axioms pruning_preserves_solutions
#print axioms pruning_reduces_rounds
#print axioms memory_and_workers

end FiniteSearch
