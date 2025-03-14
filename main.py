#!/usr/bin/env python3
"""
PiPet - Virtual Pet Game for Raspberry Pi Zero
Main entry point for the application
"""
import time
import sys
import RPi.GPIO as GPIO
from utils.display import Display
from utils.input import InputHandler
from utils.battery import BatteryMonitor
from pet_manager import PetManager
from screens.adoption_screen import AdoptionScreen
from screens.main_screen import MainScreen
from screens.stats_screen import StatsScreen
from screens.feeding_screen import FeedingScreen
from screens.play_screen import PlayScreen
from screens.settings_screen import SettingsScreen
import config


class PiPet:
    def __init__(self):
        """Initialize the PiPet game"""
        # Initialize hardware
        self.display = Display()
        self.input_handler = InputHandler(callback=self.handle_input)
        self.battery = BatteryMonitor()

        # Initialize game components
        self.pet_manager = PetManager()

        # Initialize screens
        self.screens = {
            'adoption': AdoptionScreen(self.display, self.pet_manager),
            'main': MainScreen(self.display, self.pet_manager),
            'stats': StatsScreen(self.display, self.pet_manager),
            'feeding': FeedingScreen(self.display, self.pet_manager),
            'play': PlayScreen(self.display, self.pet_manager),
            'settings': SettingsScreen(self.display, self.pet_manager)
        }

        # Set initial screen
        self.current_screen = 'adoption'

        # Game state
        self.running = True
        self.last_update = time.time()
        self.last_battery_check = time.time()

    def start(self):
        """Start the main game loop"""
        try:
            print("Starting PiPet...")
            self.display.init()
            self.input_handler.init()
            self.battery.init()

            # Check if there's a saved pet
            if self.pet_manager.has_saved_pet():
                self.pet_manager.load_pet()
                self.current_screen = 'main'

            # Main game loop
            while self.running:
                current_time = time.time()

                # Update the current screen
                self.screens[self.current_screen].update(current_time - self.last_update)
                self.last_update = current_time

                # Check battery status every minute
                if current_time - self.last_battery_check > 60:
                    self.check_battery()
                    self.last_battery_check = current_time

                # Small delay to reduce CPU usage
                time.sleep(0.05)

        except KeyboardInterrupt:
            print("Exiting PiPet...")
        finally:
            self.cleanup()

    def handle_input(self, key):
        """Handle input from buttons"""
        # Let the current screen handle the input
        next_screen = self.screens[self.current_screen].handle_input(key)

        # Change screen if requested
        if next_screen and next_screen in self.screens:
            self.current_screen = next_screen

    def check_battery(self):
        """Check battery level and warn if low"""
        battery_level = self.battery.get_level()

        if battery_level < config.BATTERY_LOW_THRESHOLD:
            self.display.show_low_battery_warning(battery_level)

        if battery_level < config.BATTERY_CRITICAL_THRESHOLD:
            # Auto-save and warn about critical battery
            self.pet_manager.save_pet()
            self.display.show_critical_battery_warning()

    def cleanup(self):
        """Clean up resources before exit"""
        self.pet_manager.save_pet()
        self.display.clear()
        self.input_handler.cleanup()
        GPIO.cleanup()
        print("PiPet shutdown complete")


if __name__ == "__main__":
    game = PiPet()
    game.start()