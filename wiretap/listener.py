import logging

from requests import get, Response

logging.basicConfig(
    format='%(asctime)s - {%(pathname)s} %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


class TelegramListener:
    """ basic polling-based listener for Telegram updates """

    def __init__(self, bot_token: str, poll_delay: int = 1):
        """
        :param bot_token: the token that identifies the bot
        :param poll_delay:
            the delay in seconds between update requests,
            by default it's 1 second (which also is the minimum possible delay)
        """
        self.token: str = bot_token
        self.poll_delay: int = poll_delay

    def _build_request_url(self, method: str) -> str:
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self) -> dict:
        """ returns updates received by the bot since last call of this method """
        response: Response = get(
            self._build_request_url("getUpdates")
        )
        try:
            response_dictionary = response.json()
        except Exception as e:
            log.error(f"can't parse response into json {e}")
            response_dictionary = None
        if response.ok:
            return response_dictionary if response_dictionary else response.text
        if response_dictionary:
            return {
                "error": response_dictionary.get("description"),
                "error code": response_dictionary.get("error_code")
            }
        return {"error": "Could not call getUpdates method"}
