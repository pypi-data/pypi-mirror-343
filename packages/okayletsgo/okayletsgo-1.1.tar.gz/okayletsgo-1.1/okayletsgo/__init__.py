import threading
from just_playback import Playback


def _play_sound():
    playback = Playback('./sound.mp3')
    try:
        playback.play()
        while playback.active:
            pass
    except Exception as e:
        print(f"Error playing okayletsgo-sound: {e}")


# Run _play_sound in a separate thread
sound_thread = threading.Thread(target=_play_sound)
sound_thread.start()
