import json


class Message:

    def __init__(self, message_dict: dict):
        if "message" in message_dict:
            container: str = "message"
            sender_id_container: str = "from"
        else:
            container: str = "channel_post"
            sender_id_container: str = "sender_chat"
        self.message_id: int = message_dict[container]["message_id"]
        self.chat_id: int = message_dict[container]["chat"]["id"]
        self.chat_type: str = message_dict[container]["chat"]["type"]
        self.timestamp: int = message_dict[container]["date"]
        self.text: str = message_dict[container]["text"]
        self.sender_id: int = message_dict[container][sender_id_container]["id"]
        self.lower_text: str = self.text.lower()

    def __str__(self):
        return json.dumps(self.__dict__)
