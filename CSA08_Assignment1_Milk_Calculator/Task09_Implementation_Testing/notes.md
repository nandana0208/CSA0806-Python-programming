# Task 9 – Implement and Test

The tests cover the standard rate, fat/SNF above and below standard, exact fat boundaries, negative quantity, out-of-range fat and invalid text. The five-entry hand-check total is Rs 1,397.50. Run `python run_tests.py`; every check is enforced with `assert` so a regression causes a non-zero failure.

Typing tests manually is useful for usability checks but repetitive and easy to perform inconsistently. A test function runs the same cases after every change, with O(n) work for n test cases; manual reruns also take O(n) human actions and are slower. Automated assertions are repeatable and can be integrated into GitHub workflows.
