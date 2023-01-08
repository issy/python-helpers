from typing import Any, Callable, Iterator, TypeVar, Self, Literal

T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")


class Stream:
    _it: Iterator[T1]
    _actions: list[tuple[Literal["map", "filter"], Callable[[Any], Any]]]

    def __init__(self, _iter: Iterator[T1]):
        self._it = _iter
        self._actions = []

    def map(self, fn: Callable[[T1 | Any], T2]) -> Self:
        self._actions.append(("map", fn))
        return self

    def filter(self, fn: Callable[[T1 | T2], bool]) -> Self:
        self._actions.append(("filter", fn))
        return self

    def _get_results(self) -> list[Any]:
        items = []
        ignore_indexes = []
        for i, elem in enumerate(self._it):
            if i in ignore_indexes:
                continue

            for action_type, action in self._actions:
                if action_type == "filter":
                    if not action(elem):
                        ignore_indexes.append(i)
                        break
                elif action_type == "map":
                    elem = action(elem)

            if i not in ignore_indexes:
                items.append(elem)

        return items

    def reduce(self, fn: Callable[[T3, Any], T3], start_value: T3) -> T3:
        current_value = start_value
        for item in self._get_results():
            current_value = fn(current_value, item)

        return current_value

    def to_list(self) -> list[Any]:
        return self._get_results()

    @staticmethod
    def not_op(fn: Callable[[Any], bool]) -> Callable[[Any], bool]:
        def inner(i: Any) -> bool:
            return not fn(i)

        return inner

    @staticmethod
    def eq(to_match: T3) -> Callable[[T3], bool]:
        def inner(i: T3) -> bool:
            return i == to_match

        return inner

    @staticmethod
    def in_list(li: list[T3]) -> Callable[[T3], bool]:
        def inner(i: T3) -> bool:
            return i in li

        return inner
