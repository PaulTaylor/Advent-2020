from ex01a import worker2, worker3

def test_worker():
    x = [1721,979,366,299,675,1456]
    assert worker2(x) == 514579
    assert worker3(x) == 241861950