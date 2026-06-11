#include <iostream>
#include <string>

// Now returns bool to pass the overflow status back up the stack
bool successorTailOptimized(std::string& bits, int index, int carry = 1) {
    // Base Case 1: Carry is completely consumed. No overflow.
    if (carry == 0) return false;
    
    // Base Case 2: Out of bounds but carry is still 1 -> OVERFLOW!
    if (index < 0) return true;

    if (bits[index] == '1') {
        bits[index] = '0';
        // Tail recursive call, passing the result (overflow status) up
        return successorTailOptimized(bits, index - 1, 1);
    } else {
        bits[index] = '1';
        // EARLY EXIT: Carry consumed, recursion stops instantly, no overflow.
        return false;
    }
}

/* * Main wrapper function for the recursive C++ successor.
 * Returns true if an overflow occurred.
 */
bool bitstring_successor_recursive(std::string& bits) {
    if (bits.empty()){
        return false;
    }
    return successorTailOptimized(bits, bits.length() - 1, 1);
}

int main() {
    // Test case 1: Standard recursive increment (1011 -> 1100)
    std::string binary_sample1 = "1011";

    std::cout << "Before: " << binary_sample1 << std::endl;
    bool overflow1 = bitstring_successor_recursive(binary_sample1);
    std::cout << "After:  " << binary_sample1 << " (Overflow: " << (overflow1 ? "Yes" : "No") << ")\n\n";

    // Test case 2: Edge case with global overflow (111 -> 000)
    std::string binary_sample2 = "111";

    std::cout << "Before: " << binary_sample2 << std::endl;
    bool overflow2 = bitstring_successor_recursive(binary_sample2);
    std::cout << "After:  " << binary_sample2 << " (Overflow: " << (overflow2 ? "Yes" : "No") << ")" << std::endl;

    return 0;
}
