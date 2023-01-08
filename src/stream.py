from typing import Any, Callable, Iterator, Literal, Self, TypeVar

T = TypeVar("T")
T = TypeVar("T")
T = TypeVar("T")


class Stream:
    _it: Iterator[T]
    _actions: list[tuple[Literal["map", "filter"], Callable[[Any], Any]]]

    def __init__(self, _iter: Iterator[T]):
        self._it = _iter
        self._actions = []

    def map(self, fn: Callable[[T | Any], Any]) -> Self:
        self._actions.append(("map", fn))
        return self

    def filter(self, fn: Callable[[T | T], bool]) -> Self:
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

    def reduce(self, fn: Callable[[T, Any], T], start_value: T) -> T:
        current_value = start_value
        for item in self._get_results():
            current_value = fn(current_value, item)

        return current_value

    def group_by(self, get_key: Callable[[Any], T]) -> dict[T, Any]:
        def collector(groups: dict, item: Any) -> dict:
            key = get_key(item)
            if key not in groups:
                groups[key] = []

            groups[key].append(item)
            return groups

        return self.reduce(collector, {})

    def to_list(self) -> list[Any]:
        return self._get_results()

    @staticmethod
    def not_op(fn: Callable[[Any], bool]) -> Callable[[Any], bool]:
        def inner(i: Any) -> bool:
            return not fn(i)

        return inner

    @staticmethod
    def eq(to_match: T) -> Callable[[T], bool]:
        def inner(i: T) -> bool:
            return i == to_match

        return inner

    @staticmethod
    def in_list(li: list[T]) -> Callable[[T], bool]:
        def inner(i: T) -> bool:
            return i in li

        return inner
