from fractions import Fraction
import re

NUMBER_RE = re.compile(r"^([1-9][0-9]*)$")
MIXED_RE = re.compile(r"^([1-9][0-9]*)[ ]+([1-9][0-9]*)/([1-9][0-9]*)$")
FRACTION_RE = re.compile(r"^([1-9][0-9]*)/([1-9][0-9]*)$")

def parse_amount(amount):
    match = NUMBER_RE.match(amount)
    if match:
        return Fraction(int(match.group(1)))
    match = FRACTION_RE.match(amount)
    if match:
        return Fraction(int(match.group(1)), int(match.group(2)))
    match = MIXED_RE.match(amount)
    if match:
        return Fraction(int(match.group(1))) + Fraction(int(match.group(2)), int(match.group(3)))
    raise ValueError("Invalid amount")

def fraction_to_mixed(fraction):
    mixed_number = []
    whole_number = fraction.numerator // fraction.denominator
    new_numerator = fraction.numerator % fraction.denominator
    if whole_number > 0:
        mixed_number.append(str(whole_number))
    if new_numerator > 0:
        mixed_number.append(str(new_numerator) + "/" + str(fraction.denominator))
    return " ".join(mixed_number)
