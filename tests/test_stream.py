from src import Stream


def test_to_list():
    assert Stream(range(5)).to_list() == [0, 1, 2, 3, 4]


def test_filter():
    assert Stream(i + 1 for i in range(5)).filter(lambda n: n % 2 == 0).to_list() == [2, 4]


def test_reduce():
    assert (
        Stream(i + 2 for i in range(5))
        .map(lambda n: n + 5)
        .filter(lambda n: n % 2 == 0)
        .map(lambda n: n * 8)
        .reduce(lambda a, b: a + b, 0)
    ) == 144


def test_operation_helpers():
    assert (Stream(range(5)).filter(Stream.not_op(Stream.eq(2))).filter(Stream.in_list([0, 1, 2])).to_list()) == [0, 1]


def test_map():
    assert (
        Stream([["hello", "world"], ["hello", "foo"], ["baz", "bar"]])
        .map(lambda t: {"foo": t[0], "bar": t[1]})
        .map(lambda d: d["foo"])
        .filter(Stream.not_op(Stream.eq("hello")))
        .to_list()
    ) == ["baz"]


def test_group_by():
    assert Stream(["abc", "acdc", "bar", "baz"]).group_by(lambda s: s[0]) == {"a": ["abc", "acdc"], "b": ["bar", "baz"]}
