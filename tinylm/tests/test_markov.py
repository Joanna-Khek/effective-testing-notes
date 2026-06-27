import pytest
import tinylm

def test_get_table() -> None:
    assert tinylm.get_table("xyxz") == {
        "x": {"y": 1, "z": 1},
        "y": {"x": 1}
    }


def test_predict_determinstic() -> None:
    model = tinylm.Markov("abc")
    assert model.predict("a") == "b"
    assert model.predict("b") == "c"

def test_predict_unknown_raises() -> None:
    model = tinylm.Markov("abc")
    with pytest.raises(KeyError):
        model.predict("z")