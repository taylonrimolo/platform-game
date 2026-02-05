"""Constantes centralizadas do jogo"""

# Física e jogabilidade
GRAVITY = 0.5
BASE_SPEED = 5.0
BASE_JUMP = 15.0

# Geração de plataformas
PLATFORM_BASE_SPACING = 120
RANDOM_VERTICAL_OFFSET = 18
PLATFORM_SPEED = 2.2
MOVING_PLATFORM_CHANCE = 0.45
POWERUP_CHANCE = 0.22

# Dificuldade
DIFFICULTY_MAX_HEIGHT = 3000.0

# Cores
COLOR_NORMAL = (0.12, 0.45, 0.9)
COLOR_BOOST  = (0.14, 0.85, 0.35)
COLOR_BREAK  = (1.00, 0.85, 0.12)

PLATFORM_COLORS = {
    "normal": COLOR_NORMAL,
    "boost": COLOR_BOOST,
    "break": COLOR_BREAK
}

POWERUP_COLORS = {
    "jump":   (1, 0, 1),
    "speed":  (0, 1, 1),
    "shield": (1, 1, 0),
    "points": (1, 1, 1)
}

# Arquivos
HIGH_SCORE_FILE = "data/high_score.json"