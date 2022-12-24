import json
from typing import Dict, Tuple, List, Union

UPDATE_TYPE_CONTAINERS_MAP: Dict[str, Tuple[str, str]] = {
    "message": ("text", "from"),
    "channel_post": ("text", "sender_chat")
}


class MessageEntity:

    def __init__(self, entity_dictionary: dict, encoded_text: bytes):
        # entity offsets need to be converted from utf-16 to utf-8
        self.text: str = encoded_text[
                         entity_dictionary["offset"] * 2:
                         (entity_dictionary["offset"] + entity_dictionary["length"]) * 2]\
            .decode('utf-16-le')
        self.type: str = entity_dictionary["type"]
        self.url: Union[str, None] = entity_dictionary.get("url", None)


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
        self.entities: Union[List[MessageEntity], None] = []
        # build entities list not up to api spec for ease of use reason
        encoded_text: bytes = self.text.encode('utf-16-le')
        for entity_dict in message_dict[container].get("entities", []):
            self.entities.append(MessageEntity(entity_dict, encoded_text))

    def __str__(self):
        return json.dumps(self.__dict__)
