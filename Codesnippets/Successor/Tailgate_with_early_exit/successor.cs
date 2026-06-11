using System;

class SuccessorRecursive
{
      /* * Recursive helper that returns true if an overflow occurred.
     */
    public static bool SuccessorTailOptimized(char[] bits, int index, int carry) {
        // Base Cases
        if (carry == 0) return false;
        if (index < 0) return true;

        if (bits[index] == '1') {
            bits[index] = '0';
            // Tail recursive call
            return SuccessorTailOptimized(bits, index - 1, 1);
        } else {
            bits[index] = '1';
            // EARLY EXIT: Stop recursion instantly.
            return false;
        }
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
        bool overflow = SuccessorTailOptimized(charArray, charArray.Length - 1, 1);

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
