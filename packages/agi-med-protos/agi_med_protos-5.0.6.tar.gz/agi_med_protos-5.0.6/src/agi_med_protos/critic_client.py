from .commons_pb2 import (
    InnerContextItem,
    ChatItem,
    ReplicaItem,
    OuterContextItem,
)
from .Critic_pb2_grpc import CriticStub
from .Critic_pb2 import (
    CriticRequest,
    CriticResponse,
)
from .abstract_client import AbstractClient
from .converters import convert_outer_context


class CriticClient(AbstractClient):
    def __init__(self, address) -> None:
        super().__init__(address)
        self._stub = CriticStub(self._channel)

    def __call__(self, text: str, dict_chat: dict, request_id: str = "") -> str:
        dict_outer_context = dict_chat["OuterContext"]
        outer_context: OuterContextItem = convert_outer_context(dict_outer_context)

        dict_inner_context = dict_chat["InnerContext"]
        dict_replicas = dict_inner_context["Replicas"]

        replicas = [
            ReplicaItem(
                Body=dict_replica["Body"],
                Role=dict_replica["Role"],
                DateTime=dict_replica["DateTime"],
            )
            for dict_replica in dict_replicas
        ]

        inner_context = InnerContextItem(Replicas=replicas)

        chat = ChatItem(OuterContext=outer_context, InnerContext=inner_context)

        request = CriticRequest(Text=text, Chat=chat, RequestId=request_id)

        response: CriticResponse = self._stub.GetCriticResponse(request)
        return response.Score
