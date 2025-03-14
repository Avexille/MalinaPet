"""
PiPet - Configuration settings
"""
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "saves")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

# Display settings
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 128
REFRESH_RATE = 30  # frames per second

# Game settings
PET_AGING_RATE = 1  # hours of real time = 1 day for pet
HUNGER_DECREASE_RATE = 5  # points per hour
HAPPINESS_DECREASE_RATE = 7  # points per hour
ENERGY_DECREASE_RATE = 3  # points per hour
HEALTH_DECREASE_RATE = 1  # points per hour

# Pet limits
MAX_HUNGER = 100
MAX_HAPPINESS = 100
MAX_ENERGY = 100
MAX_HEALTH = 100

# AI integration
AI_ENABLED = True  # Set to False to disable AI features if offline
AI_MODEL_ENDPOINT = "http://localhost:5000/generate"  # Local endpoint or cloud API

# Hardware settings
BUTTON_KEY1 = 21
BUTTON_KEY2 = 20
BUTTON_KEY3 = 16
BUTTON_JOYSTICK_UP = 6
BUTTON_JOYSTICK_DOWN = 19
BUTTON_JOYSTICK_LEFT = 5
BUTTON_JOYSTICK_RIGHT = 26
BUTTON_JOYSTICK_PRESS = 13

# Battery settings
BATTERY_LOW_THRESHOLD = 20  # percentage
BATTERY_CRITICAL_THRESHOLD = 10  # percentage

# Create directories if they don't exist
os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(SPRITES_DIR, exist_ok=True)
os.makedirs(FONTS_DIR, exist_ok=True)
