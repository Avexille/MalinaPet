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

        # Import required modules for image generation
        try:
            import requests
            from PIL import Image
            self.requests = requests
            self.Image = Image
            self.image_libs_available = True
        except ImportError:
            print("Warning: requests and/or PIL libraries not available. Image generation will be disabled.")
            self.image_libs_available = False

        # Predefined offline responses
        self.offline_facts = [
            "The world's oldest known pet was a tortoise that lived to be 188 years old!",
            "Rabbits can't vomit.",
            "Parrots can live up to 80 years!",
            "Dogs' nose prints are as unique as human fingerprints.",
            "Cats can make over 100 vocal sounds, while dogs can only make about 10.",
            "A group of ferrets is called a 'business'.",
            "Guinea pigs can see behind themselves without turning their heads.",
            "Goldfish have a memory span of up to 3 months, not just a few seconds.",
            "Snakes don't have eyelids, so they sleep with their eyes open.",
            "A frog's tongue can be up to a third of the length of its body.",
        ]
        self.offline_jokes = [
            "Why don't cats play poker in the jungle? Too many cheetahs!",
            "What do you call a cold pet? A chili dog!",
            "Why did the fish blush? Because it saw the ocean's bottom!",
            "What do you call a dog magician? A labracadabrador!",
            "Why was the cat sitting on the computer? To keep an eye on the mouse!",
            "What do you call a rabbit with fleas? Bugs Bunny!",
            "What do you call a sleeping bull? A bulldozer!",
            "What do you get when you cross a snake and a pie? A pie-thon!",
            "How do you count cows? With a cow-culator!",
        ]

        # AI-generated pet types that we've successfully created
        self.ai_pet_types = []

        # Try to initialize OpenAI API
        self.initialize()

    def initialize(self):
        """Initialize the OpenAI API with the provided key"""
        if self.api_key:
            try:
                # We'll initialize the client when needed
                # in each API call rather than setting a global
                print("API key found, will test connection")
                self.is_available = self._check_connection()
            except Exception as e:
                print(f"Failed to initialize API: {e}")
                self.is_available = False
        else:
            print("No API key provided, AI features disabled")
            self.is_available = False

    def _check_connection(self):
        """Check if the internet and API connection is available"""
        current_time = time.time()

        # Only check connection every check_interval seconds
        if current_time - self.last_check_time < self.check_interval:
            return self.is_available

        self.last_check_time = current_time

        try:
            # Try a simple API request to check connection with new API
            from openai import OpenAI

            # Create a client instance
            client = OpenAI(api_key=self.api_key)

            # Test connection with a simple request
            response = client.chat.completions.create(
                model=DEFAULT_AI_MODEL,
                messages=[
                    {"role": "system", "content": "Just respond with 'OK' to test the connection."},
                    {"role": "user", "content": "Test connection"}
                ],
                max_tokens=10
            )
            print("API connection successful")
            return True
        except Exception as e:
            print(f"API connection failed: {e}")
            return False

    def generate_pet_name(self, pet_type):
        """Generate a pet name using AI or fallback to predefined names"""
        if self.is_available and self._check_connection():
            try:
                # Import client here to avoid issues if not installed
                from openai import OpenAI

                # Create a client instance
                client = OpenAI(api_key=self.api_key)

                # Generate name with the new API
                response = client.chat.completions.create(
                    model=DEFAULT_AI_MODEL,
                    messages=[
                        {"role": "system",
                         "content": "You are a cute pet name generator. Generate a single short, cute name for a virtual pet. Just provide the name, nothing else."},
                        {"role": "user", "content": f"Generate a cute name for a {pet_type} virtual pet."}
                    ],
                    max_tokens=20
                )

                # Extract name from response (structure is different in API v1)
                name = response.choices[0].message.content.strip()

                # Ensure the name is not too long
                if len(name) > 10:
                    name = name[:10]
                return name
            except Exception as e:
                print(f"Error generating pet name: {e}")
                self.is_available = False

        # Fallback to predefined names
        prefixes = ["Pixel", "Bit", "Chip", "Nano", "Tiny", "Byte", "Spark", "Glitch", "Blip", "Dot"]
        suffixes = ["Bot", "Pet", "Friend", "Pal", "Buddy", "Mate", "Chum", "Companion", "Amigo", "Comrade"]

        return f"{random.choice(prefixes)}{random.choice(suffixes)}"

    def generate_fun_fact(self, pet_type, pet_name):
        """Generate a fun fact or joke from the pet using AI or fallback to predefined facts"""
        if self.is_available and self._check_connection():
            try:
                from openai import OpenAI

                # Create a client instance
                client = OpenAI(api_key=self.api_key)

                prompt = f"You are {pet_name}, a virtual {pet_type} pet. Share one cute, interesting, and short fun fact or joke. Keep it under 100 characters if possible. Make it fun for kids. Only use basic ASCII characters - no emojis or special Unicode characters. Just provide the fun fact or joke, nothing else."

                response = client.chat.completions.create(
                    model=DEFAULT_AI_MODEL,
                    messages=[
                        {"role": "system",
                         "content": "You are a cute virtual pet that shares interesting facts or jokes with your owner. Only use basic ASCII characters - no emojis or special symbols."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=150
                )

                fact = response.choices[0].message.content.strip()

                # Filter out any non-ASCII characters to prevent Unicode errors
                fact = ''.join(char for char in fact if ord(char) < 128)

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
        if self.is_available and self._check_connection() and self.image_libs_available:
            try:
                # First generate a random pet type
                pet_ideas = ["Cat", "Dog", "Bird", "Dragon", "Fox", "Rabbit", "Frog", "Panda",
                             "Turtle", "Octopus", "Axolotl", "Owl", "Hamster", "Dinosaur"]
                pet_type = random.choice(pet_ideas)

                # Then generate an image with DALL-E
                print(f"Generating image for AI pet type: {pet_type}")

                # DALL-E prompt for a simple standalone pixel art pet
                prompt = f"""Generate a single small simple pixel art {pet_type} character with black background. Animal should face forward, looking at player. Only the animal should be present on the picture, nothing else, no background shading or other objects"""

                try:
                    # Import the OpenAI client
                    from openai import OpenAI

                    # Create a client instance
                    client = OpenAI(api_key=self.api_key)

                    # Call DALL-E API with new client
                    response = client.images.generate(
                        model="dall-e-3",  # Use DALL-E 3
                        prompt=prompt,
                        n=1,  # Generate 1 image
                        size="1024x1024",  # Standard size
                        response_format="url"  # Get URL to download
                    )

                    # Get image URL from the updated response structure
                    image_url = response.data[0].url

                    # Use the properly imported requests and PIL libraries
                    from io import BytesIO

                    # Download the image
                    image_response = self.requests.get(image_url)
                    image = self.Image.open(BytesIO(image_response.content))

                    # Create a new image with black background
                    black_bg = self.Image.new("RGBA", image.size, (0, 0, 0, 255))

                    # Paste the downloaded image onto the black background
                    # This ensures any transparent or checkered areas will be black
                    if image.mode == 'RGBA':
                        black_bg.paste(image, (0, 0), image)
                    else:
                        black_bg.paste(image, (0, 0))

                    # Resize to match pet size
                    black_bg = black_bg.resize((PET_SIZE[0], PET_SIZE[1]))

                    # Save the image
                    os.makedirs(PETS_PATH, exist_ok=True)
                    image_path = os.path.join(PETS_PATH, f"{pet_type}Tami.png")
                    black_bg.save(image_path)

                    print(f"Successfully created AI pet: {pet_type}")
                    return pet_type
                except Exception as e:
                    print(f"Error generating pet image with DALL-E: {e}")
            except Exception as e:
                print(f"Error in AI pet generation: {e}")
                self.is_available = False

        # Fallback to predefined pets if AI generation fails
        return random.choice(PET_TYPES)