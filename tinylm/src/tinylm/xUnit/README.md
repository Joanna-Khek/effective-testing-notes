# xUnit

Uses a Four-Phase Test approach, which is a simple way to sturcture the logic inside a test so that the reader can immediately see what is going on.

- Fixture setup establish test fixture (set up the world)
- Exercise runs the system under test (exercise the system)
- Result verification checks the outcome (verify the results)
- Fixture teardown (cleans up resources)

## Fixtures
Fixture is everything that makes the code runnable in the context of the test. It is the world that you build so you can test a thing.

It can be the following
- file
- environment variable
- database row
- fake service

If it is difficult to write a fixture for a test, that might be a sign that the system under test is hard to test. If we are writing large fixtures, then ask ourselves if the system under the test can be redesigned to make the tests smaller and clearer

The easiest tests to understand tend to have fixtures that a reminimal and explicit.

Many testing frameworks encourage you to isolate IO boundaries (where code interacts with outside world like databases, files, networks, environment variables etc). 
- More IO boundaries = larger your fixtures.
- More pure computation = smaller fixtures = readable

## Teardown
Simplest case: setup and teardown live directly in the test. 

If we don't have teardown, it could lead to leaked state where the failure appeasr later, in a completely different test.

Examples:
- A test creates a directory and forgets to delete it
- A test opens a file and never closes it

Here are some examples of how we can perform teardown.

1. Temporary directory.

```python
from pathlib import Path
import tempfile
from tinylm.filecalc import sum_file
def test_sum_file_happy_path():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "nums.txt"
        path.write_text("1\n2\n3\n", encoding="utf-8") # setup
        result = sum_file(path) # exercise
        assert result == 6 # verify
        # teardown is handled by TemporaryDirectory
 ```

 2. Using pytest fixtures for the temporary directory

 ```python
 from pathlib import Path
import pytest
import tempfile
from tinylm.filecalc import sum_file

@pytest.fixture
def temp_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "nums.txt"
        path.write_text("1\n2\n3\n", encoding="utf-8")
        yield path # setup
    # teardown is handled by TemporaryDirectory

def test_sum_file_happy_path(temp_file):
    result = sum_file(temp_file) # exercise
    assert result == 6 # verify
```

3. Using try/finally. This is a naive approach because Python has a cleaner context manager syntax.

```python
from pathlib import Path
import tempfile
from tinylm.filecalc import sum_file
def test_sum_file_happy_path():
    tmpdir = tempfile.TemporaryDirectory()
    try:
        path = Path(tmpdir.name) / "nums.txt"
        path.write_text("1\n2\n3\n", encoding="utf-8") # setup
        result = sum_file(path) # exercise
        assert result == 6 # verify
    finally:
        tmpdir.cleanup() # teardown
```

4. Using `unittest` style, which comes with the `addCleanup` method.
```python
import tempfile
import unittest
from pathlib import Path
from tinylm.filecalc import sum_file

class TestSumFile(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup) # register cleanup
        self.path = Path(self._tmp.name) / "nums.txt"
        self.path.write_text("1\n2\n3\n", encoding="utf-8")

    def test_sum_file(self):
        result = sum_file(self.path)
        self.assertEqual(result, 6)
```


Note: if your test changes the global state (for example here we change the env var value), we must restore it. It is part of the clean up. 

```python
import os
from configcalc import multiply_by_mode
def test_pytest_style_restores_env_var() -> None:
    old_mode = os.environ.get("MODE") # setup
    try:
        os.environ["MODE"] = "triple" # setup (made modification to the global state)
        assert multiply_by_mode(3) == 9 # exercise + verify
    finally:
        # teardown
        if old_mode is None:
            os.environ.pop("MODE", None)
        else:
            os.environ["MODE"] = old_mode
```


We can use `monkeypatch` fixture from pytest to make this cleaner. The environment variable is only chaged for the duration of the test when called through monkeypatch.setenv. 

```python
import os
import pytest
from configcalc import multiply_by_mode
def test_monkeypatch_restores_env_var(monkeypatch) -> None:
    monkeypatch.setenv("MODE", "triple") # setup (only for the duration of this test)
    assert multiply_by_mode(4) == 12 # exercise + verify
```


## Exceptions
To test for exceptins, be specific. `ValueError` means input was wrong, `KeyError` means a key was missing. Instead of just asserting that `Exception` was raised, be specific

1. `unittest` method, we can use the `assertRaises` method
```python
import os
import unittest
from tinylm.filecalc import multiply_by_mode
class TestMultiplyByMode(unittest.TestCase):
    def test_unknown_mode_raises_valueerror(self):
        os.environ["MULTIPLY_MODE"] = "quadruple" # setup
        with self.assertRaises(ValueError) as cm: # verify
            multiply_by_mode(10) # exercise
        self.assertIn("Unknown MULTIPLY_MODE", str(cm.exception)) # verify
```

2. `pytest` method
```python
import os
import pytest
from tinylm.filecalc import multiply_by_mode
def test_unknown_mode_raises_valueerror():
    os.environ["MULTIPLY_MODE"] = "quadruple" # setup
    with pytest.raises(ValueError) as exc_info: # verify
        multiply_by_mode(10) # exercise
    assert "Unknown MULTIPLY_MODE" in str(exc_info.value) # verify
```

