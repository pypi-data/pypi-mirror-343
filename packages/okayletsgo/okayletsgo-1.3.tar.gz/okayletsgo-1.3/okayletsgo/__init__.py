import threading
import os
import importlib.resources
from just_playback import Playback


def _play_sound():
    try:
        with importlib.resources.files('okayletsgo') as package_path:
            sound_path = os.path.join(package_path, 'sound.mp3')
    except AttributeError:
        package_dir = os.path.dirname(os.path.abspath(__file__))
        sound_path = os.path.join(package_dir, 'sound.mp3')

    try:
        playback = Playback(sound_path)
        playback.play()
        while playback.active:
            pass
    except Exception as e:
        print(f"Error playing okayletsgo-sound: {e}")


# Run _play_sound in a separate thread
sound_thread = threading.Thread(target=_play_sound)
sound_thread.start()