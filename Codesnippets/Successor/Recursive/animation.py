import sys
import pygame
import cv2

# Initialize Pygame
pygame.init()

# SHORTS CONFIGURATION: Strict 9:16 Vertical Format
WIDTH, HEIGHT = 1080, 1920
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Binary Successor – Deep Unwinding Visualization")

# Color Palette (Aesthetic Dark Cyberpunk)
COLOR_BG = (10, 12, 24)          # Ultra dark navy
COLOR_BIT_0 = (30, 41, 59)       # Muted slate gray
COLOR_BIT_1 = (34, 197, 94)      # Neon green
COLOR_ACTIVE = (234, 179, 8)     # Gold pointer / Active knowledge
COLOR_TEXT = (241, 245, 249)     # White text
COLOR_NODE_BG = (18, 26, 48)     # Deep blue for gate boxes
COLOR_FLIP = (255, 255, 255)     # White flash for gate execution

# Fonts (Scaled for mobile screens)
font_sm = pygame.font.SysFont("Consolas", 32)
font_md = pygame.font.SysFont("Consolas", 42)
font_lg = pygame.font.SysFont("Consolas", 72)

# Video Recorder Setup (Shorts format)
video_filename = "binary_successor_unwinding.avi"
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_writer = cv2.VideoWriter(video_filename, fourcc, 30.0, (WIDTH, HEIGHT))

def capture_frame():
    """Captures the frame and writes it into the video container."""
    view = pygame.surfarray.array3d(screen).transpose([1, 0, 2])
    video_writer.write(cv2.cvtColor(view, cv2.COLOR_RGB2BGR))

def draw_unwinding_interface(bits_list: list, current_index: int, phase_text: str, gate_nodes: list, flashing_index: int = -1):
    """Renders the vertical layout tracking progressive knowledge and gate resolution."""
    screen.fill(COLOR_BG)

    # 1. Main Header
    title_surface = font_md.render("BINARY SUCCESSOR FUNCTION", True, COLOR_TEXT)
    screen.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, 120)))
    sub_title = font_sm.render("Visualizing Progressive Knowledge Unwinding", True, COLOR_TEXT)
    screen.blit(sub_title, sub_title.get_rect(center=(WIDTH // 2, 170)))

    # 2. Render 8-Bit Register
    num_bits = len(bits_list)
    box_size, spacing = 95, 15
    total_width = (num_bits * box_size) + ((num_bits - 1) * spacing)
    start_x, y_position = (WIDTH - total_width) // 2, 280
    
    for i in range(num_bits):
        x = start_x + i * (box_size + spacing)
        
        # Color logic: flash white if currently executing gates
        if i == flashing_index:
            box_color = COLOR_FLIP
        else:
            box_color = COLOR_BIT_1 if bits_list[i] == '1' else COLOR_BIT_0
            
        pygame.draw.rect(screen, box_color, (x, y_position, box_size, box_size), border_radius=14)
        
        if i == current_index:
            pygame.draw.rect(screen, COLOR_ACTIVE, (x-6, y_position-6, box_size+12, box_size+12), width=6, border_radius=18)
            
        bit_char = font_lg.render(bits_list[i], True, COLOR_BG if i == flashing_index else COLOR_TEXT)
        screen.blit(bit_char, bit_char.get_rect(center=(x + box_size//2, y_position + box_size//2)))

    # 3. Dynamic Action Banner (Middle of the screen)
    pygame.draw.rect(screen, COLOR_ACTIVE, (60, 460, WIDTH - 120, 80), width=3, border_radius=12)
    action_surface = font_sm.render(phase_text, True, COLOR_ACTIVE)
    screen.blit(action_surface, action_surface.get_rect(center=(WIDTH // 2, 500)))

    # 4. DRAW THE PROGRESSIVE KNOWLEDGE GATES Tree (Unwinding)
    # Stacks vertically down the remaining phone screen space
    stack_y_start = 600
    node_height = 140
    node_spacing = 30
    
    for idx, node in enumerate(gate_nodes):
        node_y = stack_y_start + idx * (node_height + node_spacing)
        
        is_latest = (idx == len(gate_nodes) - 1)
        border_color = COLOR_ACTIVE if is_latest else COLOR_BIT_0
        
        # Draw the physical Gate Container (Module)
        pygame.draw.rect(screen, COLOR_NODE_BG, (60, node_y, WIDTH - 120, node_height), border_radius=20)
        pygame.draw.rect(screen, border_color, (60, node_y, WIDTH - 120, node_height), width=3, border_radius=20)
        
        # Render the stored knowledge details & logic state inside the module
        node_title = f"Knowledge Node {idx+1} (Analyzing Bit [{node['index']}])"
        state_str = f"Bit: {node['bit']} | Incoming Carry: {node['carry']}"
        
        # Dynamic connection line to show branching dependency from previous layer
        if idx > 0:
            prev_y = node_y - node_spacing
            pygame.draw.line(screen, COLOR_BIT_0, (120, prev_y), (120, node_y), width=3)
            
        # Draw explicit gate operations (XOR / AND results, appearing after resolution)
        # Note: In the final pop/resolve phase, we will dynamically update this text to show results.
        if 'xor_result' in node:
            # Phase 2: Resolving Gatter with final values
            gate_data = f"EXECUTION: XOR -> {node['xor_result']} | AND (Next Carry) -> {node['next_carry']}"
            screen.blit(font_sm.render(gate_data, True, COLOR_ACTIVE), (100, node_y + 85))
        else:
            # Phase 1: Deploying with only inputs known
            gate_data = "EXECUTION: Gates waiting for Base Case resolve..."
            screen.blit(font_sm.render(gate_data, True, COLOR_BIT_0), (100, node_y + 85))

        screen.blit(font_sm.render(node_title, True, COLOR_ACTIVE if is_latest else COLOR_TEXT), (100, node_y + 15))
        screen.blit(font_sm.render(state_str, True, COLOR_TEXT), (100, node_y + 50))

    pygame.display.flip()
    
    # Capture multiple frames per step (approx. 0.7s step-delay for readability on mobile)
    for _ in range(21):
        capture_frame()

def increment_bit_unwinding_logic(bits_list: list, current_index: int, carry: int, gate_nodes: list) -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Base Case handling: When index is out of bounds, start unwinding the gathered data
    if current_index < 0:
        draw_unwinding_interface(bits_list, current_index, "Base Case Hit! Unwinding Knowledge Tree...", gate_nodes)
        return carry == 1

    current_bit = int(bits_list[current_index])

    # PHASE 1: Downward Execution (Vorstoß nach links, Knowledge PUSH)
    current_node_data = {
        'index': current_index,
        'bit': current_bit,
        'carry': carry
    }
    gate_nodes.append(current_node_data)
    
    draw_unwinding_interface(bits_list, current_index, f"DEPLOYING: Knowledge Node {len(gate_nodes)} (Gates offline)", gate_nodes)

    # Calculate local hardware gates
    new_bit = current_bit ^ carry
    next_carry = current_bit & carry

    # Jump deeper into tail recursion, passing knowledge along the way
    overflow = increment_bit_unwinding_logic(bits_list, current_index - 1, next_carry, gate_nodes)

    # PHASE 2: Resolution (Zurückkommen und Gatter umschalten, Knowledge POP)
    # We update the current active knowledge node to show the calculated gate outputs
    
    # We find the node we previously deployed (by index), and add the result data
    target_node = next((node for node in gate_nodes if node['index'] == current_index), None)
    if target_node:
        target_node['xor_result'] = new_bit
        target_node['next_carry'] = next_carry

    # Visual Update: Show the gate cell flashing white as it executes its logic
    draw_unwinding_interface(bits_list, current_index, f"RESOLVING: Node {len(gate_nodes)} Gatter", gate_nodes, flashing_index=current_index)
    
    # Write back step state
    bits_list[current_index] = str(new_bit)
    
    return overflow

def run_shorts_generation():
    # 8-Bit test input showing deep stack behavior (e.g., forces a cascade at index 4)
    test_binary = "10111101" 
    bits_list = list(test_binary)
    gate_nodes = []
    
    # Initial systems draw
    draw_unwinding_interface(bits_list, -1, "Initializing Core Architecture...", gate_nodes)
    
    # Run active unwinding logic
    overflow = increment_bit_unwinding_logic(bits_list, len(bits_list) - 1, 1, gate_nodes)
    
    # Hold final result for 3 seconds (90 frames) so the viewer can process the end state
    draw_unwinding_interface(bits_list, -1, f"Finished! Global Overflow: {overflow}", gate_nodes)
    for _ in range(90):
        capture_frame()

if __name__ == "__main__":
    print("Compiling stabilized YouTube Short video file... Please wait.")
    run_shorts_generation()
    video_writer.release()
    pygame.quit()
    print(f"Short successfully generated and saved as '{video_filename}'!")
