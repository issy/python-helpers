from src import Stream


def test_to_list():
    nums = range(5)
    result = Stream(nums).to_list()
    assert result == [0, 1, 2, 3, 4]


def test_filter():
    nums = (i + 1 for i in range(5))
    filtered_nums = Stream(nums).filter(lambda n: n % 2 == 0).to_list()
    assert filtered_nums == [2, 4]


def test_reduce():
    nums = (i + 2 for i in range(5))
    result = (
        Stream(nums)
        .map(lambda n: n + 5)
        .filter(lambda n: n % 2 == 0)
        .map(lambda n: n * 8)
        .reduce(lambda a, b: a + b, 0)
    )
    assert result == 144


def test_operation_helpers():
    nums = range(5)
    result = Stream(nums).filter(Stream.not_op(Stream.eq(2))).filter(Stream.in_list([0, 1, 2])).to_list()
    assert result == [0, 1]


def test_map():
    li = [["hello", "world"], ["hello", "foo"], ["baz", "bar"]]
    result = (
        Stream(li)
        .map(lambda t: {"foo": t[0], "bar": t[1]})
        .map(lambda d: d["foo"])
        .filter(Stream.not_op(Stream.eq("hello")))
        .to_list()
    )
    assert result == ["baz"]
