from kivy.core.audio import SoundLoader


class SoundManager:
    def __init__(self):
        self.sounds = {}

    def load(self, name: str, path: str, loop=False, volume=0.7):
        sound = SoundLoader.load(path)
        if sound:
            sound.volume = volume
            sound.loop = loop
            self.sounds[name] = sound
        return sound is not None

    def play(self, name: str):
        if name in self.sounds:
            self.sounds[name].stop()
            self.sounds[name].play()

    def stop(self, name: str):
        if name in self.sounds:
            self.sounds[name].stop()