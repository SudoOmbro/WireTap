import threading
from enum import Enum
from functools import cache
from typing import Any, List, Callable

from wiretap.utils import Message


class FilterPredicate(Enum):
    EQUALS = 0
    IN = 1
    LESS_THAN = 2
    LESS_OR_EQUAL_THAN = 3


class ActionFilter:
    """
    filter messages by metadata (message_id, chat_id, chat_type, timestamp, sender_id).

    Cache results to speed up filtering
    """

    def __init__(self, target_attribute: str, predicate: FilterPredicate, param: Any, negated: bool):
        self.target_attribute = target_attribute
        self.predicate = predicate
        self.param = param
        self.negated = negated

    @cache
    def evaluate(self, value: Any):
        result: bool = False
        match self.predicate:
            case FilterPredicate.EQUALS:
                result = value == self.param
            case FilterPredicate.IN:
                result = value in self.param
            case FilterPredicate.LESS_THAN:
                result = value < self.param
            case FilterPredicate.LESS_OR_EQUAL_THAN:
                result = value <= self.param
        return not result if self.negated else result

    def apply(self, message: Message):
        return self.evaluate(message.__dict__[self.target_attribute])


class AnalyzerAction:

    def __init__(self, filters: List[ActionFilter], regex: str or None, action: Callable):
        pass


class MessageAnalyzer:

    def __init__(self):
        self.lock = threading.Lock()
