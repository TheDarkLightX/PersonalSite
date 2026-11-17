import Arithmetic

/-! An exact scalar representation of the full real exp-minus-log calculator
is either injective or constant. This is not a theorem about a single seed's orbit. -/
noncomputable section
namespace StrictEML

def colorEval {Q : Type*} (op : Q → Q → Q) (unit : Q) (ρ : Nat → Q) : Term → Q
  | .one => unit
  | .var n => ρ n
  | .node a b => op (colorEval op unit ρ a) (colorEval op unit ρ b)

theorem colorEval_eq {Q : Type*} (h : ℝ → Q) (op : Q → Q → Q)
    (hF : ∀ a b : ℝ, 0 < b → h (Real.exp a - Real.log b) = op (h a) (h b))
    (t : Term) (ρ : Nat → ℝ) (ht : Valid t ρ) :
    h (val t ρ) = colorEval op (h 1) (fun n => h (ρ n)) t := by
  induction t with
  | one => rfl
  | var n => rfl
  | node a b iha ihb =>
    rcases ht with ⟨ha, hb, hpos⟩
    change h (Real.exp (val a ρ) - Real.log (val b ρ)) = _
    rw [hF _ _ hpos, iha ha, ihb hb]
    rfl

theorem sub_mul_injective_or_constant {Q : Type*} (h : ℝ → Q)
    (subQ mulQ : Q → Q → Q)
    (hsub : ∀ x y, h (x-y) = subQ (h x) (h y))
    (hmul : ∀ x y, h (x*y) = mulQ (h x) (h y)) :
    Function.Injective h ∨ ∀ x, h x = h 0 := by
  by_cases h01 : h 0 = h 1
  · right
    intro x
    calc
      h x = h (x * 1) := by rw [mul_one]
      _ = mulQ (h x) (h 1) := hmul x 1
      _ = mulQ (h x) (h 0) := by rw [h01]
      _ = h (x * 0) := (hmul x 0).symm
      _ = h 0 := by rw [mul_zero]
  · left
    intro a b hab
    by_contra hne
    have hd : a-b ≠ 0 := sub_ne_zero.mpr hne
    have hdiff : h (a-b) = h 0 := by
      calc
        h (a-b) = subQ (h a) (h b) := hsub a b
        _ = subQ (h b) (h b) := by rw [hab]
        _ = h (b-b) := (hsub b b).symm
        _ = h 0 := by rw [sub_self]
    have h10 : h 1 = h 0 := by
      calc
        h 1 = h ((a-b) * (a-b)⁻¹) := by rw [mul_inv_cancel₀ hd]
        _ = mulQ (h (a-b)) (h ((a-b)⁻¹)) := hmul _ _
        _ = mulQ (h 0) (h ((a-b)⁻¹)) := by rw [hdiff]
        _ = h (0 * (a-b)⁻¹) := (hmul _ _).symm
        _ = h 0 := by rw [zero_mul]
    exact h01 h10.symm

theorem exact_scalar_injective_or_constant {Q : Type*} (h : ℝ → Q)
    (op : Q → Q → Q)
    (hF : ∀ a b : ℝ, 0 < b → h (Real.exp a - Real.log b) = op (h a) (h b)) :
    Function.Injective h ∨ ∀ x, h x = h 0 := by
  let env (x y : ℝ) : Nat → ℝ := fun n => if n = 0 then x else y
  let envQ (x y : Q) : Nat → Q := fun n => if n = 0 then x else y
  let subQ (x y : Q) := colorEval op (h 1) (envQ x y) (S (.var 0) (.var 1))
  let mulQ (x y : Q) := colorEval op (h 1) (envQ x y) (M (.var 0) (.var 1))
  apply sub_mul_injective_or_constant h subQ mulQ
  · intro x y
    have hx : Realizes (.var 0) (env x y) x := by exact ⟨trivial, rfl⟩
    have hy : Realizes (.var 1) (env x y) y := by exact ⟨trivial, rfl⟩
    have hs := repS hx hy
    have hc := colorEval_eq h op hF (S (.var 0) (.var 1)) (env x y) hs.1
    rw [hs.2] at hc
    convert hc using 1
  · intro x y
    have hx : Realizes (.var 0) (env x y) x := by exact ⟨trivial, rfl⟩
    have hy : Realizes (.var 1) (env x y) y := by exact ⟨trivial, rfl⟩
    have hm := repM hx hy
    have hc := colorEval_eq h op hF (M (.var 0) (.var 1)) (env x y) hm.1
    rw [hm.2] at hc
    convert hc using 1

theorem finite_exact_scalar_constant {Q : Type*} [Finite Q] (h : ℝ → Q)
    (op : Q → Q → Q)
    (hF : ∀ a b : ℝ, 0 < b → h (Real.exp a - Real.log b) = op (h a) (h b)) :
    ∀ x, h x = h 0 := by
  rcases exact_scalar_injective_or_constant h op hF with hi | hc
  · exact False.elim (Finite.false (Finite.of_injective h hi))
  · exact hc

/-- Four arithmetic tests already forbid a two-color map distinguishing zero and one.
`half` is the color assigned to 1/2; its choice does not affect the contradiction. -/
theorem no_two_color_half_extension (zero one two half : Bool)
    (subQ mulQ : Bool → Bool → Bool)
    (h01 : zero ≠ one)
    (hsub21 : subQ two one = one)
    (hsub11 : subQ one one = zero)
    (hmul2half : mulQ two half = one)
    (hmul0half : mulQ zero half = zero) : False := by
  have h21 : two ≠ one := by
    intro h
    rw [h] at hsub21
    exact h01 (hsub11.symm.trans hsub21)
  have h20 : two = zero := by
    cases zero <;> cases one <;> cases two <;> simp_all
  rw [h20] at hmul2half
  exact h01 (hmul0half.symm.trans hmul2half)

#print axioms exact_scalar_injective_or_constant
#print axioms finite_exact_scalar_constant
#print axioms no_two_color_half_extension
end StrictEML
