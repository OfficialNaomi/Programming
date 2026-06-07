import pygame
import cv2
import numpy as np

# --- KONFIGURATION ---
WIDTH, HEIGHT = 1080, 1920
FPS = 30
VIDEO_NAME = "recursive_successor_alu_perfect_wires.mp4"

# ==========================================
# ====== FARBPALETTE: DEEP OCEAN ===========
# ==========================================
BG_COLOR = (7, 14, 28)           
SEA_FOAM = (212, 241, 244)       
BOX_BLUE = (30, 115, 175)        
PROCESSED_BLUE = (15, 45, 75)    
GATE_OFF = (20, 40, 60)          
GATE_ON = (0, 210, 255)          

pygame.init()
screen = pygame.Surface((WIDTH, HEIGHT))

font_title = pygame.font.SysFont("Consolas", 56, bold=True)
font_sub = pygame.font.SysFont("Consolas", 28)
font_box = pygame.font.SysFont("Consolas", 42, bold=True)
font_small = pygame.font.SysFont("Consolas", 22, bold=True)
font_alu = pygame.font.SysFont("Consolas", 26, bold=True)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(VIDEO_NAME, fourcc, FPS, (WIDTH, HEIGHT))

boxes = {}
alu_active = False

# Layout-Zentren
ALU_CENTER_Y = HEIGHT // 2
ALU_IN_X_LEFT = WIDTH // 2 - 110
ALU_IN_X_RIGHT = WIDTH // 2 + 110
ALU_IN_Y = ALU_CENTER_Y - 140      
GATE_Y = ALU_CENTER_Y + 100        
ALU_OUT_Y = GATE_Y + 120           

def ease_in_out(t):
    return t * t * (3.0 - 2.0 * t)

def draw_custom_wire(surface, color, start, end, mid_y, width=4):
    """Zeichnet geknickte Linien für die sich kreuzenden inneren Leitungen"""
    x1, y1 = start
    x2, y2 = end
    pygame.draw.line(surface, color, (x1, y1), (x1, mid_y + width//2), width)
    pygame.draw.line(surface, color, (x1, mid_y), (x2, mid_y), width)
    pygame.draw.line(surface, color, (x2, mid_y - width//2), (x2, y2), width)

def draw_alu_circuitry(surface, is_active):
    color = GATE_ON if is_active else GATE_OFF
    w = 5 if is_active else 3
    
    start_L = (ALU_IN_X_LEFT, ALU_IN_Y + 35)
    start_R = (ALU_IN_X_RIGHT, ALU_IN_Y + 35)
    
    # --- PERFEKTES ALIGNMENT ---
    # AND-Eingänge (Zentrum ist WIDTH//2 - 100)
    and_in_L = (ALU_IN_X_LEFT, GATE_Y - 30)      # Exakt vertikal unter der linken Box
    and_in_R = (WIDTH // 2 - 90, GATE_Y - 30)    # Innerer Eingang
    
    # XOR-Eingänge (Zentrum ist WIDTH//2 + 100)
    xor_in_L = (WIDTH // 2 + 90, GATE_Y - 45)    # Innerer Eingang
    xor_in_R = (ALU_IN_X_RIGHT, GATE_Y - 45)     # Exakt vertikal unter der rechten Box
    
    # 1. Äußere Leitungen: Komplett gerade nach unten ziehen (kein Zick-Zack mehr!)
    pygame.draw.line(surface, color, start_L, and_in_L, w)
    pygame.draw.line(surface, color, start_R, xor_in_R, w)
    
    # 2. Innere Leitungen: Kreuzen sich weiterhin sauber in der Mitte
    draw_custom_wire(surface, color, start_L, xor_in_L, ALU_CENTER_Y - 40, w)   
    draw_custom_wire(surface, color, start_R, and_in_R, ALU_CENTER_Y + 10, w)   

def draw_and_gate(surface, cx, cy, color, size=65):
    rect = pygame.Rect(cx - size//2, cy - size//2, size, size//2)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.circle(surface, color, (cx, cy), size//2)

def draw_xor_gate(surface, cx, cy, color, size=65):
    w = size / 2
    h = size / 2
    pts = []
    
    for t in np.linspace(-1, 1, 20):
        x = cx + w * t
        y = cy - h + (h / 3) * (1 - t**2)
        pts.append((x, y))
        
    for t in np.linspace(0, 1, 20):
        x = cx + w * (1 - t**2)  
        y = cy - h + 2 * h * t
        pts.append((x, y))
        
    for t in np.linspace(1, 0, 20):
        x = cx - w * (1 - t**2)
        y = cy - h + 2 * h * t
        pts.append((x, y))
        
    pygame.draw.polygon(surface, color, pts)
    
    arc_pts = []
    for t in np.linspace(-1, 1, 20):
        x = cx + w * t
        y = cy - h - 12 + (h / 3) * (1 - t**2)
        arc_pts.append((x, y))
    pygame.draw.lines(surface, color, False, arc_pts, 4)

def render_frame():
    screen.fill(BG_COLOR)
    
    screen.blit(font_title.render("SUCCESSOR FUNCTION", True, SEA_FOAM), (60, 50))
    screen.blit(font_sub.render("Based on ALU Processor Architecture", True, BOX_BLUE), (100, 115))
    pygame.draw.line(screen, GATE_OFF, (60, 160), (WIDTH-60, 160), 3)
    
    alu_rect = pygame.Rect(WIDTH//2 - 260, ALU_CENTER_Y - 220, 520, 500)
    pygame.draw.rect(screen, GATE_OFF, alu_rect, 3, border_radius=25)
    
    t_alu = font_alu.render("PROCESSING UNIT", True, GATE_OFF)
    screen.blit(t_alu, (alu_rect.right - t_alu.get_width() - 20, alu_rect.bottom - 40))

    draw_alu_circuitry(screen, alu_active)
    
    gate_color = GATE_ON if alu_active else GATE_OFF
    text_color = SEA_FOAM if alu_active else GATE_OFF
    
    draw_and_gate(screen, WIDTH // 2 - 100, GATE_Y, gate_color)
    screen.blit(font_small.render("AND", True, text_color), (WIDTH // 2 - 120, GATE_Y - 15))
    
    draw_xor_gate(screen, WIDTH // 2 + 100, GATE_Y, gate_color)
    screen.blit(font_small.render("XOR", True, text_color), (WIDTH // 2 + 80, GATE_Y - 15))

    for b_id, b in boxes.items():
        if not b.get('visible', True): continue
        
        rect = pygame.Rect(b['x'] - 35, b['y'] - 35, 70, 70)
        color = PROCESSED_BLUE if b.get('processed', False) else BOX_BLUE
        
        pygame.draw.rect(screen, color, rect, border_radius=12)
        if b.get('highlight', False):
            pygame.draw.rect(screen, SEA_FOAM, rect, width=3, border_radius=12)
            
        t_val = font_box.render(str(b['val']), True, SEA_FOAM)
        screen.blit(t_val, t_val.get_rect(center=(b['x'], b['y'])))
        
        if 'idx_label' in b:
            t_idx = font_small.render(b['idx_label'], True, SEA_FOAM if not b.get('processed', False) else PROCESSED_BLUE)
            screen.blit(t_idx, t_idx.get_rect(center=(b['x'], b['y'] + 55)))

    frame = pygame.surfarray.pixels3d(screen).transpose([1, 0, 2])
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    video.write(frame)

def animate_boxes(move_data, duration_sec):
    frames = int(FPS * duration_sec)
    starts = {b_id: (boxes[b_id]['x'], boxes[b_id]['y']) for b_id in move_data.keys()}
    
    for f in range(frames):
        t = f / float(frames - 1)
        ease_t = ease_in_out(t)
        for b_id, target in move_data.items():
            start_x, start_y = starts[b_id]
            end_x, end_y = target
            boxes[b_id]['x'] = start_x + (end_x - start_x) * ease_t
            boxes[b_id]['y'] = start_y + (end_y - start_y) * ease_t
        render_frame()

def hold(seconds):
    for _ in range(int(FPS * seconds)):
        render_frame()

def bit_x(index):
    start_x = 140
    spacing = 110
    return start_x + index * spacing 

# ==========================================
# ============ ANIMATIONS LOOP =============
# ==========================================

print("Rendere Update mit schnurgeraden äußeren Leitungen...")

bits = [1, 1, 1, 1, 1, 1, 1, 1]

for i in range(8):
    boxes[f"top_{i}"] = {'x': bit_x(i), 'y': 250, 'val': bits[i], 'idx_label': f"b{7-i}"}

carry_start_pos = (WIDTH - 150, 480)
boxes["carry"] = {'x': carry_start_pos[0], 'y': carry_start_pos[1], 'val': 1, 'highlight': True, 'idx_label': "Carry"}
hold(1.5)

for i in range(7, -1, -1):
    top_id = f"top_{i}"
    orig_top_x = boxes[top_id]['x']
    orig_top_y = boxes[top_id]['y']
    
    boxes[top_id]['highlight'] = True
    hold(0.5)
    
    animate_boxes({
        top_id: (ALU_IN_X_LEFT, ALU_IN_Y),
        "carry": (ALU_IN_X_RIGHT, ALU_IN_Y)
    }, 1.0)
    hold(0.3)
    
    alu_active = True
    b = boxes[top_id]['val']
    c = boxes["carry"]['val']
    new_c = b & c  
    new_b = b ^ c  
    
    boxes["out_carry"] = {'x': WIDTH // 2 - 100, 'y': ALU_OUT_Y, 'val': new_c, 'highlight': True}
    boxes["out_bit"] = {'x': WIDTH // 2 + 100, 'y': ALU_OUT_Y, 'val': new_b, 'highlight': True}
    boxes["carry"]['visible'] = False 
    
    hold(1.0)
    alu_active = False
    
    animate_boxes({
        top_id: (orig_top_x, orig_top_y),
        "out_bit": (orig_top_x, 1680),
        "out_carry": (carry_start_pos[0], carry_start_pos[1])
    }, 1.2)
    
    boxes[top_id]['highlight'] = False
    boxes[top_id]['processed'] = True  
    
    boxes["out_bit"]['highlight'] = False
    boxes["out_bit"]['idx_label'] = f"b{7-i}'"
    
    boxes["carry"] = boxes.pop("out_carry")
    boxes["carry"]['idx_label'] = "Carry"
    boxes[f"bot_{i}"] = boxes.pop("out_bit")
    
    hold(0.5)

boxes["carry"]['highlight'] = False
hold(3.0)
video.release()
pygame.quit()
print("Fertig!")
