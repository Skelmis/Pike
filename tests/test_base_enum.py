import pytest

from pike.docx.structs import EnumBase


class TestingEnum(EnumBase):
    ONE = 1
    TWO = 2
    THREE = 3

def test_get_next():
    te_1 = TestingEnum.ONE
    assert te_1.get_next() == TestingEnum.TWO

    te_2 = TestingEnum.TWO
    assert te_2.get_next() == TestingEnum.THREE

    te_3 = TestingEnum.THREE
    with pytest.raises(ValueError):
        te_3.get_next()

def test_get_previous():
    te_1 = TestingEnum.ONE
    with pytest.raises(ValueError):
        te_1.get_previous()

    te_2 = TestingEnum.TWO
    assert te_2.get_previous() == TestingEnum.ONE

    te_3 = TestingEnum.THREE
    assert te_3.get_previous() == TestingEnum.TWO