#!/usr/bin/env python3
# MalinaPet - Conversation screen

import pygame
import time
from src.constants import *
from src.screens import ScreenType


class ConversationScreen:
    def __init__(self, display, input_handler, pet, ai_handler):
        self.display = display
        self.input = input_handler
        self.pet = pet
        self.ai_handler = ai_handler

        # Screen dimensions
        self.width = self.display.width
        self.height = self.display.height

        # Speech bubble dimensions (increased size)
        self.bubble_width = self.width - 20  # Wider bubble with margins
        self.bubble_height = 40  # Taller bubble

        # Calculate positions
        self.pet_pos = (self.width // 2 - PET_SIZE[0] // 2,
                        self.height - PET_SIZE[1] - 25)  # Slightly higher to make room for bubble and arrow

        self.bubble_pos = (10,  # Left margin
                           self.pet_pos[1] - self.bubble_height - 10)  # Above pet with some padding

        # Load down arrow
        self.down_arrow = self.load_down_arrow()

        # Generate conversation text
        self.conversation_text = self.ai_handler.generate_fun_fact(
            self.pet.pet_type,
            self.pet.name
        )

        # Remember the time we started
        self.start_time = time.time()

    def load_down_arrow(self):
        """Load down arrow indicator"""
        try:
            arrow_path = f"{INDICATORS_PATH}/down_arrow.png"
            image = pygame.image.load(arrow_path).convert_alpha()
            return pygame.transform.scale(image, ARROW_SIZE)
        except Exception as e:
            print(f"Error loading down arrow: {e}")
            # Create a placeholder
            arrow = pygame.Surface(ARROW_SIZE)
            arrow.fill(YELLOW)
            return arrow

    def update(self):
        """Update the conversation screen"""
        # Check if pet is playing
        self.pet.play()

        # Handle joystick input
        if self.input.is_pressed("down") or self.input.is_pressed("key1"):
            # Return to main screen
            return (ScreenType.MAIN, None)

        # Check if conversation should time out
        if time.time() - self.start_time > 10:  # 10 seconds timeout
            return (ScreenType.MAIN, None)

        return None

    def draw(self):
        """Draw the conversation screen"""
        # Clear the screen
        self.display.clear()

        # Draw pet
        self.pet.draw(self.display.screen, self.pet_pos[0], self.pet_pos[1])

        # Draw speech bubble
        pygame.draw.rect(
            self.display.screen,
            WHITE,
            (self.bubble_pos[0], self.bubble_pos[1],
             self.bubble_width, self.bubble_height),
            1  # border width
        )

        # Calculate text area slightly smaller than bubble
        text_width = self.bubble_width - 10  # 5px padding on each side
        text_height = self.bubble_height - 10  # 5px padding on each side
        text_x = self.bubble_pos[0] + 5
        text_y = self.bubble_pos[1] + 5

        # Render text with wrapping
        text_surface = self.display.render_text(
            self.conversation_text,
            WHITE,
            self.display.small_font,
            max_width=text_width
        )

        # Blit text to screen
        self.display.screen.blit(text_surface, (text_x, text_y))

        # Draw down arrow indicator at the bottom of the screen
        if self.down_arrow:
            arrow_x = self.width // 2 - ARROW_SIZE[0] // 2
            arrow_y = self.height - ARROW_SIZE[1] - 5  # 5px from bottom
            self.display.screen.blit(self.down_arrow, (arrow_x, arrow_y))

        # Draw instruction
        instruction_text = "Press down to return"
        instruction_surface = self.display.render_text(instruction_text, WHITE, self.display.small_font)
        instruction_x = (self.width - instruction_surface.get_width()) // 2
        instruction_y = arrow_y - instruction_surface.get_height() - 2
        self.display.screen.blit(instruction_surface, (instruction_x, instruction_y))

        # Update the display
        self.display.update()