/* * Helper function that processes the char vector from right to left recursively.
 * Returns true if an overflow occurred, false otherwise.
 */
fn successor_tail_optimized(bits: &mut Vec<char>, index: isize, carry: u8) -> bool {
    // Base Case 1: Carry is consumed. No overflow.
    if carry == 0 { 
        return false; 
    }
    
    // Base Case 2: Out of bounds but carry is still 1 -> OVERFLOW!
    if index < 0 { 
        return true; 
    }

    let i = index as usize;

    if bits[i] == '1' {
        bits[i] = '0';
        // Tail recursive call, passing the overflow status up
        return successor_tail_optimized(bits, index - 1, 1);
    } else {
        bits[i] = '1';
        // EARLY EXIT: We halt the function calls here. No overflow.
        return false;
    }
}

/* * Main wrapper function for the recursive Rust successor.
 * Takes a mutable reference to a String and modifies it in place.
 */
pub fn bitstring_successor_recursive(bits: &mut String) -> bool {
    if bits.is_empty() {
        return false;
    }

    // Safe conversion to a char vector instead of unsafe byte manipulation
    let mut char_vec: Vec<char> = bits.chars().collect();

    // Start at the rightmost index (length - 1) as a signed pointer (isize)
    let start_index = (char_vec.len() as isize) - 1;

    // Perform the recursive calculation and catch the overflow
    let overflow = successor_tail_optimized(&mut char_vec, start_index, 1);

    // Reconstruct the original string safely from the char vector
    *bits = char_vec.into_iter().collect();

    overflow
}

fn main() {
    // Test case 1: Standard recursive increment (1011 -> 1100)
    let mut binary_sample1 = String::from("1011");
    println!("Before: {}", binary_sample1);
    let overflow1 = bitstring_successor_recursive(&mut binary_sample1);
    println!("After:  {} (Overflow: {})\n", binary_sample1, overflow1);

    // Test case 2: Edge case with global overflow (111 -> 000)
    let mut binary_sample2 = String::from("111");
    println!("Before: {}", binary_sample2);
    let overflow2 = bitstring_successor_recursive(&mut binary_sample2);
    println!("After:  {} (Overflow: {})", binary_sample2, overflow2);
}
