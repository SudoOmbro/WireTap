import logging
import threading

from requests import get, Response

from wiretap.analyzer import AbstractMessageAnalyzer
from wiretap.utils import Message

logging.basicConfig(
    format='%(asctime)s - {%(pathname)s} %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class TelegramListener(threading.Thread):
    """ basic polling-based listener for Telegram updates """

    def __init__(self, bot_token: str, analyzer: AbstractMessageAnalyzer, poll_delay: int = 1):
        """
        :param bot_token: the token that identifies the bot
        :param poll_delay:
            the delay in seconds between update requests,
            by default it's 1 second (which also is the minimum possible delay)
        """
        super().__init__()
        self._kill = threading.Event()
        self.token: str = bot_token
        self.poll_delay: int = poll_delay
        self.last_update: int = -1
        self.analyzer = analyzer

    def get_updates(self) -> dict:
        """ returns updates received by the bot since last call of this method """
        response: Response = get(
            f"https://api.telegram.org/bot{self.token}/getUpdates?offset={self.last_update}"
        )
        try:
            response_dictionary = response.json()
        except Exception as e:
            log.error(f"can't parse response into json {e}")
            response_dictionary = None
        if response.ok:
            return response_dictionary if response_dictionary else {"ok": False, "error": "Could not parse response"}
        if response_dictionary:
            return {
                "error": response_dictionary.get("description"),
                "error code": response_dictionary.get("error_code")
            }
        return {"ok": False, "error": "Could not call getUpdates method"}

    def run(self):
        log.info("Listener started")
        while True:
            updates_result: dict = self.get_updates()
            if updates_result["ok"]:
                for update in updates_result["result"]:
                    self.last_update = update["update_id"] + 1
                    message: Message = Message(update)
                    self.analyzer.analyze(message)
            else:
                log.error(f"getUpdates error: {updates_result.get('error', 'Unknown error')}")
            is_killed = self._kill.wait(self.poll_delay)
            if is_killed:
                log.warning("Listener killed")
                return

    def kill(self):
        self._kill.set()
