#include <stdio.h>
#include <string.h>
#include <stdbool.h>

/* * Helper function that processes the string recursively.
 * Returns true if a global overflow occurs.
 */
bool successor_tail_optimized(char* bits, int index, int carry) {
    // Base Case 1: Carry is consumed. We are done.
    if (carry == 0) return false;
    
    // Base Case 2: Out of bounds + carry is 1. Overflow!
    if (index < 0) return true;

    if (bits[index] == '1') {
        bits[index] = '0';
        // Tail recursive call
        return successor_tail_optimized(bits, index - 1, 1);
    } else {
        bits[index] = '1';
        // EARLY EXIT: We halt the function calls here. No further stack growth.
        return false;
    }
}

/* * Main wrapper function for the recursive successor.
 * Modifies the string in place and returns true if an overflow occured.
 */
bool bitstring_successor_recursive(char* bits, int length){
  // Start at the rightmost bit (length -1) with an initial carry of 1 (for +1)
  return successor_tail_optimized(bits, length -1, 1);
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
