// PWN04 - Access System
// Category: Binary & Exploitation (Rust) - Integer Wrapping / Logic Flaw
// Difficulty: Medium
//
// Story: A badge-access terminal. New employees start with a small
// number of "access credits" (u8). Each failed door swipe costs you
// a credit. Admin console only unlocks once your credit balance
// reads exactly 255 (0xFF) -- which should be unreachable by
// spending credits down from a small starting value... unless you
// can make the subtraction wrap around.
//
// Intended solution: the program is compiled in --release mode,
// where Rust's integer overflow checks are DISABLED by default
// (they only panic in debug builds). So `credits -= 1` on a `u8`
// that is already 0 silently wraps to 255 instead of panicking,
// instantly satisfying the "== 255" admin check.
//
// This teaches: not every bug is memory-unsafe. Rust's type safety
// doesn't save you from integer wraparound in release builds, and a
// pure logic/arithmetic flaw can be just as exploitable as a buffer
// overflow.

use std::io::{self, Write};

fn read_line(prompt: &str) -> String {
    print!("{prompt}");
    io::stdout().flush().unwrap();
    let mut buf = String::new();
    io::stdin().read_line(&mut buf).unwrap();
    buf.trim().to_string()
}

fn print_flag() {
    match std::fs::read_to_string("flag.txt") {
        Ok(flag) => println!("{}", flag.trim()),
        Err(_) => println!("[!] flag.txt not found on this host."),
    }
}

fn main() {
    let mut credits: u8 = 3; // small starting balance, on purpose

    println!("=== ACCESS SYSTEM ===");
    println!("Starting access credits: {credits}");
    println!("Each failed door swipe costs 1 credit.");
    println!("Admin console unlocks automatically at 255 credits");
    println!("(don't worry, that's not reachable from 3... right?)\n");

    loop {
        println!("\nCurrent credits: {credits}");
        println!("[1] Attempt door swipe (uses 1 credit)");
        println!("[2] Check admin console");
        println!("[3] Exit");
        let choice = read_line("> ");

        match choice.as_str() {
            "1" => {
                // BUG: plain `-=` on a u8 in release mode wraps
                // silently instead of panicking or being clamped.
                // Should have been credits.saturating_sub(1) or a
                // checked_sub with a guard.
                credits -= 1;
                println!("Swipe failed. Credits remaining: {credits}");
            }
            "2" => {
                if credits == 255 {
                    println!("\n[!] Admin console unlocked!");
                    print_flag();
                } else {
                    println!("Access denied. ({credits} != 255)");
                }
            }
            "3" => {
                println!("Goodbye.");
                break;
            }
            _ => println!("Invalid option."),
        }
    }
}
