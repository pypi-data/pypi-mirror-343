from .ContentInterpreter_pb2_grpc import ContentInterpreterStub
from .ContentInterpreter_pb2 import (
    ContentInterpreterRequest,
    ContentInterpreterResponse,
)
from .abstract_client import AbstractClient


class ContentInterpreterClient(AbstractClient):
    def __init__(self, address):
        super().__init__(address)
        self._stub = ContentInterpreterStub(self._channel)

    def interpret(
        self,
        kind: str,
        query: str = "",
        resource: bytes = None,
        resource_id: str = None,
        request_id: str = "",
    ) -> ContentInterpreterResponse:
        if resource is None and resource_id is None:
            raise ValueError("Argument `resource` or `resource_id` should be passed!")
        request = ContentInterpreterRequest(
            RequestId=request_id,
            Kind=kind,
            Query=query,
            Resource=resource,
            ResourceId=resource_id,
        )
        response: ContentInterpreterResponse = self._stub.Get(request)
        return response
