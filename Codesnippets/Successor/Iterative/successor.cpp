#include <iostream>
#include <string>

/* * Iterative successor function.
 * Modifies the string in place and returns true if an overflow occurred.
 */
bool bitstring_successor_iterative(std::string& bits){
  if (bits.empty()){
    return false;
  }

  // Start at the rightmost bit and move left
  for (int i = bits.length() - 1; i >= 0; i--) {
    if (bits[i] == '1') {
      // The bit is 1, so 1 + 1 = 0 with a carry of 1.
      // We set it to 0 and let the loop continue to the next bit.
      bits[i] = '0';
    } else {
      // We found the first '0'. 0 + 1 (carry) = 1;
      // The carry is now consumed (0), so we can stop immediately!
      bits[i] = '1';
      return false; // No global overflow
    }
  }

  // If the loop finishes completely without hitting a 'return false',
  // it means every single bit was a '1' (e.g., "1111").
  return true; // Global overflow occurred
}

int main() {
  // Test case 1: Standard iterative increment (11 -> 12)
  std::string binary_sample1 = "1011";

  std::cout << "Before: " << binary_sample1 << std::endl;
  bool overflow1 = bitstring_successor_iterative(binary_sample1);
  std::cout << "After: " << binary_sample1 << " (Overflow: " << (overflow1 ? "Yes" : "No") << ")\n\n";

  // Test case 2: Edge case with global overflow (7 -> 0)
  std::string binary_sample2 = "111";

  std::cout << "Before: " << binary_sample2 << std::endl;
  bool overflow2 = bitstring_successor_iterative(binary_sample2);
  std::cout << "After: " << binary_sample2 << " (Overflow: " << (overflow2 ? "Yes" : "No") << ")\n\n";

  return 0;
}
