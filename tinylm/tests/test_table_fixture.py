def test_table_fixture(table) -> None:
    assert table == {"a": {"b": 1},
                     "b": {"c": 1}}