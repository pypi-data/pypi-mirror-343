from agi_med_protos import commons_pb2 as _commons_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChatManagerRequest(_message.Message):
    __slots__ = ("Text", "OuterContext", "RequestId", "ResourceId")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    OUTERCONTEXT_FIELD_NUMBER: _ClassVar[int]
    REQUESTID_FIELD_NUMBER: _ClassVar[int]
    RESOURCEID_FIELD_NUMBER: _ClassVar[int]
    Text: str
    OuterContext: _commons_pb2.OuterContextItem
    RequestId: str
    ResourceId: str
    def __init__(self, Text: _Optional[str] = ..., OuterContext: _Optional[_Union[_commons_pb2.OuterContextItem, _Mapping]] = ..., RequestId: _Optional[str] = ..., ResourceId: _Optional[str] = ...) -> None: ...

class ChatManagerResponse(_message.Message):
    __slots__ = ("Text", "State", "Action", "ResourceId")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    RESOURCEID_FIELD_NUMBER: _ClassVar[int]
    Text: str
    State: str
    Action: str
    ResourceId: str
    def __init__(self, Text: _Optional[str] = ..., State: _Optional[str] = ..., Action: _Optional[str] = ..., ResourceId: _Optional[str] = ...) -> None: ...

class DomainInfo(_message.Message):
    __slots__ = ("DomainId", "Name")
    DOMAINID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DomainId: str
    Name: str
    def __init__(self, DomainId: _Optional[str] = ..., Name: _Optional[str] = ...) -> None: ...

class DomainsRequest(_message.Message):
    __slots__ = ("RequestId",)
    REQUESTID_FIELD_NUMBER: _ClassVar[int]
    RequestId: str
    def __init__(self, RequestId: _Optional[str] = ...) -> None: ...

class DomainsResponse(_message.Message):
    __slots__ = ("Domains",)
    DOMAINS_FIELD_NUMBER: _ClassVar[int]
    Domains: _containers.RepeatedCompositeFieldContainer[DomainInfo]
    def __init__(self, Domains: _Optional[_Iterable[_Union[DomainInfo, _Mapping]]] = ...) -> None: ...

class TrackInfo(_message.Message):
    __slots__ = ("TrackId", "Name", "DomainId")
    TRACKID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DOMAINID_FIELD_NUMBER: _ClassVar[int]
    TrackId: str
    Name: str
    DomainId: str
    def __init__(self, TrackId: _Optional[str] = ..., Name: _Optional[str] = ..., DomainId: _Optional[str] = ...) -> None: ...

class TracksRequest(_message.Message):
    __slots__ = ("RequestId",)
    REQUESTID_FIELD_NUMBER: _ClassVar[int]
    RequestId: str
    def __init__(self, RequestId: _Optional[str] = ...) -> None: ...

class TracksResponse(_message.Message):
    __slots__ = ("Tracks",)
    TRACKS_FIELD_NUMBER: _ClassVar[int]
    Tracks: _containers.RepeatedCompositeFieldContainer[TrackInfo]
    def __init__(self, Tracks: _Optional[_Iterable[_Union[TrackInfo, _Mapping]]] = ...) -> None: ...
