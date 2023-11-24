import json
import dotenv
import pytest
from src.channel import Channel

dotenv.load_dotenv()

@pytest.fixture
def moscowpython_channel():
    return Channel('UC-OVMPlMA3-YCIeg4z5z23A')

def test_channel_attributes(moscowpython_channel):
    assert moscowpython_channel.id == 'UC-OVMPlMA3-YCIeg4z5z23A'
    assert len(moscowpython_channel.title) > 0
    assert len(moscowpython_channel.description) > 0
    assert len(moscowpython_channel.url) > 0
    assert moscowpython_channel.subscriber_count >= 0
    assert moscowpython_channel.video_count >= 0
    assert moscowpython_channel.view_count >= 0

def test_channel_to_json(moscowpython_channel, tmp_path):
    json_filename = tmp_path / 'moscowpython.json'
    moscowpython_channel.to_json(str(json_filename))

    # Проверяем, что файл был создан
    assert json_filename.is_file()

    # Проверяем содержимое файла
    with open(json_filename, 'r', encoding='utf-8') as json_file:
        channel_data = json.load(json_file)
        assert 'id' in channel_data
        assert 'title' in channel_data
        assert 'description' in channel_data
        assert 'url' in channel_data
        assert 'subscriber_count' in channel_data
        assert 'video_count' in channel_data
        assert 'view_count' in channel_data
