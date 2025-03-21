#!/usr/bin/env python3
# MalinaPet - Input handling (joystick and buttons)

import pygame
import RPi.GPIO as GPIO
from src.constants import *

class InputHandler:
    def __init__(self):
        # Initialize GPIO for buttons
        GPIO.setmode(GPIO.BCM)

        # Setup GPIO pins with pull-up resistors
        GPIO.setup(KEY_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY_PRESS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Initialize button states
        self.button_states = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "press": False,
            "key1": False,
            "key2": False,
            "key3": False
        }

        # Debounce timers - increase for more stability
        self.debounce_time = 400  # Increased to 400ms for more stable input
        self.last_pressed = {button: 0 for button in self.button_states}

        # Keep track of when buttons were released to prevent multiple rapid presses
        self.last_released = {button: 0 for button in self.button_states}
        self.release_delay = 150  # Milliseconds to wait after release before accepting new press

        # Store raw button states
        self.raw_states = {button: False for button in self.button_states}
        
    def cleanup(self):
        """Clean up GPIO resources"""
        GPIO.cleanup()

    def update(self):
        """Update button states and handle events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        current_time = pygame.time.get_ticks()

        # Helper function to check button state with improved debouncing
        def check_button(pin, button_name):
            # Read the current physical state - active low logic
            current_state = GPIO.input(pin) == 0
            self.raw_states[button_name] = current_state

            # If button is currently inactive in our state
            if not self.button_states[button_name]:
                # And physically pressed
                if current_state:
                    # And passed debounce/release timing checks
                    if ((current_time - self.last_pressed[button_name]) > self.debounce_time and
                            (current_time - self.last_released[button_name]) > self.release_delay):
                        # Activate button
                        self.button_states[button_name] = True
                        self.last_pressed[button_name] = current_time
                        return True
            # If button is active in our state and physically released
            elif not current_state:
                # Deactivate button
                self.button_states[button_name] = False
                self.last_released[button_name] = current_time

            return False

        # Map GPIO pins to button names
        button_map = {
            KEY_UP_PIN: "up",
            KEY_DOWN_PIN: "down",
            KEY_LEFT_PIN: "left",
            KEY_RIGHT_PIN: "right",
            KEY_PRESS_PIN: "press",
            KEY1_PIN: "key1",
            KEY2_PIN: "key2",
            KEY3_PIN: "key3"
        }

        # Check all buttons with improved debouncing
        for pin, button_name in button_map.items():
            check_button(pin, button_name)

        # Check for KEY3 to exit the game
        if self.is_pressed("key3"):
            print("KEY3 pressed - exiting game")
            return False

        return True

    def is_pressed(self, button):
        """Check if a button is pressed"""
        # Additional debug for conversation screen navigation issues
        if button == "up" and self.button_states.get(button, False):
            print(f"UP button detected as pressed: {self.button_states.get(button, False)}")

        return self.button_states.get(button, False)
        
    def get_input_state(self):
        """Get a copy of the current button states"""
        return self.button_states.copy()
