# unittest

## Assertions
- `assertEqual`: It checks `==` and produces a failure message that tries to help you see what diverged.
- `assertIn`
- `assertTrue`
- `assertAlmostEqual`
- `assertRaises`
- `assertRaisesRegex`


## setUp and tearDown
- `setUp` runs before each test method
- `tearDown` runs after each test method

The moment your tests touch global state, files, environment variables, network sockets, randomness, or time, we need to ensure teardown is in place

## Testing multiple cases
1. Unit test

```python
def test_get_table_subtests(self) -> None:
    cases = [
        ("xyxz", {"x": {"y": 1, "z": 1}, "y": {"x": 1}}),
        ("abca", {"a": {"b": 1}, "b": {"c": 1}, "c": {"a": 1}}),
    ]
    for txt, expected in cases:
        with self.subTest(txt=txt):
            self.assertEqual(mc.get_table(txt), expected)
 ```



2. Pytest

```python
def test_get_table_subtests(subtests) -> None:
    cases = [
        ("xyxz", {"x": {"y": 1, "z": 1}, "y": {"x": 1}}),
        ("abca", {"a": {"b": 1}, "b": {"c": 1}, "c": {"a": 1}}),
    ]
    for i, (txt, expected) in enumerate(cases):
        with subtests.test(msg=txt, i=i):
            assert mc.get_table(txt) == expected
```

## Skipping Tests
Sometimes we might want to run a test only in certain environment or when a test is temporarily disabled while you fix a bug.

```python
@unittest.skipIf(True, "example skip for the book")
class TestSkipping(unittest.TestCase):
    def test_skipped_example(self) -> None:
        self.fail("should be skipped")
```

## Expected Failures
Say if you come across a bug but can't fix it right away, you can write a test that exposes the bug, mark it with an expeceted failure and then fix the bug later. We expect the test to fail when bug is unfixed.

```python
class TestExpectedFailure(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = Markov("abc")
        
        
    @unittest.expectedFailure
    def test_expected_failure_example(self) -> None:
        # in the future, we might support length-2 predictions
        # # for now, this test is expected to fail
        res = self.model.predict("ab")
        self.assertEqual(res, "c")
```

## Running unittests tests
Run test for a specific file: `uv run python -m unittest tests.test_unittest_markov`

Show number of tests ran: `uv run python -m unittest discover -s tests`

Show test names:
`uv run python -m unittest discover -s tests -v`