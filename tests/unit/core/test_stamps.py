from bumpit.core.stamps import StaticStamp, IncrementingStamp


def test_static_stamp():
    stamp = StaticStamp("the_stamp")
    assert "the_stamp" == stamp()


def test_incrementing_stamp():
    stamp = IncrementingStamp(1)
    assert 2 == stamp()
