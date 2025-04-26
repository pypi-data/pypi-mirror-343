from .abstract_client import AbstractClient
from .commons_pb2 import (
    InnerContextItem,
    OuterContextItem,
    ChatItem,
    ReplicaItem,
)
from .Text_pb2 import (
    TextRequest,
    TextResponse,
)
from .Text_pb2_grpc import (
    TextStub,
)
from .converters import convert_outer_context

class TextClient(AbstractClient):
    def __init__(self, address) -> None:
        super().__init__(address)
        self._stub = TextStub(self._channel)

    def __call__(self, text: str, dict_chat: dict, request_id: str = "") -> str:
        dict_outer_context = dict_chat["OuterContext"]
        outer_context: OuterContextItem = convert_outer_context(dict_outer_context)

        dict_inner_context = dict_chat["InnerContext"]
        dict_replicas = dict_inner_context["Replicas"]

        replicas = [
            ReplicaItem(Body=dict_replica["Body"], Role=dict_replica["Role"], DateTime=dict_replica["DateTime"])
            for dict_replica in dict_replicas
        ]

        inner_context = InnerContextItem(Replicas=replicas)

        chat = ChatItem(OuterContext=outer_context, InnerContext=inner_context)

        request = TextRequest(Text=text, Chat=chat, RequestId=request_id)

        response: TextResponse = self._stub.GetTextResponse(request)
        return response.Text
