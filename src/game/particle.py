from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty
from kivy.graphics import Color, Ellipse
import random
import math


class Particle(Widget):
    velocity = ListProperty([0, 0])
    life = NumericProperty(0.3)

    def __init__(self, pos, color=(1, 1, 1), ptype='jump', **kwargs):
        super().__init__(**kwargs)
        self.size = (10, 10) if ptype == 'jump' else (14, 14)
        self.pos = pos

        if ptype == 'jump':
            self.velocity = [random.uniform(-2, 2), random.uniform(2, 5)]
            self.life = 0.3
        elif ptype == 'powerup':
            angle = random.uniform(0, 2 * math.pi)
            strength = random.uniform(3, 7)
            self.velocity = [strength * math.cos(angle), strength * math.sin(angle)]
            self.life = 0.6

        with self.canvas:
            Color(*color, 0.9)
            self.ellipse = Ellipse(pos=self.pos, size=self.size)

        self.bind(pos=self._update_graphics)

    def _update_graphics(self, *args):
        self.ellipse.pos = self.pos

    def update(self, dt):
        self.x += self.velocity[0] * dt * 60
        self.y += self.velocity[1] * dt * 60
        self.velocity[1] -= 0.15 * dt * 60
        self.life -= dt
        return self.life <= 0