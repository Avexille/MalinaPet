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
        
        # Button positions and sizes
        self.button_width = 50
        self.button_height = 20
        self.ai_button_width = 118
        self.ai_button_height = 20
        
        # Calculate button positions
        self.screen_center_x = self.display.width // 2
        self.screen_center_y = self.display.height // 2
        
        # The number of standard pet buttons
        self.num_pet_buttons = len(PET_TYPES) + 1  # +1 for random
        
        # The standard buttons are arranged in rows
        self.buttons_per_row = 2
        self.num_rows = (self.num_pet_buttons + self.buttons_per_row - 1) // self.buttons_per_row
        
        # Calculate the total height needed for all buttons
        total_button_height = self.num_rows * self.button_height + (self.num_rows - 1) * 5  # 5px spacing
        if self.ai_handler.is_available:
            total_button_height += self.ai_button_height + 5  # Add AI button height
            
        # Start Y position for the first row of buttons
        self.start_y = self.screen_center_y - total_button_height // 2
        
        # Define button positions and data
        self.buttons = []
        
        # Add pet type buttons
        for i, pet_type in enumerate(PET_TYPES):
            row = i // self.buttons_per_row
            col = i % self.buttons_per_row
            
            x = self.screen_center_x - self.button_width - 5 + col * (self.button_width + 10)
            y = self.start_y + row * (self.button_height + 5)
            
            self.buttons.append({
                "rect": pygame.Rect(x, y, self.button_width, self.button_height),
                "text": pet_type,
                "type": pet_type,
                "ai": False
            })
            
        # Add random pet button
        row = len(PET_TYPES) // self.buttons_per_row
        col = len(PET_TYPES) % self.buttons_per_row
        
        x = self.screen_center_x - self.button_width - 5 + col * (self.button_width + 10)
        y = self.start_y + row * (self.button_height + 5)
        
        self.buttons.append({
            "rect": pygame.Rect(x, y, self.button_width, self.button_height),
            "text": "?",
            "type": "random",
            "ai": False
        })
        
        # Add AI generated pet button if available
        if self.ai_handler.is_available:
            ai_button_y = self.start_y + self.num_rows * (self.button_height + 5)
            self.buttons.append({
                "rect": pygame.Rect(
                    self.screen_center_x - self.ai_button_width // 2,
                    ai_button_y,
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
            
            # Draw pet image for pet type buttons (except random and AI)
            if button["type"] not in ["random", "ai"] and button["type"] in self.pet_images:
                image = self.pet_images[button["type"]]
                image_x = button["rect"].x + (button["rect"].width - image.get_width()) // 2
                image_y = button["rect"].y - image.get_height() - 5
                self.display.screen.blit(image, (image_x, image_y))
        
        # Show instructions at the bottom
        instructions = "Use joystick to select, press to adopt"
        instruction_surface = self.display.render_text(instructions, WHITE, self.display.small_font)
        instruction_x = (self.display.width - instruction_surface.get_width()) // 2
        instruction_y = self.display.height - instruction_surface.get_height() - 5
        self.display.screen.blit(instruction_surface, (instruction_x, instruction_y))
        
        # Update the display
        self.display.update()
