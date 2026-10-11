import sys
sys.path.insert(0, ".")

from src.yuck import AstPrinter
from src.yuck import Grouping
from src.yuck import Literal
from src.yuck import Token
from src.yuck import TokenType
from src.yuck import Unary
from src.yuck import Binary

# NOTE: to run this test, enter this in the terminal: python test/lab2/test_ast.py

# NOTE: I had AI help once again with the steps i needed to take. I noted the response below

# START OF AI HELP
"""
Step 1: Check your classes made for each expression type and verify correct expression format

Step 2: Import the classes made for each expression type, along with the AST printer and token classes

Step 3: Create one AST printer to use for all the examples

Step 4: Make a number literal and put it inside a grouping expression. Print it and compare the output with what you expect

Step 5: Make a unary minus expression using a number, a minus token, and a Unary node. Print it and check the output

Step 6: Make a nested exponent expression. Build the inner ** expression first, then use it inside the outer expression

Step 7: Make separate literal examples for a string, true, false, and nil. Print each one and check the output

Step 8 Make an addition expression with multiplication inside it. Print it and check that the output shows the nesting

Step 9: Make a subtraction expression inside a division expression. Print it and check the output

Step 10: Make examples for >, <, ==, !=, >=, and <=. Print each one and check that the operator and values appear correctly

Step 11: Make a unary not expression using ! and false. Print it and check the output

Step 12: Make an and expression and put it inside an or expression. Print it and check that the nesting is shown

Step 13: For each example, print the expected output and actual output, then display PASS if they match or FAIL if they do not

Step 14: Run the test in the terminal to verify output
"""
# END OF AI HELP
#========================================================

"""NOTE - Syntax reminder for Token:
Token(token_type, original_text, interpreted_value, line_number)
"""

printer = AstPrinter()

# testing out the Grouping class with literal

number = Literal(45.67)
grouped_number = Grouping(number)

# assigning what actually gets printed
actual_output = printer.magic_printer(grouped_number)

# comparing the printer output with what is expected to print
expected_output = "(group expression: 45.67)"

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# testing a negative number as a unary expression

# making a negative number using a unary expression
number_for_unary = Literal(123)
minus_token = Token(TokenType.MINUS, "-", None, 1)
negative_number = Unary(minus_token, number_for_unary)

# print the expression and compare it to what we expect
actual_output = printer.magic_printer(negative_number)
expected_output = "(- 123)"

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# making an expression to test that groups from the right.
first_number = Literal(2)
second_number = Literal(3)
third_number = Literal(2)

power_token = Token(TokenType.POWER, "**", None, 1)

inner_power = Binary(second_number, power_token, third_number)
full_power = Binary(first_number, power_token, inner_power)

# print the expression and compare to what i expect it should print
actual_output = printer.magic_printer(full_power)
expected_output = "(** 2 (** 3 2))"

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# testing wiht a string literal
message = Literal("Why did you make this language")

actual_output = printer.magic_printer(message)
expected_output = "Why did you make this language"

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# testing true
true_value = Literal(True)

actual_output = printer.magic_printer(true_value)
expected_output = "true"

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# testing false
false_value = Literal(False)

actual_output = printer.magic_printer(false_value)
expected_output = "false"

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# testing nil
nil_value = Literal(None)

actual_output = printer.magic_printer(nil_value)
expected_output = "nil"

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# testing addition with multiplication inside it
one = Literal(1)
two = Literal(2)
three = Literal(3)

multiply_token = Token(TokenType.STAR, "*", None, 1)
add_token = Token(TokenType.PLUS, "+", None, 1)

multiplication = Binary(two, multiply_token, three)
addition = Binary(one, add_token, multiplication)

actual_output = printer.magic_printer(addition)
expected_output = "(+ 1 (* 2 3))"

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# testing subtraction inside division
ten = Literal(10)
six = Literal(6)
two = Literal(2)

minus_token = Token(TokenType.MINUS, "-", None, 1)
divide_token = Token(TokenType.SLASH, "/", None, 1)

subtraction = Binary(ten, minus_token, six)
division = Binary(subtraction, divide_token, two)

actual_output = printer.magic_printer(division)
expected_output = "(/ (- 10 6) 2)"

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# testing greater than
three = Literal(3)
two = Literal(2)
greater_token = Token(TokenType.GREATER, ">", None, 1)
greater_expression = Binary(three, greater_token, two)

actual_output = printer.magic_printer(greater_expression)
expected_output = "(> 3 2)"

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


# testing less than
one = Literal(1)
four = Literal(4)
less_token = Token(TokenType.LESS, "<", None, 1)
less_expression = Binary(one, less_token, four)

actual_output = printer.magic_printer(less_expression)
expected_output = "(< 1 4)"

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# testing equal to
five_left = Literal(5)
five_right = Literal(5)
equal_token = Token(TokenType.EQUAL_EQUAL, "==", None, 1)
equal_expression = Binary(five_left, equal_token, five_right)

actual_output = printer.magic_printer(equal_expression)
expected_output = "(== 5 5)"

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


# testing not equal to
six = Literal(6)
seven = Literal(7)
not_equal_token = Token(TokenType.BANG_EQUAL, "!=", None, 1)
not_equal_expression = Binary(six, not_equal_token, seven)

actual_output = printer.magic_printer(not_equal_expression)
expected_output = "(!= 6 7)"

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# testing greater than or equal to
eight = Literal(8)
four = Literal(4)
greater_equal_token = Token(TokenType.GREATER_EQUAL, ">=", None, 1)
greater_equal_expression = Binary(eight, greater_equal_token, four)

actual_output = printer.magic_printer(greater_equal_expression)
expected_output = "(>= 8 4)"

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


# testing less than or equal to
two = Literal(2)
nine = Literal(9)
less_equal_token = Token(TokenType.LESS_EQUAL, "<=", None, 1)
less_equal_expression = Binary(two, less_equal_token, nine)

actual_output = printer.magic_printer(less_equal_expression)
expected_output = "(<= 2 9)"

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# testing logical not
false_value = Literal(False)
not_token = Token(TokenType.BANG, "!", None, 1)
not_expression = Unary(not_token, false_value)

actual_output = printer.magic_printer(not_expression)
expected_output = "(! false)"

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# testing or with and inside it
true_value = Literal(True)
false_value = Literal(False)
another_true_value = Literal(True)

and_token = Token(TokenType.AND, "and", None, 1)
or_token = Token(TokenType.OR, "or", None, 1)

and_expression = Binary(false_value, and_token, another_true_value)
or_expression = Binary(true_value, or_token, and_expression)

actual_output = printer.magic_printer(or_expression)
expected_output = "(or true (and false true))"

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")



#========================================================