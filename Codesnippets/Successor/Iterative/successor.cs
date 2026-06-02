using System;

class SuccessorIterative
{
  /* 
   * Iterative successor function.
   * Modifies the string via ref and returns true if a global overflow occurred.
   */
  public static bool BitstringSuccessorIterative(ref string bits)
  {
    if (string.IsNullOrEmpty(bits))
    {
      return false;
    }

    // Convert string to a mutable char array
    char[] charArray = bits.ToCharArray();

    // Start at the rightmost index and iterate leftwards
    for (int i = charArray.Length - 1; i >= 0; i--)
    {
      if(charArray[i] == '1')
      {
        // 1 + 1 = 0 (Carry moves to the next bit)
        charArray[i] = '0';
      }
      else
      {
        // Found the first '0'. 0 + 1 (from carry) = 1.
        // We consume the carry and stop immediately.
        charArray[i] = '1';

        // Reconstruct the string and return
        bits = new string(charArray);
        return false; // No global overflow
      }
    }

    // If the loop finishes completely, all bits were '1' (e.g., "111")
    bits = new string(charArray);
    return true; // Global overflow occurred
  }

  static void Main()
  {
    // Test case 1: Standard iterative increment (11 -> 12)
    string binarySample1 = "1011";
    Console.WriteLine($"Before: {binarySample1}");
    bool overflow1 = BitstringSuccessorIterative(ref binarySample1);
    Console.WriteLine($"After: {binarySample1} (Overflow: {(overflow1 ? "Yes" : "No")})\n");

    // Test case 2: Edge case with global overflow (7 -> 0)
    string binarySample2 = "111";
    Console.WriteLine($"Before: {binarySample2}");
    bool overflow2 = BitstringSuccessorIterative(ref binarySample2);
    Console.WriteLine($"After: {binarySample2} (Overflow: {(overflow2 ? "Yes" : "No")})");
  }
}
