from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ContentInterpreterRequest(_message.Message):
    __slots__ = ("RequestId", "Kind", "Query", "Resource", "ResourceId")
    REQUESTID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    RESOURCEID_FIELD_NUMBER: _ClassVar[int]
    RequestId: str
    Kind: str
    Query: str
    Resource: str
    ResourceId: str
    def __init__(self, RequestId: _Optional[str] = ..., Kind: _Optional[str] = ..., Query: _Optional[str] = ..., Resource: _Optional[str] = ..., ResourceId: _Optional[str] = ...) -> None: ...

class ContentInterpreterResponse(_message.Message):
    __slots__ = ("Interpretation", "Resource", "ResourceId")
    INTERPRETATION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    RESOURCEID_FIELD_NUMBER: _ClassVar[int]
    Interpretation: str
    Resource: bytes
    ResourceId: str
    def __init__(self, Interpretation: _Optional[str] = ..., Resource: _Optional[bytes] = ..., ResourceId: _Optional[str] = ...) -> None: ...
