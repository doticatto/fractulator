import unittest
from fractulator import Fraction, parse_command_line, gcf, lcm


class GcmLcfTest(unittest.TestCase):
    def test_lcm(self):
        self.assertEqual(lcm(3, 2), 6)
        self.assertEqual(lcm(13, 21), 273)
        self.assertEqual(lcm(2, 4), 4)

    def test_gcf(self):
        self.assertEqual(gcf(14, 8), 2)
        self.assertEqual(gcf(5, 13), 1)
        self.assertEqual(gcf(8, 4), 4)


class FractulatorTest(unittest.TestCase):
    f1 = Fraction(1, 2)
    f2 = Fraction(2, 3)

    f1_negative = Fraction(-1, 2)
    f2_negative = Fraction(-2, 3)

    def test_zero_denominator(self):
        with self.assertRaises(ZeroDivisionError) as zero_denom_error:
            Fraction(1, 0)
        self.assertEqual(
            "Cannot have 0 as a denominator.", str(zero_denom_error.exception)
        )

    def test_addition(self):
        result = self.f1 + self.f2
        self.assertEqual(result.numerator, 7)
        self.assertEqual(result.denominator, 6)

        self.assertEqual(result, Fraction(7, 6))

    def test_addition_negative(self):
        result = self.f1 + self.f2_negative
        self.assertEqual(result.numerator, -1)
        self.assertEqual(result.denominator, 6)

        self.assertEqual(result, Fraction(-1, 6))

    def test_subtraction(self):
        result = self.f2 - self.f1
        self.assertEqual(result.numerator, 1)
        self.assertEqual(result.denominator, 6)

        self.assertEqual(result, Fraction(1, 6))

    def test_subtraction_negative(self):
        result = self.f2 - self.f1_negative
        self.assertEqual(result.numerator, 7)
        self.assertEqual(result.denominator, 6)

        self.assertEqual(result, Fraction(7, 6))

    def test_multiplication(self):
        result = self.f1 * self.f2
        self.assertEqual(result.numerator, 1)
        self.assertEqual(result.denominator, 3)

        self.assertEqual(result, Fraction(1, 3))

    def test_multiplication_negative(self):
        result = self.f1_negative * self.f2
        self.assertEqual(result.numerator, -1)
        self.assertEqual(result.denominator, 3)

        self.assertEqual(result, Fraction(-1, 3))

    def test_division(self):
        result = self.f2 / self.f1
        self.assertEqual(result.numerator, 4)
        self.assertEqual(result.denominator, 3)

        self.assertEqual(result, Fraction(4, 3))

    def test_division_negative(self):
        result = self.f1 / self.f2_negative
        self.assertEqual(result.numerator, -3)
        self.assertEqual(result.denominator, 4)

        self.assertEqual(result, Fraction(-3, 4))

    def test_order_operations(self):
        result = self.f1 + self.f2 * self.f1_negative - self.f2_negative / self.f1
        self.assertEqual(result.numerator, 3)
        self.assertEqual(result.denominator, 2)

        self.assertEqual(result, Fraction(3, 2))

    def test_equals(self):
        self.assertEqual(self.f1, Fraction(1, 2))

    def test_equals_not_normalized(self):
        self.assertEqual(self.f1, Fraction(8, 16))

    def test_not_equal(self):
        self.assertNotEqual(self.f1, self.f2)

    def test_simplify(self):
        result = Fraction(8, 6, simplify=True)
        self.assertEqual(result.numerator, 4)
        self.assertEqual(result.denominator, 3)

    def test_simplify_fix_negative_denominator(self):
        result = Fraction(8, -6, simplify=True)
        self.assertEqual(result.numerator, -4)
        self.assertEqual(result.denominator, 3)

    def test_simplified(self):
        result = Fraction(12, 4).simplified()
        self.assertEqual(result.numerator, 3)
        self.assertEqual(result.denominator, 1)

    def test_scale(self):
        result = Fraction(18, 9).scale(4)
        self.assertEqual(result.numerator, 72)
        self.assertEqual(result.denominator, 36)

    def test_inverse(self):
        result = Fraction(56, 49).inverse()
        self.assertEqual(result.numerator, 49)
        self.assertEqual(result.denominator, 56)

    def test_inverse_simplify(self):
        result = Fraction(100, 50).inverse(simplify=True)
        self.assertEqual(result.numerator, 1)
        self.assertEqual(result.denominator, 2)

    def test_normalize(self):
        result = self.f1.normalize(self.f2)
        self.assertEqual(result, (Fraction(3, 6), Fraction(4, 6)))

    def test_normalize_same_denominator(self):
        result = Fraction(1, 2).normalize(Fraction(3, 2))
        self.assertEqual(result, (Fraction(1, 2), Fraction(3, 2)))

    def test_is_normalized(self):
        self.assertTrue(self.f1.is_normalized(Fraction(3, 2)))

    def test_is_normalized_false(self):
        self.assertFalse(self.f1.is_normalized(self.f2))

    def test_tostring_zero(self):
        result = str(Fraction(0, 1))
        self.assertEqual(result, "0")

    def test_tostring_fraction(self):
        result = str(self.f1)
        self.assertEqual(result, "1/2")

    def test_tostring_negative_fraction(self):
        result = str(self.f1_negative)
        self.assertEqual(result, "-1/2")

    def test_tostring_whole_number(self):
        result = str(Fraction(2, 2))
        self.assertEqual(result, "1")

    def test_tostring_mixed_number(self):
        result = str(Fraction(8, 3))
        self.assertEqual(result, "2_2/3")

    def test_tostring_negative_mixed_number(self):
        result = str(Fraction(-8, 3))
        self.assertEqual(result, "-2_2/3")

    def test_parse_fraction(self):
        result = Fraction.parse("2/3")
        self.assertEqual(result, self.f2)

    def test_parse_negative_fraction(self):
        result = Fraction.parse("-2/3")
        self.assertEqual(result, self.f2_negative)

    def test_parse_negative_fraction_denominator(self):
        result = Fraction.parse("2/-3")
        self.assertEqual(result, self.f2_negative)

    def test_parse_whole_number(self):
        result = Fraction.parse("7")
        self.assertEqual(result, Fraction(7, 1))

    def test_parse_negative_whole_number(self):
        result = Fraction.parse("-7")
        self.assertEqual(result, Fraction(-7, 1))

    def test_parse_bad_whole_number(self):
        parse_val = ":("
        with self.assertRaises(ValueError) as invalid_whole_ex:
            Fraction.parse(parse_val)
        self.assertEqual(str(invalid_whole_ex.exception), "Invalid fraction input: :(")

    def test_parse_mixed_number(self):
        result = Fraction.parse("2_3/7")
        self.assertEqual(result, Fraction(17, 7))

    def test_parse_negative_mixed_number(self):
        result = Fraction.parse("-2_3/7")
        self.assertEqual(result, Fraction(-17, 7))

    def test_parse_bad_negative_mixed_number(self):
        for bad_negative_mixed_number in ["-2_-3/7", "2_-3/7", "2_3/-7"]:
            with self.assertRaises(ValueError) as invalid_negative_mixed_exc:
                Fraction.parse(bad_negative_mixed_number)
            self.assertEqual(
                str(invalid_negative_mixed_exc.exception),
                f"Invalid fraction input: {bad_negative_mixed_number}: Please input negative mixed "
                "fractions with the minus sign at the beginning to reduce ambiguity (i.e. -2_3/7)",
            )

    def test_parse_invalid_mixed_number(self):
        parse_val = "x_3/7"
        with self.assertRaises(ValueError) as invalid_mixed_exc:
            Fraction.parse(parse_val)
        self.assertEqual(
            str(invalid_mixed_exc.exception), "Invalid fraction input: x_3/7"
        )

    def test_parse_too_many_items(self):
        parse_val = "x_3_/7"
        with self.assertRaises(ValueError) as too_many_items_exc:
            Fraction.parse(parse_val)
        self.assertEqual(
            str(too_many_items_exc.exception), "Invalid fraction input: x_3_/7"
        )

    def test_parse_bad_fraction(self):
        parse_val = "z/7"
        with self.assertRaises(ValueError) as bad_fraction_exc:
            Fraction.parse(parse_val)
        self.assertEqual(str(bad_fraction_exc.exception), "Invalid fraction input: z/7")


class CommandLineParserTest(unittest.TestCase):
    def test_parse_good_expression(self):
        arguments = ["4/3", "+", "1/2"]
        result = parse_command_line(arguments)
        self.assertEqual(result, Fraction(11, 6))

        arguments = ["4/3", "+", "1/2", "*", "3_1/6"]
        result = parse_command_line(arguments)
        self.assertEqual(result, Fraction(35, 12))

        arguments = ["4/3", "/", "1/2", "-", "3_1/6"]
        result = parse_command_line(arguments)
        self.assertEqual(result, Fraction(-1, 2))

        arguments = ["4/3", "/", "1/2", "-", "3_1/6", "+", "-2_1/8", "*", "13/27"]
        result = parse_command_line(arguments)
        self.assertEqual(result, Fraction(-329, 216))

    def test_parse_bad_operator(self):
        bad_op = "#"
        arguments = ["3/4", bad_op, "1/2"]
        with self.assertRaises(ValueError) as bad_operator_error:
            parse_command_line(arguments)
        self.assertIn(
            f"Invalid input: 3/4 {bad_op} 1/2, {bad_op} is not a valid operator",
            str(bad_operator_error.exception),
        )

    def test_parse_invalid_number_operators(self):
        arguments = ["3/4", "+", "1/2", "-"]
        with self.assertRaises(ValueError) as bad_operator_error:
            parse_command_line(arguments)
        self.assertIn(
            f"Invalid input: 3/4 + 1/2 -, incorrect number of operands",
            str(bad_operator_error.exception),
        )


if __name__ == "__main__":
    unittest.main()
