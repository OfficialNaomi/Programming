#include <stdio.h>
#include <string.h>
#include <stdbool.h>

/* * Iterative successor function.
 * Modifies the string in place and returns true if an overflow occurred.
 */
bool bitstring_successor_iterative(char* bits, int length){
  // Start at the rightmost bit and move left
  for(int i = length - 1; i >= 0; i--){
    if(bits[i] == '1'){
      // The bit is 1, so 1 + 1 = 0 with a carry of 1.
      // We set it to 0 and let the loop continue to the next bit.
      bits[i] = '0';
    }else {
      // We found the first '0'. 0 + 1 (carry) = 1.
      // The carry is now consumed (0), so we can stop immediately!
      bits[i] = '1';
      return false; // No global overflow
    }
  }

  // If the loop finishes completely without hitting a 'return false',
  // it means every single bit was a '1' (e.g., "1111").
  return true; // Global overflow occurred
}

int main(){
  // Test case 1: Standard iterative increment (11 -> 12)
  char binary_sample1[] = "1011";
  int length1 = strlen(binary_sample1);

  printf("Before: %s\n", binary_sample1);
  bool overflow1 = bitstring_successor_iterative(binary_sample1, length1);
  printf("After: %s (Overflow: %s)\n\n", binary_sample1, overflow1 ? "Yes": "No");

  // Test case 2: Edge case with global overflow (7 -> 0)
  char binary_sample2[] = "111";
  int length2 = strlen(binary_sample2);

  printf("Before: %s\n", binary_sample2);
  bool overflow2 = bitstring_successor_iterative(binary_sample2, length2);
  printf("After: %s (Overflow: %s)\n", binary_sample2, overflow2 ? "Yes" : "No");

  return 0;

}
