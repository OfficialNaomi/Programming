# Helper function that processes the string from right to left recursively.
# In Ruby, functions automatically return the value of their last evaluated expression.
def increment_bit_recursive(bits, current_index, carry)
  # Base Case: We passed the leftmost bit (index 0)
  if current_index < 0
    return carry == 1
  end

  # Convert the character at the current index to an integer
  current_bit = bits[current_index].to_i

  #Apply hardware gate logic
  new_bit = current_bit ^ carry # XOR gate
  next_carry = current_bit & carry # AND gate

  # Write the result directly back into the mutable string
  bits[current_index] = new_bit.to_s

  # Tail Recursion: Move left to the next position
  increment_bit_recursive(bits, current_index - 1, next_carry)
end

# Main wrapper function for the recursive Ruby successor.
# Since Ruby passes object references, modifications to the string happen in place.
def bitstring_successor_recursive(bits)
  if bits.nil? || bits.empty?
    return false
  end

  # Start at the rightmost index ( length - 1) with an initial carry of 1
  increment_bit_recursive(bits, bits.length - 1, 1)
end

# --- Test Execution ---

# Test case 1: Standard recursive increment (11 -> 12) 
binary_sample1 = "1011"
puts "Before: #{binary_sample1}"
overflow1 = bitstring_successor_recursive(binary_sample1)
puts "After: #{binary_sample1} (Overflow: #{overflow1 ? 'Yes' : 'No'})\n\n"

# Test case 2: Edge case with global overflow (7 -> 0)
binary_sample2 = "111"
puts "Before: #{binary_sample2}"
overflow2 = bitstring_successor_recursive(binary_sample2)
puts "After: #{binary_sample2} (Overflow: #{overflow2 ? 'Yes' : 'No'})"
