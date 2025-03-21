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

        # Load right arrow indicator
        self.right_arrow = self.load_right_arrow()

    def load_right_arrow(self):
        """Load right arrow indicator"""
        try:
            arrow_path = f"{INDICATORS_PATH}/right_arrow.png"
            image = pygame.image.load(arrow_path).convert_alpha()
            return pygame.transform.scale(image, ARROW_SIZE)
        except Exception as e:
            print(f"Error loading right arrow: {e}")
            # Create a placeholder
            arrow = pygame.Surface(ARROW_SIZE)
            arrow.fill(YELLOW)
            return arrow

    def update(self):
        """Update the stats screen"""
        # Check if the pet is dead
        if not self.pet.is_alive():
            return (ScreenType.GAME_OVER, None)

        # Handle joystick input
        if self.input.is_pressed("right") or self.input.is_pressed("key1"):
            # Return to main screen
            return (ScreenType.MAIN, None)

        return None

    def draw(self):
        """Draw the stats screen"""
        # Clear the screen
        self.display.clear()

        # Draw pet name and age
        name_text = f"Name: {self.pet.name}"
        name_surface = self.display.render_text(name_text, WHITE)
        name_x = (self.width - name_surface.get_width()) // 2
        name_y = 10
        self.display.screen.blit(name_surface, (name_x, name_y))

        # Draw pet age (smaller font)
        age_text = f"Age: {self.pet.get_age()}"
        age_surface = self.display.render_text(age_text, WHITE, self.display.small_font)
        age_x = (self.width - age_surface.get_width()) // 2
        age_y = name_y + name_surface.get_height() + 2
        self.display.screen.blit(age_surface, (age_x, age_y))

        # Draw stat bars
        stats = self.pet.get_stats()

        # Calculate positions
        bar_width = 70  # Increased bar width
        bar_height = 12  # Slightly taller bar

        # Determine the maximum width of stat name labels for centering
        stat_labels = []
        for stat_name in stats.keys():
            display_name = "Happy" if stat_name == "Happiness" else stat_name
            stat_labels.append(f"{display_name}:")

        # Render stat names and get their widths
        max_label_width = max(
            self.display.render_text(label, WHITE, self.display.small_font).get_width()
            for label in stat_labels
        )

        # Calculate total height of stats area
        stat_bar_spacing = 20  # Increased spacing between stats
        total_stats_height = len(stats) * bar_height + (len(stats) - 1) * stat_bar_spacing

        # Calculate starting vertical position to center stats
        stat_bar_y_start = (self.height - total_stats_height) // 2

        # Calculate starting horizontal positions
        stat_name_x = (self.width - (max_label_width + 10 + bar_width)) // 2
        stat_bar_x = stat_name_x + max_label_width + 10

        for i, (stat_name, stat_value) in enumerate(stats.items()):
            # Shorten "Happiness" if it doesn't fit
            display_name = "Happy" if stat_name == "Happiness" else stat_name

            # Draw stat name
            stat_surface = self.display.render_text(f"{display_name}:", WHITE, self.display.small_font)
            stat_y = stat_bar_y_start + i * (bar_height + stat_bar_spacing)
            self.display.screen.blit(stat_surface, (stat_name_x, stat_y))

            # Draw stat bar with more visible segments
            self.display.draw_stat_bar(
                stat_bar_x,
                stat_y,
                stat_value,
                MAX_STAT,
                bar_width,
                bar_height
            )

        # Draw right arrow indicator
        if self.right_arrow:
            arrow_x = self.width - ARROW_SIZE[0] - 5
            arrow_y = self.height // 2 - ARROW_SIZE[1] // 2
            self.display.screen.blit(self.right_arrow, (arrow_x, arrow_y))

        # Update the display
        self.display.update()  # !/usr/bin/env python3