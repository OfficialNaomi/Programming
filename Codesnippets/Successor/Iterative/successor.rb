# Iterative successor function in Ruby
# Modifies the string in place and returns true if a global overflow occurred.
def bitstring_successor_iterative(bits)
  return false if bits.nil? || bits.empty?

  # Iterate from the last index down to 0
  (bits.length - 1).downto(0 ) do |i|
    if bits[i] == '1'
      bits[i] = '0' # 1 + 1 = 0 (Carry)
    else
      bits[i] = '1' # Found the first '0'k, consume carry
      return false # Early exit: no global overflow
    end
  end

  true # Loop finished completely -> global overflow (e.g., "111")
end

# --- Test Cases ---
sample1 = "1011"
puts "Before: #{sample1}"
overflow1 = bitstring_successor_iterative(sample1)
puts "After: #{sample1} (Overflow: #{overflow1 ? 'Yes' : 'No'} )\n\n"

sample2 = "111"
puts "Before : #{sample2}"
overflow2 = bitstring_successor_iterative(sample2)
puts "After: #{sample2} (Overflow: #{overflow2 ? 'Yes' : 'No'})"
      
