from pygame import mixer
import pygame

MUSIC_END = pygame.USEREVENT + 1


class MusicPlayer:
    def __init__(self) -> None:
        mixer.init()
        self.audio = mixer.music.load("media/MDGE.mp3")
        mixer.music.set_volume(0.8)
        pygame.mixer.music.set_endevent(MUSIC_END)

    def play(self) -> None:
        mixer.music.play()

    # NOT WORKING IN PYGBAG
    # def pauseUnpause(self) -> None:
    #     mixer.music.pause() if mixer.music.get_busy() else mixer.music.unpause()

    def pause(self) -> None:
        mixer.music.pause()

    def unpause(self) -> None:
        mixer.music.unpause()
