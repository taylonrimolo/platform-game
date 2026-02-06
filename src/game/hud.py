from kivy.uix.label import Label
from kivy.core.window import Window


def create_score_label():
    return Label(
        text="Score: 0",
        pos=(12, Window.height - 36),
        font_size=20
    )


def create_controls_label():
    return Label(
        text="W / ↑ = Pular    A/D ou ←/→ = Mover",
        pos=(12, 8),
        font_size=14
    )


def create_title_label():
    return Label(
        text="Platform Game",
        font_size=28,
        pos=(Window.width / 2 - 120, Window.height - 50)
    )
