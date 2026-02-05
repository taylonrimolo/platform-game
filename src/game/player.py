from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, BooleanProperty
from kivy.vector import Vector
from kivy.graphics import Color, Rectangle, Ellipse   # ← ADICIONE AQUI
from src.constants import BASE_SPEED, BASE_JUMP

class Player(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    speed = NumericProperty(BASE_SPEED)
    jump_strength = NumericProperty(BASE_JUMP)
    on_ground = BooleanProperty(False)
    shield = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (40, 40)

        with self.canvas:
            self._shield_color = Color(0, 1, 1, a=0)
            self._shield_ellipse = Ellipse(pos=(-100, -100), size=(64, 64))
            Color(1, 0.15, 0.15)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update_graphics, size=self._update_graphics, shield=self._update_shield)

    def _update_graphics(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        if self.shield:
            self._update_shield()

    def _update_shield(self, *args):
        if self.shield:
            self._shield_color.a = 0.45
            s = (self.width * 1.6, self.height * 1.6)
            self._shield_ellipse.size = s
            self._shield_ellipse.pos = (self.center_x - s[0]/2, self.center_y - s[1]/2)
        else:
            self._shield_color.a = 0
            self._shield_ellipse.pos = (-100, -100)

    def move(self, gravity):
        self.velocity_y -= gravity
        self.pos = Vector(*self.velocity) + self.pos

    def reset_stats(self):
        self.speed = BASE_SPEED
        self.jump_strength = BASE_JUMP
        self.shield = False