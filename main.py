from kivy.app import App
from kivy.core.window import Window
from src.game.core import Game
from src.utils.audio import SoundManager

Window.maximize()

class PlatformGameApp(App):
    def build(self):
        self.title = "Platform Game"

        sound_manager = SoundManager()
        sound_manager.load("bg", "assets/audio/bg_music.mp3", loop=True, volume=0.35)
        sound_manager.load("jump", "assets/audio/sfx_jump.wav", volume=0.6)
        sound_manager.load("break", "assets/audio/sfx_break.wav", volume=0.6)

        sound_manager.play("bg")

        game = Game(sound_manager=sound_manager)
        return game


if __name__ == "__main__":
    PlatformGameApp().run()