#!/usr/bin/env python3
# MalinaPet - Display initialization and management

import os
import pygame
import subprocess
from src.constants import *

class Display:
    def __init__(self):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.screen = None
        self.font = None
        self.small_font = None
        self.clock = None
        
    def initialize(self):
        """Initialize the display and pygame"""
        print("Initializing pygame...")
        pygame.init()
        self.clock = pygame.time.Clock()
        
        # Try to detect actual screen resolution
        try:
            # Use fbset to get display resolution
            output = subprocess.check_output(['fbset', '-s']).decode('utf-8')
            for line in output.split('\n'):
                if 'geometry' in line:
                    parts = line.split()
                    self.width = int(parts[1])
                    self.height = int(parts[2])
                    print(f"Detected screen resolution: {self.width}x{self.height}")
                    break
        except:
            # Default to 1.44" LCD resolution if detection fails
            print(f"Using default resolution: {self.width}x{self.height}")
        
        # Initialize the display with different drivers until one works
        print("Setting up display...")
        try:
            # Try with directfb driver first
            os.environ['SDL_VIDEODRIVER'] = 'directfb'
            pygame.display.init()
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            screen_width, screen_height = self.screen.get_size()
            print(f"Fullscreen resolution with directfb: {screen_width}x{screen_height}")
            pygame.display.set_caption("MalinaPet")
            print("DirectFB display initialized successfully")
        except Exception as e:
            print(f"DirectFB initialization failed: {e}")
            try:
                # Try with fbcon driver next
                os.environ['SDL_VIDEODRIVER'] = 'fbcon'
                pygame.display.quit()
                pygame.display.init()
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                screen_width, screen_height = self.screen.get_size()
                print(f"Fullscreen resolution with fbcon: {screen_width}x{screen_height}")
                print("FBcon display initialized successfully")
            except Exception as e:
                print(f"FBcon initialization failed: {e}")
                try:
                    # Finally try the default driver
                    os.environ.pop('SDL_VIDEODRIVER', None)
                    pygame.display.quit()
                    pygame.display.init()
                    self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
                    screen_width, screen_height = self.screen.get_size()
                    print(f"Default driver resolution: {screen_width}x{screen_height}")
                except Exception as e:
                    print(f"Default display initialization failed: {e}")
                    # Last resort - try windowed mode
                    self.screen = pygame.display.set_mode((self.width, self.height))
                    screen_width, screen_height = self.screen.get_size()
                    print(f"Windowed mode resolution: {screen_width}x{screen_height}")
        
        # Update dimensions based on actual screen size
        if screen_width != 0 and screen_height != 0:
            self.width = screen_width
            self.height = screen_height
            
        # Now that display is initialized, we can set mouse visibility
        try:
            pygame.mouse.set_visible(False)  # Hide mouse cursor
        except Exception as e:
            print(f"Could not hide mouse cursor: {e}")
            
        # Initialize fonts
        try:
            # Try to load a pixel-style font for 8-bit/16-bit look
            font_path = os.path.join(FONTS_PATH, "Qadang.ttf")
            if os.path.exists(font_path):
                self.font = pygame.font.Font(font_path, max(10, self.height // 12))
                self.small_font = pygame.font.Font(font_path, max(8, self.height // 16))
            else:
                # Fallback to default monospace font
                self.font = pygame.font.SysFont("monospace", max(10, self.height // 12))
                self.small_font = pygame.font.SysFont("monospace", max(8, self.height // 16))
        except Exception as e:
            print(f"Font initialization failed: {e}. Using default.")
            self.font = pygame.font.Font(None, max(10, self.height // 12))
            self.small_font = pygame.font.Font(None, max(8, self.height // 16))
            
        print(f"Display initialized with dimensions {self.width}x{self.height}")
        return self.screen

    def load_image(self, path, size=None):
        """Load and scale an image"""
        try:
            image = pygame.image.load(path)
            if size:
                image = pygame.transform.scale(image, size)
            return image
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            # Create a placeholder colored rectangle
            surf = pygame.Surface(size if size else (30, 30))
            surf.fill(RED)  # Red indicates missing image
            return surf
            
    def render_text(self, text, color=WHITE, font=None, max_width=None):
        """Render text with the specified font"""
        if font is None:
            font = self.font
            
        # If max_width is specified, we need to wrap the text
        if max_width:
            words = text.split(' ')
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                # Get size of the test line
                test_width, _ = font.size(test_line)
                
                if test_width <= max_width:
                    current_line.append(word)
                else:
                    # If current_line is empty, force add the word (it's too long but we have to show it)
                    if not current_line:
                        current_line.append(word)
                    
                    lines.append(' '.join(current_line))
                    current_line = [word]
            
            # Add the last line
            if current_line:
                lines.append(' '.join(current_line))
                
            # Render each line
            rendered_lines = [font.render(line, True, color) for line in lines]
            
            # Calculate total height
            line_height = rendered_lines[0].get_height()
            total_height = line_height * len(rendered_lines)
            
            # Create a surface for all lines
            text_surface = pygame.Surface((max_width, total_height), pygame.SRCALPHA)
            
            # Blit each line onto the surface
            for i, line_surface in enumerate(rendered_lines):
                text_surface.blit(line_surface, (0, i * line_height))
                
            return text_surface
        else:
            # Simple case - no wrapping needed
            return font.render(text, True, color)
            
    def draw_stat_bar(self, x, y, value, max_value=100, width=STAT_BAR_SIZE[0], height=STAT_BAR_SIZE[1], border_color=WHITE, fill_color=GREEN):
        """Draw a stat bar with the given value"""
        # Draw border
        pygame.draw.rect(self.screen, border_color, (x, y, width, height), 1)
        
        # Calculate fill width
        fill_width = int((value / max_value) * (width - 2))
        
        # Draw segments (vertical lines) for the filled part
        segment_width = (width - 2) / 10  # 10 segments for 0-100%
        
        for i in range(int(value / 10)):
            segment_x = x + 1 + int(i * segment_width)
            pygame.draw.line(self.screen, fill_color, 
                            (segment_x, y + 1), 
                            (segment_x, y + height - 2), 
                            2)

    def update(self):
        """Update the display"""
        pygame.display.flip()
        self.clock.tick(FPS)
        
    def clear(self, color=BLACK):
        """Clear the screen with the specified color"""
        self.screen.fill(color)
