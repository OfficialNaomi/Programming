import pygame
import cv2
import numpy as np

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1080, 1920
FPS = 30
VIDEO_NAME = "optimized_tail_recursion.mp4"
INPUT_STRING = "00000000" 

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
font_sub = pygame.font.SysFont("Consolas", 40, bold=True)
font_box = pygame.font.SysFont("Consolas", 55, bold=True)
font_small = pygame.font.SysFont("Consolas", 24, bold=True)
font_status = pygame.font.SysFont("Consolas", 35)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(VIDEO_NAME, fourcc, FPS, (WIDTH, HEIGHT))

bits_rec = [int(x) for x in INPUT_STRING]
processed_rec = [False] * 8
carry_rec = 1

def get_box_x(index):
    # Centered for 1080p screen width
    # 8 boxes * 100 spacing -> 700 total span. 
    # (1080 - 700) / 2 = 190 start position
    start_x = 190
    spacing = 100
    return start_x + index * spacing

def ease_in_out(t):
    return t * t * (3.0 - 2.0 * t)

def draw_scanner(surface, cx, cy, color):
    w = 40
    h = 30
    pts = [(cx, cy - h), (cx - w//2, cy), (cx + w//2, cy)]
    pygame.draw.polygon(surface, color, pts)
    pygame.draw.rect(surface, color, (cx - w//4, cy, w//2, 20))

def draw_memory_stack(y_pos, count):
    mem_x = WIDTH // 2
    mem_y = y_pos + 520  # Pushed significantly down to avoid overlap
    pygame.draw.rect(screen, GATE_OFF, (mem_x - 120, mem_y - 200, 240, 450), width=4, border_radius=15)
    
    t_mem = font_small.render("RAM (CALL STACK)", True, SEA_FOAM)
    screen.blit(t_mem, t_mem.get_rect(center=(mem_x, mem_y - 230)))
    
    for i in range(count):
        block_y = (mem_y + 180) - (i * 55)
        pygame.draw.rect(screen, MEMORY_COLOR, (mem_x - 100, block_y, 200, 45), border_radius=8)
        t_label = font_small.render(f"Stack Frame {i+1}", True, SEA_FOAM)
        screen.blit(t_label, t_label.get_rect(center=(mem_x, block_y + 22)))

def render_frame(scan_x, is_active, status_text, status_color, memory_count):
    screen.fill(BG_COLOR)
    
    t_main = font_title.render("OPTIMIZED TAIL RECURSION", True, SEA_FOAM)
    screen.blit(t_main, t_main.get_rect(center=(WIDTH//2, 150)))
    
    t_sub = font_sub.render("The 'Early Exit' in Action", True, HIGHLIGHT_RED)
    screen.blit(t_sub, t_sub.get_rect(center=(WIDTH//2, 230)))

    y_pos = 450 # Pulled the bit-string up slightly
    for i in range(8):
        bx = get_box_x(i)
        rect = pygame.Rect(bx - 45, y_pos - 45, 90, 90)
        
        bg_c = PROCESSED_BLUE if processed_rec[i] else BOX_BLUE
        border_c = SEA_FOAM if (get_box_x(i) == scan_x and is_active) else bg_c
        
        pygame.draw.rect(screen, bg_c, rect, border_radius=15)
        if get_box_x(i) == scan_x and is_active:
             pygame.draw.rect(screen, border_c, rect, width=4, border_radius=15)
             
        t_val = font_box.render(str(bits_rec[i]), True, SEA_FOAM)
        screen.blit(t_val, t_val.get_rect(center=(bx, y_pos)))
        
        t_idx = font_small.render(f"b{7-i}", True, SEA_FOAM if not processed_rec[i] else GATE_OFF)
        screen.blit(t_idx, t_idx.get_rect(center=(bx, y_pos + 70)))

    draw_scanner(screen, scan_x, y_pos + 120, GATE_ON if is_active else GATE_OFF)

    # Status text is now safely sandwiched between the scanner and the memory stack
    t_stat = font_status.render(status_text, True, status_color)
    screen.blit(t_stat, t_stat.get_rect(center=(WIDTH//2, y_pos + 220)))
    
    draw_memory_stack(y_pos, memory_count)

    frame = pygame.surfarray.pixels3d(screen).transpose([1, 0, 2])
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    video.write(frame)

def hold(seconds, scan_x, is_active, status_text, status_color, memory_count):
    for _ in range(int(FPS * seconds)):
        render_frame(scan_x, is_active, status_text, status_color, memory_count)

# ==========================================
# ============ ANIMATION LOGIC =============
# ==========================================
scan_rec = get_box_x(8)
mem_rec = 0
active_rec = True

hold(1.5, scan_rec, False, "READY", BOX_BLUE, 0)

for i in range(7, -1, -1):
    if not active_rec:
        break # Skip animation for the rest if early exit triggered
        
    start_rec = scan_rec
    target_x = get_box_x(i)
    
    frames = int(FPS * 0.4)
    for f in range(frames):
        t = f / float(frames - 1)
        ease_t = ease_in_out(t)
        scan_rec = start_rec + (target_x - start_rec) * ease_t
        render_frame(scan_rec, active_rec, "Moving...", SEA_FOAM, mem_rec)

    mem_rec += 1 # Push Stack Frame
    
    if bits_rec[i] == 1 and carry_rec == 1:
        bits_rec[i] = 0
        processed_rec[i] = True
        hold(0.8, scan_rec, active_rec, "1 -> 0 | Stack Grows", BOX_BLUE, mem_rec)
    elif bits_rec[i] == 0 and carry_rec == 1:
        bits_rec[i] = 1
        processed_rec[i] = True
        carry_rec = 0
        hold(1.0, scan_rec, active_rec, "0 -> 1 | EARLY EXIT TRIGGERED 🛑", SUCCESS_GREEN, mem_rec)
        active_rec = False # Break the recursion chain!

# Unwinding Phase
hold(1.0, scan_rec, False, "RECURSION HALTED. UNWINDING...", HIGHLIGHT_RED, mem_rec)

while mem_rec > 0:
    mem_rec -= 1
    hold(0.3, scan_rec, False, f"Popping Frame... ({mem_rec} left)", HIGHLIGHT_RED, mem_rec)

hold(3.0, scan_rec, False, "FINISHED - SAVED O(n) MEMORY", SUCCESS_GREEN, 0)

video.release()
pygame.quit()
