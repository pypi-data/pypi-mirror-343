from .abstract_client import AbstractClient
from .commons_pb2 import ChatItem
from .Text_pb2 import TextRequest, TextResponse
from .Text_pb2_grpc import TextStub
from .converters import convert_chat

class TextClient(AbstractClient):
    def __init__(self, address) -> None:
        super().__init__(address)
        self._stub = TextStub(self._channel)

    def __call__(self, text: str, dict_chat: dict, request_id: str = "") -> str:
        chat: ChatItem = convert_chat(dict_chat)
        request = TextRequest(Text=text, Chat=chat, RequestId=request_id)
        response: TextResponse = self._stub.GetTextResponse(request)
        return response.Text
