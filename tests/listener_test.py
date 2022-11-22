from typing import List

from tests.test_utils import get_test_config
from wiretap.analyzer import AbstractMessageAnalyzer, AnalyzerAction
from wiretap.listener import TelegramListener
from wiretap.utils import Message


ACTION = AnalyzerAction(r"test", True, lambda m: print(f"message contains \"test\": {m.text}"))


class TestAnalyzer(AbstractMessageAnalyzer):

    def filter_actions(self, message: Message) -> List[AnalyzerAction]:
        return [ACTION]


LISTENER = TelegramListener(
    get_test_config()["token"],
    TestAnalyzer()
)


def test_get_updates():
    print(LISTENER.get_updates())


def test_poll_updates():
    LISTENER.start()


if __name__ == "__main__":
    test_get_updates()
    test_poll_updates()
