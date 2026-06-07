using System;

class SuccessorRecursive
{
      /*
       * Helper method that processes the charact er array from right to left recursively.
       * current_index: The position in the array we are currently processing.
       * carry: The incoming carry bit from the lower layer.
       */
      private static bool IncrementBitRecursive(char[] bits, int current_index, int carry)
      {
        // Base Case: We passed the leftmost bit (index 0)
        if (current_index  < 0)
        {
          // If carry is still 1, a global overflow occurred
          return carry == 1;
        }

        // Convert character ('0' or '1') to integer (0 or 1)
        int current_bit = bits[current_index] == '1' ? 1 : 0;

        //Apply hardware gate logic
        int new_bit = current_bit ^ carry; // XOR gate for the new bit value
        int next_carry = current_bit & carry; // AND gate for the next carry layer

        // Write the result back into the array as a character 
        bits[current_index] = new_bit == 1  ? '1' : '0';

        // Tail Recursion: Move left to the next bit position
        return IncrementBitRecursive(bits, current_index - 1, next_carry);
    }

    /*
     * Main wrapper method for the recursive C# successor.
     * Modifies the string in place (via char array) and returns true if an overflow occurs.
     */
     public static bool BitstringSuccessorRecursive(ref string bits)
    {
        if (string.IsNullOrEmpty(bits))
            {
                return false;
            }

        //Convert string to a mutable char array for efficient modification
        char[] charArray = bits.ToCharArray();

        //Start at the rightmost index with an initial carry of 1
        bool overflow = IncrementBitRecursive(charArray, charArray.Length - 1, 1);

        //Reconstruct the string from the modified array
        bits = new string(charArray);

        return overflow;
    }

    static void Main()
    {
        //Test case 1: Standard recursive increment (11 -> 12)
        string binarySample1 = "1011";
        Console.WriteLine($"Before: {binarySample1}");
        bool overflow1 = BitstringSuccessorRecursive(ref binarySample1);
        Console.WriteLine( $"After: {binarySample1} (Overflow: {(overflow1 ? "Yes" : "No")})");

        //Test case 2: Edge case with global overflow (7 -> 0)
        string binarySample2 = "111";
        Console.WriteLine($"Before: {binarySample2}");
        bool overflow2 = BitstringSuccessorRecursive(ref binarySample2);
        Console.WriteLine($"After: {binarySample2} (Overflow: {(overflow2 ? "Yes" : "No")})");
    }
}
