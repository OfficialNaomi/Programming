// Iterative successor function in Rust
// Modifies the String via mutable reference and returns true if an overflow occurred.
fn bitstring_successor_iterative(bits: &mut String) -> bool {
  if bits.is_empty() {
    return false;
  }

  // Connvert the UTF-8 String into a mutable Vector of chars for safe indexing
  let mut chars: Vec<char> = bits.chars().collect();

  // Iterate backwards from the last index to 0
  for i in (0..chars.len()).rev() {
    if chars[i] == '1' {
      chars[i] = '0'; // 1 + 1 = 0 (Carry)
    } else {
      chars[i] = '1'; // Found the first '0', consume carry

      // Reconstruct the string in place from the vector
      *bits = chars.into_iter().collect();
      return false; // Early exit: no global overflow
    }
  }

  // Reconstruct the string for the overflow case
  *bits = chars.into_iter().collect();
  true // Loop finished completely -> global overflow
}

fn main() {
  // Test case 1: Standard iterative increment (11 -> 12)
  let mut binary_sample1 = String::from("1011");
  println!("Before: {}", binary_sample1);
  let overflow1 = bitstring_successor_iterative(&mut binary_sample1);
  println!("After: {} (Overflow: {})\n", binary_sample1, if overflow1 { "Yes" } else { "No" });

  // Test case 2: Edge case with global overflow (7 -> 0)
  let mut binary_sample2 = String::from("111");
  println!("Before: {}", binary_sample2);
  let overflow2 = bitstring_successor_iterative(&mut binary_sample2);
  println!("After: {} (Overflow: {})", binary_sample2, if overflow2 { "Yes" } else { "No" });
}
