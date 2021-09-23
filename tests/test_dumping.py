from datetime import datetime
from decimal import Decimal
from fractions import Fraction

from mson import dumps


def test_string():
    assert dumps("bonjour") == b'"bonjour"'
    assert dumps("éléphant") == b'"\\u00e9l\\u00e9phant"'


def test_binary():
    assert dumps(b"abc") == b'b"abc"'
    assert dumps(b'\0\r\n"\x42') == b'b"\\0\\r\\n\\"\x42"'


def test_datetime():
    now = datetime.now()
    assert dumps(now) == now.isoformat().encode("ascii")


def test_date():
    now = datetime.now().date()
    assert dumps(now) == now.isoformat().encode("ascii")


def test_float():
    assert dumps(1e100) == b"1e+100"
    assert dumps(42.42) == b"42.42"
    assert dumps(-1.0) == b"-1.0"


def test_int():
    assert dumps(1234567890123456789012) == b"i1234567890123456789012"
    assert dumps(-12345678901234567890) == b"i-12345678901234567890"


def test_rational():
    assert dumps(Fraction(1)) == b"r1/1"
    assert dumps(Fraction(42)) == b"r42/1"
    assert dumps(Fraction("1/3")) == b"r1/3"
    assert dumps(Fraction("-1/3")) == b"r-1/3"


def test_decimal():
    assert dumps(Decimal("123456789123.123456789123")) == b"d123456789123.123456789123"
    assert dumps(Decimal("-1")) == b"d-1"


def test_special_values():
    assert dumps(None) == b"null"
    assert dumps(True) == b"true"
    assert dumps(False) == b"false"


def test_encode_list():
    assert dumps([1, 2, 3]) == b"[i1,i2,i3]"
    assert dumps((1, 2, 3)) == b"[i1,i2,i3]"


def test_encode_dict():
    assert dumps({42: True}) == b"{i42:true}"
    assert dumps({(1,): True, (2,): False}) == b"{[i1]:true,[i2]:false}"
