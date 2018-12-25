from utils.helper import check_index_valid, exclude_json_fields


def test_check_index_valid():
    assert check_index_valid(0, 0) is False
    assert check_index_valid(-1, 10) is False
    assert check_index_valid(10, 10) is False
    assert check_index_valid(23, 10) is False
    assert check_index_valid(5, 10) is True
    assert check_index_valid(1, 2) is True


def test_exclude_json_fields():
    result = exclude_json_fields({"a": "a", "b": "b", "c": "c"}, ["b", "c"])
    assert result == {"b": "b", "c": "c"}

    result = exclude_json_fields({"a": "a", "b": "b", "c": "c"}, ["b", "c", "e"])
    assert result == {"b": "b", "c": "c"}

    result = exclude_json_fields({"a": "a", "b": "b", "c": "c"}, ["d", "f", "e"])
    assert result == {}

    result = exclude_json_fields({}, [])
    assert result == {}