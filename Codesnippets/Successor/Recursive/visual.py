import sys
import pygame

# Initialize Pygame
pygame.init()

# Window Configuration
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Binary Successor - Recursive Visualization")
clock = pygame.time.Clock()

# Color Palette (Aesthetic Dark Mode)
COLOR_BG = (15, 23, 42) # Deep slate blue
COLOR_BIT_0 = (51, 65, 85) # Muted gray-blue
COLOR_BIT_1 = (34, 197, 94) # Bright neon green
COLOR_POINTER = (234, 179, 8) #Warning yellow
COLOR_TEXT = (248, 250, 252) # Crisp white

# Font Setup
font = pygame.font.SysFont("Consolas", 24)
font_large = pygame.font.SysFont("Consolas", 64)

def draw_interface(bits_list: list, current_index: int, carry: int):
  """
  Renders the entire binary register, text information, and the recursive pointer.
  """
  screen.fill(COLOR_BG)

  #Render top info text
  info_text = font.render(f"Recursive Layer Analysis | Current Carry: {carry}", True, COLOR_TEXT)
  screen.blit(info_text, (40, 30))

  # Calculate dynamic spacing for the bits
  num_bits = len(bits_list)
  box_size = 70
  spacing = 20 
  total_width = (num_bits * box_size) + ((num_bits - 1) * spacing)
  start_x = (WIDTH - total_width) // 2
  start_y = (HEIGHT - box_size) // 2

  # Draw each bit block
  for i in range(num_bits):
    x = start_x + i * (box_size + spacing)
    y = start_y

    # Determine block color based on bit value
    box_color = COLOR_BIT_1 if bits_list[i] == '1' else COLOR_BIT_0
    pygame.draw.rect(screen, box_color, (x, y, box_size, box_size), border_radius = 8)

    # Draw the text inside the block
    bit_text = font_large.render(bits_list[i], True, COLOR_TEXT)
    text_rext = bit_text.get_rect(center=(x + box_size // 2, y + box_size // 2))

    #Draw the recursive actice pointer frame
    if i == current_index:
      pygame.draw.rect(screen, COLOR_POINTER, (x - 4, y - 4, box_size + 8, box_size + 8), width = 4, border_radius = 10)

  pygame.display.flip()

def increment_bit_visual(bits_list: list, current_index: int, carry: int) -> bool: 
  """
  Core recursive gate logic, synchronized with real-time visual rendering.
  """
  # Standard Pygame event pum to prevent the window from freezing/crashing
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

  # 1. Convert character to integer
  current_bit = int(bits_list[current_index])

  # 2. Apply hardware gate logic (HIER WIRD ES DEFINIERT)
  new_bit = current_bit ^ carry # XOR gate
  next_carry = current_bit & carry # AND gate

  # 3. Write the result back into the list
  bits_list[current_index] = str(new_bit)
      
  # Visual Update: Show the current state before processing the gates
  draw_interface(bits_list, current_index, carry)
  pygame.time.delay(800) # 800ms delay so human eyes (and YouTube) can follow along

  # Tail Recursion: Move left 
  return increment_bit_visual(bits_list, current_index - 1, next_carry)

def run_visualization(binary_string: str):
  """
  Main wrapper framework managing the visualization scene.
  """
  bits_list = list(binary_string)

  # Execute the animated recursive algortihm
  overflow = increment_bit_visual(bits_list, len(bits_list) - 1, 1)

  # Final state presentation loop
  result_string = "".join(bits_list)
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
        running = False
  
    screen.fill(COLOR_BG)
    # Render final completion screen
    done_text = font.render(f"Processing Complete! Overflow: {'Yes' if overflow else 'No'}", True, COLOR_TEXT)
    screen.blit(done_text, (40, 30))

    # Keep drawing the final stable state
    draw_interface(bits_list, -1, 0)
    pygame.time.delay(100)

if __name__=="__main__":
  # Feel free to change this string to test different values (e.g., "1111"for an overflow show)
  test_binary = "1011"
  run_visualization(test_binary)
  pygame.quit()
