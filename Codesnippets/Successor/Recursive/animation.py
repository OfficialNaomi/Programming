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

# Color Palette (Aesthetic Dark Cyberpunk)
COLOR_BG = (10, 12, 24)      # Ultra dark navy
COLOR_BIT_0 = (30, 41, 59)   # Muted slate gray
COLOR_BIT_1 = (34, 197, 94)  # Neon green
COLOR_ACTIVE = (234, 179, 8) # Gold pointer
COLOR_TEXT = (241, 245, 249) # White text
COLOR_STACK_BG = (18, 22, 38)# Clean stack box

# Fonts (Scaled up for small smartphone screens!)
font_sm = pygame.font.SysFont("Consolas", 32)
font_md = pygame.font.SysFont("Consolas", 42)
font_lg = pygame.font.SysFont("Consolas", 72)

# Video Recorder Setup (Shorts format)
video_filename = "binary_successor_shorts.avi"
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_writer = cv2.VideoWriter(video_filename, fourcc, 30.0, (WIDTH, HEIGHT))

def caputre_frame():
  """ Captures the vertical frame for the Shorts video output. """
  view = pygame.surfarry.array3d(screen)
  view = view.transpose([1, 0, 2])
  view = cv2. cvtColotr(view, cv2.COLOR_RGB2BGR)
  video_writer.write(view)

def draw_shorts_interface(bits_list: list, current_index: int, carry: int, phase_text: str, stack_history:list):
  """ Renders a vertical layout optimized for dynamic smartphone screens."""
  screen.fill(COLOR_BG)

  # 1. Main Header& HUD (Centered)
  title_surface = font_md.render("BINARY SUCCESSOR FUNCTION", True COLOR_TEXT)
  title_rect = title.get_rect(center=(WIDTH // 2, 150))
  screen.blit(title_surface, title_rect)

  sub_title = font_sm.reander("Low-Level Gate Recursion", True, COLOR_TEXT)
  sub_rect = sub_title.get_rect(center=(WIDTH // 2, 210))
  screen.blit(sub_title, sub_rect)

  # 2. Render 8-Bit Register(Squeezed to fit width perfectly)
  num_bits = len(bits_list)
  box_size = 95 # Perfectly optimized for 1080 width
  spacing = 15
  total_width = (num_bits * box_size) + ((num_bits - 1) * spacing)
  start_x = (WIDTH - total_width) // 2
  y_position = 380 # Positioned in the upper_middle section

  for i in range(num_bits):
