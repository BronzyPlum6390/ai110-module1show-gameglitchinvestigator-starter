# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

it looked nice but the functionality was off
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

  The bugs I found: (1) guesses below the valid range (e.g. negative numbers) were accepted with no error, (2) hints were backwards — secret was 99, I guessed 1, and it kept saying LOWER, and (3) even after fixing the string/int comparison bug, the hint messages themselves were swapped: "Too Low" was paired with "Go LOWER!" and "Too High" with "Go HIGHER!", which is the opposite of what they should say.
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

  I used Claude Code (Claude Sonnet 4.6) as my primary AI assistant throughout this project. I used it inside VSCode to read through the code, identify bugs, and apply fixes directly to the files.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  Claude correctly identified that on even-numbered attempts, the code was converting the secret number to a string before comparing it to the player's integer guess. This caused Python to do string comparison instead of numeric comparison, which made the hints go backwards. I verified this by reading lines 158–163 of app.py and tracing through the logic manually — string comparison like `"1" > "99"` returns False in Python, which explains exactly the backwards hint I observed.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

  At first I assumed the secret number itself was being re-randomized on every rerun, which would also explain why hints seemed inconsistent. Claude helped me check the session_state initialization block (lines 92–93 of app.py) and confirmed the secret was actually protected by the `if "secret" not in st.session_state` guard, so it was not re-randomizing. The real cause was the string/int comparison bug — a good reminder not to assume the most obvious explanation is correct.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

  I read through the fixed code carefully to trace what would happen step by step for a given guess. For the string/int bug, I confirmed `secret` is always an integer so the fallback branch is never triggered. For the range bug, I confirmed out-of-range guesses show an error and don't consume a turn. For the swapped messages bug, I verified by playing the game — guessing 9 with secret 24 was still showing "Go LOWER!" even after the first fix, which led me to spot that the outcome labels and hint messages were paired incorrectly in `check_guess`.

- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.

  I ran `pytest tests/test_game_logic.py -v` after implementing `check_guess` in `logic_utils.py`. 5 of 6 tests passed. The one failing test — `test_string_secret_gives_wrong_hint` — is intentional: it proves that passing a string secret to `check_guess` still breaks the comparison (`"10" < "9"` lexicographically), which is exactly why `app.py` was fixed to always pass an integer. That failing test documents the root cause of the original bug.

- Did AI help you design or understand any tests? How?

  Yes — Claude explained that the `check_guess` function has a fallback branch (lines 42–47 of app.py) that handles the case where `guess` and `secret` are different types by converting both to strings. Understanding that fallback was key to seeing why the bug existed: the app was deliberately (but incorrectly) triggering that branch by converting the secret to a string on even attempts.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

  Streamlit reruns the entire Python script from top to bottom every time the user interacts with the app — clicking a button, typing input, anything. If you call `random.randint()` at the top level without protecting it, a new random number gets generated on every single rerun. That's why the secret appeared to change: each interaction triggered a full re-run, picking a new secret. In this app, the secret was protected by `if "secret" not in st.session_state`, but the string/int comparison bug made hints appear to change, which looked like the secret was moving.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  Imagine your script is like a recipe that gets cooked from scratch every time you click anything. Normally that means all your variables reset to zero each time. Session state is like a sticky notepad that survives between those reruns — anything you store there stays put. So if you want the secret number to stay the same across guesses, you store it in session state the first time and then just read it from there on every rerun instead of generating a new one.

- What change did you make that finally gave the game a stable secret number?

  The `if "secret" not in st.session_state` guard (line 92 of app.py) was already correct — it only generates the secret once. The key fix was removing the code that converted `st.session_state.secret` to a string on even attempts (the `attempts % 2 == 0` branch). Once the secret is always passed as an integer to `check_guess`, the hints are stable and correct every time.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?

  Reading the code carefully before trusting the behavior. The bugs here were subtle — the hint logic looked almost right at first glance, but tracing through what actually happens with types (int vs string) revealed the real issue. I want to keep the habit of asking "what type is this variable right now?" when debugging unexpected behavior.

- What is one thing you would do differently next time you work with AI on a coding task?

  I would ask AI to explain *why* a bug exists before asking it to fix it. In this project, understanding the root cause (string comparison semantics in Python) made the fix obvious and also helped me spot the second bug (missing range validation) that I might have missed if I just accepted a patch blindly.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

  AI-generated code can look polished and complete while hiding subtle logic errors that only show up at runtime under specific conditions. Treating AI-generated code with the same skepticism I'd apply to any unfamiliar codebase — reading it, testing it, and questioning its assumptions — is not optional.
