#!/usr/bin/env python3
# MalinaPet - Screen package initialization

from enum import Enum

class ScreenType(Enum):
    """Enum for different screen types"""
    ADOPTION = 0
    MAIN = 1
    STATS = 2
    CONVERSATION = 3
    GAME_OVER = 4
