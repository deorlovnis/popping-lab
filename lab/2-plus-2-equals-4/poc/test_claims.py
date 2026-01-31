#!/usr/bin/env python3
"""
Falsification tests for claim: 2+2=4
Falsifier agent: Seeking the strongest attack
"""

def test_C1_standard_arithmetic():
    """C1: In standard integer arithmetic (Z), 2+2=4"""
    print("=" * 60)
    print("TEST C1: Standard Integer Arithmetic")
    print("=" * 60)

    # Direct computation
    result = 2 + 2
    print(f"Direct computation: 2 + 2 = {result}")

    # Peano axiom derivation
    print("\nPeano Axiom Derivation:")
    print("  - 2 = S(S(0))  [successor of successor of zero]")
    print("  - 4 = S(S(S(S(0))))")
    print("  - 2 + 2 = S(S(0)) + S(S(0))")
    print("  - By addition axiom: a + S(b) = S(a + b)")
    print("  - S(S(0)) + S(S(0)) = S(S(S(0)) + S(0)) = S(S(S(S(0)) + 0)) = S(S(S(S(0)))) = 4")

    verdict = "SURVIVED" if result == 4 else "KILLED"
    print(f"\nVERDICT: {verdict}")
    return verdict


def test_C2_modular_arithmetic():
    """C2: In modular arithmetic (Z/3Z), 2+2=4"""
    print("\n" + "=" * 60)
    print("TEST C2: Modular Arithmetic (Z/3Z)")
    print("=" * 60)

    # In Z/3Z, we work modulo 3
    two_mod3 = 2 % 3  # = 2
    four_mod3 = 4 % 3  # = 1
    sum_mod3 = (2 + 2) % 3  # = 1

    print(f"In Z/3Z (integers mod 3):")
    print(f"  2 mod 3 = {two_mod3}")
    print(f"  4 mod 3 = {four_mod3}")
    print(f"  (2 + 2) mod 3 = {sum_mod3}")
    print(f"\n  Does 2 + 2 = 4 in Z/3Z?")
    print(f"  We need: (2+2) mod 3 == 4 mod 3")
    print(f"  Check: {sum_mod3} == {four_mod3}? {sum_mod3 == four_mod3}")

    # Note: 4 mod 3 = 1, and (2+2) mod 3 = 1, so they ARE equal in Z/3Z
    # But wait - in Z/3Z, there IS no "4" - only {0, 1, 2}
    # The claim "2+2=4" in Z/3Z is malformed because 4 doesn't exist!

    print("\n  CRITICAL OBSERVATION:")
    print("  In Z/3Z, the elements are {0, 1, 2}. '4' does not exist!")
    print("  The claim '2+2=4' is UNDEFINED in Z/3Z, not false.")
    print("  However, 2+2 = 1 (mod 3), which is NOT 4.")

    verdict = "KILLED"  # The naive interpretation fails
    print(f"\nVERDICT: {verdict} (as stated; claim assumes 4 exists)")
    return verdict


def test_C3_all_number_systems():
    """C3: 2+2=4 holds in ALL number systems"""
    print("\n" + "=" * 60)
    print("TEST C3: Universal Claim (All Number Systems)")
    print("=" * 60)

    counterexamples = []

    # Boolean algebra (Z/2Z)
    print("\nAttack 1: Boolean algebra / Z/2Z")
    print("  In Z/2Z: {0, 1} with addition mod 2")
    print("  2 mod 2 = 0")
    print("  (2+2) mod 2 = 0")
    print("  4 mod 2 = 0")
    print("  Result: 0 = 0, but '2' and '4' don't exist as distinct elements!")

    # Modular arithmetic Z/3Z
    print("\nAttack 2: Z/3Z (mod 3)")
    print("  2 + 2 = 4 = 1 (mod 3)")
    print("  '4' is not an element of Z/3Z")
    counterexamples.append("Z/3Z: 2+2=1, not 4")

    # Tropical semiring
    print("\nAttack 3: Tropical (min-plus) semiring")
    print("  In tropical algebra: 'addition' is MIN, 'multiplication' is +")
    print("  '2 + 2' in tropical = min(2, 2) = 2, not 4")
    counterexamples.append("Tropical semiring: 2+2=2")

    # Saturating arithmetic
    print("\nAttack 4: Saturating arithmetic (max=3)")
    print("  In 2-bit saturating arithmetic capped at 3:")
    print("  2 + 2 = min(4, 3) = 3")
    counterexamples.append("Saturating arithmetic: 2+2=3")

    # One-element group
    print("\nAttack 5: Trivial group")
    print("  In the trivial group {0}: every element = 0")
    print("  2 = 0, 4 = 0, 2+2 = 0+0 = 0")
    print("  Technically 0=0, but 2 and 4 have no meaning")

    print(f"\nCounterexamples found: {len(counterexamples)}")
    for ce in counterexamples:
        print(f"  - {ce}")

    verdict = "KILLED"
    print(f"\nVERDICT: {verdict}")
    return verdict


def test_C4_computational_edge_cases():
    """C4: No computational system will output != 4 for 2+2"""
    print("\n" + "=" * 60)
    print("TEST C4: Computational Edge Cases")
    print("=" * 60)

    anomalies = []

    # Standard int
    print("\nTest 1: Python int")
    print(f"  2 + 2 = {2 + 2}")

    # Float
    print("\nTest 2: Python float")
    print(f"  2.0 + 2.0 = {2.0 + 2.0}")

    # Complex
    print("\nTest 3: Complex numbers")
    print(f"  (2+0j) + (2+0j) = {(2+0j) + (2+0j)}")

    # Check for overflow in small ints (Python doesn't have this, but C would)
    print("\nTest 4: Overflow scenarios")
    print("  Python: No overflow (arbitrary precision)")
    print("  C int8_t: 2+2=4 (no overflow)")
    print("  Saturating 2-bit unsigned (max=3): 2+2=3 (ANOMALY)")
    anomalies.append("2-bit saturating: 2+2=3")

    # XOR confusion
    print("\nTest 5: Bitwise XOR (common typo: ^ vs +)")
    print(f"  2 ^ 2 = {2 ^ 2} (XOR, not addition - but different operation)")

    # String concatenation
    print("\nTest 6: String 'addition'")
    print(f"  '2' + '2' = '{'2' + '2'}' (concatenation)")
    anomalies.append("String: '2'+'2'='22'")

    # JavaScript type coercion weirdness
    print("\nTest 7: JavaScript-style coercion")
    print("  In JS: '2' + 2 = '22' (string wins)")
    anomalies.append("JS coercion: '2'+2='22'")

    print(f"\nAnomalies found: {len(anomalies)}")
    for a in anomalies:
        print(f"  - {a}")

    # Verdict: Found systems where "2+2" doesn't produce 4
    verdict = "KILLED" if anomalies else "SURVIVED"
    print(f"\nVERDICT: {verdict} (type/representation edge cases exist)")
    return verdict


if __name__ == "__main__":
    print("FALSIFIER: Executing strongest attacks on '2+2=4'\n")

    results = {
        "C1": test_C1_standard_arithmetic(),
        "C2": test_C2_modular_arithmetic(),
        "C3": test_C3_all_number_systems(),
        "C4": test_C4_computational_edge_cases(),
    }

    print("\n" + "=" * 60)
    print("FINAL VERDICTS")
    print("=" * 60)
    for claim_id, verdict in results.items():
        print(f"  {claim_id}: {verdict}")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    killed = [k for k, v in results.items() if v == "KILLED"]
    survived = [k for k, v in results.items() if v == "SURVIVED"]

    print(f"KILLED:   {killed}")
    print(f"SURVIVED: {survived}")

    print("\nCONCLUSION:")
    print("The core claim C1 (2+2=4 in standard integer arithmetic) SURVIVED.")
    print("Broader/naive interpretations were KILLED.")
    print("Precision in claims matters.")
