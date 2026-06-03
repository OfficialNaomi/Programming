import pygame
import cv2
import numpy as np

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1080, 1920
FPS = 30
VIDEO_NAME = "iterative_successor_early_exit.mp4"

# ============================================
# ========= COLOR PALE: DEEP OCEAN ===========
# ============================================
BG_COLOR = ( 7, 14, 28)
SEA_FOAM = (212, 241, 244)
BOX_BLUE = (30, 115, 175)
PROCESSED_BLUE = (15, 45, 75)
GATE_OFF = (20, 40, 60)
GATE_ON = (0, 210, 255)
HIGHLIGHT_RED = (255, 70, 90) # For the Break/Early Exit

pygame.init()
screen = pygame.Surface((WIDTH, HEIGHT ))

# --- FONTS ---
font_title = pygame.font.SysFont("Consolas", 56, bold=True)
font_sub = pygame.font.SysFont("Consolas", 28)
font_box = pygame.font.SysFont("Consolas", 52, bold=True)
font_small = pygame.font.SysFont("Consolas", 22, bold=True)
font_code = pygame.font.SysFont("Consolas", 32)
font_status = pygame.font.SysFont("Consolas", 42, bold=True)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2. VideoWriter(VIDEO_NAME, fourcc, FPS, (WIDTH, HEIGHT))

# ---  GLOBAL STATE VARIABLES ---
bits = [1, 1, 1, 1, 0, 1, 1, 1] # The '0' is at index 4. The loop will break here!
processed_flags = [False] * 8
scanner_x = 0
scanner_active = False
status_text = ""
status_color = SEA_FOAM
active_code_line = -1

# Code block for the visualization panel
code_lines = [
  "for i in range(len(bits)-1, -1, -1):",
  "    if bits[i] == 1:",
  "        bits[i] = 0",
  "    else:",
  "        bits[i] = 1",
  "        break # EARLY EXIT"
]

def get_box_x(index):
  start_x = 135
  spacing = 115
  return start_x + index * spacing

def ease_in_out(t):
  return t * t * (3.0 - 2.0 * t)

def draw_scanner(surface, cx, cy, color):
  # Draws a futuristic arrow/scanner pointing upwards
  w = 40
  h = 30
  pts = [(cx, cy - h), (cx -w//2, cy), (cx + w//2, cy)]
  pygame.draw.polygon(surface, color, pts)
  pygame.draw.rect(surface, color, (cx - w//4, cy, w//2, 20))
  # Small glow effect
  pygame.draw.line(surface, SEA_FOAM, (cx - w//2, cy), (cx + w//2, cy), 2)

def render_frame():
  screen.fill(BG_COLOR)

  # --- HEADER WITH PYTHON IDENTATION ---  
  screen.blit(font_title.render("SUCCESSOR FUNCTION", True, SEA_FOAM), (60, 50))
  # Subtitle indented to X=100
  screen.blit(font_sub.render("Iterative Approach - O(n) Scan", True, BOX_BLUE), (100, 115))
  pygame.draw.line(screen, GATE_OFF, (60, 160), (WIDTH-60, 160), 3)

  # --- BITS ARRAY ---
  for i in range(8):
    bx = get_box_x(i)
    by = 450
    rect = pygame.Rect(bx - 45, by - 45, 90, 90)

    bg_c = PROCESSED_BLUE if processed_flags[i] else BOX_BLUE
    border_c = SEA_FOAM if (get_box_x(i) == scanner_x and scanner_active) else bg_c

    pygame.draw.rect(screen, bg_c, rect, border_radius=15)
    if get_box_x(i) == scanner_x and scanner_active:
      pygame.draw.rect(screen, border_c, rect, width=4, border_radius=15)

    t_val = font_box.render(str(bits[i]), True, SEA_FOAM)
    screen.blit(t_val, t_val.get_rect(center=(bx, by)))

    t_idx = font_small.render(f"b{7-i}", True, SEA_FOAM if not processed_flags[i] else GATE_OFF)
    screen.blit(t_idx, t_idx.get_rect(center=(bx, by + 70)))

  # --- SCANNER ---
  draw_scanner(screen, scanner_x, 600, GATE_ON if scanner_active else GATE_OFF)

  # --- STATUS TEXT ---
  if status_text:
    t_stat = font_status.render(status_text, True, status_color)
    screen.blit(t_stat, t_stat.get_rect(center=(WIDTH//2, 700)))

  # --- LIVE CODE PANEL ---
  panel_rect = pygame.Rect(WIDTH//2 - 350, 900, 700, 350)
  pygame.draw.rect(screen, PROCESSED_BLUE, panel_rect, border_radius = 20)
  pygame.draw.rect(screen, GATE_OFF, panel_rect, width=4, border_radius=20)

  t_ui = font_small.render("SOFTWARE EXECUTION", True, BOX_BLUE)
  screen.blit(t_ui, (panel_rect.left + 20, panel_rect.top + 15))

  for i, line in enumerate(code_lines):
    c = SEA_FOAM if i == active_code_line else  BOX_BLUE
    if i == 5 and i == active_code_line: c = HIGHLIGHT_RED

    line_surf = font_code.render(line, True, c)

    # Highlight background for the active line
    if i == active_code_line:
      bg_rect = pygame.Rect(panel_rect.left + 10, panel_rect.top + 60 + i*45 - 2, 680, 36)
      bg_color = (25, 60, 95) if i != 5 else (100, 30, 40)
      pygame.draw.rect(screen, bg_color, bg_rect, border_radius=8)

    screen.blit(line_surf, (panel_rect.left + 30, panel_rect.top + 60 + i*45))

  # --- WRITE FRAME ---
  frame = pygame.surfarray.pixels3d(screen).transpose([1, 0, 2])
  frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
  video.write(frame)

def animate_scanner_move(start_x, end_x, duration_sec):
  global scanner_x
  frames = int(FPS * duration_sec)
  for f in range(frames):
    t = f / float(frames - 1)
    ease_t = ease_in_out(t)
    scanner_x = start_x + (end_x - start_x) * ease_t
    render_frame()

def hold(seconds):
  for _ in range(int(FPS * seconds)):
    render_frame()

# ========================================================
# ========================== ANIMATION LOOP ==============
# ========================================================

print("Rendering iterative Successor with Early Exit...")

# Scanner start position (hidden on the far right, then moves in)
scanner_x = get_box_x(8)
hold(1.0)

for i in range(7, -1, -1):
  active_code_line = 0
  status_text = "Moving to next bit..."
  status_color = BOX_BLUE
  scanner_active = False

  # Move scanner to the current bit
  animate_scanner_move(scanner_x, get_box_x(i), 0.6)

  # Scanning...
  scanner_active = True
  active_code_line = 1
  status_text = f"Read b{7-i} == {bits[i]}"
  status_color = GATE_ON
  hold(0.6)

  if bits[i] == 1:
    active_code_line = 2
    status_text = "Bit is 1 -> Flips to 0, Carry generated"
    status_color = GATE_ON
    hold(0.4)

    bits[i] = 0
    processed_flags[i] = True
    hold(0.6)

  else: # We found the first '0'!
    active_code_line = 3
    status_text = "First '0' found!"
    status_color = HIGHLIGHT_RED
    hold(0.5)

    active_code_line = 4
    status_text = "Bit is 0 -> Flips to 1, Carry consumed" 
    hold(0.5)

    bits[i] = 1
    processed_flags[i] = True
    hold(0.5)

    active_code_line = 5
    status_text = "EARLY EXIT! No need to check further."
    scanner_active = False

    # Keep the break status for a few seconds to show the contrast to the ALU
    hold(2.5)
    break # <-- The magic of the iterative code!

active_code_line = -1
status_text = "PROCESS COMPLETE"
status_color = SEA_FOAM
scanner_active = False
hold(3.0)

video.release()
pygame.quit()
print("Done! The video was successfully generated.")
