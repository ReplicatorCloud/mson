from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from fractions import Fraction

from mson import loads


def test_string():
    assert loads(b'"bonjour"') == "bonjour"
    assert loads(b'"\\u00e9l\\u00e9phant"') == "éléphant"


def test_binary():
    assert loads(b'b"abc"') == b"abc"
    assert loads(b'b"\\0\\r\\n\\"\x42"') == b'\0\r\n"\x42'


def test_datetime():
    assert (
        loads(b"1989-09-18 06:12:03.123456+0200").isoformat()
        == datetime(
            1989, 9, 18, 6, 12, 3, 123456, tzinfo=timezone(timedelta(hours=2))
        ).isoformat()
    )
    assert (
        loads(b"1989-09-18T061203.123456+02:00").isoformat()
        == datetime(
            1989, 9, 18, 6, 12, 3, 123456, tzinfo=timezone(timedelta(hours=2))
        ).isoformat()
    )


def test_date():
    assert loads(b"1989-09-18") == date(1989, 9, 18)


def test_float():
    assert loads(b"1e+100") == 1e100
    assert loads(b"42.42") == 42.42
    assert loads(b"-1.0") == -1.0


def test_int():
    assert loads(b"i1234567890123456789012") == 1234567890123456789012
    assert loads(b"i-12345678901234567890") == -12345678901234567890


def test_rational():
    assert loads(b"r1/1") == Fraction(1)
    assert loads(b"r42/1") == Fraction(42)
    assert loads(b"r1/3") == Fraction("1/3")
    assert loads(b"r-1/3") == Fraction("-1/3")


def test_decimal():
    assert loads(b"d123456789123.123456789123") == Decimal("123456789123.123456789123")
    assert loads(b"d-1") == Decimal("-1")


def test_special_values():
    assert loads(b"null") is None
    assert loads(b"true") is True
    assert loads(b"false") is False


def test_decode_list():
    assert loads(b"[i1,i2,i3]") == [1, 2, 3]


def test_decode_dict():
    assert loads(b"{i42:true}") == {42: True}
    assert loads(b"{[i1]:true,[i2]:false}") == {(1,): True, (2,): False}
