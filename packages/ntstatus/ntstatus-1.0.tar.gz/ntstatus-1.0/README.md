# py-ntstatus

`py-ntstatus` is a library that defines a Python enum to represent [WinAPI NTSTATUS values](https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/using-ntstatus-values).

## ntstatus.NtStatus

`NtStatus` is enumeration representing WinAPI NTSTATUS values.

`NtStatus` values can be equality-compared to integers; the comparision will return True for both the signed and unsigned interpretation of the underlying 32 bits.

Properties:
- `signed_value`: The numeric value of the `NtStatus`, interpreted as a 32-bit signed integer.
- `unsigned_value`: The numeric value of the `NtStatus`, interpreted as a 32-bit unsigned integer.
- `exit_code`: The numeric value of the `NtStatus`, interpreted in a way that it can be passed to `sys.exit()` without information loss. (Alias to signed_value.)

Static methods:
- `make(code)`: Factory method for creating an `NtStatus` from an integer. Raises ValueError if argument is not a known `NtStatus` value.
- `decode(code)`: Factory method for creating an `NtStatus` from an integer. Returns None if argument is not a known `NtStatus` value.
- `decode_name(code, default='')`: Returns the name of the `NtStatus` value associated with the first argument if there is such a value. Otherwise, returns the second argument.

## Usage examples

Import the enum:

```
>>> from ntstatus import NtStatus
```

The 32-bit `NTSTATUS` value can be interpreted both as signed and unsigned integer:

```
>>> NtStatus.STATUS_DLL_NOT_FOUND
<NtStatus.STATUS_DLL_NOT_FOUND: 0xC0000135>

>>> NtStatus.STATUS_DLL_NOT_FOUND.unsigned_value
3221225781

>>> NtStatus.STATUS_DLL_NOT_FOUND.signed_value
-1073741515
```

`NtStatus` can be compared to both the signed and unsigned interpretation of the underlying 32 bits:

```
>>> NtStatus.STATUS_DLL_NOT_FOUND == 0xC0000135
True

>>> NtStatus.STATUS_DLL_NOT_FOUND == 3221225781
True

>>> NtStatus.STATUS_DLL_NOT_FOUND == -1073741515
True
```

`NtStatus` can be created from both the signed and unsigned interpretation of the underlying 32 bits:

```
>>> NtStatus.decode(0xC0000135)
<NtStatus.STATUS_DLL_NOT_FOUND: 0xC0000135>

>>> NtStatus.decode(3221225781)
<NtStatus.STATUS_DLL_NOT_FOUND: 0xC0000135>

>>> NtStatus.decode(-1073741515)
<NtStatus.STATUS_DLL_NOT_FOUND: 0xC0000135>

>>> NtStatus.make(0xC0000135)
<NtStatus.STATUS_DLL_NOT_FOUND: 0xC0000135>

>>> NtStatus.make(3221225781)
<NtStatus.STATUS_DLL_NOT_FOUND: 0xC0000135>

>>> NtStatus.make(-1073741515)
<NtStatus.STATUS_DLL_NOT_FOUND: 0xC0000135>
```

`NtStatus.make()` raises `ValueError` if the value is not representable in 32 bits, or if it is not a known `NtStatus`:

```
>>> NtStatus.make(0xCC0300000)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "d:\projects\ntstatus\ntstatus\__init__.py", line 172, in make
    return NtStatus(ThirtyTwoBits(code))
  File "d:\projects\ntstatus\ntstatus\__init__.py", line 26, in __init__
    raise ValueError(f'Value must be in [{min_signed}, {max_unsigned}] to be representable in 32 bits: {value}')
ValueError: Value must be in [-2147483648, 4294967295] to be representable in 32 bits: 54763978752

>>> NtStatus.make(0xC0300000)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "d:\projects\ntstatus\ntstatus\__init__.py", line 172, in make
    return NtStatus(ThirtyTwoBits(code))
  File "C:\Python39\lib\enum.py", line 360, in __call__
    return cls.__new__(cls, value)
  File "C:\Python39\lib\enum.py", line 677, in __new__
    raise ve_exc
ValueError: ThirtyTwoBits(underlying_unsigned_value=3224371200) is not a valid NtStatus
```

`NtStatus.decode()` returns `None` in both cases:

```
>>> NtStatus.decode(0xC0300000) == None
True

>>> NtStatus.decode(0xCC0300000) == None
True
```

Name for numeric values can be safely queried:

```
>>> NtStatus.decode_name(-1073741515)
'STATUS_DLL_NOT_FOUND'

>>> NtStatus.decode_name(0xC0000135)
'STATUS_DLL_NOT_FOUND'

>>> NtStatus.decode_name(0xC0300000)
''

>>> NtStatus.decode_name(-1073741515, 'No NTSTATUS definition found')
'STATUS_DLL_NOT_FOUND'

>>> NtStatus.decode_name(0xC0000135, 'No NTSTATUS definition found')
'STATUS_DLL_NOT_FOUND'

>>> NtStatus.decode_name(0xC0300000, 'No NTSTATUS definition found')
'No NTSTATUS definition found'
```

`exit_code` can be used in `sys.exit()` without information loss:
```
>>> import sys
>>> sys.exit(NtStatus.STATUS_DLL_NOT_FOUND.exit_code)

(.venv) d:\projects\ntstatus>echo %ERRORLEVEL%
-1073741515
```

Using the unsigned interpretation would lead to information loss ([see explanation](https://stackoverflow.com/a/63387879)):

```
>>> import sys
>>> sys.exit(NtStatus.STATUS_DLL_NOT_FOUND.unsigned_value)

(.venv) d:\projects\ntstatus>echo %ERRORLEVEL%
-1
```

## List of values

The complete list of `NTSTATUS` values can be found [here](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-erref/596a1078-e883-4972-9bbc-49e60bebca55
).

`NtStatus` encodes most of them, with the exception of:

- `STATUS_WAIT_n`, where `n` is 0, 1, 2, 3, and 63
- `STATUS_ABANDONED_WAIT_n`, where `n` is 0 and 63
- `STATUS_FLT_DISALLOW_FSFILTER_IO`

## Licensing

This library is licensed under the MIT license.

