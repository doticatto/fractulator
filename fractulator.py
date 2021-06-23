#!/usr/bin/env python
from sys import argv

__author__ = "John Mahoney"


def gcf(a, b):
    if abs(a) < abs(b):
        x = a
        y = b
    else:
        x = b
        y = a

    y = y % x

    if y == 0:
        return abs(x)

    return gcf(x, y)


def lcm(a, b):
    return int(a / gcf(a, b) * b)


class Fraction:
    def __init__(self, numerator, denominator, simplify=False):
        self.numerator = int(numerator)
        self.denominator = int(denominator)
        if self.denominator == 0:
            raise ZeroDivisionError("Cannot have 0 as a denominator.")
        if simplify:
            self.simplify()

    def simplify(self):
        self_simplified = self.simplified()
        self.numerator = self_simplified.numerator
        self.denominator = self_simplified.denominator

    def simplified(self):
        scalar = gcf(self.numerator, self.denominator)
        numerator = int(self.numerator / scalar)
        denominator = int(self.denominator / scalar)
        if denominator < 0:
            numerator *= -1
            denominator *= -1
        return Fraction(numerator, denominator)

    def scale(self, scalar):
        return Fraction(self.numerator * scalar, self.denominator * scalar)

    def inverse(self, simplify=False):
        return Fraction(self.denominator, self.numerator, simplify=simplify)

    def normalize(self, other):
        if not self.is_normalized(other):
            lcm_denominator = lcm(self.denominator, other.denominator)
            self_scale = lcm_denominator / self.denominator
            other_scale = lcm_denominator / other.denominator
            return self.scale(self_scale), other.scale(other_scale)
        return self, other

    def is_normalized(self, other):
        return self.denominator == other.denominator

    def __add__(self, other):
        self_scaled, other_scaled = self.normalize(other)
        return Fraction(
            self_scaled.numerator + other_scaled.numerator,
            self_scaled.denominator,
            simplify=True,
        )

    def __sub__(self, other):
        self_scaled, other_scaled = self.normalize(other)
        return Fraction(
            self_scaled.numerator - other_scaled.numerator,
            self_scaled.denominator,
            simplify=True,
        )

    def __mul__(self, other):
        return Fraction(
            self.numerator * other.numerator,
            self.denominator * other.denominator,
            simplify=True,
        )

    def __truediv__(self, other):
        return self * other.inverse()

    def __eq__(self, other):
        if not self.is_normalized(other):
            self_normalized, other_normalized = self.normalize(other)
            return self_normalized == other_normalized

        return self.numerator == other.numerator

    def __str__(self):
        if self.numerator == 0:
            return "0"
        if abs(self.numerator) >= abs(self.denominator):
            whole_part = int(self.numerator / self.denominator)
            numerator = self.numerator - (whole_part * self.denominator)
            if numerator == 0:
                return str(whole_part)
            if whole_part < 0 and numerator < 0:
                numerator *= -1
            return f"{whole_part}_{numerator}/{self.denominator}"

        return f"{self.numerator}/{self.denominator}"

    def __repr__(self):
        return str(self)

    @classmethod
    def parse(cls, input_str):
        parsed = input_str.split("_")
        whole = 0
        if len(parsed) == 2:
            try:
                whole = int(parsed[0])
            except ValueError:
                raise ValueError(f"Invalid fraction input: {input_str}")
            fraction = parsed[1]
        elif len(parsed) != 1:
            raise ValueError(f"Invalid fraction input: {input_str}")
        else:
            fraction = input_str

        fraction_parsed = fraction.split("/")
        if len(fraction_parsed) == 1:
            try:
                whole = int(fraction_parsed[0])
            except ValueError:
                raise ValueError(f"Invalid fraction input: {input_str}")
            return cls(whole, 1)

        try:
            denominator = int(fraction_parsed[1])
            numerator = int(fraction_parsed[0])
        except ValueError:
            raise ValueError(f"Invalid fraction input: {input_str}")

        return_fraction = Fraction(numerator, denominator, simplify=True)
        if return_fraction.numerator < 0 and whole != 0:
            raise ValueError(
                f"Invalid fraction input: {input_str}: Please input negative mixed fractions with the "
                "minus sign at the beginning to reduce ambiguity "
                f"(i.e. -{abs(whole)}_{abs(numerator)}/{abs(denominator)})"
            )

        if whole < 0:
            return_fraction *= Fraction(-1, 1)
        return_fraction += Fraction(whole, 1)

        return return_fraction.simplified()


def parse_command_line(arguments):
    valid_operators = ["+", "-", "*", "/"]
    parsed_list = []
    full_command = " ".join(arguments)

    is_fraction = True
    for item in arguments:
        if is_fraction:
            f = Fraction.parse(item)
            parsed_list.append(f)
        else:
            if item in valid_operators:
                parsed_list.append(item)
            else:
                raise ValueError(
                    f"Invalid input: {full_command}, {item} is not a valid operator"
                )
        is_fraction = not is_fraction

    if is_fraction:
        raise ValueError(f"Invalid input: {full_command}, incorrect number of operands")

    constructed_eval = ""
    for item in parsed_list:
        if isinstance(item, Fraction):
            constructed_eval += f"Fraction({item.numerator},{item.denominator}) "
        else:
            constructed_eval += f"{item} "

    result = eval(constructed_eval)
    return result


helptext = (
    "Input expression to evaluate. \nValid operators are + - / *. \nFractions should be expressed as X/Y or "
    "-X/Y for proper fractions, and X_Y/Z or -X_Y/Z for mixed fractions"
)

# Note: argparse does not play well with - characters, so it made negative numbers an issue. Raw argv parsing works
#       just as well for simple string data
if __name__ == "__main__":
    if len(argv) == 1 or {"-h", "--help"}.intersection(argv):
        print(helptext)
    else:
        print(parse_command_line(argv[1:]))
