import pytest
import tinylm as mc
@pytest.fixture
def table() -> dict[str, dict[str, int]]:
    """A basic Markov table for 'abc'."""
    return mc.get_table("abc")