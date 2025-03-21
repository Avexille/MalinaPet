#!/usr/bin/env python3
# MalinaPet - Constants and configuration

# Screen dimensions for 1.44inch LCD HAT
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 128

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)

# Game speeds
FPS = 30
STATS_DECREASE_INTERVAL = 60  # seconds between stat decreases

# Pet constants
PET_SIZE = (64, 64)  # Pet image size
MESS_SIZE = (25, 25)  # Mess image size
ICON_SIZE = (30, 30)  # Menu icon size
ARROW_SIZE = (20, 20)  # Direction arrow size
STAT_BAR_SIZE = (50, 10)  # Size of the stat bars

# Button GPIO pins (for Waveshare 1.44inch LCD HAT)
KEY_UP_PIN     = 6 
KEY_DOWN_PIN   = 19
KEY_LEFT_PIN   = 5
KEY_RIGHT_PIN  = 26
KEY_PRESS_PIN  = 13  # Joystick press
KEY1_PIN       = 21
KEY2_PIN       = 20
KEY3_PIN       = 16

# Pet types
PET_TYPES = ["Cat", "Rat", "Raccoon", "Froggy", "Chicken", "Mario"]

# Pet stats
MAX_STAT = 100
MIN_STAT = 0
STAT_DECREASE_AMOUNT = 5

# Pet state constants
STATE_NORMAL = "normal"
STATE_EATING = "eating"
STATE_SLEEPING = "sleeping"
STATE_SICK = "sick"
STATE_DEAD = "dead"

# Stat names
STAT_HUNGER = "Hunger"
STAT_HAPPINESS = "Happiness"
STAT_ENERGY = "Energy"
STAT_HEALTH = "Health"

# Time constants
MILLISECONDS_PER_HOUR = 3600000
HOURS_PER_DAY = 24

# Paths
ASSETS_PATH = "/home/anna/Desktop/MalinaPet/assets"
PETS_PATH = f"{ASSETS_PATH}/pets"
ICONS_PATH = f"{ASSETS_PATH}/icons"
INDICATORS_PATH = f"{ASSETS_PATH}/indicators"
MESS_PATH = f"{ASSETS_PATH}/mess"
GAME_OVER_PATH = f"{ASSETS_PATH}/game_over"
FONTS_PATH = f"{ASSETS_PATH}/fonts"

# OpenAI API configuration
DEFAULT_AI_MODEL = "gpt-3.5-turbo"
