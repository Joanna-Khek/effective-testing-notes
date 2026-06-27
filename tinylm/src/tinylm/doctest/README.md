# Doctest

Turns documentation examples into executable checks. Can be used together with pytest.

- Doctests: handles simpler examples
- Pytest: handles complex scenarios

## Using Docstrings
We can specify doctests in the docstrings and run it with ```uv run python -m doctest -v src/tinylm/__init__.py```

```python
def get_table(txt: str, size: int = 1) -> dict[str, dict[str, int]]:
 """
 Build a transition table from a training string.
 >>> get_table("xyxz")
 {'x': {'y': 1, 'z': 1}, 'y': {'x': 1}}
 """
```

## With pytest
We can integrate doctest in pytest.

```bash
uv run pytest --doctest-modules -q src/tinylm/__init__.py
```

Add this in the pytest configuration file
```yaml
[tool.pytest]
addopts = ["--doctest-modules"]
doctest_optionflags = "NORMALIZE_WHITESPACE ELLIPSIS IGNORE_EXCEPTION_DETAIL"
```