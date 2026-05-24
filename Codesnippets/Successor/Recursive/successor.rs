/* * Helper function that processes the byte vector from right to left recursively
 * In Rust, we use 'isize' for indices because it can become negative (-1),
 * whereas 'usize' cannot go below zero.
 */

fn increment_bit_recursive(bits: &mut Vec<u8>, current_index: isize, carry: u8) -> bool {
  // Base Case: We passed the leftmost bit
  if current_index <0 {
      return carry == 1;
  }

  // Convert the ASCII byte (48 for '0', 49 for '1') to a raw integer (0 or 1`) 
  let current_bit = bits[current_index as usize] - b'0';

  // Apply hardware gate logic using Rust's bitwise operators
  let new_bit = current_bit ^ carry; //XOR gate
  let next_carry = current_bit & carry; // AND gate

  // Convert the integer result back to the ASCII byte and write it in place
  bits[current_index as usize] = new_bit + b'0';

  // Tail Recursion: Move left to the next position
  increment_bit_recursive(bits, current_index - 1, next_carry)
}

/* * Main wrapper function for the recursive Rust successor.
 * Takes a mutable reference to a String and modifies it in place.
 */
pub fn bitstring_successor_recursive(bits: &mut String) -> bool {
  if bits.is_empty(){
    return false;
  }

  // Convert the string into a raw byte vector for safe and fast in-place mutation
  let mut byte_vec = unsafe { bits.as_mut_vec().clone()};

  // Start at the rightmost index (length -1) as a signed pointer (isize)
  let start_index = (bits.len() as isize) - 1;

  let overflow = increment_bit_recursive(&mut byte_vec, start_index, 1);

  // Reconstruct the original string from the modified byte vector
  *bits = String::from_utf8(byte_vec).unwrap();

  overflow
}

fn main() {
  // Test case 1: Standard recursive increment (11 -> 12)
  let mut binary_sample1 = String::from("1011");
  println!("Before: {}", binary_sample1);
  let overflow1 = bitstring_successor_recursive(&mut binary_sample1);
  println!("After: {} (Overflow: {}\n", binary_sample1, overflow1);

  // Test case 2: Edge case with global overflow (7 -> 0)
  let mut binary_sample2 = String::from("111");
  println!("Before: {}", binary_sample2);
  let overflow2 = bitstring_successor_recursive(&mut binary_sample2);
  println!("After: {} (Overflow: {})", binary_sample2, overflow2);
}
