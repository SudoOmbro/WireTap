import json
from typing import Dict, Tuple


UPDATE_TYPE_CONTAINERS_MAP: Dict[str, Tuple[str, str]] = {
    "message": ("text", "from"),
    "channel_post": ("text", "sender_chat")
}


class Message:

    def __init__(self, message_dict: dict):
        # handle callbacks
        if "callback_query" in message_dict:
            message_dict = message_dict["callback_query"]
        elif "inline_query" in message_dict:
            message_dict = message_dict["inline_query"]
        # declare defaults
        container = "message"
        data_container = "text"
        sender_id_container = "from"
        # map to correct data containers
        for _container in UPDATE_TYPE_CONTAINERS_MAP:
            if _container in message_dict:
                container = _container
                data_container, sender_id_container = UPDATE_TYPE_CONTAINERS_MAP[_container]
        # fill all data fields
        self.message_id: int = message_dict[container]["message_id"]
        self.chat_id: int = message_dict[container]["chat"]["id"]
        self.chat_type: str = message_dict[container]["chat"]["type"]
        self.timestamp: int = message_dict[container]["date"]
        self.text: str = message_dict[container][data_container]
        self.sender_id: int = message_dict[container][sender_id_container]["id"]
        self.lower_text: str = self.text.lower()

    def __str__(self):
        return json.dumps(self.__dict__)
