import time

from hemlock.timer import Timer

VARIABLE_NAME = "timer_variable"


def test_repr():
    timer = Timer(VARIABLE_NAME)
    assert repr(timer) == f"<Timer {VARIABLE_NAME} paused 0 seconds>"
    timer.start()
    assert repr(timer).startswith(f"<Timer {VARIABLE_NAME} running")


def test_start():
    timer = Timer(VARIABLE_NAME)
    assert timer.total_seconds == 0
    assert not timer.is_running
    timer.start()
    assert timer.is_running
    total_seconds = timer.total_seconds
    time.sleep(0.1)
    assert total_seconds < timer.total_seconds < total_seconds + 0.2


def test_pause():
    timer = Timer(VARIABLE_NAME)
    timer.start()
    time.sleep(0.1)
    timer.pause()
    assert not timer.is_running
    total_seconds = timer.total_seconds
    time.sleep(0.1)
    assert timer.total_seconds == total_seconds


def test_pack_data():
    timer = Timer(VARIABLE_NAME)
    timer.start()
    time.sleep(0.1)
    timer.pause()
    assert timer.pack_data() == {VARIABLE_NAME: [timer.total_seconds]}
