import uuid
from lespy.converters.base import BaseConverter

class StringConverter(BaseConverter):
    regex = r"[^/]+"

class IntConverter(BaseConverter):
    regex: str = r"[0-9]+"
    convertor: int = int

class SlugConverter(BaseConverter):
    regex = r"[-a-zA-Z0-9_]+"

class UUIDConverter(BaseConverter):
    regex = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    convertor: uuid.UUID = uuid.UUID

class PathConverter(BaseConverter):
    regex = r".+"
