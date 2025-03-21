#!/usr/bin/env python3
# MalinaPet - Main game screen

import os
import pygame
import time
import random
from src.constants import *
from src.screens import ScreenType

class MainScreen:
    def __init__(self, display, input_handler, pet):
        self.display = display
        self.input = input_handler
        self.pet = pet

        # Screen dimensions
        self.width = self.display.width
        self.height = self.display.height

        # Load images
        self.icons = self.load_icons()
        self.arrows = self.load_arrows()
        self.mess_images = self.load_mess_images()

        # Active toolbar icon
        self.active_icon_index = 0
        # Total number of regular icons (excluding conversation)
        self.regular_icons = 4  # Eat, Sleep, Clean, Heal

        # Positions
        self.pet_pos = (self.width // 2 - PET_SIZE[0] // 2, self.height // 2)

        # Layout positions for regular toolbar icons (spread across the top)
        self.icon_positions = []

        # Calculate space between icons to spread across screen
        screen_usable_width = self.width - 10  # 5px padding on each side
        total_icon_width = self.regular_icons * ICON_SIZE[0]
        icon_spacing = (screen_usable_width - total_icon_width) // (self.regular_icons - 1)

        # Position the regular icons across the top
        for i in range(self.regular_icons):
            x = 5 + i * (ICON_SIZE[0] + icon_spacing)
            y = 5  # Top padding
            self.icon_positions.append((x, y))

        # Position for conversation icon - center bottom of light bulb
        self.conversation_icon_pos = (self.width // 2 - ICON_SIZE[0] // 2,
                                      self.icon_positions[0][1] + ICON_SIZE[1] + 10)

        # Indicator flags
        self.show_left_arrow = True  # Always show stats arrow
        self.show_up_arrow = False  # Only show when conversation available

        # Happiness threshold for conversation
        self.conversation_threshold = 80

    def load_icons(self):
        """Load toolbar icons"""
        # We'll load the regular icons first, then conversation icon separately
        regular_icon_files = ["Eat.png", "Sleep.png", "Clean.png", "Heal.png"]
        conversation_icon_file = "Conversation.png"
        icons = []

        # Load regular icons
        for file in regular_icon_files:
            path = os.path.join(ICONS_PATH, file)
            try:
                image = pygame.image.load(path).convert_alpha()
                image = pygame.transform.scale(image, ICON_SIZE)
                icons.append(image)
            except Exception as e:
                print(f"Error loading icon {path}: {e}")
                # Create a placeholder
                image = pygame.Surface(ICON_SIZE)
                image.fill(RED)  # Red for error
                icons.append(image)

        # Load conversation icon
        path = os.path.join(ICONS_PATH, conversation_icon_file)
        try:
            conversation_image = pygame.image.load(path).convert_alpha()
            conversation_image = pygame.transform.scale(conversation_image, ICON_SIZE)
            self.conversation_icon = conversation_image
        except Exception as e:
            print(f"Error loading conversation icon {path}: {e}")
            # Create a placeholder
            self.conversation_icon = pygame.Surface(ICON_SIZE)
            self.conversation_icon.fill(YELLOW)  # Yellow for conversation

        return icons
        
    def load_arrows(self):
        """Load arrow indicators"""
        arrow_files = ["left_arrow.png", "right_arrow.png", "up_arrow.png", "down_arrow.png"]
        arrows = {}
        
        for file in arrow_files:
            direction = file.split("_")[0]
            path = os.path.join(INDICATORS_PATH, file)
            try:
                image = pygame.image.load(path).convert_alpha()
                image = pygame.transform.scale(image, ARROW_SIZE)
                arrows[direction] = image
            except Exception as e:
                print(f"Error loading arrow {path}: {e}")
                # Create a placeholder
                image = pygame.Surface(ARROW_SIZE)
                image.fill(YELLOW)  # Yellow for arrows
                arrows[direction] = image
                
        return arrows
        
    def load_mess_images(self):
        """Load mess images"""
        mess_files = {"poop": "poop.png", "can": "can.png"}
        mess_images = {}
        
        for mess_type, file in mess_files.items():
            path = os.path.join(MESS_PATH, file)
            try:
                image = pygame.image.load(path).convert_alpha()
                image = pygame.transform.scale(image, MESS_SIZE)
                mess_images[mess_type] = image
            except Exception as e:
                print(f"Error loading mess image {path}: {e}")
                # Create a placeholder
                image = pygame.Surface(MESS_SIZE)
                image.fill(BROWN if mess_type == "poop" else GRAY)
                mess_images[mess_type] = image
                
        return mess_images

    def update(self):
        """Update the main screen"""
        # Update pet
        self.pet.update()

        # Check if pet is dead
        if not self.pet.is_alive():
            return (ScreenType.GAME_OVER, None)

        # Handle joystick input
        if self.input.is_pressed("left"):
            # Go to stats screen
            return (ScreenType.STATS, None)

        if self.input.is_pressed("up") and self.show_up_arrow:
            # Go to conversation screen if happiness is low enough
            if self.pet.stats[STAT_HAPPINESS] < self.conversation_threshold:
                return (ScreenType.CONVERSATION, None)

        # Navigate between toolbar icons
        if self.input.is_pressed("right"):
            # Move to next icon
            self.active_icon_index = (self.active_icon_index + 1) % self.regular_icons

        if self.input.is_pressed("left"):
            # Move to previous icon
            self.active_icon_index = (self.active_icon_index - 1) % self.regular_icons

        # Handle icon activation
        if self.input.is_pressed("press") or self.input.is_pressed("key1"):
            # Activate the current icon
            if self.active_icon_index == 0:  # Eat
                self.pet.eat()
            elif self.active_icon_index == 1:  # Sleep
                if self.pet.state == STATE_SLEEPING:
                    self.pet.wake()
                else:
                    self.pet.sleep()
            elif self.active_icon_index == 2:  # Clean
                self.pet.clean()
            elif self.active_icon_index == 3:  # Heal
                self.pet.heal()

        # Update conversation need status based on happiness
        self.pet.needs_conversation = self.pet.stats[STAT_HAPPINESS] < self.conversation_threshold

        # Update arrow visibility
        self.show_up_arrow = self.pet.needs_conversation

        return None

    def draw(self):
        """Draw the main screen"""
        # Clear the screen
        self.display.clear()

        # Draw pet
        self.pet.draw(self.display.screen, self.pet_pos[0], self.pet_pos[1])

        # Draw messes
        for i, (x, y) in enumerate(self.pet.mess_positions):
            mess_type = self.pet.mess_types[i]
            mess_image = self.mess_images.get(mess_type, self.mess_images["poop"])  # Default to poop if type not found
            self.display.screen.blit(mess_image, (x, y))

        # Draw toolbar icons (spread across the top)
        for i, (x, y) in enumerate(self.icon_positions):
            # Draw icon
            self.display.screen.blit(self.icons[i], (x, y))

            # Draw highlight around active icon
            if i == self.active_icon_index:
                pygame.draw.rect(self.display.screen, WHITE,
                                 (x - 2, y - 2, ICON_SIZE[0] + 4, ICON_SIZE[1] + 4), 1)

        # Draw conversation icon if happiness is low enough
        if self.pet.needs_conversation:
            self.display.screen.blit(self.conversation_icon, self.conversation_icon_pos)

        # Draw indicators
        if self.show_left_arrow and "left" in self.arrows:
            arrow_x = 5
            arrow_y = self.height // 2 - ARROW_SIZE[1] // 2
            self.display.screen.blit(self.arrows["left"], (arrow_x, arrow_y))

        if self.show_up_arrow and "up" in self.arrows:
            arrow_x = self.width // 2 - ARROW_SIZE[0] // 2
            arrow_y = self.conversation_icon_pos[1] + ICON_SIZE[1] + 5  # Below conversation icon
            self.display.screen.blit(self.arrows["up"], (arrow_x, arrow_y))

        # Draw pet needs indicators
        need_y = self.height - 15
        if self.pet.needs_feeding:
            text = "Hungry!"
            text_surface = self.display.render_text(text, RED, self.display.small_font)
            self.display.screen.blit(text_surface, (5, need_y))

        if self.pet.needs_healing:
            text = "Sick!"
            text_surface = self.display.render_text(text, RED, self.display.small_font)
            text_x = self.width - text_surface.get_width() - 5
            self.display.screen.blit(text_surface, (text_x, need_y))

        # Draw pet state indicators if needed
        if self.pet.state == STATE_SLEEPING:
            text = "Zzz..."
            text_surface = self.display.render_text(text, BLUE, self.display.small_font)
            text_x = self.pet_pos[0] + PET_SIZE[0] - text_surface.get_width() // 2
            text_y = self.pet_pos[1] - text_surface.get_height() - 5
            self.display.screen.blit(text_surface, (text_x, text_y))

        # Update the display
        self.display.update()
