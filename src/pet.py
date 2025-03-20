#!/usr/bin/env python3
# MalinaPet - Pet class

import os
import pygame
import time
import random
from src.constants import *


class Pet:
    def __init__(self, pet_type, name, ai_generated=False):
        self.pet_type = pet_type
        self.name = name
        self.ai_generated = ai_generated
        self.birth_time = time.time()

        # Initialize stats
        self.stats = {
            STAT_HUNGER: MAX_STAT,
            STAT_HAPPINESS: MAX_STAT,
            STAT_ENERGY: MAX_STAT,
            STAT_HEALTH: MAX_STAT
        }

        # Pet state
        self.state = STATE_NORMAL

        # Load pet image
        self.image = self.load_pet_image()

        # Mess properties
        self.mess_positions = []
        self.mess_types = []
        self.max_mess = 3

        # Stat decrease timer
        self.last_stat_decrease = time.time()

        # Need indicators
        self.needs_feeding = False
        self.needs_healing = False
        self.needs_conversation = False

        # Special event timers
        self.last_poop_time = time.time()
        self.last_conversation_time = time.time()
        self.poop_interval = random.randint(60, 120)  # 1-2 minutes between poops
        self.conversation_interval = random.randint(120, 240)  # 2-4 minutes between conversation needs

    def load_pet_image(self):
        """Load the pet image"""
        try:
            image_path = f"{PETS_PATH}/{self.pet_type}Tami.png"
            image = pygame.image.load(image_path).convert_alpha()
            return pygame.transform.scale(image, PET_SIZE)
        except Exception as e:
            print(f"Error loading pet image: {e}")
            # Create a placeholder
            image = pygame.Surface(PET_SIZE)
            image.fill(GRAY)
            return image

    def update(self):
        """Update pet state and stats"""
        current_time = time.time()

        # Decrease stats over time
        if current_time - self.last_stat_decrease > STATS_DECREASE_INTERVAL:
            self.decrease_stats()
            self.last_stat_decrease = current_time

        # Check for poop generation
        if current_time - self.last_poop_time > self.poop_interval:
            self.add_mess("poop")
            self.last_poop_time = current_time
            self.poop_interval = random.randint(60, 120)  # Reset interval

        # Check for conversation need
        if current_time - self.last_conversation_time > self.conversation_interval:
            self.needs_conversation = True

        # Update need indicators
        self.needs_feeding = self.stats[STAT_HUNGER] < 30
        self.needs_healing = self.stats[STAT_HEALTH] < 30

        # If health drops to zero, pet dies
        if self.stats[STAT_HEALTH] <= 0:
            self.state = STATE_DEAD

    def decrease_stats(self):
        """Decrease pet stats based on current state"""
        # Energy decreases faster when awake
        if self.state != STATE_SLEEPING:
            self.decrease_stat(STAT_ENERGY, STAT_DECREASE_AMOUNT)
        else:
            # Energy recovers when sleeping
            self.increase_stat(STAT_ENERGY, STAT_DECREASE_AMOUNT)

        # Hunger always decreases
        self.decrease_stat(STAT_HUNGER, STAT_DECREASE_AMOUNT)

        # Happiness decreases
        self.decrease_stat(STAT_HAPPINESS, STAT_DECREASE_AMOUNT)

        # Health decreases if hunger or happiness is low
        if self.stats[STAT_HUNGER] < 20 or self.stats[STAT_HAPPINESS] < 20:
            self.decrease_stat(STAT_HEALTH, STAT_DECREASE_AMOUNT // 2)

        # Having too much mess decreases happiness and health
        if len(self.mess_positions) >= self.max_mess:
            self.decrease_stat(STAT_HAPPINESS, STAT_DECREASE_AMOUNT)
            self.decrease_stat(STAT_HEALTH, STAT_DECREASE_AMOUNT // 2)

    def decrease_stat(self, stat, amount):
        """Decrease a stat by the given amount"""
        self.stats[stat] = max(MIN_STAT, self.stats[stat] - amount)

    def increase_stat(self, stat, amount):
        """Increase a stat by the given amount"""
        self.stats[stat] = min(MAX_STAT, self.stats[stat] + amount)

    def eat(self):
        """Feed the pet"""
        if self.state != STATE_SLEEPING:
            self.increase_stat(STAT_HUNGER, 30)
            self.increase_stat(STAT_HAPPINESS, 10)
            self.state = STATE_EATING
            # Chance to generate mess
            if random.random() < 0.3:
                self.add_mess("can")

    def sleep(self):
        """Put the pet to sleep"""
        if self.state != STATE_SLEEPING:
            self.state = STATE_SLEEPING

    def wake(self):
        """Wake the pet up"""
        if self.state == STATE_SLEEPING:
            self.state = STATE_NORMAL

    def play(self):
        """Play with the pet"""
        if self.state != STATE_SLEEPING:
            self.increase_stat(STAT_HAPPINESS, 30)
            self.decrease_stat(STAT_ENERGY, 10)
            self.needs_conversation = False
            self.last_conversation_time = time.time()
            self.conversation_interval = random.randint(120, 240)  # Reset interval

    def clean(self):
        """Clean up messes"""
        if self.mess_positions:
            self.mess_positions = []
            self.mess_types = []
            self.increase_stat(STAT_HAPPINESS, 10)

    def heal(self):
        """Heal the pet"""
        if self.state != STATE_SLEEPING:
            self.increase_stat(STAT_HEALTH, 30)
            self.state = STATE_NORMAL

    def add_mess(self, mess_type="poop"):
        """Add a mess at a random position"""
        if len(self.mess_positions) < self.max_mess:
            # Generate a random position that's not too close to the pet
            margin = 20
            x = random.randint(margin, SCREEN_WIDTH - MESS_SIZE[0] - margin)
            y = random.randint(margin, SCREEN_HEIGHT - MESS_SIZE[1] - margin)

            self.mess_positions.append((x, y))
            self.mess_types.append(mess_type)

    def draw(self, screen, x, y):
        """Draw the pet at the specified position"""
        if self.image:
            screen.blit(self.image, (x, y))
        else:
            # Draw placeholder if image is not available
            pygame.draw.rect(screen, GRAY, (x, y, PET_SIZE[0], PET_SIZE[1]))

    def is_alive(self):
        """Check if the pet is alive"""
        return self.state != STATE_DEAD

    def get_stats(self):
        """Get a copy of the pet's stats"""
        return self.stats.copy()

    def get_age(self):
        """Get the pet's age in hours or days"""
        age_seconds = time.time() - self.birth_time
        age_hours = age_seconds / 3600

        if age_hours < 24:
            return f"{int(age_hours)} hours"
        else:
            age_days = age_hours / 24
            return f"{int(age_days)} days"