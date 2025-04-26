from .commons_pb2 import (
    OuterContextItem,
)

def convert_outer_context(dict_outer_context: dict | None) -> OuterContextItem:
    if dict_outer_context is None:
        return None
    outer_context = OuterContextItem(
        Sex=dict_outer_context["Sex"],
        Age=dict_outer_context["Age"],
        UserId=dict_outer_context["UserId"],
        SessionId=dict_outer_context["SessionId"],
        ClientId=dict_outer_context["ClientId"],
        TrackId=dict_outer_context["TrackId"],
    )
    return outer_context
