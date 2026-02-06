from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.button import Button

import random
import math

from src.constants import *
from src.game.player import Player
from src.game.platform import Platform
from src.game.powerup import PowerUp
from src.game.particle import Particle
from src.game.effects import activate_powerup, update_active_effects
from src.utils.highscore import HighScoreManager
from src.game.platform_generator import PlatformGenerator

class Game(Widget):
    score = NumericProperty(0)

    def __init__(self, sound_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.sound_manager = sound_manager

        self.game_over = False
        self.particles = []
        self.powerups = []
        self.platforms = []
        self.active_effects = []
        self.total_height = 0.0
        self.platform_index = 0

        self.highscore_manager = HighScoreManager(HIGH_SCORE_FILE)
        self.high_score = self.highscore_manager.high_score

        # Painel superior
        self.hud_panel = Widget(pos=(0, Window.height - 100), size=(Window.width, 100))

        with self.hud_panel.canvas.before:
            Color(0.06, 0.10, 0.22, 0.70)
            self.hud_bg = Rectangle(pos=self.hud_panel.pos, size=self.hud_panel.size)

        # Score com sombra
        self.score_label = Label(
            text="Score: 0",
            font_size=36,
            bold=True,
            color=(1, 1, 1, 1),
            pos=(25, Window.height - 65)
        )
        self.score_shadow = Label(
            text="Score: 0",
            font_size=36,
            bold=True,
            color=(0, 0, 0, 0.65),
            pos=(27, Window.height - 67)
        )

        # Recorde
        self.highscore_label = Label(
            text=f"Recorde: {self.high_score}",
            font_size=22,
            color=(1.0, 0.92, 0.4, 1.0),
            pos=(25, Window.height - 100)
        )

        # Título do jogo
        self.title_label = Label(
            text="Platform Game",
            font_size=26,
            color=(0.85, 0.85, 1.0, 0.9),
            pos=(Window.width / 2 - 110, Window.height - 50)
        )

        # Controles (canto inferior)
        self.controls_label = Label(
            text="W / ↑ = Pular     A / D ou ← / → = Mover",
            font_size=15,
            color=(0.92, 0.92, 0.92, 0.75),
            pos=(25, 18)
        )

        # Adiciona ao widget
        self.add_widget(self.hud_panel)
        self.add_widget(self.score_shadow)
        self.add_widget(self.score_label)
        self.add_widget(self.highscore_label)
        self.add_widget(self.title_label)
        self.add_widget(self.controls_label)

        # Responsividade
        self.bind(size=self.on_size)

        # Fundo degradê
        self._create_background()

        self.init_game()
        self.setup_keyboard()

        Clock.schedule_interval(self.update, 1/60.0)
        Clock.schedule_interval(self.animate_powerups, 1/60.0)

    def on_size(self, *args):
        """Atualiza HUD quando a janela muda de tamanho"""
        if hasattr(self, 'hud_panel'):
            self.hud_panel.pos = (0, Window.height - 100)
            self.hud_panel.size = (Window.width, 100)
            self.hud_bg.pos = self.hud_panel.pos
            self.hud_bg.size = self.hud_panel.size

            self.score_label.pos = (25, Window.height - 65)
            self.score_shadow.pos = (27, Window.height - 67)
            self.highscore_label.pos = (25, Window.height - 100)
            self.title_label.pos = (Window.width / 2 - 110, Window.height - 50)

    def _create_background(self):
        h = Window.height
        w = Window.width
        with self.canvas.before:
            Color(0.04, 0.06, 0.12)
            Rectangle(pos=(0, 0), size=(w, h*0.25))
            Color(0.05, 0.12, 0.28)
            Rectangle(pos=(0, h*0.25), size=(w, h*0.25))
            Color(0.10, 0.22, 0.45)
            Rectangle(pos=(0, h*0.5), size=(w, h*0.25))
            Color(0.18, 0.35, 0.65)
            Rectangle(pos=(0, h*0.75), size=(w, h*0.25))

    def init_game(self):
        first = Platform(
            pos=(Window.width / 2 - 50, 0),
            size=(100, 40),
            moving=False,
            ptype="normal"
        )
        self.add_widget(first)
        self.platforms = [first]

        self.player = Player(pos=(Window.width / 2 - 20, first.top))
        self.add_widget(self.player)

        self.generate_initial_platforms(10)

    def generate_initial_platforms(self, count=10):
        last_y = self.platforms[0].y
        for _ in range(1, count):
            last_y += PLATFORM_BASE_SPACING
            self.add_platform(y_pos=last_y)

    def add_platform(self, y_pos):
        params = self.get_dynamic_params()
        last_x = self.platforms[-1].x if self.platforms else (Window.width / 2 - 50)

        y = y_pos + random.uniform(-RANDOM_VERTICAL_OFFSET, RANDOM_VERTICAL_OFFSET)

        min_w, max_w = 80, 140
        plat_width = random.randint(min_w, max_w)

        delta = random.uniform(-180, 180)
        plat_x = last_x + delta
        plat_x = max(0, min(plat_x, Window.width - plat_width))

        moving = random.random() < MOVING_PLATFORM_CHANCE
        ptype = random.choices(["normal", "boost", "break"], weights=[0.74, 0.13, 0.13])[0]

        min_x = max_x = plat_x
        if moving:
            movement_range = 160
            min_x = max(0, plat_x - movement_range//2)
            max_x = min(Window.width - plat_width, plat_x + movement_range//2)

        plat = Platform(
            pos=(plat_x, y),
            size=(plat_width, 20),
            moving=moving,
            ptype=ptype,
            min_x=min_x,
            max_x=max_x
        )
        self.add_widget(plat)
        self.platforms.append(plat)

        if random.random() < POWERUP_CHANCE:
            pu_type = random.choice(["jump", "speed", "shield", "points"])
            pu = PowerUp(pos=(plat_x + plat_width//2 - 11, y + 30), ptype=pu_type)
            self.add_widget(pu)
            self.powerups.append(pu)

        self.platform_index += 1

    def get_difficulty(self):
        return min(1.0, self.total_height / DIFFICULTY_MAX_HEIGHT)

    def get_dynamic_params(self):
        d = self.get_difficulty()
        spacing = int(PLATFORM_BASE_SPACING - 35 * d)
        spacing = max(90, spacing)
        return {'spacing': spacing}

    def setup_keyboard(self):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)
        self.keys_pressed = set()

    def _keyboard_closed(self):
        pass

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.keys_pressed.add(keycode[1])
        return True

    def _on_key_up(self, keyboard, keycode):
        self.keys_pressed.discard(keycode[1])
        return True

    def handle_input(self):
        if 'a' in self.keys_pressed or 'left' in self.keys_pressed:
            self.player.velocity_x = -self.player.speed
        elif 'd' in self.keys_pressed or 'right' in self.keys_pressed:
            self.player.velocity_x = self.player.speed
        else:
            self.player.velocity_x = 0

        if ('w' in self.keys_pressed or 'up' in self.keys_pressed) and self.player.on_ground:
            self.player.velocity_y = self.player.jump_strength
            self.player.on_ground = False
            self.spawn_jump_particles()
            if self.sound_manager:
                self.sound_manager.play("jump")

    def spawn_jump_particles(self, count=7):
        for _ in range(count):
            p = Particle(pos=(self.player.center_x, self.player.y), ptype='jump')
            self.add_widget(p)
            self.particles.append(p)

    def spawn_powerup_particles(self, pos, color, count=15):
        for _ in range(count):
            p = Particle(pos=pos, color=color, ptype='powerup')
            self.add_widget(p)
            self.particles.append(p)

    def animate_powerups(self, dt):
        for pu in self.powerups[:]:
            pu.animate(dt)

    def update(self, dt):
        if self.game_over:
            return

        update_active_effects(self, dt)
        self.handle_input()

        self.player.move(GRAVITY)
        self.check_collision()
        self.check_powerup_collision()
        self.scroll_screen()
        self.move_platforms()
        self.update_score()
        self.check_fall()
        self.update_particles(dt)
        self.check_bounds()

    def check_collision(self):
        self.player.on_ground = False
        for plat in list(self.platforms):
            if self.player.collide_widget(plat) and self.player.velocity_y <= 0:
                self.player.y = plat.top
                if plat.ptype == "boost":
                    self.player.velocity_y = self.player.jump_strength * 1.55
                    self.spawn_jump_particles(12)
                    self.player.on_ground = False
                else:
                    self.player.velocity_y = 0
                    self.player.on_ground = True

                if plat.ptype == "break" and plat != self.platforms[0]:
                    if self.sound_manager:
                        self.sound_manager.play("break")
                    data = {
                        'pos': plat.pos,
                        'size': plat.size,
                        'moving': plat.moving,
                        'ptype': plat.ptype,
                        'min_x': plat.min_x,
                        'max_x': plat.max_x
                    }
                    Clock.schedule_once(lambda dt, d=data: self._respawn_platform(d), 3.0)
                    self.remove_widget(plat)
                    self.platforms.remove(plat)

    def check_powerup_collision(self):
        for pu in list(self.powerups):
            if self.player.collide_widget(pu):
                activate_powerup(self, pu.ptype)
                self.spawn_powerup_particles(pu.center, pu.current_color)
                self.remove_widget(pu)
                self.powerups.remove(pu)

    def scroll_screen(self):
        if self.player.y > Window.height / 2:
            diff = self.player.y - Window.height / 2
            self.player.y -= diff
            for plat in self.platforms:
                plat.y -= diff
            for pu in self.powerups:
                pu.y -= diff
            self.total_height += diff

            while max(p.y for p in self.platforms) < Window.height + 200:
                next_y = max(p.y for p in self.platforms) + PLATFORM_BASE_SPACING
                self.add_platform(next_y)

            self.cleanup_offscreen()

    def cleanup_offscreen(self):
        for plat in list(self.platforms[1:]):
            if plat.top < -100:
                self.remove_widget(plat)
                self.platforms.remove(plat)
        for pu in list(self.powerups):
            if pu.top < -100:
                self.remove_widget(pu)
                self.powerups.remove(pu)

    def move_platforms(self):
        for plat in self.platforms:
            plat.move_platform(PLATFORM_SPEED)

    def _respawn_platform(self, data):
        plat = Platform(**data)
        self.add_widget(plat)
        self.platforms.append(plat)

    def update_score(self):
        current = int(self.total_height + self.player.y)
        if current > self.score:
            self.score = current
            self.score_label.text = f"Score: {self.score}"
            self.score_shadow.text = f"Score: {self.score}"

            if self.score > self.high_score:
                self.high_score = self.score
                self.highscore_manager.update(self.score)
                self.highscore_label.text = f"Recorde: {self.high_score}"

    def check_fall(self):
        if self.player.top < 0:
            if self.player.shield:
                self.player.shield = False
                self.player.y = 140
                self.player.velocity_y = self.player.jump_strength * 0.9
            else:
                self.game_over = True
                self.highscore_manager.update(self.score)
                self.show_game_over()

    def check_bounds(self):
        self.player.x = max(0, min(self.player.x, Window.width - self.player.width))

    def update_particles(self, dt):
        to_remove = [p for p in self.particles if p.update(dt)]
        for p in to_remove:
            self.remove_widget(p)
            self.particles.remove(p)

    def _reposition_effect_labels(self):
        margin = 25
        x = Window.width - margin
        y = Window.height - 135  # abaixo do painel
        for effect in self.active_effects[::-1]:
            lbl = effect['label']
            lbl.pos = (x - lbl.width, y)
            x -= lbl.width + 15

    def show_game_over(self):
        overlay = Widget(size=self.size, pos=self.pos)

        with overlay.canvas.before:
            Color(0.1, 0.1, 0.1, 0.75)
            Rectangle(size=self.size, pos=self.pos)

        go_title = Label(
            text="GAME OVER",
            font_size=60,
            color=(1,1,1,1),
            center_x=Window.width/2,
            y=Window.height/2 + 120
        )

        go_score = Label(
            text=f"Pontuação: {self.score}",
            font_size=32,
            color=(0.9,0.9,0.9,1),
            center_x=Window.width/2,
            y=Window.height/2 + 40
        )

        is_new = self.score == self.high_score and self.score > 0
        record_text = "Novo Recorde!" if is_new else f"Recorde: {self.high_score}"
        record_color = (1,1,0,1) if is_new else (0.2,0.9,0.2,1)

        go_record = Label(
            text=record_text,
            font_size=26,
            color=record_color,
            center_x=Window.width/2,
            y=Window.height/2 - 10
        )

        restart_btn = Button(
            text="Reiniciar",
            size_hint=(None, None),
            size=(260, 70),
            background_color=(0.1, 0.7, 0.1, 1),
            font_size=26,
            center_x=Window.width/2,
            y=Window.height/2 - 100
        )
        restart_btn.bind(on_release=self.restart_game)

        press_r = Label(
            text="ou pressione R para reiniciar",
            font_size=18,
            color=(0.7,0.7,0.7,1),
            center_x=Window.width/2,
            y=Window.height/2 - 170
        )

        overlay.add_widget(go_title)
        overlay.add_widget(go_score)
        overlay.add_widget(go_record)
        overlay.add_widget(restart_btn)
        overlay.add_widget(press_r)

        self.add_widget(overlay)
        self.game_over_overlay = overlay

    def restart_game(self, *args):
        if hasattr(self, 'game_over_overlay'):
            self.remove_widget(self.game_over_overlay)

        for plat in list(self.platforms[1:]):
            self.remove_widget(plat)
        self.platforms = [self.platforms[0]]
        self.platforms[0].pos = (Window.width / 2 - 50, 0)
        self.platforms[0].min_x = self.platforms[0].x
        self.platforms[0].max_x = self.platforms[0].x

        self.player.pos = (Window.width / 2 - 20, self.platforms[0].top)
        self.player.velocity = [0, 0]
        self.player.reset_stats()

        self.score = 0
        self.total_height = 0
        self.score_label.text = "Score: 0"
        self.score_shadow.text = "Score: 0"
        self.highscore_label.text = f"Recorde: {self.high_score}"

        for pu in list(self.powerups):
            self.remove_widget(pu)
        self.powerups.clear()

        for e in list(self.active_effects):
            self.remove_widget(e['label'])
        self.active_effects.clear()

        for p in list(self.particles):
            self.remove_widget(p)
        self.particles.clear()

        self.generate_initial_platforms(10)
        self.game_over = False
