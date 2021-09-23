# MSON

MSON &mdash; "More Serialized Object Notations" &mdash; is a JSON-inspired
format that try to overcome typical JSON limitations while staying simpler than
more theoretically-correct-but-boring-and-complicated ASN.1, XML and friends.

What JSON lacks is:

-   Support for dates (why O why)
-   Support for binary data
-   Support for better number formats
-   Guaranteed order of dictionary keys
-   Support for more than strings as dictionary keys

I'm sure there is other serialization formats that exist around there but I've
got my own fetishes and it's fun to make this.

## Usage

That'll feel quite familiar.

```python
import mson

print(mson.dumps([1, 2, 3]))
print(mson.loads(b'[i1, i2, i3]'))
```

You'll note that mson literals are binary strings. Indeed, since binary data is
supported, mson strings must be binary.

## Supported literals

You'll find it very similar to JSON, weirdly

### String

A string is any valid unicode string. As opposed to JSON, the `\u` notation is
mandatory for any non-ASCII or non-printable character (except the usual `\r`,
`\n` and friends that JSON supports).

```
"this is a string"
```

**Format**

```regexp
"(([^\x00-\x1f\x7f-\xff"\\]|\\[bfnrt]|\\u[0-9a-fA-F]{4})*)"
```

### Binary data

You can encode raw binary data using this literal

```
b"foo"
```

You can keep most of the data intact but you must escape the following
characters:

- `"` becomes `\"`
- `\n` must be encoded as such
- `\r` as well

This allows to keep new lines as a separator between MSON strings.

**Format**

```regexp
b"([^"\\\x00\n\r]|\\[0nr"])*"
```

### Numbers

Numbers are fine most of the time, until you start losing precision stupidly.
Depending on what you want to express, there is different formats of numbers
available in mson.

#### Default floats

To avoid confusion, this is the same as the JSON float.

```
42.42
```

Most of the time you'll be fine but there is a lot of specific things you may
want to do or express that won't be possible using this format. Most notably,
you can't have numbers too big without losing precision, you can't be sure that
a digit won't get rounded up, etc. Monetary APIs often resort to using strings
instead of those floats. That's why this format exists for convenience but is
not really recommended.

**Format**

```regexp
[+-]?([0-9]+([.][0-9]*)?([eE][+-]?[0-9]+)?|[.][0-9]+([eE][+-]?[0-9]+)?)
```

#### Integer

Integers have an arbitrary precision

```
i1234567
```

**Format**

```regexp
i[+-]?[0-9]+
```

#### Decimal

Well, like the [decimal](https://docs.python.org/3/library/decimal.html) Python
module.

```
d4224.235244
```

**Format**

```regexp
d[+-]?([0-9]+)?(\.[0-9]+)?
```

#### Rational

Numbers that can be expressed as a fraction of two integers (like the integers
from above, that have arbitrary precision)

```
r4528/325356
```

**Format**

```regexp
r[+-]?[0-9]+(/([0-9]+))?
```

### Time formats

#### Dates

ISO dates are accepted

```
1989-09-18
```

**Format**

```regexp
[+-]?[0-9]{4,}-[0-9]{2}-[0-9]{2}
```

#### Date/time

Datetimes in ISO format are accepted.

```
1989-09-18 06:13:00+0200
```

**Format**

```regexp
[+-]?[0-9]{4,}-[0-9]{2}-[0-9]{2}( \d{2}(:\d{2}(:\d{2}(\.\d+)?)?)?|T\d{2}(\d{2}(\d{2}(\.\d+)?)?)?)(Z|[+-]\d{2}(:?\d{2})?)?
```

### Lists

Lists are like in JSON except you can put any MSON type in them.

### Dictionaries

Dictionaries are like JSON except you can put any MSON type which can be made
immutable (aka everything exception dictionary) as a key and any MSON type as
a value.
