from kivy.uix.label import Label
import random
from src.constants import BASE_JUMP, BASE_SPEED


def activate_powerup(game, ptype: str):
    if ptype == "points":
        game.score += 300
        game.score_label.text = f"Score: {game.score}"
        game.score_shadow.text = f"Score: {game.score}"
        return

    duration = 3.0 + random.uniform(0, 2.0)

    existing = next((e for e in game.active_effects if e['type'] == ptype), None)
    if existing:
        existing['time_left'] = max(existing['time_left'], duration)
        existing['duration'] = max(existing['duration'], duration)
        existing['label'].text = f"{ptype.upper()} {int(existing['time_left'])}s"
        return

    # Cores diferentes para cada power-up
    colors = {
        "jump":   (1.0, 0.4, 1.0, 1.0),   
        "speed":  (0.3, 1.0, 1.0, 1.0),   
        "shield": (1.0, 1.0, 0.4, 1.0),   
        "points": (1.0, 1.0, 1.0, 1.0)    
    }

    color = colors.get(ptype, (1,1,1,1))

    lbl = Label(
        text=f"{ptype.upper()} {int(duration)}s",
        font_size=17,
        bold=True,
        color=color,
        size_hint=(None, None),
        size=(150, 32),
        outline_color=(0,0,0,1),
        outline_width=2
    )
    game.add_widget(lbl)

    game.active_effects.append({
        'type': ptype,
        'time_left': duration,
        'duration': duration,
        'label': lbl
    })

    game._reposition_effect_labels()


def update_active_effects(game, dt):
    to_remove = []
    for effect in game.active_effects:
        effect['time_left'] -= dt
        if effect['time_left'] <= 0:
            to_remove.append(effect)
        else:
            effect['label'].text = f"{effect['type'].upper()} {int(effect['time_left'])}s"

    for effect in to_remove:
        t = effect['type']
        if t == "jump":
            game.player.jump_strength = BASE_JUMP
        elif t == "speed":
            game.player.speed = BASE_SPEED
        elif t == "shield":
            game.player.shield = False
        game.remove_widget(effect['label'])

    game.active_effects = [e for e in game.active_effects if e not in to_remove]

    if to_remove:
        game._reposition_effect_labels()
