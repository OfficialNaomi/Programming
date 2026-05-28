import sys
import pygame
import cv2
import numpy as np

# Initialize Pygame
pygame.init()

# SHORTS CONFIGURATION: Strict 9:16 Vertical Format
WIDTH, HEIGHT = 1000, 1920
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Binary Successor - Shorts Edition")

