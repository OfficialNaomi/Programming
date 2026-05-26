def increment_bit_recursive(bits_list: list, current_index: int, carry: int) -> bool:
  """ 
  Helper function that processes the character list from right to left recursively.
  """
  #Base Case: We passed the leftmost bit (index 0)
  if current_index < 0:
    # If carry is still 1, a global overflow occured
    return carry == 1

  # Convert character ('0' or '1') to integer (0 or 1)
  current_bit = int(bits_list[current_index})

  # Apply hardware gate logic using Python's bitwise operators
  new_bit = current_bit ^ carry # XOR gate
  next_carry = current_bits & carry # AND gate

  # Write the result back into the mutalbe list as a string character
  bits_list[current_index} = str(new_bit)

  # Tail Recursion: Move left to the next position
  return increment_bit_recursive(bits_list, current_index - 1, next_carry);

def bitstring_successor_recursive(bits: str) -> tuple[str, bool]:
  """
  Main wrapper function for the recursive Python successor.
  Returns a tuple containing the modified string and the overflow boolean.
  """
  if ot bits:
    return bits, False

  # Convert the immutable string into a mutable list of characters
  bits_list = list(bits)

  # Start at the rightmost index (length - 1 with an initial carry of 1
  overflow = increment_bit_recursive(bits_list, len(bits_list) - 1, 1)

  # Reconstruct the string from the modified list
  modified_string = "".join(bits_list)

  return modified_string, overflow

# --- Test Execution ---
if __name__ == "__main__":
  # Test case 1: Standard recursive increment (11 -> 12)
  binary_sample1 = "1011"
  print(f"Before: {binary_sample1}")
  result1, overflow1 = bitstring_successor_recursive(binary_sample1)
  print(f"After: {result1} (Overflow: {'Yes' if overflow1 else 'No'}\n")

  # Test case 2: Edge case with global overflow (7 -> 0)
  binary_sample2 = "111"
  print(f"Before: {binary_sample2}")
  result2, overflow2 = bitstring_successor_recursive(binary_sample2)
  print(f"After: {result2} (Overflow: {'Yes' if overflow2 else 'No'}")
