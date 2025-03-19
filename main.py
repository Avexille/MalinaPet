#!/usr/bin/env python3
# MalinaPet - Main entry point

import os
import sys
import time
import pygame
import RPi.GPIO as GPIO

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import game modules
from src.constants import *
from src.display import Display
from src.input import InputHandler
from src.ai_integration import AIHandler
from src.config import Config
from src.pet import Pet
from src.screens import ScreenType
from src.screens.adoption import AdoptionScreen
from src.screens.main_screen import MainScreen
from src.screens.stats_screen import StatsScreen
from src.screens.conversation import ConversationScreen
from src.screens.game_over import GameOverScreen

def main():
    print("Starting MalinaPet...")
    
    # Initialize configuration
    config = Config()
    
    # Initialize display
    display = Display()
    screen = display.initialize()
    
    # Initialize input handler
    input_handler = InputHandler()
    
    # Initialize AI handler
    api_key = config.get("openai_api_key", "")
    ai_handler = AIHandler(api_key)
    
    # Game state
    running = True
    current_screen_type = ScreenType.ADOPTION
    pet = None
    current_screen = None
    
    # Create assets directory if it doesn't exist
    os.makedirs(ASSETS_PATH, exist_ok=True)
    os.makedirs(PETS_PATH, exist_ok=True)
    os.makedirs(ICONS_PATH, exist_ok=True)
    os.makedirs(INDICATORS_PATH, exist_ok=True)
    os.makedirs(MESS_PATH, exist_ok=True)
    os.makedirs(GAME_OVER_PATH, exist_ok=True)
    os.makedirs(FONTS_PATH, exist_ok=True)
    
    # Main game loop
    try:
        while running:
            # Process inputs and events
            running = input_handler.update()
            
            # Initialize/switch screens if necessary
            if current_screen is None:
                if current_screen_type == ScreenType.ADOPTION:
                    current_screen = AdoptionScreen(display, input_handler, ai_handler)
                elif current_screen_type == ScreenType.MAIN:
                    current_screen = MainScreen(display, input_handler, pet)
                elif current_screen_type == ScreenType.STATS:
                    current_screen = StatsScreen(display, input_handler, pet)
                elif current_screen_type == ScreenType.CONVERSATION:
                    current_screen = ConversationScreen(display, input_handler, pet, ai_handler)
                elif current_screen_type == ScreenType.GAME_OVER:
                    current_screen = GameOverScreen(display, input_handler, pet)
            
            # Update current screen
            result = current_screen.update()
            
            # Handle screen transitions
            if result is not None:
                next_screen_type, data = result
                
                if next_screen_type == ScreenType.ADOPTION:
                    # Reset pet
                    pet = None
                elif next_screen_type == ScreenType.MAIN:
                    # If coming from adoption screen, set the new pet
                    if current_screen_type == ScreenType.ADOPTION and data is not None:
                        pet = data
                        
                # Switch to the new screen
                current_screen_type = next_screen_type
                current_screen = None
            else:
                # Draw current screen
                current_screen.draw()
            
            # Small delay to prevent maxing out CPU
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        print("Game terminated by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        print("Cleaning up...")
        input_handler.cleanup()
        pygame.quit()
        print("MalinaPet terminated")

if __name__ == "__main__":
    main()
