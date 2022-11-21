import re
from typing import List, Callable, Any

from wiretap.utils import Message


class AnalyzerAction:
    """ An action that can be executed conditionally (or not) on message reception """

    def __init__(self, regex: str or None, lower: bool,  action: Callable[[Message], Any]):
        """
        :param regex: the regex to search for in the received message text, use None to avoid using regex
        :param lower: whether to call lower() on the received message text
        :param action:
            what to do with the received message.
            The return value of the action will determine list iteration termination on the list of actions.
        """
        self.regex = regex
        self.action = action
        if regex:
            self.run = self.run_with_regex_lower if lower else self.run_with_regex
        else:
            self.run = self.run_no_regex

    def run_with_regex(self, message: Message) -> bool:
        if re.search(self.regex, message.text):
            return self.action(message)
        return False

    def run_with_regex_lower(self, message: Message) -> bool:
        if re.search(self.regex, message.lower_text):
            return self.action(message)
        return False

    def run_no_regex(self, message: Message) -> bool:
        return self.action(message)


class GenericMessageAnalyzer:
    """ The most barebones version of a message analyzer, filter_action must be implemented """

    def filter_actions(self, message: Message) -> List[AnalyzerAction]:
        """ return a list of actions to be checked against the received message """
        raise NotImplemented

    def analyze(self, message: Message):
        """ analyze the received message """
        actions = self.filter_actions(message)
        for action in actions:
            if action.run(message):
                return
