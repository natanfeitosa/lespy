import base64

from lespy.converters.converters import IntConverter
from lespy.converters import get_converter, register_converter, BaseConverter


def test_get_converter():
    assert get_converter('int') == IntConverter

def test_register_converter():
    @register_converter
    class Base64Converter(BaseConverter):
        regex = r"[a-zA-Z0-9+/]*={0,2}"
        convertor = lambda c: base64.b64decode(c).decode('ascii')

    assert get_converter('base64') == Base64Converter

    b = Base64Converter('aGVsbG8=')

    assert isinstance(b, Base64Converter)
    assert b.to_python == 'hello'

def test_named_register_converter():
    @register_converter('base64')
    class Base64Converter(BaseConverter):
        regex = r"[a-zA-Z0-9+/]*={0,2}"
        convertor = lambda c: base64.b64decode(c).decode('ascii')

    assert get_converter('base64') == Base64Converter

    b = Base64Converter('aGVsbG8=')

    assert isinstance(b, Base64Converter)
    assert b.to_python == 'hello'

def test_call_register_converter():
    class Base64Converter(BaseConverter):
        regex = r"[a-zA-Z0-9+/]*={0,2}"
        convertor = lambda c: base64.b64decode(c).decode('ascii')

    register_converter('base64', Base64Converter)

    assert get_converter('base64') == Base64Converter

    b = Base64Converter('aGVsbG8=')

    assert isinstance(b, Base64Converter)
    assert b.to_python == 'hello'
