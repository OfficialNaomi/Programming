#include <stdio.h>
#include <string.h>
#include <stdbool.h>

/* * Helper function that processes the bitstring from right to left recursively
 * current_index: The bit position we are currently looking at.
 * carry: The incoming carry bit from the previous (lower) layer
 */
bool increment_bit_recursive(char* bits, int current_index, int carry) {
  // Base Case: We passed the leftmost bit (index 0)
  if (current_index < 0) {
    // If carry is still 1, a global overflow occurred
    return (carry == 1);
  }

  // Convert character ('0' or '1') to integer (0 or 1) for bitwise logic
  int current_bit = bits[current_index] - '0';

  // Apply hardware gate logic:
  // XOR determines the new value of the current bit
  int new_bit = current_bit ^carry;

  // AND determines if a carry propagates to the next layer on the left
  int next_carry = current_bit & carry;

  // Write the result back as a character
  bits[current_index] = new_bit + '0';

  // Tail Recursion: Move to the next bit on the left, passing the new carry
  return increment_bit_recursive(bits, current_index - 1, next_carry);
}

/* * Main wrapper function for the recursive successor.
 * Modifies the string in place and returns true if an overflow occured.
 */
bool bitstring_successor_recursive(char* bits, int length){
  // Start at the rightmost bit (length -1) with an initial carry of 1 (for +1)
  return increment_bit_recursive(bits, length -1, 1);
}

int main() {
  // Test case 1: Standard recursive increment (11 -> 12)
  char binary_sample1[] =  "1011";
  int length1 = strlen(binary_sample1);

  printf("Before: %s\n", binary_sample1);
  bool overflow1 = bitstring_successor_recursive(binary_sample1, length1);
  printf("After: %s (Overflow: %s)\n\n", binary_sample1, overflow1 ? "Yes" : "No");

  //Test case 2: Edge case with gloval overflow (7 -> 0)
  char binary_sample2[] = "111";
  int length2 = strlen(binary_sample2);

  printf("Before: %s\n", binary_sample2);
  bool overflow2 = bitstring_successor_recursive(binary_sample2, length2);
  printf("After: %s (Overflow: %s)\n", binary_sample2, overflow2 ? "Yes" : "No");

  return 0;
}
