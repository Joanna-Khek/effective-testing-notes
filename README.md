# Effective Testing Notes

This repository contains my notes on the [Effective Testing](https://store.metasnake.com/testing) book written by Matt Harrison.

Some quotes from the book that I personally like:
> *"In an era where AI can generate code on demand, tests are no longer just a safety net, they are steering wheel. Clear, well-chosen tests guide the AI toward the behaviour that you actually want."*

> *"If fixtures are painful to write, it might mean that the system under test is doing too much. We should treat fixture pain as a design signal so that we can make the code easier to test and easier to maintain."*

> *"Test structure is not only a testing concern but also a design concern. If a tiny behaviour requires a huge fixture, then you might be looking at a design that is tightly coupled to boundaries."*


## Test Names Convention
We can name the tests after the functions but can also make it more informative. Examples:

| Function | Information| Test name |
| :--- | :--------: | :---: |
| `sum_file` | Test if it ignores blank lines | `test_sum_file_ignores_blank_lines` |
| `sum_file` | Test if it raises error on non integer | `test_sum_file_raises_valueerror_on_non_int` |

This behaviour-focused names make it easier to keep one behaviour per test.

## Rules of Thumb
- Keep fixture setup small. Start with the smallest scenario that can demostrate the behaviour.
- Prefer one exercise action per test as a default
- Write verification that matches the contract. Assert on values for pure functions. Assert on exception types for error behaviour. Assert on observable effects for side-effecting code. Assert behaviour that you care about.
- Treat teardown as manual garbage collection. Cleanup should happen even when test fails.
- Tests beneit from straightforward reptition.

## Topics
Please refer to the various READMEs for the respective topic.

| Topic | Link |
| :--- | :---: |
| `doctest` | [Notes](src/tinylm/doctest/README.md) |
| `pytest` | [Notes](src/tinylm/pytest/README.md) |
| `unittest` | [Notes](src/tinylm/unittest/README.md) |
| `xUnit` | [Notes](src/tinylm/xUnit/README.md) |
| `TDD` | [Notes](src/tinylm/TDD/README.md) |
| `monkeypatch` and `mocking` | [Notes](src/tinylm//monkeypatch_mocking/README.md) |
| `coverage` | [Notes](src/tinylm/coverage/README.md)|


