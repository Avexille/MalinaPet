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
        self.debounce_time = 300  # Increased from 200 to 300 milliseconds for better stability
        self.last_pressed = {button: 0 for button in self.button_states}

        # Keep track of when buttons were released to prevent multiple rapid presses
        self.last_released = {button: 0 for button in self.button_states}
        self.release_delay = 100  # Milliseconds to wait after release before accepting new press
        
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
            button_pressed = GPIO.input(pin) == 0  # Active low logic

            # Button is currently not active in our state
            if not self.button_states[button_name]:
                # Check if button is physically pressed
                if button_pressed:
                    # Check if enough time passed since last press and release
                    if ((current_time - self.last_pressed[button_name]) > self.debounce_time and
                            (current_time - self.last_released[button_name]) > self.release_delay):
                        # Activate button
                        self.button_states[button_name] = True
                        self.last_pressed[button_name] = current_time
                        return True
            # Button is currently active in our state but physically released
            elif not button_pressed:
                # Deactivate button
                self.button_states[button_name] = False
                self.last_released[button_name] = current_time

            return False

        # Check all buttons with improved debouncing
        check_button(KEY_UP_PIN, "up")
        check_button(KEY_DOWN_PIN, "down")
        check_button(KEY_LEFT_PIN, "left")
        check_button(KEY_RIGHT_PIN, "right")
        check_button(KEY_PRESS_PIN, "press")
        check_button(KEY1_PIN, "key1")
        check_button(KEY2_PIN, "key2")
        check_button(KEY3_PIN, "key3")

        # Check for KEY3 to exit the game
        if self.button_states["key3"]:
            print("KEY3 pressed - exiting game")
            return False

        return True
        
    def is_pressed(self, button):
        """Check if a button is pressed"""
        return self.button_states.get(button, False)
        
    def get_input_state(self):
        """Get a copy of the current button states"""
        return self.button_states.copy()
