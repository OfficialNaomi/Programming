public class SuccessorRecursive {

  // Global variable to store the overflow status
  private static boolean hasOverflow = false;

  /*
   * Helper method that processes the character array from right to left recursively.
   * currentIdx: The position in the array we are currently processing.
   * carry: This incoming carry bit from the lower layer.
   */
  public static void successorTailOptimized(char[] bits, int index, int carry) {
        // Base Case
        if (index < 0 || carry == 0) return;

        if (bits[index] == '1') {
            bits[index] = '0';
            // Tail recursive call
            successorTailOptimized(bits, index - 1, 1);
        } else {
            bits[index] = '1';
            // EARLY EXIT: Instant stop, no further calls.
            return;
        }
    }

  /* 
   * Main wrapper method for the recursive Java successor.
   * Returns the modified binary string.
   */
  public static String bitstringSuccessorRecursive(String bits){
    if (bits == null || bits.isEmpty()){
      hasOverflow = false;
      return bits;
    }

    // Convert string to a mutable char array
    char[] charArray = bits.toCharArray();

    // Reset the global overflow flag before calculation
    hasOverflow = false;

    // Start at the rightmost index with an initial carry of 1
    successorTailOptimized(charArray, charArray.length - 1, 1);

    // Return the freshly constructed string
    return new String(charArray);
  }

  // Getter method to check if the last operation caused an overflow
  public static boolean getOverflow() {
    return hasOverflow;
  }

  public static void main(String[] args){
    // Test case 1: Standard recursive increment (11 -> 12)
    String binarySample1 = "1011";
    System.out.println("Before: " + binarySample1);
    String result1 = bitstringSuccessorRecursive(binarySample1);
    System.out.println("After: " + result1 + " (Overflow: " + (getOverflow() ? "Yes" : "No") + ")\n");

    // Test case 2: Edge case with global overflow (7 -> 0)
    String binarySample2 = "111";
    System.out.println("Before: " + binarySample2);
    String result2 = bitstringSuccessorRecursive(binarySample2);
    System.out.println("After: " + result2 + " (Overflow: " + (getOverflow() ? "Yes" : "No") + ")\n");
  }
}
