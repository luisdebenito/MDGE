from pygame import mixer


class MusicPlayer:
    def __init__(self) -> None:
        mixer.init()
        self.audio = mixer.music.load("media/MDGE.mp3")
        mixer.music.set_volume(0.8)

    def play(self) -> None:
        mixer.music.play()

    def stop(self) -> None:
        mixer.music.stop()

    def pauseUnpause(self) -> None:
        mixer.music.pause() if mixer.music.get_busy() else mixer.music.unpause()
