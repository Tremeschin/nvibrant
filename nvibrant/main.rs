#![allow(dead_code)]
#![allow(non_snake_case)]
#![allow(non_upper_case_globals)]
#![allow(non_camel_case_types)]
mod driver;

// Fixme: How to dynamically use at runtime?
// Use latest driver for reference
use driver::v590_48_01::*;

fn main() {
    println!("Hello, world!");
}
