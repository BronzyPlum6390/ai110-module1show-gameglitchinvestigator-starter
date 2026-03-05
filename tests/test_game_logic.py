from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Bug regression tests ---

def test_low_guess_vs_high_secret_is_too_low():
    # Regression for the backwards-hint bug.
    # Bug: app.py was passing secret as a string on even attempts, causing
    # Python string comparison ("1" > "99" is False, "1" < "99" is True,
    # but str("1") > str("9") is False because "1" < "9" lexicographically).
    # The real broken case: guess=1, secret=99 was returning "Too High" instead of "Too Low".
    # Both arguments must be integers for correct numeric comparison.
    outcome, message = check_guess(1, 99)
    assert outcome == "Too Low", (
        f"Expected 'Too Low' but got '{outcome}'. "
        "This likely means secret was compared as a string instead of an int."
    )
    assert "HIGHER" in message, (
        f"Guess is too low so hint must say Go HIGHER, but got: '{message}'"
    )

def test_high_guess_vs_low_secret_is_too_high():
    # Companion regression: guess=99, secret=1 must be "Too High", not "Too Low".
    outcome, message = check_guess(99, 1)
    assert outcome == "Too High", (
        f"Expected 'Too High' but got '{outcome}'. "
        "This likely means secret was compared as a string instead of an int."
    )
    assert "LOWER" in message, (
        f"Guess is too high so hint must say Go LOWER, but got: '{message}'"
    )

def test_string_secret_gives_wrong_hint():
    # Explicitly documents what the bug looked like before the fix.
    # When secret is accidentally passed as a string, the fallback in check_guess
    # does lexicographic comparison: str(1)="1", str(99)="99", "1" < "9" → "Too Low" ✓
    # but str(1)="1" vs str(9)="9" → "1" < "9" is True (correct by luck),
    # while str(10)="10" vs str(9)="9" → "10" > "9" is False (WRONG — 10 > 9 numerically).
    # This test catches that string comparison breaks for multi-digit numbers.
    outcome, message = check_guess(10, "9")
    # 10 > 9 numerically → should be "Too High", but string "10" < "9" → would give "Too Low"
    assert outcome == "Too High", (
        f"Expected 'Too High' but got '{outcome}'. "
        "String comparison of '10' vs '9' is lexicographic and gives the wrong answer."
    )
