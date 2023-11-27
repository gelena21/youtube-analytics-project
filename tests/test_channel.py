import json

import pytest

from src.channel import Channel


@pytest.fixture
def moscowpython_channel():
    return Channel('UC-OVMPlMA3-YCIeg4z5z23A')


def test_channel_attributes(moscowpython_channel):
    assert moscowpython_channel._channel_id == 'UC-OVMPlMA3-YCIeg4z5z23A'
    assert len(moscowpython_channel.title) > 0
    assert len(moscowpython_channel.description) > 0
    assert len(moscowpython_channel.url) > 0
    assert moscowpython_channel.subscriber_count >= 0
    assert moscowpython_channel.video_count >= 0
    assert moscowpython_channel.view_count >= 0


def test_channel_to_json(moscowpython_channel, tmp_path):
    json_filename = tmp_path / 'moscowpython.json'
    moscowpython_channel.to_json(str(json_filename))

    assert json_filename.is_file()

    with open(json_filename, 'r', encoding='utf-8') as json_file:
        channel_data = json.load(json_file)
        assert 'id' in channel_data
        assert 'title' in channel_data
        assert 'description' in channel_data
        assert 'url' in channel_data
        assert 'subscriber_count' in channel_data
        assert 'video_count' in channel_data
        assert 'view_count' in channel_data


def test_channel_str(moscowpython_channel):
    expected_str = f"{moscowpython_channel.title} ({moscowpython_channel.url})"
    assert str(moscowpython_channel) == expected_str


@pytest.fixture
def highload_channel():
    return Channel('UCwHL6WHUarjGfUM_586me8w')


def test_channel_addition(moscowpython_channel, highload_channel):
    total_subscribers = (moscowpython_channel.subscriber_count
                         + highload_channel.subscriber_count)
    assert moscowpython_channel + highload_channel == total_subscribers


def test_channel_subtraction(moscowpython_channel, highload_channel):
    difference_subscribers = (moscowpython_channel.subscriber_count
                              - highload_channel.subscriber_count)
    assert moscowpython_channel - highload_channel == difference_subscribers


def test_channel_comparison(moscowpython_channel, highload_channel):
    assert moscowpython_channel < highload_channel
    assert moscowpython_channel <= highload_channel
    assert not moscowpython_channel > highload_channel
    assert not moscowpython_channel >= highload_channel
    assert not moscowpython_channel == highload_channel
    assert moscowpython_channel != highload_channel
