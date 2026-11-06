import sys
sys.path.insert(0, ".")

from src.yuck import Scanner
from src.yuck import Parser
from src.yuck import Evaluator


def test_expression(input_text, expected_value):
    scanner = Scanner(input_text)
    tokens = scanner.scan_all_tokens()

    parser = Parser(tokens)
    expression = parser.parse_input()

    evaluator = Evaluator()
    actual_value = evaluator.evaluate(expression)

    print("Input:", input_text)
    print("Expected:", expected_value)
    print("Actual:", actual_value)

    if actual_value == expected_value and type(actual_value) == type(expected_value):
        print("PASSED")
    else:
        print("FAILED")

    print("===================================================")


print("---TESTING A NUMBER---")
test_expression("123", 123)

print("---TESTING A GROUPED EXPRESSION---")
test_expression("(1 + 2) * 3", 9)

print("---TESTING ADDITION AND MULTIPLICATION---")
test_expression("1 + 2 * 3", 7)

print("---TESTING POWER---")
test_expression("2 ** 3 ** 2", 512)

print("---TESTING STRING ADDITION---")
test_expression('"hello" + " there"', "hello there")

print("---TESTING UNARY MINUS---")
test_expression("-123", -123)

print("---TESTING LOGICAL NOT---")
test_expression("!false", True)

print("---TESTING COMPARISONS---")
test_expression("3 > 2", True)
test_expression("2 <= 9", True)

print("---TESTING EQUALITY---")
test_expression("1 + 2 == 3", True)
test_expression("6 != 7", True)

print("---TESTING AND---")
test_expression("true and 5", 5)

print("---TESTING OR---")
test_expression("false or 5", 5)

print("---TESTING AND 0---")
test_expression("false and (1 / 0)", False)

print("---TESTING OR 0---")
test_expression("true or (1 / 0)", True)