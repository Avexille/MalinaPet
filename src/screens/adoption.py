#!/usr/bin/env python3
# MalinaPet - Adoption screen

import os
import pygame
from src.constants import *
from src.screens import ScreenType
from src.pet import Pet

class AdoptionScreen:
    def __init__(self, display, input_handler, ai_handler):
        self.display = display
        self.input = input_handler
        self.ai_handler = ai_handler

        # Load pet preview images (although we won't display them)
        self.pet_images = {}
        self.load_pet_images()

        # Define the allowed pet types for offline mode
        self.offline_pet_types = ["Cat", "Rat", "Raccoon"]

        # Button positions and sizes - larger buttons
        self.button_width = 75  # Slightly wider to fit "Raccoon"
        self.button_height = 30  # Taller buttons for better visibility
        self.ai_button_width = 118
        self.ai_button_height = 20

        # Calculate button positions - 2x2 grid layout
        self.buttons_per_row = 2
        button_spacing_x = 10  # Horizontal spacing between buttons
        button_spacing_y = 15  # Vertical spacing between buttons

        # Calculate total width needed for buttons in a row
        total_row_width = (self.button_width * self.buttons_per_row) + (button_spacing_x * (self.buttons_per_row - 1))

        # Calculate starting position to center the buttons
        start_x = (self.display.width - total_row_width) // 2
        start_y = 45  # Add more space below the title

        # Define button positions and data - only for offline pet types plus random
        self.buttons = []

        # Add Cat and Rat buttons (first row)
        self.buttons.append({
            "rect": pygame.Rect(start_x, start_y, self.button_width, self.button_height),
            "text": "Cat",
            "type": "Cat",
            "ai": False
        })

        self.buttons.append({
            "rect": pygame.Rect(start_x + self.button_width + button_spacing_x, start_y,
                                self.button_width, self.button_height),
            "text": "Rat",
            "type": "Rat",
            "ai": False
        })

        # Add Raccoon and ? buttons (second row)
        self.buttons.append({
            "rect": pygame.Rect(start_x, start_y + self.button_height + button_spacing_y,
                                self.button_width, self.button_height),
            "text": "Raccoon",
            "type": "Raccoon",
            "ai": False
        })

        self.buttons.append({
            "rect": pygame.Rect(start_x + self.button_width + button_spacing_x,
                                start_y + self.button_height + button_spacing_y,
                                self.button_width, self.button_height),
            "text": "?",
            "type": "random",
            "ai": False
        })

        # Add AI generated pet button at the bottom if available (for online mode)
        if self.ai_handler.is_available:
            ai_y = start_y + (self.button_height + button_spacing_y) * 2 + 10
            self.buttons.append({
                "rect": pygame.Rect(
                    (self.display.width - self.ai_button_width) // 2,  # Center horizontally
                    ai_y,
                    self.ai_button_width,
                    self.ai_button_height
                ),
                "text": "AI Generated Pet",
                "type": "ai",
                "ai": True
            })

        # Selected button
        self.selected_button_index = 0

        # Title text
        self.title_text = "Choose Your Pet"
        
    def load_pet_images(self):
        """Load pet preview images"""
        for pet_type in PET_TYPES:
            image_path = f"{PETS_PATH}/{pet_type}Tami.png"
            try:
                image = pygame.image.load(image_path).convert_alpha()
                image = pygame.transform.scale(image, (30, 30))  # Smaller preview
                self.pet_images[pet_type] = image
            except Exception as e:
                print(f"Error loading pet image {image_path}: {e}")
                # Create a placeholder
                image = pygame.Surface((30, 30))
                image.fill(GRAY)
                self.pet_images[pet_type] = image
                
    def update(self):
        """Update the adoption screen"""
        # Handle joystick input for button selection
        if self.input.is_pressed("up"):
            self.selected_button_index = (self.selected_button_index - self.buttons_per_row) % len(self.buttons)
        elif self.input.is_pressed("down"):
            self.selected_button_index = (self.selected_button_index + self.buttons_per_row) % len(self.buttons)
        elif self.input.is_pressed("left"):
            self.selected_button_index = (self.selected_button_index - 1) % len(self.buttons)
        elif self.input.is_pressed("right"):
            self.selected_button_index = (self.selected_button_index + 1) % len(self.buttons)
            
        # Check for selection
        if self.input.is_pressed("press") or self.input.is_pressed("key1"):
            selected_button = self.buttons[self.selected_button_index]
            pet_type = selected_button["type"]
            
            # Handle different pet types
            if pet_type == "random":
                # Choose a random pet type
                pet_type = PET_TYPES[pygame.time.get_ticks() % len(PET_TYPES)]
            elif pet_type == "ai":
                # Generate a random pet with AI
                pet_type = self.ai_handler.generate_random_pet()
                
            # Create the pet
            name = self.ai_handler.generate_pet_name(pet_type)
            pet = Pet(pet_type, name, selected_button["ai"])
            
            return (ScreenType.MAIN, pet)
            
        return None

    def draw(self):
        """Draw the adoption screen"""
        # Clear the screen
        self.display.clear()

        # Draw title
        title_surface = self.display.render_text(self.title_text, WHITE)
        title_x = (self.display.width - title_surface.get_width()) // 2
        self.display.screen.blit(title_surface, (title_x, 10))

        # Draw buttons
        for i, button in enumerate(self.buttons):
            # Draw button background
            color = BLUE if i == self.selected_button_index else DARK_GRAY
            pygame.draw.rect(self.display.screen, color, button["rect"])

            # Draw button border
            border_color = WHITE if i == self.selected_button_index else LIGHT_GRAY
            pygame.draw.rect(self.display.screen, border_color, button["rect"], 1)

            # Draw button text
            text_surface = self.display.render_text(button["text"], WHITE, self.display.small_font)
            text_x = button["rect"].x + (button["rect"].width - text_surface.get_width()) // 2
            text_y = button["rect"].y + (button["rect"].height - text_surface.get_height()) // 2
            self.display.screen.blit(text_surface, (text_x, text_y))

        # Show instructions at the bottom - break into two lines for better visibility
        line1 = "Use joystick to select"
        line2 = "press to adopt"

        line1_surface = self.display.render_text(line1, WHITE, self.display.small_font)
        line2_surface = self.display.render_text(line2, WHITE, self.display.small_font)

        line1_x = (self.display.width - line1_surface.get_width()) // 2
        line2_x = (self.display.width - line2_surface.get_width()) // 2

        # Position near bottom but leave enough space
        line1_y = self.display.height - line1_surface.get_height() - line2_surface.get_height() - 4
        line2_y = self.display.height - line2_surface.get_height() - 2

        self.display.screen.blit(line1_surface, (line1_x, line1_y))
        self.display.screen.blit(line2_surface, (line2_x, line2_y))

        # Update the display
        self.display.update()
