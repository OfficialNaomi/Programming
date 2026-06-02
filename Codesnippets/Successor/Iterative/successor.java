public class SuccessorIterative {

  /*
   * Iterative successor function.
   * Modifies the char array in place and returns true if a global overflow occurred.
   */
  public static boolean bitstringSuccessorIterative(char[] bits) {
    if (bits == null || bits.length == 0) {
      return false;
    }

    // Start at the rightmost index and iterate leftwards
    for  (int i = bits.length - 1; i >= 0; i--) {
      if (bits[i] == '1') {
        // 1 + 1 = 0 (Carry moves to the next bit)
        bits[i] = '0';
      } else {
        // Found the first '0'. 0 + 1 (from carry) = 1.
        // We consume the carry and stop immediately.
        bits[i] = '1';
        return false; // No global overflow
      }
    }

    // If the loop finishes completely, all bits were '1' (e.g., "111")
    return true; // Global overflow occurred
  }

public static void main(String[] args) {
  // Test case 1: Standard iterative increment (11 -> 12)
  String stringSample1 = "1011";
  char[] bits1 = stringSample1.toCharArray();

  System.out.println("Before: " + stringSample1);
  boolean overflow1 = bitstringSuccessorIterative(bits1);
  System.out.println("After: "+ new String(bits1) + " (Overflow: " + (overflow1 ? "Yes" : "No") + ")\n");

  // Test case 2: Edge case with global overflow (7 -> 0)
  String stringSample2 = "111";
  char[] bits2 = stringSample2.toCharArray();

  System.out.println("Before: " + stringSample2);
  boolean overflow2 = bitstringSuccessorIterative(bits2);
  System.out.println("After: " + new String(bits2) + " (Overflow: " + (overflow2 ? "Yes" : "No") + "\n");
  }
}
