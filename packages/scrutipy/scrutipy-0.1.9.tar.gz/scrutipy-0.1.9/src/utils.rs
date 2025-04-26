use crate::rounding::*;
use crate::sd_binary::*;
use regex::Regex;
// 124-125, 127-128, 130-132, 134-138
const FUZZ_VALUE: f64 = 1e-12;

/// Fuzzes the value of a float by 1e-12
///
/// Parameters:
///     x: floating-point number
///
/// Returns:
///     a vector of 2 floating-point numbers
///
/// Raises:
///     ValueError: If x is not a floating-point number
pub fn dustify(x: f64) -> Vec<f64> {
    vec![x - FUZZ_VALUE, x + FUZZ_VALUE]
}

/// Returns the number of values after the decimal point, or else None if there are no such values,
/// no decimal, or if the string cannot be converted to a numeric type
///
/// Note that this function will only record the number of values after the first decimal point
/// ```
/// let num_decimals = crate::decimal_places_scalar(Some("1.52.1"), ".");
/// assert_eq!(num_decimals, Some(2));
/// ```
pub fn decimal_places_scalar(x: Option<&str>, sep: &str) -> Option<i32> {
    let s = x?;

    let pattern = format!(r"{}(\d+)", regex::escape(sep));
    let re = Regex::new(&pattern).ok()?;
    let caps = re.captures(s)?;

    caps.get(1).map(|c| c.as_str().len() as i32)
}

use thiserror::Error;

#[derive(Debug, Error)]
pub enum ReconstructSdError {
    #[error("{0} is not a number")]
    NotANumber(String),
    #[error("{0} is not a formula")]
    NotAFormula(String),
    #[error("Inputs to reconstruct_sd_scalar failed. The reconstruction formula {0} was called but resulted in a {1}")]
    SdBinaryError(String, SdBinaryError),
    // complete this so that the error propagates from the function below
}

pub fn reconstruct_sd_scalar(
    formula: &str,
    x: &str,
    n: u32,
    zeros: u32,
    ones: u32,
) -> Result<f64, ReconstructSdError> {
    let x_num: f64 = match x.parse() {
        Ok(num) => num,
        Err(string) => return Err(ReconstructSdError::NotANumber(string.to_string())),
    };

    let sd_rec: Result<f64, SdBinaryError> = match formula {
        "mean_n" => sd_binary_mean_n(x_num, n),
        "mean" => sd_binary_mean_n(x_num, n), // convenient aliases
        "0_n" => sd_binary_0_n(zeros, n),
        "0" => sd_binary_0_n(zeros, n), // convenient aliases
        "1_n" => sd_binary_1_n(ones, n),
        "1" => sd_binary_1_n(ones, n), // convenient aliases
        "groups" => sd_binary_groups(zeros, ones),
        "group" => sd_binary_groups(zeros, ones), // convenient aliases
        _ => return Err(ReconstructSdError::NotAFormula(formula.to_string())),
    };

    match sd_rec {
        Ok(num) => Ok(num),
        Err(e) => Err(ReconstructSdError::SdBinaryError(formula.to_string(), e)),
    }
}

//to_round <- number * 10^(decimals + 1) - floor(number * 10^(decimals)) * 10
//    number_rounded <- ifelse(to_round == 5,
//                             floor(number * 10^decimals) / 10^decimals,
//                             round(number, digits = decimals))
//    return(number_rounded)

pub fn check_threshold_specified(threshold: f64) {
    if threshold == 5.0 {
        panic!("Threshold must be set to some number other than its default, 5.0");
    }
}

/// reconstruct_rounded_numbers fn for reround
/// notably the R version of this function can take a vector as x or a scalar, we
/// should probably turn this into taking a vector with at least one element, and that means the
/// rounding functions also need to be updated to do that
/// but both this and the vectorized version return doubles, and the same number of them, just in a
/// different format
pub fn reconstruct_rounded_numbers_scalar(
    x: f64,
    digits: i32,
    rounding: &str,
    threshold: f64,
    symmetric: bool,
) -> Vec<f64> {
    // requires the round_up and round_down functions
    match rounding {
        "up_or_down" => vec![round_up(x, digits), round_down(x, digits)], // this is supposed to
        // contain a `symmetric` argument in the R code, but that's not present in the definition
        // for round up and round down ??
        "up_from_or_down_from" => {
            check_threshold_specified(threshold); // untested
            vec![
                round_up_from(vec![x], digits, threshold, symmetric)[0], // untested
                round_down_from(vec![x], digits, threshold, symmetric)[0], // this is a hacky // untested
                                                                           // solution to suppress the errors while we're migrating this from scalar to
            ]
        }
        "ceiling_or_floor" => vec![round_ceiling(x, digits), round_floor(x, digits)],
        "even" => vec![rust_round(x, digits)],
        "up" => vec![round_up(x, digits)], // supposed to have a symmetric keyword, but round up
        // definition doesn't have it, ???
        "down" => vec![round_down(x, digits)], // supposed to have a symmetric keyword, but round down definition doesn't have it ??? // untested
        "up_from" => {
            check_threshold_specified(threshold);
            round_up_from(vec![x], digits, threshold, symmetric)
        }
        "down_from" => {
            check_threshold_specified(threshold);
            vec![round_down_from(vec![x], digits, threshold, symmetric)[0]]
        }
        "ceiling" => vec![round_ceiling(x, digits)],
        "floor" => vec![round_floor(x, digits)], // untested
        "trunc" => vec![round_trunc(x, digits)], // untested
        "anti_trunc" => vec![round_anti_trunc(x, digits)], // untested
        _ => panic!("`rounding` must be one of the designated string keywords"), // untested
    }
}

/// the reround function
/// redo so that it just takes a vec instead of a vec of vec, the R version can take arbitrarily
/// nested vectors, but it's the same as just flattening the input into a single vector
pub fn reround(
    x: Vec<f64>,
    digits: i32,
    rounding: &str,
    threshold: f64,
    symmetric: bool,
) -> Vec<f64> {

    x.iter()
        .flat_map(|&x| {
            reconstruct_rounded_numbers_scalar(x, digits, rounding, threshold, symmetric)
        })
        .collect()
        // this is the root, we need to have it zip across multiple rounding options, returning a
    // vec of vec, where the inner vector includes all the rounded numbers for a given rounding
    // scheme, and the outer vector includes a vector for each rounding scheme
   
}

/// check rounding singular, necessary for the reround function
pub fn check_rounding_singular(
    rounding: Vec<&str>,
    bad: &str,
    good1: &str,
    good2: &str,
) -> Result<(), String> {
    if rounding.contains(&bad) {
        Err(format!("If rounding has length > 1, only single rounding procedures are supported, such as {good1} and {good2}. Instead, rounding was given as {bad} plus others. You can still concatenate multiple of them; just leave out those with 'or'."))
    } else {
        Ok(())
    }
}

