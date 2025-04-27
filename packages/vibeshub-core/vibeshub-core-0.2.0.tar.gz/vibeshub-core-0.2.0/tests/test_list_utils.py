# tests/test_list_utils.py

import pytest
from vibeshub import chunk_list, flatten_list

def test_chunk_list_basic():
    data = [1, 2, 3, 4, 5]
    result = list(chunk_list(data, 2))
    assert result == [[1, 2], [3, 4], [5]]

def test_chunk_list_exact_chunks():
    data = [1, 2, 3, 4]
    result = list(chunk_list(data, 2))
    assert result == [[1, 2], [3, 4]]

def test_chunk_list_invalid_size():
    data = [1, 2, 3]
    try:
        list(chunk_list(data, 0))
    except ValueError:
        assert True
    else:
        assert False


def test_flatten_list_basic():
    data = [1, [2, 3], 4]
    result = flatten_list(data)
    assert result == [1, 2, 3, 4]

def test_flatten_list_nested():
    data = [1, [2, [3, 4]], 5]
    result = flatten_list(data)
    assert result == [1, 2, 3, 4, 5]
    