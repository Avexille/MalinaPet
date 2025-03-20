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

        # Load pet preview images
        self.pet_images = {}
        self.load_pet_images()

        # Button positions and sizes - based on wireframe specs
        self.button_width = 50
        self.button_height = 20
        self.ai_button_width = 118
        self.ai_button_height = 20

        # Adjust for small screen
        screen_padding = 10  # Padding from screen edges

        # Calculate button positions - 2 columns layout
        self.buttons_per_row = 2
        button_spacing_x = 10  # Horizontal spacing between buttons
        button_spacing_y = 10  # Vertical spacing between buttons

        # Calculate total width needed for buttons in a row
        total_row_width = (self.button_width * self.buttons_per_row) + (button_spacing_x * (self.buttons_per_row - 1))

        # Calculate starting position to center the buttons
        start_x = (self.display.width - total_row_width) // 2
        start_y = 40  # Start below the title

        # Define button positions and data
        self.buttons = []

        # Add pet type buttons - 2 columns with proper spacing
        for i, pet_type in enumerate(PET_TYPES):
            row = i // self.buttons_per_row
            col = i % self.buttons_per_row

            x = start_x + col * (self.button_width + button_spacing_x)
            y = start_y + row * (self.button_height + button_spacing_y)

            self.buttons.append({
                "rect": pygame.Rect(x, y, self.button_width, self.button_height),
                "text": pet_type,
                "type": pet_type,
                "ai": False
            })

        # Add random pet button
        random_row = len(PET_TYPES) // self.buttons_per_row
        random_col = len(PET_TYPES) % self.buttons_per_row

        random_x = start_x + random_col * (self.button_width + button_spacing_x)
        random_y = start_y + random_row * (self.button_height + button_spacing_y)

        self.buttons.append({
            "rect": pygame.Rect(random_x, random_y, self.button_width, self.button_height),
            "text": "?",
            "type": "random",
            "ai": False
        })

        # Add AI generated pet button at the bottom if available
        if self.ai_handler.is_available:
            ai_y = start_y + (random_row + 1) * (self.button_height + button_spacing_y)
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

        # Show instructions at the bottom - ensure it fits on screen
        instructions = "Use joystick to select, press to adopt"
        instruction_surface = self.display.render_text(instructions, WHITE, self.display.small_font)
        instruction_x = (self.display.width - instruction_surface.get_width()) // 2
        instruction_y = self.display.height - instruction_surface.get_height() - 2  # Move closer to bottom
        self.display.screen.blit(instruction_surface, (instruction_x, instruction_y))

        # Update the display
        self.display.update()
