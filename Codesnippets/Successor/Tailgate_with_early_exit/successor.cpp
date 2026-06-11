#include <iostream>
#include <string>

// Passing the string by reference to modify it directly
void successorTailOptimized(std::string& bits, int index, int carry = 1) {
    // Base Case: Out of bounds or carry consumed
    if (index < 0 || carry == 0) return;

    if (bits[index] == '1') {
        bits[index] = '0';
        // Tail recursive call
        successorTailOptimized(bits, index - 1, 1);
    } else {
        bits[index] = '1';
        // EARLY EXIT: We stop the recursion chain instantly.
        return;
    }
}

/* * Main wrapper function for the recurisive C++ successor.
 * Returns true if an overflow occurred.
 */
bool bitstring_successor_recursive(std::string& bits) {
  if (bits.empty()){
    return false;
  }
  return successorTailOptimized(bits, bits.length() - 1, 1);
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
