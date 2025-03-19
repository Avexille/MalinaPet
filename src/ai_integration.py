#!/usr/bin/env python3
# MalinaPet - OpenAI API integration

import os
import time
import random
import openai
from src.constants import *

class AIHandler:
    def __init__(self, api_key=None):
        # Initialize OpenAI API
        self.api_key = api_key
        self.is_available = False
        self.last_check_time = 0
        self.check_interval = 60  # Check internet connection every 60 seconds
        
        # Predefined offline responses
        self.offline_facts = [
            "Did you know that cats sleep for about 70% of their lives?",
            "The world's oldest known pet was a tortoise that lived to be 188 years old!",
            "Hamsters' teeth never stop growing throughout their lives.",
            "Rabbits can't vomit.",
            "Parrots can live up to 80 years!",
            "Dogs' nose prints are as unique as human fingerprints.",
            "Cats can make over 100 vocal sounds, while dogs can only make about 10.",
            "A group of ferrets is called a 'business'.",
            "Guinea pigs can see behind themselves without turning their heads.",
            "Goldfish have a memory span of up to 3 months, not just a few seconds.",
            "Snakes don't have eyelids, so they sleep with their eyes open.",
            "A frog's tongue can be up to a third of the length of its body.",
            "Some birds can recognize themselves in mirrors!",
            "A turtle's shell is actually part of its skeleton.",
            "Rats laugh when they're tickled!"
        ]
        self.offline_jokes = [
            "Why don't cats play poker in the jungle? Too many cheetahs!",
            "What do you call a cold pet? A chili dog!",
            "Why did the fish blush? Because it saw the ocean's bottom!",
            "What do you call a dog magician? A labracadabrador!",
            "Why was the cat sitting on the computer? To keep an eye on the mouse!",
            "What do you call a rabbit with fleas? Bugs Bunny!",
            "How do you make an octopus laugh? With ten-tickles!",
            "What do you call a sleeping bull? A bulldozer!",
            "What do you get when you cross a snake and a pie? A pie-thon!",
            "Why couldn't the pony sing? Because she was a little hoarse!",
            "What's a frog's favorite game? Leapfrog!",
            "Why don't snakes have friends? They're too cold-blooded!",
            "How do you count cows? With a cow-culator!",
            "What happened when the dog went to the flea circus? He stole the show!",
            "Why do fish live in salt water? Because pepper makes them sneeze!"
        ]
        
        # Try to initialize OpenAI API
        self.initialize()
        
    def initialize(self):
        """Initialize the OpenAI API with the provided key"""
        if self.api_key:
            try:
                openai.api_key = self.api_key
                # Check if we can connect to the API
                self.is_available = self._check_connection()
            except:
                self.is_available = False
        else:
            self.is_available = False
            
    def _check_connection(self):
        """Check if the internet and API connection is available"""
        current_time = time.time()
        
        # Only check connection every check_interval seconds
        if current_time - self.last_check_time < self.check_interval:
            return self.is_available
            
        self.last_check_time = current_time
        
        try:
            # Try a simple API request to check connection
            response = openai.ChatCompletion.create(
                model=DEFAULT_AI_MODEL,
                messages=[
                    {"role": "system", "content": "Just respond with 'OK' to test the connection."},
                    {"role": "user", "content": "Test connection"}
                ],
                max_tokens=10
            )
            return True
        except:
            return False
            
    def generate_pet_name(self, pet_type):
        """Generate a pet name using AI or fallback to predefined names"""
        if self.is_available:
            try:
                response = openai.ChatCompletion.create(
                    model=DEFAULT_AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a cute pet name generator. Generate a single short, cute name for a virtual pet. Just provide the name, nothing else."},
                        {"role": "user", "content": f"Generate a cute name for a {pet_type} virtual pet."}
                    ],
                    max_tokens=20
                )
                name = response.choices[0].message.content.strip()
                # Ensure the name is not too long
                if len(name) > 10:
                    name = name[:10]
                return name
            except:
                self.is_available = False
                
        # Fallback to predefined names
        prefixes = ["Pixel", "Bit", "Chip", "Nano", "Tiny", "Byte", "Spark", "Glitch", "Blip", "Dot"]
        suffixes = ["Bot", "Pet", "Friend", "Pal", "Buddy", "Mate", "Chum", "Companion", "Amigo", "Comrade"]
        
        return f"{random.choice(prefixes)}{random.choice(suffixes)}"
        
    def generate_fun_fact(self, pet_type, pet_name):
        """Generate a fun fact or joke from the pet using AI or fallback to predefined facts"""
        if self.is_available and self._check_connection():
            try:
                prompt = f"You are {pet_name}, a virtual {pet_type} pet. Share one cute, interesting, and short fun fact or joke. Keep it under 100 characters if possible. Make it fun for kids. Just provide the fun fact or joke, nothing else."
                
                response = openai.ChatCompletion.create(
                    model=DEFAULT_AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a cute virtual pet that shares interesting facts or jokes with your owner."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=150
                )
                
                fact = response.choices[0].message.content.strip()
                return fact
            except Exception as e:
                print(f"Error generating fun fact: {e}")
                self.is_available = False
                
        # Fallback to predefined facts/jokes
        if random.random() < 0.7:  # 70% chance of fact, 30% chance of joke
            return random.choice(self.offline_facts)
        else:
            return random.choice(self.offline_jokes)
            
    def generate_random_pet(self):
        """Generate a random pet type using AI or fallback to predefined pets"""
        # For now, just return a random pet from the predefined list
        # since generating images is beyond the scope of text-based AI
        return random.choice(PET_TYPES)
