import re
import threading
from typing import List, Callable, Any

from wiretap.utils import Message


class AnalyzerAction:

    def __init__(self, regex: str or None, lower: bool,  action: Callable[[Message], Any]):
        self.regex = regex
        self.action = action
        if regex:
            self.run = self.run_with_regex_lower if lower else self.run_with_regex
        else:
            self.run = self.run_no_regex

    def run_with_regex(self, message: Message):
        if re.match(self.regex, message.text):
            self.action(message)

    def run_with_regex_lower(self, message: Message):
        if re.match(self.regex, message.lower_text):
            self.action(message)

    def run_no_regex(self, message: Message):
        self.action(message)


class GenericMessageAnalyzer:

    def __init__(self):
        self.lock = threading.Lock()

    def filter_actions(self, message: Message) -> List[AnalyzerAction]:
        raise NotImplemented

    def analyze(self, message: Message):
        actions = self.filter_actions(message)
        for action in actions:
            action.run(message)
