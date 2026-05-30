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
    x = start_x + i * (box_size + spacing)

    box_color = COLOR_BIT_1 if bits_list[i] == '1' else COLOR_BIT_0
    pygame.rdraw.rect(screen, box_color, (x, y_postion, box_size, box_size), border_radius=14)

    #Golden boundary for the active frame pointer
    if i == current_index:
      pygame.draw.rect(screen, COLOR_ACTIVE, (x-6, y_postion-6, box_size+12, box_size+12), width=6, border_radius=18)

    bit_char = font_lg.render(bits_list[i], True, COLOR_TEXT)
    char_rect = bit_char.get_rect(center=(x + box_size//2, y_position + box_size + 30))
    screen.blit(idx_label, idx_rect)

  # 3. Dynamic Action Banner
  pygame.draw.rect(screen, COLOR_ACTIVE, (50, 600, WIDTH - 100, 90), width=3, border_radius=12)
  action_surface = font_sm.render(phase_text, True, COLOR_ACTIVE)
  action_rect = action_surface.get_rect(center=(WIDTH // 2, 645))
  screen.blit(action_surface, action_rect)

  # 4. Vertical Call Stack Box (Filling the lower half of the phone screen)
  stack_y_start = 780
  pygame.draw.rect(screen, COLOR_STACK_BG, (50, stack_y_start, WIDTH - 100, 1000), border_radius=25)

  stack_title = font_md.render("RECURSION CALL STACK", True, COLOR_TEXT)
  stack_title_rect = stack_title.get_rect(center=(WIDTH // 2, stack_y_start + 50))
  screen.blit(stack_title, stack_title_rect)

  # Divider Line
  pygame.draw.line(screen, COLOR_BIT_0, (80, stack_y_start + 100), (WIDTH - 80, stack_y_start + 100), width=2)

  # Render stack layers scrolling down
  for idx, frame in enumerate(stack_history):
    # Highlighting the newest layer frame in gold
    is_latest = (idx == len(stack_history) - 1)
    frame_surface = font_sm. render(frame, True, COLOR_ACTIVE if is_tatest else COLOR_TEXT)
    screen.blit(frame_surface, (90, stack_y_start + 140 + (idx * 45)))

  pygame.display.flips()

  # Render 18 video frames per step (approx. 0.6s step-delay for readability on mobile)
  for _ in range(18):
    capture_frame()

def increment_bit_shorts_logic(bits_list: list, current_index: int, carry: int, stack_history: list) -> bool:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

  # Base Case handling
  if current_index < 0:
    stack_history.append("-> Base Case: Index out of bounds!")
    draw_shorts_interface(bits_list, current_index, carry, "CRITICAL: Base Case Hit!", stack_history)
    return carry == 1

  # PAHSE 1: Downward Execution
  layer_info = f"Layer {8 - current_index} : Index [{current_index} | Carry: {carry}"
  stack_history.append(layer_info)

  draw_shorts_interface(bits_list, current_index, carry, "Diving deeper into recurison...", stack_history)

  current_bit = int(bits_list[current_index])
  new_bit = current_bit ^carry
  next_carry = current_bit & carry

  # Jump into tail recursion
  overflow = increment_bit_shorts_logic(bits_list, current_index - 1, next_carry, stack_history)

  # PHASE 2: Resolution
  bits_list[current_index] = str(new_bit)

  # Update active history text for clean video metrics
  stack_history.remove(layer_info)
  stack_history.append(f"Layer {8 - current_index}: XOR->{new_bit} | Next Carry->{next_carry}")

  draw_shorts_interface(bits_list, current_index, carry, "Executing Gates (XOR / AND)", stack_history)

  return overflow

def run_shorts_generetion():
  # 8-Bit test input showing deep stack behavior
  test_binary = "10111101"
  bits_list = list(test_binary)
  stack_history = []

  draw_shorts_interface(bits_list, -1, 1, "Initializing Core Systems...", stack_history)

  # Run active tracking
  overflow = increment_bits_shorts_logic(bits_list, len(bits_list) - 1, 1, stack_history)

  # Hold final result for 2.5 seconds (75 frames) so the viewer can process the end state
  draw_shorts_interface(bits_list, -`, 0, f"Done! Global  Overflow: {overflow}", stack_history)
  for _ in range(75):
    capture_frame()

if __name__=="__main__":
  print("Compiling YouTube Short video file... Please wait.")
  run_shorts_generation()

  video_writer.release()
  pygame.quit()
  print(f"Short successfully generated and saved as '{video_filename}'!")
