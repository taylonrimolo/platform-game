from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivy.graphics import Color, Rectangle
from src.constants import PLATFORM_COLORS


class Platform(Widget):
    moving = BooleanProperty(False)
    ptype = StringProperty("normal")
    min_x = NumericProperty(0)
    max_x = NumericProperty(0)
    direction = NumericProperty(1)

    def __init__(self, **kwargs):
        self.moving = kwargs.pop('moving', False)
        self.ptype = kwargs.pop('ptype', "normal")
        size = kwargs.pop('size', (100, 20))
        self.min_x = kwargs.pop('min_x', 0)
        self.max_x = kwargs.pop('max_x', 0)

        super().__init__(**kwargs)
        self.size = size

        with self.canvas.before:
            Color(0, 0, 0, 0.22)
            self._shadow = Rectangle(pos=(self.x, self.y - 6), size=(size[0], 8))

        with self.canvas:
            Color(*PLATFORM_COLORS.get(self.ptype, (0,0,1)))
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update_graphics, size=self._update_graphics)

    def _update_graphics(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self._shadow.pos = (self.x + 3, self.y - 6)
        self._shadow.size = (self.size[0] - 6, 8)

    def move_platform(self, speed=2.0):
        if self.moving:
            self.x += self.direction * speed
            if self.x <= self.min_x:
                self.x = self.min_x
                self.direction = 1
            elif self.x >= self.max_x:
                self.x = self.max_x
                self.direction = -1