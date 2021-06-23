#!/usr/bin/env python
from sys import argv

__author__ = "John Mahoney"


def gcf(a, b):
    """
    Determine the greatest common positive factor which a and b share

    :param a: First integer
    :param b: Second integer
    :return: Greatest common factor of both integer
    """
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
    """
    Return the least common multiple of a and b

    :param a: First integer
    :param b: Second integer
    :return: Least common multiple of both integers
    """
    return int(a / gcf(a, b) * b)


class Fraction:
    """
    Class which contains all of the logic for parsing, printing, manipulation, and arithmetic of fractions
    """
    def __init__(self, numerator, denominator=1, simplify=False):
        """
        Build a fraction from the given numerator and (optional) denominator.

        :param numerator: Numerator of fraction
        :param denominator: Denominator of fraction (optional), if not specified defaults to 1. Cannot be zero
        :param simplify: Boolean specifying if you wish for this fraction to be simplified in initialization
        """
        self.numerator = int(numerator)
        self.denominator = int(denominator)
        if self.denominator == 0:
            raise ZeroDivisionError("Cannot have 0 as a denominator.")
        if simplify:
            self.simplify()

    def simplify(self):
        """
        Function which simplifies this fraction to it's lowest terms ( i.e. 6/4 -> 3/2 )

        :return: None
        """
        self_simplified = self.simplified()
        self.numerator = self_simplified.numerator
        self.denominator = self_simplified.denominator

    def simplified(self):
        """
        Function which returns the simplified version of this fraction ( i.e. 6/4 returns 3/2 )

        :return: Simplified instance of this Fraction
        """
        scalar = gcf(self.numerator, self.denominator)
        numerator = int(self.numerator / scalar)
        denominator = int(self.denominator / scalar)
        if denominator < 0:
            numerator *= -1
            denominator *= -1
        return Fraction(numerator, denominator)

    def scale(self, scalar):
        """
        Function used to scale fraction for comparison in addition and subtraction operations

        :param scalar: Amount to multiply both the numerator and denominator by
        :return: Scaled instance of this fraction ( i.e. Fraction(3, 2).scale(3) -> Fraction(9, 6) )
        """
        return Fraction(self.numerator * scalar, self.denominator * scalar)

    def inverse(self, simplify=False):
        """
        Returns the inverse of this fraction for use in division operations

        :param simplify: Should the inverted fraction be simplified ( i.e. 6/4 -> 2/3 )
        :return: Inverse of this fraction ( i.e. 6/4 returns 4/6)
        """
        return Fraction(self.denominator, self.numerator, simplify=simplify)

    def normalize(self, other):
        """
        Return a normalized pair where both denominators are equal to support addition, subtraction, and comparison
        ( i.e. Fraction(2, 3).normalize(Fraction(3, 5)) returns ( Fraction(10, 15), Fraction(9, 15) )

        :param other: The other fraction to normalize against
        :return: Normalized pair of fractions with matching denominators
        """
        if not self.is_normalized(other):
            lcm_denominator = lcm(self.denominator, other.denominator)
            self_scale = lcm_denominator / self.denominator
            other_scale = lcm_denominator / other.denominator
            return self.scale(self_scale), other.scale(other_scale)
        return self, other

    def is_normalized(self, other):
        """
        Boolean value which states if the two fractions are normalized, meaning if they share the same denominator

        :param other: Other fraction instance to compare to
        :return: Boolean stating if these two fractions are normalized
        """
        return self.denominator == other.denominator

    def __add__(self, other):
        """
        Addition operator between two fractions, will normalize before addition and simplify after

        :param other: Other fraction instance to add
        :return: Fraction instance of self added to other ( i.e. 4/3 + 1/6 = 9/6 )
        """
        self_scaled, other_scaled = self.normalize(other)
        return Fraction(
            self_scaled.numerator + other_scaled.numerator,
            self_scaled.denominator,
            simplify=True,
        )

    def __sub__(self, other):
        """
        Subtraction operator between two fractions, will normalize before subtraction and simplify after

        :param other: Other fraction instance to subtract
        :return: Fraction instance of other subtracted from self ( i.e. 4/3 - 1/6 = 7/6 )
        """
        self_scaled, other_scaled = self.normalize(other)
        return Fraction(
            self_scaled.numerator - other_scaled.numerator,
            self_scaled.denominator,
            simplify=True,
        )

    def __mul__(self, other):
        """
        Multiplication operator between two fractions, will simplify after multiplication

        :param other: Other fraction instance to multiply
        :return: Fraction instance of other multiplied by self ( i.e. 2/3 * 5/10 = 1/3 )
        """
        return Fraction(
            self.numerator * other.numerator,
            self.denominator * other.denominator,
            simplify=True,
        )

    def __truediv__(self, other):
        """
        Division operator between two fractions, will simplify after division

        :param other: Other fraction instance to divide by
        :return: Fraction instance of self divided by other ( i.e. 2/3 / 1/2 = 4/3 )
        """
        return self * other.inverse()

    def __eq__(self, other):
        """
        Equality comparator between this and other fraction, will normalize before comparison

        :param other: Other fraction to compare for equality
        :return: Boolean specifying equality between self and other ( i.e. 2/3 == 1/2 -> False, 2/3 == 4/6 -> True )
        """
        if not self.is_normalized(other):
            self_normalized, other_normalized = self.normalize(other)
            return self_normalized == other_normalized

        return self.numerator == other.numerator

    def __str__(self):
        """
        Stringify this fraction.
        Fractions simplifying to whole numbers will be displayed as only the whole number: 4/2 -> 2
        Proper fractions will display as such: 2/4 -> 2/4
        Improper fractions will be displayed as mixed numbers: 5/2 -> 2_1/2

        :return: Stringified version of self
        """
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
        """
        Copy of str, for use in debugger etc.

        :return: Stringified version of self
        """
        return str(self)

    @classmethod
    def parse(cls, input_str):
        """
        Parse a string from the command line into a fraction. Will simplify the input value
        For whole numbers: 3 -> 3/1
        For proper/improper fractions: 4/5 -> 4/5
        For mixed numbers: 2_1/3 -> 7/3

        :param input_str: Input from command line to parse as fraction
        :return: Constructed, simplified Fraction instance
        """
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
            return cls(whole)

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
            return_fraction *= Fraction(-1)
        return_fraction += Fraction(whole)

        return return_fraction.simplified()


def parse_command_line(arguments):
    """
    Parse the command line arguments into an eval function to return the result. Raise an exception if any improperly
    formatted fractions or operators are found. This eval is safe because all inputs are either cast into integers or
    sanitized against a list of allowed operands. If 'set -f' is not set before running this script, then * characters
    must be escaped or quoted when used on the command line.

    :param arguments: Arguments passed in from command line.
    :return: Fraction result from evaluated expression
    """
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
    'Input expression to evaluate. \n\nValid operators are + - / "*" \n(Asterisk must be quoted or escaped to prevent '
    "glob expansion in shell, or you can run 'set -f' beforehand to disable shell expansion) \n\nFractions should be "
    "expressed as X/Y or -X/Y, and X_Y/Z or -X_Y/Z for mixed fractions"
)

# Note: argparse does not play well with - characters, so it made negative numbers an issue. Raw argv parsing works
#       just as well for simple string data
if __name__ == "__main__":
    if len(argv) == 1 or {"-h", "--help"}.intersection(argv):
        print("\n")
        print(helptext)
    else:
        try:
            print(parse_command_line(argv[1:]))
        except Exception as e:
            print("\n")
            print(str(e), "\n")
            print(helptext)
