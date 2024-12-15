//! Sample functions for benchmarking

pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

pub fn subtract(a: i32, b: i32) -> i32 {
    a - b
}

pub fn multiply(a: i32, b: i32) -> i32 {
    a * b
}

pub fn divide(a: i32, b: i32) -> Option<i32> {
    if b == 0 {
        None
    } else {
        Some(a / b)
    }
}

pub fn factorial(n: u32) -> u32 {
    match n {
        0 | 1 => 1,
        _ => n * factorial(n - 1),
    }
}

pub fn fibonacci(n: u32) -> u32 {
    match n {
        0 => 0,
        1 => 1,
        _ => fibonacci(n - 1) + fibonacci(n - 2),
    }
}

pub fn is_prime(n: u32) -> bool {
    if n <= 1 {
        return false;
    }
    for i in 2..=(n as f64).sqrt() as u32 {
        if n % i == 0 {
            return false;
        }
    }
    true
}

pub fn gcd(a: u32, b: u32) -> u32 {
    if b == 0 {
        a
    } else {
        gcd(b, a % b)
    }
}

pub fn lcm(a: u32, b: u32) -> u32 {
    a * b / gcd(a, b)
}

pub fn power(base: i32, exp: u32) -> i32 {
    match exp {
        0 => 1,
        1 => base,
        _ => base * power(base, exp - 1),
    }
}
