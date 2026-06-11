# Helper function for tail recursion with early exit
# Returns true for overflow, false otherwise
def successor_tail_optimized(bits, index, carry = 1)
  # Base Cases
  return false if carry == 0
  return true if index < 0

  if bits[index] == '1'
    bits[index] = '0'
    # Recursive call (Ruby implicitly returns the result of the last evaluation)
    successor_tail_optimized(bits, index - 1, 1)
  else
    bits[index] = '1'
    # EARLY EXIT: Stops recursion and returns false (no overflow)
    false
  end
end

# Main wrapper function for the recursive Ruby successor.
# Since Ruby passes object references, modifications to the string happen in place.
def bitstring_successor_recursive(bits)
  if bits.nil? || bits.empty?
    return false
  end

  # Start at the rightmost index ( length - 1) with an initial carry of 1
  successor_tail_optimized(bits, bits.length - 1, 1)
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
