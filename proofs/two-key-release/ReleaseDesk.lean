import Std

/-! A policy model for the two-key release case. This is not a proof of the
Rust compiler, JavaScript, authentication, SQLite or external delivery.
All finite typed inputs are separately compared with the real Authority.
The correspondence between that executable check and this model is reviewed,
not a machine-checked Rust-to-Lean refinement. No human approval is assumed. -/

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000

namespace ReleaseDesk

inductive Status | pending | approved | cancelled deriving DecidableEq, Repr
inductive Officer | nobody | alice | bob | carol deriving DecidableEq, Repr
inductive Command | approve | cancel deriving DecidableEq, Repr
inductive Class | accept | reject | failure | refused deriving DecidableEq, Repr

structure State where
  status : Status
  first : Officer
  second : Officer
  deriving DecidableEq, Repr

structure Decision where
  kind : Class
  next : State
  releases : Nat

def valid (s : State) : Prop :=
  if s.status = .approved then
    s.first ≠ .nobody ∧ s.second ≠ .nobody ∧ s.first ≠ s.second
  else s.second = .nobody

instance (s : State) : Decidable (valid s) := by unfold valid; infer_instance

def genesis : State := ⟨.pending, .nobody, .nobody⟩

def commit (pre post : State) (kind : Class) (releases : Nat) : Decision :=
  if valid post then ⟨kind, post, releases⟩ else ⟨.refused, pre, 0⟩

def step (s : State) (a : Command) (o : Officer) : Decision :=
  if s.status ≠ .pending then ⟨.reject, s, 0⟩
  else if o = .nobody then ⟨.reject, s, 0⟩
  else if a = .cancel then commit s ⟨.cancelled, s.first, s.second⟩ .failure 0
  else if o = s.first then ⟨.reject, s, 0⟩
  else if s.first = .nobody then commit s ⟨.pending, o, s.second⟩ .accept 0
  else commit s ⟨.approved, s.first, o⟩ .accept 1

/-- The small one-step obligation is checked for every enum combination. -/
theorem step_preserves (s : State) (a : Command) (o : Officer) :
    valid s → valid (step s a o).next := by
  rcases s with ⟨status, first, second⟩
  cases status <;> cases first <;> cases second <;> cases a <;> cases o <;> decide

theorem reject_changes_nothing (s : State) (a : Command) (o : Officer) :
    (step s a o).kind = .reject → (step s a o).next = s ∧ (step s a o).releases = 0 := by
  rcases s with ⟨status, first, second⟩
  cases status <;> cases first <;> cases second <;> cases a <;> cases o <;> decide

theorem release_requires_two_keys (s : State) (a : Command) (o : Officer) :
    (step s a o).releases = 1 →
    s.first ≠ .nobody ∧ o ≠ .nobody ∧ s.first ≠ o ∧ (step s a o).next.status = .approved := by
  rcases s with ⟨status, first, second⟩
  cases status <;> cases first <;> cases second <;> cases a <;> cases o <;> decide

def credit (s : State) : Nat := if s.status = .pending then 1 else 0

theorem release_spends_credit (s : State) (a : Command) (o : Officer) :
    (step s a o).releases + credit (step s a o).next ≤ credit s := by
  rcases s with ⟨status, first, second⟩
  cases status <;> cases first <;> cases second <;> cases a <;> cases o <;> decide

def run (s : State) : List (Command × Officer) → State
  | [] => s
  | (a, o) :: rest => run (step s a o).next rest

def released (s : State) : List (Command × Officer) → Nat
  | [] => 0
  | (a, o) :: rest => (step s a o).releases + released (step s a o).next rest

theorem history_preserves (s : State) (actions : List (Command × Officer))
    (initial : valid s) : valid (run s actions) := by
  induction actions generalizing s with
  | nil => exact initial
  | cons head tail ih =>
    exact ih (step s head.1 head.2).next (step_preserves s head.1 head.2 initial)

theorem history_spends_credit (s : State) (actions : List (Command × Officer)) :
    released s actions + credit (run s actions) ≤ credit s := by
  induction actions generalizing s with
  | nil => simp [released, run]
  | cons head tail ih =>
    have h := ih (step s head.1 head.2).next
    have k := release_spends_credit s head.1 head.2
    change (step s head.1 head.2).releases + released (step s head.1 head.2).next tail +
      credit (run (step s head.1 head.2).next tail) ≤ credit s
    exact Nat.le_trans (Nat.add_assoc _ _ _ ▸ Nat.add_le_add_left h _) k

/-- This quantifies over arbitrary finite histories, not only a test depth. -/
theorem every_history_is_safe (actions : List (Command × Officer)) :
    valid (run genesis actions) ∧ released genesis actions ≤ 1 := by
  constructor
  · exact history_preserves genesis actions (by decide)
  · have h := history_spends_credit genesis actions
    exact Nat.le_trans (Nat.le_add_right _ _) h

#print axioms step_preserves
#print axioms reject_changes_nothing
#print axioms release_requires_two_keys
#print axioms release_spends_credit
#print axioms history_preserves
#print axioms history_spends_credit
#print axioms every_history_is_safe

end ReleaseDesk
