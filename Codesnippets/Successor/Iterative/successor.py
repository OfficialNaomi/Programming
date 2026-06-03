def bitstring_successor_iterative(bits_str):
  if not bits_str:
    return False, bits_str

  # Convert the string into a mutable list of characters
  char_list = list(bits_str)

  # Iterate from right to the left: range(start, stop_exclusive, step)
  for i in range(len(char_list) -1, -1, -1):
    if char_list[i] == '1':
      char_list[i] = '0' # 1 + 1 = 0 (Carry moves further to the left)
    else:
      char_list[i] = '1' # First '0' found, carry is consumed

      # Reconstruct the string and trigger early exit (no global overflow)
      return False, "".join(char_list)

  #If the loop finishes completely, all bits were '1' (e.g., "111")
  return True, "".join(char_list)

#===============================================
#=============== TEST CASE =====================
#===============================================
if __name__ == "__main__":
  # Test case 1: Standard iterative increment (11 -> 12)
  sample_1 = "1011"
  print(f"Before: {sample_1}")
  overflow_1, result_1 = bitstring_successor_iterative(sample_1)
  print(f"After: {result_1} (Overflow: {'Yes' if overflow_1 else 'No'})\n")

  # Test case 2: Edge case with global overflow (7 -> 0)
  sample_2 = "111"
  print(f"Before: {sample_2}")
  overflow_2, result_2 = bitstring_successor_iterative(sample_2)
  print(f"After: {result_2} (Overflow: {'Yes' if overflow_2 else 'No'})")
  
