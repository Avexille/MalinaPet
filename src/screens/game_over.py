#!/usr/bin/env python3
# MalinaPet - Game over screen

import pygame
import os
from src.constants import *
from src.screens import ScreenType

class GameOverScreen:
    def __init__(self, display, input_handler, pet):
        self.display = display
        self.input = input_handler
        self.pet = pet
        
        # Screen dimensions
        self.width = self.display.width
        self.height = self.display.height
        
        # Load grave image
        self.grave_image = self.load_grave_image()
        
        # Load left arrow
        self.left_arrow = self.load_left_arrow()
        
        # Calculate positions
        self.grave_pos = (self.width // 2 - PET_SIZE[0] // 2,
                          self.height // 2 - PET_SIZE[1] // 2)
                          
    def load_grave_image(self):
        """Load grave image"""
        try:
            grave_path = f"{GAME_OVER_PATH}/grave.png"
            image = pygame.image.load(grave_path).convert_alpha()
            return pygame.transform.scale(image, PET_SIZE)
        except Exception as e:
            print(f"Error loading grave image: {e}")
            # Create a placeholder
            image = pygame.Surface(PET_SIZE)
            image.fill(GRAY)
            pygame.draw.rect(image, BLACK, (0, 0, PET_SIZE[0], PET_SIZE[1]), 2)
            return image
            
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
        """Update the game over screen"""
        # Handle joystick input
        if self.input.is_pressed("key1"):
            # Start a new game
            return (ScreenType.ADOPTION, None)
            
        if self.input.is_pressed("left"):
            # Show stats screen
            return (ScreenType.STATS, None)
            
        return None
        
    def draw(self):
        """Draw the game over screen"""
        # Clear the screen
        self.display.clear()
        
        # Draw title
        title_text = "GAME OVER"
        title_surface = self.display.render_text(title_text, RED)
        title_x = (self.width - title_surface.get_width()) // 2
        self.display.screen.blit(title_surface, (title_x, 10))
        
        # Draw pet name and age
        info_text = f"{self.pet.name} lived for {self.pet.get_age()}"
        info_surface = self.display.render_text(info_text, WHITE, self.display.small_font)
        info_x = (self.width - info_surface.get_width()) // 2
        self.display.screen.blit(info_surface, (info_x, 30))
        
        # Draw grave
        if self.grave_image:
            self.display.screen.blit(self.grave_image, self.grave_pos)
            
        # Draw left arrow indicator
        if self.left_arrow:
            arrow_x = 5
            arrow_y = self.height // 2 - ARROW_SIZE[1] // 2
            self.display.screen.blit(self.left_arrow, (arrow_x, arrow_y))
            
        # Draw instructions
        instructions = [
            "Press KEY1 to adopt a new pet",
            "Press LEFT to view final stats"
        ]
        
        y_pos = self.height - 40
        for instruction in instructions:
            instruction_surface = self.display.render_text(instruction, WHITE, self.display.small_font)
            instruction_x = (self.width - instruction_surface.get_width()) // 2
            self.display.screen.blit(instruction_surface, (instruction_x, y_pos))
            y_pos += 15
            
        # Update the display
        self.display.update()
