#include <iostream>
#include <string>

/* * Helper function that processes the std:: string from right to left recursively.
 * The string is passed by reference (&) to modify it in place without copying.
 */
bool increment_bit_recursive(std::string& bits, int current_index, int carry) {
  // Base Case: We passed the leftmost bit (index 0)
  if (current_index < 0) { 
    // If carry is still 1, a global overflow occurred
    return (carry == 1);
  }

  // Convert character ('0' or '1') to integer (0 or 1)
  int current_bit = (bits[current_index] == '1') ? 1:0;

  // Apply hardware gate logic
  int new_bit = current_bit ^ carry; //XOR gate for the new bit value
  int next_carry = current_bit & carry; //AND gate for the next carry layer

  // Write the result back into the string
  bits[current_index] = (new_bit == 1) ? '1': '0';

  // Tail Recursion: Move left to the next bit position
  return increment_bit_recursive(bits, current_index - 1, next_carry);
}

/* * Main wrapper function for the recurisive C++ successor.
 * Returns true if an overflow occurred.
 */
bool bitstring_successor_recursive(std::string& bits) {
  if (bits.empty()){
    return false;
  }
  return increment_bit_recursive(bits, bits.length() - 1, 1);
}

int main() {
  // Test case 1: Standard recursive increment (11 -> 12)
  std::string binary_sample1 = "1011";

  std::cout <<"Before: " << binary_sample1 << std::endl;
  bool overflow1 = bitstring_successor_recursive(binary_sample1);
  std::cout << "After: " << binary_sample1 << "(Overflow: " << (overflow1 ? "Yes" : "No") << ")\n\n";

  //Test case 2: Edge case with global overflow (7 -> 0)
  std::string binary_sample2 = "111";

  std::cout << "Before: " << binary_sample2 << std::endl;
  bool overflow2 = bitstring_successor_recursive(binary_sample2);
  std::cout << "After: " << binary_sample2 << "(Overflow: " << (overflow2 ? "Yes" : "No") << ")" << std::endl;

  return 0;
}
