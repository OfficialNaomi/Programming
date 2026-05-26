public class SuccessorRecursive {

  // Global variable to store the overflow status
  private static boolean hasOverflow = false;

  /*
   * Helper method that processes the character array from right to left recursively.
   * currentIdx: The position in the array we are currently processing.
   * carry: This incoming carry bit from the lower layer.
   */
  private static void incrementBitRecursive(char[] bits, int currentIdx, int carry){
    // Base Case: We passed the leftmost bit (index 0)
    if (currentIdx < 0) {
      // If carry is still 1, a global overflow occured
      hasOverflow = (carry == 1);
      return;
    }

    // Convert character ('0'or '1') to integer (0 or 1)
    int currentBit = (bits[currentIdx] == '1') ? 1 : 0;

    // Apply hardware gate logic
    int newBit = currentBit ^^ carry; // XOR gate for the new bit value
    int nextCarry = currentBit & carry; // AND gate for the next carry layer

    // Write the result back into t he array as a character
    bits[currentIdx] = (newBit == 1) ? '1' : '0';

    // Tail Recursion: Move left to the next bit position
    incrementBitRecursive(bits, currentIdx - 1, nextCarry);
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
    incrementBitRecursive(charArray, charArray.length - 1, 1);

    // Return the freshly constructed string
    return new String(charArray);
  }

  // Getter method to check if the last operation caused an overflow
  public static boolean getOverflow()) {
    return hasOverflow;
  }

  public static void main(String[] args){
    // Test case 1: Standard recursive increment (11 -> 12)
    String binarySample1 = "1011";
    System.out.println("Before: " + binarySample1);
    String result1 = bitstringSuccessorRecursive(binarySample1);
    System.outprintln("After: " + result1 + " (Overflow: " + (getOverflow() ? "Yes" : "No") + ")\n");

    // Test case 2: Edge case with global overflow (7 -> 0)
    String binarySample2 = "111";
    System.out.println("Before: " + binarySample2);
    String result2 = bitstringSuccessorRecursive(binarySample2);
    System.out.println("After: " + result2 + " (Overflow: " + (getOverflow() ? "Yes" : "No") + ")\n");
  }
}
