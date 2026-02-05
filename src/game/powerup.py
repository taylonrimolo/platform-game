from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.graphics import Color, Rectangle
import math
from src.constants import POWERUP_COLORS


class PowerUp(Widget):
    ptype = StringProperty("jump")

    def __init__(self, pos, ptype="jump", **kwargs):
        super().__init__(**kwargs)
        self.ptype = ptype
        self.size = (22, 22)
        self.pos = pos
        self._t = 0.0
        self.current_color = POWERUP_COLORS.get(ptype, (1,1,1))

        with self.canvas:
            self.color = Color(*self.current_color)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update_graphics)

    def _update_graphics(self, *args):
        self.rect.pos = self.pos

    def animate(self, dt):
        self._t += dt * 4
        scale = 1 + 0.18 * math.sin(self._t)
        scaled_size = (self.size[0] * scale, self.size[1] * scale)
        offset_x = (scaled_size[0] - self.size[0]) / 2
        offset_y = (scaled_size[1] - self.size[1]) / 2
        self.rect.size = scaled_size
        self.rect.pos = (self.x - offset_x, self.y - offset_y)