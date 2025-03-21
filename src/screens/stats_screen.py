#!/usr/bin/env python3
# MalinaPet - Stats screen

import pygame
from src.constants import *
from src.screens import ScreenType

class StatsScreen:
    def __init__(self, display, input_handler, pet):
        self.display = display
        self.input = input_handler
        self.pet = pet
        
        # Screen dimensions
        self.width = self.display.width
        self.height = self.display.height
        
        # Load left arrow indicator
        self.left_arrow = self.load_left_arrow()
        
    def load_left_arrow(self):
        """Load left arrow indicator"""
        try:
            arrow_path = f"{INDICATORS_PATH}/left_arrow.png"
            image = pygame.image.load(arrow_path).convert_alpha()
            return pygame.transform.scale(image, ARROW_SIZE)
        except Exception as e:
            print(f"Error loading left arrow: {e}")
            # Create a placeholder
            arrow = pygame.Surface(ARROW_SIZE)
            arrow.fill(YELLOW)
            return arrow

    def update(self):
        """Update the stats screen"""
        # Check if the pet is dead
        if not self.pet.is_alive():
            return (ScreenType.GAME_OVER, None)

        # Handle joystick input - now using RIGHT to return to main screen
        if self.input.is_pressed("right") or self.input.is_pressed("key1"):
            # Return to main screen
            print("Returning to main screen from stats")
            return (ScreenType.MAIN, None)

        return None
        
    def draw(self):
        """Draw the stats screen"""
        # Clear the screen
        self.display.clear()
        
        # Draw title
        title_text = "Pet Stats"
        title_surface = self.display.render_text(title_text, WHITE)
        title_x = (self.width - title_surface.get_width()) // 2
        self.display.screen.blit(title_surface, (title_x, 5))
        
        # Draw pet name
        name_text = f"Name: {self.pet.name}"
        name_surface = self.display.render_text(name_text, WHITE)
        name_x = (self.width - name_surface.get_width()) // 2
        self.display.screen.blit(name_surface, (name_x, 25))
        
        # Draw pet age
        age_text = f"Age: {self.pet.get_age()}"
        age_surface = self.display.render_text(age_text, WHITE)
        age_x = (self.width - age_surface.get_width()) // 2
        self.display.screen.blit(age_surface, (age_x, 40))
        
        # Draw stat bars
        stats = self.pet.get_stats()
        
        # Calculate positions
        stat_bar_x = (self.width - STAT_BAR_SIZE[0]) // 2
        stat_bar_y_start = 60
        stat_bar_spacing = 20
        
        for i, (stat_name, stat_value) in enumerate(stats.items()):
            # Draw stat name
            stat_text = f"{stat_name}: "
            stat_surface = self.display.render_text(stat_text, WHITE)
            stat_x = stat_bar_x - stat_surface.get_width() - 5
            stat_y = stat_bar_y_start + i * stat_bar_spacing
            self.display.screen.blit(stat_surface, (stat_x, stat_y))
            
            # Draw stat bar
            bar_y = stat_y
            self.display.draw_stat_bar(
                stat_bar_x, 
                bar_y, 
                stat_value, 
                MAX_STAT,
                STAT_BAR_SIZE[0],
                STAT_BAR_SIZE[1]
            )
            
            # Draw stat value
            value_text = f"{stat_value}%"
            value_surface = self.display.render_text(value_text, WHITE, self.display.small_font)
            value_x = stat_bar_x + STAT_BAR_SIZE[0] + 5
            value_y = stat_y
            self.display.screen.blit(value_surface, (value_x, value_y))
            
        # Draw left arrow indicator
        if self.left_arrow:
            arrow_x = 5
            arrow_y = self.height // 2 - ARROW_SIZE[1] // 2
            self.display.screen.blit(self.left_arrow, (arrow_x, arrow_y))

            # Draw instruction
            instruction_text = "Press right to return"
            instruction_surface = self.display.render_text(instruction_text, WHITE, self.display.small_font)
            instruction_x = (self.width - instruction_surface.get_width()) // 2
            instruction_y = self.height - instruction_surface.get_height() - 5
            self.display.screen.blit(instruction_surface, (instruction_x, instruction_y))
        
        # Update the display
        self.display.update()