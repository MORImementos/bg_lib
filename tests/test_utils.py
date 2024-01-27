from utils import type_as_string

def test_type_as_string():
    assert type_as_string(str) == 'str'
    assert type_as_string(int) == 'int'
    assert type_as_string(float) == 'float'
