from typing import Any, Dict, List

from .commons_pb2 import OuterContextItem
from .ChatManager_pb2_grpc import ChatManagerStub
from .ChatManager_pb2 import (
    ChatManagerRequest,
    ChatManagerResponse,
    DomainsRequest,
    DomainsResponse,
    DomainInfo,
    TracksRequest,
    TracksResponse,
    TrackInfo,
)
from .abstract_client import AbstractClient
from .converters import convert_outer_context


DictStr = Dict[str, str]


class ChatManagerClient(AbstractClient):
    def __init__(self, address) -> None:
        super().__init__(address)
        self._stub = ChatManagerStub(self._channel)

    def __call__(self, text: str, dict_outer_context: dict, request_id: str, resource_id: str) -> DictStr:
        outer_context: OuterContextItem = convert_outer_context(dict_outer_context)

        request = ChatManagerRequest(
            Text=text,
            OuterContext=outer_context,
            RequestId=request_id,
            ResourceId=resource_id,
        )
        response: ChatManagerResponse = self._stub.GetChatResponse(request)
        replica: dict[str, Any] = {
            "Text": response.Text,
            "ResourceId": response.ResourceId,
            "State": response.State,
            "Action": response.Action,
        }
        return replica

    def get_domains(self, request_id: str = "") -> List[DictStr]:
        request = DomainsRequest(RequestId=request_id)
        response: DomainsResponse = self._stub.GetDomains(request)
        domains: List[DomainInfo] = response.Domains
        res = [{"DomainId": di.DomainId, "Name": di.Name} for di in domains]
        return res

    def get_tracks(self, request_id: str = "") -> List[DictStr]:
        request = TracksRequest(RequestId=request_id)
        response: TracksResponse = self._stub.GetTracks(request)
        tracks: List[TrackInfo] = response.Tracks
        res = [{"TrackId": ti.TrackId, "Name": ti.Name, "DomainId": ti.DomainId} for ti in tracks]
        return res
