import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic

/-! Strict finite real EML syntax and checked arithmetic constructions.
Every domain theorem refers to `Valid`, not merely Mathlib's total real logarithm.
-/
noncomputable section
namespace StrictEML

inductive Term where
  | one : Term
  | var : Nat → Term
  | node : Term → Term → Term
  deriving DecidableEq

open Term

def val : Term → (Nat → ℝ) → ℝ
  | one, _ => 1
  | var n, ρ => ρ n
  | node a b, ρ => Real.exp (val a ρ) - Real.log (val b ρ)

def Valid : Term → (Nat → ℝ) → Prop
  | one, _ => True
  | var _, _ => True
  | node a b, ρ => Valid a ρ ∧ Valid b ρ ∧ 0 < val b ρ

def Realizes (t : Term) (ρ : Nat → ℝ) (x : ℝ) : Prop := Valid t ρ ∧ val t ρ = x

def nodes : Term → Nat
  | one => 0
  | var _ => 0
  | node a b => 1 + nodes a + nodes b

def E (x : Term) := node x one
def L (x : Term) := node one (E (node one x))
def P (x : Term) := node x (E x)
def H (x : Term) := L (P x)
def A (x y : Term) := node y (E (node (H y) (E x)))
def S (x y : Term) := node (H y) (E (node y (E x)))
def J (x : Term) := node (H x) (P x)
def B (x y : Term) := node x (E (node (H x) (P y)))
def Q (x y : Term) := node (H x) (E (node (L (J x)) (P y)))
def T (a b d c : Term) := node a (E (node b (E (node d (E (E c))))))
def M (x y : Term) := T (A x y) (B x y) (Q x y) (B y x)
def R (x : Term) := node (E x) (E x)
def Dpos (x y : Term) := node (node x y) (E (E (node (L (L (R x))) y)))
def I (x : Term) := Dpos x (M x x)
def D (x y : Term) := Dpos (M x y) (M y y)

def envelope (x : ℝ) := Real.exp x - x
def jvalue (x : ℝ) := envelope x - Real.log (envelope x)
def renvelope (x : ℝ) := Real.exp (Real.exp x) - x

theorem envelope_ge_one (x : ℝ) : 1 ≤ envelope x := by
  have := Real.add_one_le_exp x
  dsimp [envelope]
  linarith

theorem envelope_pos (x : ℝ) : 0 < envelope x := lt_of_lt_of_le zero_lt_one (envelope_ge_one x)

theorem jvalue_ge_one (x : ℝ) : 1 ≤ jvalue x := by
  have := Real.log_le_sub_one_of_pos (envelope_pos x)
  dsimp [jvalue]
  linarith

theorem jvalue_pos (x : ℝ) : 0 < jvalue x := lt_of_lt_of_le zero_lt_one (jvalue_ge_one x)

theorem renvelope_gt_one (x : ℝ) : 1 < renvelope x := by
  have h₁ := Real.add_one_le_exp x
  have h₂ := Real.add_one_le_exp (Real.exp x)
  dsimp [renvelope]
  linarith

theorem repOne (ρ : Nat → ℝ) : Realizes one ρ 1 := ⟨trivial, rfl⟩
theorem repVar (ρ : Nat → ℝ) (n : Nat) : Realizes (var n) ρ (ρ n) := ⟨trivial, rfl⟩
theorem repNode {a b : Term} {ρ : Nat → ℝ} {x y : ℝ}
    (ha : Realizes a ρ x) (hb : Realizes b ρ y) (hy : 0 < y) :
    Realizes (node a b) ρ (Real.exp x - Real.log y) := by
  rcases ha with ⟨ha, rfl⟩
  rcases hb with ⟨hb, rfl⟩
  exact ⟨⟨ha, hb, hy⟩, rfl⟩

theorem repE {a : Term} {ρ : Nat → ℝ} {x : ℝ} (ha : Realizes a ρ x) :
    Realizes (E a) ρ (Real.exp x) := by
  simpa [E] using repNode ha (repOne ρ) zero_lt_one

theorem repL {a : Term} {ρ : Nat → ℝ} {x : ℝ} (ha : Realizes a ρ x) (hx : 0 < x) :
    Realizes (L a) ρ (Real.log x) := by
  have h := repNode (repOne ρ) (repE (repNode (repOne ρ) ha hx)) (Real.exp_pos _)
  simpa [L, Real.log_exp] using h

theorem repP {a : Term} {ρ : Nat → ℝ} {x : ℝ} (ha : Realizes a ρ x) :
    Realizes (P a) ρ (envelope x) := by
  simpa [P, envelope, Real.log_exp] using repNode ha (repE ha) (Real.exp_pos _)

theorem repH {a : Term} {ρ : Nat → ℝ} {x : ℝ} (ha : Realizes a ρ x) :
    Realizes (H a) ρ (Real.log (envelope x)) := repL (repP ha) (envelope_pos x)

theorem repA {a b : Term} {ρ : Nat → ℝ} {x y : ℝ}
    (ha : Realizes a ρ x) (hb : Realizes b ρ y) : Realizes (A a b) ρ (x+y) := by
  have h := repNode hb (repE (repNode (repH hb) (repE ha) (Real.exp_pos _))) (Real.exp_pos _)
  simp only [Real.exp_log (envelope_pos y), Real.log_exp] at h
  convert h using 1; dsimp [A, envelope]; ring

theorem repS {a b : Term} {ρ : Nat → ℝ} {x y : ℝ}
    (ha : Realizes a ρ x) (hb : Realizes b ρ y) : Realizes (S a b) ρ (x-y) := by
  have h := repNode (repH hb) (repE (repNode hb (repE ha) (Real.exp_pos _))) (Real.exp_pos _)
  simp only [Real.exp_log (envelope_pos y), Real.log_exp] at h
  convert h using 1; dsimp [S, envelope]; ring

theorem repJ {a : Term} {ρ : Nat → ℝ} {x : ℝ} (ha : Realizes a ρ x) :
    Realizes (J a) ρ (jvalue x) := by
  simpa [J, jvalue, Real.exp_log (envelope_pos x)] using
    repNode (repH ha) (repP ha) (envelope_pos x)

theorem repB {a b : Term} {ρ : Nat → ℝ} {x y : ℝ}
    (ha : Realizes a ρ x) (hb : Realizes b ρ y) :
    Realizes (B a b) ρ (x + Real.log (envelope y)) := by
  have h := repNode ha (repE (repNode (repH ha) (repP hb) (envelope_pos y))) (Real.exp_pos _)
  simp only [Real.exp_log (envelope_pos x), Real.log_exp] at h
  convert h using 1; dsimp [B, envelope]; ring

theorem repQ {a b : Term} {ρ : Nat → ℝ} {x y : ℝ}
    (ha : Realizes a ρ x) (hb : Realizes b ρ y) :
    Realizes (Q a b) ρ (Real.log (envelope x) + Real.log (envelope y)) := by
  have h := repNode (repH ha)
    (repE (repNode (repL (repJ ha) (jvalue_pos x)) (repP hb) (envelope_pos y)))
    (Real.exp_pos _)
  simp only [Real.exp_log (envelope_pos x), Real.exp_log (jvalue_pos x), Real.log_exp] at h
  convert h using 1; dsimp [Q, jvalue]; ring

theorem repT {a b d c : Term} {ρ : Nat → ℝ} {w x y z : ℝ}
    (ha : Realizes a ρ w) (hb : Realizes b ρ x)
    (hd : Realizes d ρ y) (hc : Realizes c ρ z) :
    Realizes (T a b d c) ρ (Real.exp w - Real.exp x + Real.exp y - Real.exp z) := by
  have h := repNode ha
    (repE (repNode hb (repE (repNode hd (repE (repE hc)) (Real.exp_pos _)))
      (Real.exp_pos _))) (Real.exp_pos _)
  simp only [Real.log_exp] at h
  convert h using 1; dsimp [T]; ring

theorem repM {a b : Term} {ρ : Nat → ℝ} {x y : ℝ}
    (ha : Realizes a ρ x) (hb : Realizes b ρ y) : Realizes (M a b) ρ (x*y) := by
  have h := repT (repA ha hb) (repB ha hb) (repQ ha hb) (repB hb ha)
  simp only [Real.exp_add, Real.exp_log (envelope_pos x), Real.exp_log (envelope_pos y)] at h
  convert h using 1; dsimp [M, envelope]; ring

theorem repR {a : Term} {ρ : Nat → ℝ} {x : ℝ} (ha : Realizes a ρ x) :
    Realizes (R a) ρ (renvelope x) := by
  simpa [R, renvelope, Real.log_exp] using repNode (repE ha) (repE ha) (Real.exp_pos _)

theorem repDpos {a b : Term} {ρ : Nat → ℝ} {x y : ℝ}
    (ha : Realizes a ρ x) (hb : Realizes b ρ y) (hy : 0 < y) :
    Realizes (Dpos a b) ρ (x/y) := by
  have hr := renvelope_gt_one x
  have hrp : 0 < renvelope x := lt_trans zero_lt_one hr
  have hlp : 0 < Real.log (renvelope x) := Real.log_pos hr
  have h := repNode (repNode ha hb hy)
    (repE (repE (repNode (repL (repL (repR ha) hrp) hlp) hb hy))) (Real.exp_pos _)
  simp only [Real.log_exp, Real.exp_log hlp, Real.exp_sub,
    Real.exp_log hy, Real.exp_log hrp] at h
  convert h using 1; dsimp [Dpos, renvelope]; ring

theorem repI {a : Term} {ρ : Nat → ℝ} {x : ℝ}
    (ha : Realizes a ρ x) (hx : x ≠ 0) : Realizes (I a) ρ (1/x) := by
  have hxx : 0 < x*x := mul_self_pos.mpr hx
  have h := repDpos ha (repM ha ha) hxx
  convert h using 1; dsimp [I]
  field_simp

theorem repD {a b : Term} {ρ : Nat → ℝ} {x y : ℝ}
    (ha : Realizes a ρ x) (hb : Realizes b ρ y) (hy : y ≠ 0) :
    Realizes (D a b) ρ (x/y) := by
  have hyy : 0 < y*y := mul_self_pos.mpr hy
  have h := repDpos (repM ha hb) (repM hb hb) hyy
  convert h using 1; dsimp [D]
  field_simp

/-- The positive-denominator macro has exactly its declared strict natural domain. -/
theorem validDpos_iff (a b : Term) (ρ : Nat → ℝ) :
    Valid (Dpos a b) ρ ↔ Valid a ρ ∧ Valid b ρ ∧ 0 < val b ρ := by
  constructor
  · intro h
    exact ⟨h.1.1, h.1.2.1, h.1.2.2⟩
  · rintro ⟨ha, hb, hy⟩
    exact (repDpos ⟨ha, rfl⟩ ⟨hb, rfl⟩ hy).1

theorem validM_iff (a b : Term) (ρ : Nat → ℝ) :
    Valid (M a b) ρ ↔ Valid a ρ ∧ Valid b ρ := by
  constructor
  · intro h
    exact ⟨h.1.2.1.1.2.1.1, h.1.1⟩
  · rintro ⟨ha, hb⟩
    exact (repM ⟨ha, rfl⟩ ⟨hb, rfl⟩).1

theorem validI_iff (a : Term) (ρ : Nat → ℝ) :
    Valid (I a) ρ ↔ Valid a ρ ∧ val a ρ ≠ 0 := by
  constructor
  · intro h
    obtain ⟨ha, _, hp⟩ := (validDpos_iff a (M a a) ρ).mp h
    rw [(repM ⟨ha,rfl⟩ ⟨ha,rfl⟩).2] at hp
    exact ⟨ha, mul_self_pos.mp hp⟩
  · rintro ⟨ha, hx⟩
    exact (repI ⟨ha,rfl⟩ hx).1

theorem validD_iff (a b : Term) (ρ : Nat → ℝ) :
    Valid (D a b) ρ ↔ Valid a ρ ∧ Valid b ρ ∧ val b ρ ≠ 0 := by
  constructor
  · intro h
    obtain ⟨hab, _, hp⟩ := (validDpos_iff (M a b) (M b b) ρ).mp h
    obtain ⟨ha,hb⟩ := (validM_iff a b ρ).mp hab
    rw [(repM ⟨hb,rfl⟩ ⟨hb,rfl⟩).2] at hp
    exact ⟨ha,hb,mul_self_pos.mp hp⟩
  · rintro ⟨ha,hb,hy⟩
    exact (repD ⟨ha,rfl⟩ ⟨hb,rfl⟩ hy).1

/-- A finite expression's denotation is inside every set closed under its strict constructor. -/
theorem stable_eval_mem (K : Set ℝ) (h1 : (1:ℝ) ∈ K)
    (hF : ∀ a ∈ K, ∀ b ∈ K, 0 < b → Real.exp a - Real.log b ∈ K)
    (ρ : Nat → ℝ) (hρ : ∀ n, ρ n ∈ K) (t : Term) (ht : Valid t ρ) : val t ρ ∈ K := by
  induction t with
  | one => exact h1
  | var n => exact hρ n
  | node a b ia ib => exact hF _ (ia ht.1) _ (ib ht.2.1) ht.2.2

theorem stable_realizes_mem (K : Set ℝ) (h1 : (1:ℝ) ∈ K)
    (hF : ∀ a ∈ K, ∀ b ∈ K, 0 < b → Real.exp a - Real.log b ∈ K)
    (ρ : Nat → ℝ) (hρ : ∀ n, ρ n ∈ K) {t : Term} {x : ℝ} (ht : Realizes t ρ x) : x ∈ K := by
  rw [← ht.2]
  exact stable_eval_mem K h1 hF ρ hρ t ht.1

theorem stable_add (K : Set ℝ) (h1 : (1:ℝ) ∈ K)
    (hF : ∀ a ∈ K, ∀ b ∈ K, 0 < b → Real.exp a - Real.log b ∈ K)
    {x y : ℝ} (hx : x ∈ K) (hy : y ∈ K) : x+y ∈ K := by
  let ρ : Nat → ℝ := fun n => if n = 0 then x else y
  have hρ : ∀ n, ρ n ∈ K := by intro n; dsimp [ρ]; split_ifs <;> assumption
  have hx' : Realizes (var 0) ρ x := by simpa [ρ] using repVar ρ 0
  have hy' : Realizes (var 1) ρ y := by simpa [ρ] using repVar ρ 1
  exact stable_realizes_mem K h1 hF ρ hρ (repA hx' hy')

theorem stable_sub (K : Set ℝ) (h1 : (1:ℝ) ∈ K)
    (hF : ∀ a ∈ K, ∀ b ∈ K, 0 < b → Real.exp a - Real.log b ∈ K)
    {x y : ℝ} (hx : x ∈ K) (hy : y ∈ K) : x-y ∈ K := by
  let ρ : Nat → ℝ := fun n => if n = 0 then x else y
  have hρ : ∀ n, ρ n ∈ K := by intro n; dsimp [ρ]; split_ifs <;> assumption
  have hx' : Realizes (var 0) ρ x := by simpa [ρ] using repVar ρ 0
  have hy' : Realizes (var 1) ρ y := by simpa [ρ] using repVar ρ 1
  exact stable_realizes_mem K h1 hF ρ hρ (repS hx' hy')

theorem stable_div_pos (K : Set ℝ) (h1 : (1:ℝ) ∈ K)
    (hF : ∀ a ∈ K, ∀ b ∈ K, 0 < b → Real.exp a - Real.log b ∈ K)
    {x y : ℝ} (hx : x ∈ K) (hy : y ∈ K) (hyp : 0 < y) : x/y ∈ K := by
  let ρ : Nat → ℝ := fun n => if n = 0 then x else y
  have hρ : ∀ n, ρ n ∈ K := by intro n; dsimp [ρ]; split_ifs <;> assumption
  have hx' : Realizes (var 0) ρ x := by simpa [ρ] using repVar ρ 0
  have hy' : Realizes (var 1) ρ y := by simpa [ρ] using repVar ρ 1
  exact stable_realizes_mem K h1 hF ρ hρ (repDpos hx' hy' hyp)

theorem stable_one_rat_mem (K : Set ℝ) (h1 : (1:ℝ) ∈ K)
    (hF : ∀ a ∈ K, ∀ b ∈ K, 0 < b → Real.exp a - Real.log b ∈ K) (q : ℚ) : (q:ℝ) ∈ K := by
  have h0 : (0:ℝ) ∈ K := by simpa using stable_sub K h1 hF h1 h1
  have hn : ∀ n : Nat, (n:ℝ) ∈ K := by
    intro n
    induction n with
    | zero => simpa using h0
    | succ n ih => simpa using stable_add K h1 hF ih h1
  have hz : ∀ z : Int, (z:ℝ) ∈ K := by
    intro z
    cases z with
    | ofNat n => simpa using hn n
    | negSucc n => simpa using stable_sub K h1 hF h0 (hn (n+1))
  rw [Rat.cast_def]
  exact stable_div_pos K h1 hF (hz q.num) (hn q.den) (by exact_mod_cast q.pos)

theorem multiplication_nodes : nodes (M (var 0) (var 1)) = 57 := by decide
theorem positive_division_nodes : nodes (Dpos (var 0) (var 1)) = 14 := by decide
theorem reciprocal_nodes : nodes (I (var 0)) = 128 := by decide
theorem division_nodes : nodes (D (var 0) (var 1)) = 299 := by decide

end StrictEML
