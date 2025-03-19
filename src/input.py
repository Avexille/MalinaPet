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
        
        # Debounce timers
        self.debounce_time = 200  # Milliseconds
        self.last_pressed = {button: 0 for button in self.button_states}
        
    def cleanup(self):
        """Clean up GPIO resources"""
        GPIO.cleanup()
        
    def update(self):
        """Update button states and handle events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        
        current_time = pygame.time.get_ticks()
        
        # Check joystick up
        if GPIO.input(KEY_UP_PIN) == 0:  # Active low logic
            if not self.button_states["up"] and (current_time - self.last_pressed["up"]) > self.debounce_time:
                self.button_states["up"] = True
                self.last_pressed["up"] = current_time
        else:
            self.button_states["up"] = False
            
        # Check joystick down
        if GPIO.input(KEY_DOWN_PIN) == 0:
            if not self.button_states["down"] and (current_time - self.last_pressed["down"]) > self.debounce_time:
                self.button_states["down"] = True
                self.last_pressed["down"] = current_time
        else:
            self.button_states["down"] = False
            
        # Check joystick left
        if GPIO.input(KEY_LEFT_PIN) == 0:
            if not self.button_states["left"] and (current_time - self.last_pressed["left"]) > self.debounce_time:
                self.button_states["left"] = True
                self.last_pressed["left"] = current_time
        else:
            self.button_states["left"] = False
            
        # Check joystick right
        if GPIO.input(KEY_RIGHT_PIN) == 0:
            if not self.button_states["right"] and (current_time - self.last_pressed["right"]) > self.debounce_time:
                self.button_states["right"] = True
                self.last_pressed["right"] = current_time
        else:
            self.button_states["right"] = False
            
        # Check joystick press
        if GPIO.input(KEY_PRESS_PIN) == 0:
            if not self.button_states["press"] and (current_time - self.last_pressed["press"]) > self.debounce_time:
                self.button_states["press"] = True
                self.last_pressed["press"] = current_time
        else:
            self.button_states["press"] = False
            
        # Check key1
        if GPIO.input(KEY1_PIN) == 0:
            if not self.button_states["key1"] and (current_time - self.last_pressed["key1"]) > self.debounce_time:
                self.button_states["key1"] = True
                self.last_pressed["key1"] = current_time
        else:
            self.button_states["key1"] = False
            
        # Check key2
        if GPIO.input(KEY2_PIN) == 0:
            if not self.button_states["key2"] and (current_time - self.last_pressed["key2"]) > self.debounce_time:
                self.button_states["key2"] = True
                self.last_pressed["key2"] = current_time
        else:
            self.button_states["key2"] = False
            
        # Check key3
        if GPIO.input(KEY3_PIN) == 0:
            if not self.button_states["key3"] and (current_time - self.last_pressed["key3"]) > self.debounce_time:
                self.button_states["key3"] = True
                self.last_pressed["key3"] = current_time
        else:
            self.button_states["key3"] = False
            
        return True
        
    def is_pressed(self, button):
        """Check if a button is pressed"""
        return self.button_states.get(button, False)
        
    def get_input_state(self):
        """Get a copy of the current button states"""
        return self.button_states.copy()
