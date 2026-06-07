import pygame
import cv2
import numpy as np

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1080, 1920
FPS = 30
VIDEO_NAME = "dynamic_memory_comparison.mp4"

# CHANGE THIS STRING TO TEST DIFFERENT SCENARIOS!
INPUT_STRING = "11110111" 

# ==========================================
# ====== COLOR PALETTE =====================
# ==========================================
BG_COLOR = (7, 14, 28)           
SEA_FOAM = (212, 241, 244)       
BOX_BLUE = (30, 115, 175)        
PROCESSED_BLUE = (15, 45, 75)    
GATE_OFF = (20, 40, 60)          
GATE_ON = (0, 210, 255)          
HIGHLIGHT_RED = (255, 70, 90)
SUCCESS_GREEN = (50, 200, 100)
MEMORY_COLOR = (150, 40, 180)

pygame.init()
screen = pygame.Surface((WIDTH, HEIGHT))

font_title = pygame.font.SysFont("Consolas", 60, bold=True)
font_sub = pygame.font.SysFont("Consolas", 35, bold=True)
font_box = pygame.font.SysFont("Consolas", 42, bold=True)
font_small = pygame.font.SysFont("Consolas", 18, bold=True)
font_status = pygame.font.SysFont("Consolas", 30)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(VIDEO_NAME, fourcc, FPS, (WIDTH, HEIGHT))

# --- DYNAMIC STATE ---
bits_iter = [int(x) for x in INPUT_STRING]
bits_rec = [int(x) for x in INPUT_STRING]
processed_iter = [False] * 8
processed_rec = [False] * 8

carry_iter = 1
carry_rec = 1

def get_box_x(index):
    # Shifted to the left to make room for Memory visualizer on the right
    start_x = 80
    spacing = 85
    return start_x + index * spacing

def ease_in_out(t):
    return t * t * (3.0 - 2.0 * t)

def draw_scanner(surface, cx, cy, color):
    w = 30
    h = 25
    pts = [(cx, cy - h), (cx - w//2, cy), (cx + w//2, cy)]
    pygame.draw.polygon(surface, color, pts)
    pygame.draw.rect(surface, color, (cx - w//4, cy, w//2, 15))

def draw_memory_stack(y_pos, count, label_text):
    # Draws the RAM usage on the right side of the screen
    mem_x = 850
    pygame.draw.rect(screen, GATE_OFF, (mem_x - 70, y_pos - 150, 140, 400), width=4, border_radius=10)
    
    t_mem = font_small.render("RAM / STACK", True, SEA_FOAM)
    screen.blit(t_mem, t_mem.get_rect(center=(mem_x, y_pos - 170)))
    
    # Draw blocks from bottom to top
    for i in range(count):
        block_y = (y_pos + 200) - (i * 45)
        pygame.draw.rect(screen, MEMORY_COLOR, (mem_x - 60, block_y, 120, 40), border_radius=5)
        t_label = font_small.render(label_text, True, SEA_FOAM)
        screen.blit(t_label, t_label.get_rect(center=(mem_x, block_y + 20)))

def draw_section(y_pos, title, bits, processed, scanner_x, is_active, status_text, status_color, memory_count, memory_label):
    t_title = font_sub.render(title, True, SEA_FOAM)
    screen.blit(t_title, (80, y_pos - 100))
    
    for i in range(8):
        bx = get_box_x(i)
        by = y_pos
        rect = pygame.Rect(bx - 35, by - 35, 70, 70)
        
        bg_c = PROCESSED_BLUE if processed[i] else BOX_BLUE
        border_c = SEA_FOAM if (get_box_x(i) == scanner_x and is_active) else bg_c
        
        pygame.draw.rect(screen, bg_c, rect, border_radius=10)
        if get_box_x(i) == scanner_x and is_active:
             pygame.draw.rect(screen, border_c, rect, width=4, border_radius=10)
             
        t_val = font_box.render(str(bits[i]), True, SEA_FOAM)
        screen.blit(t_val, t_val.get_rect(center=(bx, by)))
        
        t_idx = font_small.render(f"b{7-i}", True, SEA_FOAM if not processed[i] else GATE_OFF)
        screen.blit(t_idx, t_idx.get_rect(center=(bx, by + 55)))

    draw_scanner(screen, scanner_x, y_pos + 100, GATE_ON if is_active else GATE_OFF)

    t_stat = font_status.render(status_text, True, status_color)
    screen.blit(t_stat, (80, y_pos + 150))
    
    draw_memory_stack(y_pos, memory_count, memory_label)

def render_frame(sx_i, act_i, st_i, col_i, mem_i, sx_r, act_r, st_r, col_r, mem_r):
    screen.fill(BG_COLOR)
    
    t_main = font_title.render(f"INPUT: {INPUT_STRING}", True, SEA_FOAM)
    screen.blit(t_main, t_main.get_rect(center=(WIDTH//2, 100)))
    pygame.draw.line(screen, GATE_OFF, (50, 160), (WIDTH-50, 160), 4)

    draw_section(450, "1. ITERATIVE (O(1) Space)", bits_iter, processed_iter, sx_i, act_i, st_i, col_i, mem_i, "Loop var")
    pygame.draw.line(screen, GATE_OFF, (150, 750), (WIDTH-150, 750), 2)
    draw_section(1050, "2. TAIL RECURSION (O(n) Space)", bits_rec, processed_rec, sx_r, act_r, st_r, col_r, mem_r, "Stack Frame")

    frame = pygame.surfarray.pixels3d(screen).transpose([1, 0, 2])
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    video.write(frame)

def hold(seconds, sx_i, act_i, st_i, col_i, mem_i, sx_r, act_r, st_r, col_r, mem_r):
    for _ in range(int(FPS * seconds)):
        render_frame(sx_i, act_i, st_i, col_i, mem_i, sx_r, act_r, st_r, col_r, mem_r)

# ==========================================
# ============ ANIMATION LOGIC =============
# ==========================================
print(f"Rendering dynamic logic for: {INPUT_STRING}")

scan_iter = get_box_x(8)
scan_rec = get_box_x(8)
active_iter = True
active_rec = True
mem_iter = 0
mem_rec = 0

hold(1.0, scan_iter, False, "READY", BOX_BLUE, 0, scan_rec, False, "READY", BOX_BLUE, 0)

for i in range(7, -1, -1):
    start_iter = scan_iter
    start_rec = scan_rec
    target_x = get_box_x(i)
    
    # Movement animation
    frames = int(FPS * 0.4)
    for f in range(frames):
        t = f / float(frames - 1)
        ease_t = ease_in_out(t)
        
        if active_iter: scan_iter = start_iter + (target_x - start_iter) * ease_t
        if active_rec: scan_rec = start_rec + (target_x - start_rec) * ease_t
        
        st_i = "Moving..." if active_iter else "BREAK TRIGGERED 🛑"
        col_i = SEA_FOAM if active_iter else HIGHLIGHT_RED
        mem_i = 1 if active_iter else 0 # Iterative memory drops when done
        
        render_frame(scan_iter, active_iter, st_i, col_i, mem_i, scan_rec, active_rec, "Moving...", SEA_FOAM, mem_rec)

    # --- ITERATIVE LOGIC (DYNAMIC) ---
    st_iter, c_iter = "EARLY EXIT 🛑", HIGHLIGHT_RED
    mem_iter = 1 if active_iter else 0
    if active_iter:
        if bits_iter[i] == 1 and carry_iter == 1:
            bits_iter[i] = 0
            st_iter, c_iter = "1 -> 0 (Carry 1)", BOX_BLUE
        elif bits_iter[i] == 0 and carry_iter == 1:
            bits_iter[i] = 1
            carry_iter = 0
            st_iter, c_iter = "0 -> 1 (Carry consumed!)", SUCCESS_GREEN
            active_iter = False # THE DYNAMIC BREAK!
        processed_iter[i] = True

    # --- RECURSIVE LOGIC (DYNAMIC) ---
    mem_rec += 1 # Stack grows dynamically every frame!
    if active_rec:
        curr = bits_rec[i]
        new_b = curr ^ carry_rec
        carry_rec = curr & carry_rec
        bits_rec[i] = new_b
        processed_rec[i] = True
        st_rec, c_rec = f"Bit is now {new_b}", GATE_ON

    hold(0.6, scan_iter, active_iter, st_iter, c_iter, mem_iter, scan_rec, active_rec, st_rec, c_rec, mem_rec)

# --- THE UNWINDING PHASE (RECURSION ONLY) ---
hold(1.0, scan_iter, False, "FINISHED ⚡", SUCCESS_GREEN, 0, scan_rec, False, "REACHED BASE CASE. UNWINDING...", HIGHLIGHT_RED, mem_rec)

# Destroying the stack blocks one by one
while mem_rec > 0:
    mem_rec -= 1
    hold(0.2, scan_iter, False, "FINISHED ⚡", SUCCESS_GREEN, 0, scan_rec, False, f"Popping Stack Frame... ({mem_rec} left)", HIGHLIGHT_RED, mem_rec)

hold(3.0, scan_iter, False, "DONE", SUCCESS_GREEN, 0, scan_rec, False, "DONE", SUCCESS_GREEN, 0)

video.release()
pygame.quit()
print("Done! The dynamic animation was created.")
