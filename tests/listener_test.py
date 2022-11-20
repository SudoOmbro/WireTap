from tests.test_utils import get_test_config
from wiretap.listener import TelegramListener


LISTENER = TelegramListener(
    get_test_config()["token"]
)


def test_get_updates():
    print(LISTENER.get_updates())


def test_poll_updates():
    LISTENER.start()


if __name__ == "__main__":
    test_get_updates()
    test_poll_updates()
