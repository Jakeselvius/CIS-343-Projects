import sys
sys.path.insert(0, ".")

from src.yuck import Scanner
from src.yuck import Parser
from src.yuck import AstPrinter


# scan a number and turn it into tokens

print("===================================================")
print("---TESTING SIMPLE NUMARIC EXPRESSION---")
scanner = Scanner("123")
tokens = scanner.scan_all_tokens()


# parse the tokens into an expression
parser = Parser(tokens)
expression = parser.parse_input()

printer = AstPrinter()
actual_output = printer.magic_printer(expression)
expected_output = "123"

print("===================================================")
print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASSED - Expression matched what was expected")
    print("===================================================\n")
else:
    print("FAILED - Expression does not match what was expected")
    print("===================================================\n")



# scan, parse, and print an expression with additon and multiplication 
print("---TESTING EXPRESSION WITH ADDITION AND MULTIPLICATION---")
scanner = Scanner("1 + 2 * 3")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)
expression = parser.parse_input()

actual_output = printer.magic_printer(expression)
expected_output = "(+ 1 (* 2 3))"

print("===================================================")
print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASSED - Multiplication stayed inside addition")
    print("===================================================\n")
else:
    print("FAILED - The expression did not match")
    print("===================================================\n")



# tests exponentaion 
print("---TESTING EXPRESSION WITH POWER---")
scanner = Scanner("2 ** 3 ** 2")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)
expression = parser.parse_input()

actual_output = printer.magic_printer(expression)
expected_output = "(** 2 (** 3 2))"

print("===================================================")
print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASSED - Exponentiation grouped from the right")
    print("===================================================\n")
else:
    print("FAILED - The expression did not match")
    print("===================================================\n")




print("---TESTING A 'NOT' EXPRESSION WITH A GROUPED EXPRESSION---")
scanner = Scanner("!(1 + 2)")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)
expression = parser.parse_input()

actual_output = printer.magic_printer(expression)
expected_output = "(! (group expression: (+ 1 2)))"

print("===================================================")
print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASSED - Unary not and grouping worked")
    print("===================================================\n")
else:
    print("FAILED - The expression did not match")
    print("===================================================\n")



# testing a negative number
print("---TESTING A UNARY MINUS EXPRESSION---")
scanner = Scanner("-123")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)
expression = parser.parse_input()

actual_output = printer.magic_printer(expression)
expected_output = "(- 123)"

print("===================================================")
print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASSED - Unary minus worked")
    print("===================================================\n")
else:
    print("FAILED - The expression did not match")
    print("===================================================\n")


# testing that and stays grouped inside or
print("---TESTING 'AND' & 'OR'---")
scanner = Scanner("true or false and true")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)
expression = parser.parse_input()

actual_output = printer.magic_printer(expression)
expected_output = "(or true (and false true))"

print("===================================================")
print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASSED - And stayed grouped inside or")
    print("===================================================\n")
else:
    print("FAILED - The expression did not match")
    print("===================================================\n")




# testing opperatios inside a comparison
print("---TESTING OPPERATORS WITH A COMPARISON---")
scanner = Scanner("1 + 2 * 3 >= 7")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)
expression = parser.parse_input()

actual_output = printer.magic_printer(expression)
expected_output = "(>= (+ 1 (* 2 3)) 7)"

print("===================================================")
print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASSED - Arithmetic stayed grouped inside the comparison")
    print("===================================================\n")
else:
    print("FAILED - The expression did not match")
    print("===================================================\n")




# testing a string literal
print("---TESTING A STRING LITERAL---")
scanner = Scanner('"greetings and salutations my good sir"')
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)
expression = parser.parse_input()

actual_output = printer.magic_printer(expression)
expected_output = "greetings and salutations my good sir"

print("===================================================")
print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASSED - String literal worked")
    print("===================================================\n")
else:
    print("FAILED - The expression did not match")
    print("===================================================\n")



# testing nil
print("---TESTING A NIL LITERAL---")
scanner = Scanner("nil")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)
expression = parser.parse_input()

actual_output = printer.magic_printer(expression)
expected_output = "nil"

print("===================================================")
print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASSED - Nil literal worked")
    print("===================================================\n")
else:
    print("FAILED - The expression did not match")
    print("===================================================\n")






# testing equality after addition
print("---TESTING EQUALITY WITH ADDITION---")
scanner = Scanner("1 + 2 == 3")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)
expression = parser.parse_input()

actual_output = printer.magic_printer(expression)
expected_output = "(== (+ 1 2) 3)"

print("===================================================")
print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASSED - Addition stayed grouped inside equality")
    print("===================================================\n")
else:
    print("FAILED - The expression did not match")
    print("===================================================\n")



# testing subtraction inside division
print("---TESTING SUBTRACTION INSIDE DIVISION---")
scanner = Scanner("(10 - 6) / 2")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)
expression = parser.parse_input()

actual_output = printer.magic_printer(expression)
expected_output = "(/ (group expression: (- 10 6)) 2)"

print("===================================================")
print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASSED - Subtraction stayed grouped inside division")
    print("===================================================\n")
else:
    print("FAILED - The expression did not match")
    print("===================================================\n")





    # testing the greater than operator
print("---TESTING GREATER THAN---")
scanner = Scanner("3 > 2")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)
expression = parser.parse_input()

actual_output = printer.magic_printer(expression)
expected_output = "(> 3 2)"

print("===================================================")
print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASSED - Greater than worked")
    print("===================================================\n")
else:
    print("FAILED - The expression did not match")
    print("===================================================\n")



# testing the less than operator
print("---TESTING LESS THAN---")
scanner = Scanner("1 < 4")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)
expression = parser.parse_input()

actual_output = printer.magic_printer(expression)
expected_output = "(< 1 4)"

print("===================================================")
print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASSED - Less than worked")
    print("===================================================\n")
else:
    print("FAILED - The expression did not match")
    print("===================================================\n")




# testing the less than or equal operator
print("---TESTING LESS THAN OR EQUAL---")
scanner = Scanner("2 <= 9")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)
expression = parser.parse_input()

actual_output = printer.magic_printer(expression)
expected_output = "(<= 2 9)"

print("===================================================")
print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASSED - Less than or equal worked")
    print("===================================================\n")
else:
    print("FAILED - The expression did not match")
    print("===================================================\n")



# testing the not equal operator
print("---TESTING NOT EQUAL---")
scanner = Scanner("6 != 7")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)
expression = parser.parse_input()

actual_output = printer.magic_printer(expression)
expected_output = "(!= 6 7)"

print("===================================================")
print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASSED - Not equal worked")
    print("===================================================\n")
else:
    print("FAILED - The expression did not match")
    print("===================================================\n")




# testing that subtraction groups from the left
print("---TESTING SUBTRACTION ASSOCIATIVITY---")
scanner = Scanner("10 - 3 - 2")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)
expression = parser.parse_input()

actual_output = printer.magic_printer(expression)
expected_output = "(- (- 10 3) 2)"

print("===================================================")
print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASSED - Subtraction grouped from the left")
    print("===================================================\n")
else:
    print("FAILED - The expression did not match")
    print("===================================================\n")




# testing that a negative sign applies to the full power expression and not just part of it
print("---TESTING UNARY MINUS WITH POWER---")
scanner = Scanner("-2 ** 2")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)
expression = parser.parse_input()

actual_output = printer.magic_printer(expression)
expected_output = "(- (** 2 2))"

print("===================================================")
print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASSED - Unary minus and power grouped as expected")
    print("===================================================\n")
else:
    print("FAILED - The expression did not match")
    print("===================================================\n")




# testing nested grouping
print("---TESTING NESTED GROUPING---")
scanner = Scanner("((1 + 2) * 3)")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)
expression = parser.parse_input()

actual_output = printer.magic_printer(expression)
expected_output = "(group expression: (* (group expression: (+ 1 2)) 3))"

print("===================================================")
print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASSED - Nested grouping worked")
    print("===================================================\n")
else:
    print("FAILED - The expression did not match")
    print("===================================================\n")




# testing that extra tokens after an expression are reported
print("---TESTING EXTRA TOKENS---")
scanner = Scanner("123 456")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)

try:
    parser.parse_input()
    print("FAILED - Extra token was not reported")
except SyntaxError as error:
    print("Expected an angry message for the extra token\n")
    print("Actual error:\n", error)
    print("PASSED - Extra token was reported")
    print("===================================================\n")



# testing that a missing operand is reported
print("---TESTING A MISSING OPERAND---")
scanner = Scanner("1 +")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)

try:
    parser.parse_input()
    print("FAILED - Missing operand was not reported")
except SyntaxError as error:
    print("Expected to be yelled at for a missing operand\n")
    print("Actual error:\n", error)
    print("\nPASSED - Missing operand was reported")
    print("===================================================\n")




# testing that a missing closing parenthesis is reported
print("---TESTING A MISSING CLOSING PARENTHESIS---")
scanner = Scanner("(1 + 2")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)

try:
    parser.parse_input()
    print("FAILED - Missing closing parenthesis was not reported")
except SyntaxError as error:
    print("Expected to be chewed out for a missing a closing parenthesis\n")
    print("Actual error:\n", error)
    print("\nPASSED - Missing closing parenthesis was reported and feelings were hurt")
    print("===================================================\n")