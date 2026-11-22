import pytest
from television import Television


@pytest.fixture
def tv() -> Television:
    return Television()


def test_init(tv):
    assert str(tv) == 'Power = False, Channel = 0, Volume = 0'


def test_power(tv):
    tv.power()
    assert str(tv) == 'Power = True, Channel = 0, Volume = 0'
    tv.power()
    assert str(tv) == 'Power = False, Channel = 0, Volume = 0'


def test_mute(tv):
    # on, volume up once, then muted
    tv.power()
    tv.volume_up()
    tv.mute()
    assert str(tv) == 'Power = True, Channel = 0, Volume = 0'
    # on and unmuted
    tv.mute()
    assert str(tv) == 'Power = True, Channel = 0, Volume = 1'


def test_mute_when_off(tv):
    # off and muted (mute is ignored while off)
    tv.power()
    tv.volume_up()
    tv.power()
    tv.mute()
    assert str(tv) == 'Power = False, Channel = 0, Volume = 1'
    # off and unmuted
    tv.mute()
    assert str(tv) == 'Power = False, Channel = 0, Volume = 1'


def test_channel_up(tv):
    # off
    tv.channel_up()
    assert str(tv) == 'Power = False, Channel = 0, Volume = 0'
    # on
    tv.power()
    tv.channel_up()
    assert str(tv) == 'Power = True, Channel = 1, Volume = 0'
    # go to the maximum, then one more wraps to the minimum
    tv.channel_up()
    tv.channel_up()
    assert str(tv) == 'Power = True, Channel = 3, Volume = 0'
    tv.channel_up()
    assert str(tv) == 'Power = True, Channel = 0, Volume = 0'


def test_channel_down(tv):
    # off
    tv.channel_down()
    assert str(tv) == 'Power = False, Channel = 0, Volume = 0'
    # on, past minimum wraps to maximum
    tv.power()
    tv.channel_down()
    assert str(tv) == 'Power = True, Channel = 3, Volume = 0'
    tv.channel_down()
    assert str(tv) == 'Power = True, Channel = 2, Volume = 0'


def test_volume_up(tv):
    # off
    tv.volume_up()
    assert str(tv) == 'Power = False, Channel = 0, Volume = 0'
    # on
    tv.power()
    tv.volume_up()
    assert str(tv) == 'Power = True, Channel = 0, Volume = 1'
    # on, muted, volume increased -> unmuted
    tv.mute()
    tv.volume_up()
    assert str(tv) == 'Power = True, Channel = 0, Volume = 2'
    # past maximum
    tv.volume_up()
    assert str(tv) == 'Power = True, Channel = 0, Volume = 2'


def test_volume_down(tv):
    # off
    tv.volume_down()
    assert str(tv) == 'Power = False, Channel = 0, Volume = 0'
    # on, raise to max then decrease
    tv.power()
    tv.volume_up()
    tv.volume_up()
    tv.volume_down()
    assert str(tv) == 'Power = True, Channel = 0, Volume = 1'
    # on, muted, volume decreased -> unmuted
    tv.mute()
    tv.volume_down()
    assert str(tv) == 'Power = True, Channel = 0, Volume = 0'
    # past minimum
    tv.volume_down()
    assert str(tv) == 'Power = True, Channel = 0, Volume = 0'
