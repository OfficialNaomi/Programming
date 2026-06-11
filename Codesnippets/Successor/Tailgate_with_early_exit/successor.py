def successor_tail_optimized(bits: list, index: int, carry: int = 1):
    # Base Case: Left edge reached or carry is 0
    if index < 0 or carry == 0:
        return
    
    current_bit = 1 if bits[index] == '1' else 0
    
    if current_bit == 1:
        bits[index] = '0'
        # Pass carry left
        successor_tail_optimized(bits, index - 1, 1)
    else:
        bits[index] = '1'
        # EARLY EXIT: We found a '0', flipped it, and we are done.
        # No recursive call is made. The stack stops growing here.
        return

def bitstring_successor_recursive(bits: str) -> tuple[str, bool]:
  """
  Main wrapper function for the recursive Python successor.
  Returns a tuple containing the modified string and the overflow boolean.
  """
  if not bits:
    return bits, False

  # Convert the immutable string into a mutable list of characters
  bits_list = list(bits)

  # Start at the rightmost index (length - 1 with an initial carry of 1
  overflow = successor_tail_optimized(bits_list, len(bits_list) - 1, 1)

  # Reconstruct the string from the modified list
  modified_string = "".join(bits_list)

  return modified_string, overflow

# --- Test Execution ---
if __name__ == "__main__":
  # Test case 1: Standard recursive increment (11 -> 12)
  binary_sample1 = "1011"
  print(f"Before: {binary_sample1}")
  result1, overflow1 = bitstring_successor_recursive(binary_sample1)
  print(f"After: {result1} (Overflow: {'Yes' if overflow1 else 'No'})\n")

  # Test case 2: Edge case with global overflow (7 -> 0)
  binary_sample2 = "111"
  print(f"Before: {binary_sample2}")
  result2, overflow2 = bitstring_successor_recursive(binary_sample2)
  print(f"After: {result2} (Overflow: {'Yes' if overflow2 else 'No'})")
