import sys
# START AI CODE
sys.path.insert(0, ".") 
# END AI CODE

from src.yuck import Scanner

# NOTE - to run the test, enter this in the terminal: python test/lab1/test_scanner.py


# testing punctuation and operators
input_text = "( ) { } , . - + ; / ! != = == < <= > >="
scanner = Scanner(input_text)
tokens = scanner.scan_all_tokens()

actual_output = []
for token in tokens:
    actual_output.append(str(token))

expected_output = [
    "LEFT_PAREN ( (",
    "RIGHT_PAREN ) )",
    "LEFT_BRACE { {",
    "RIGHT_BRACE } }",
    "COMMA , ,",
    "DOT . .",
    "MINUS - -",
    "PLUS + +",
    "SEMICOLON ; ;",
    "SLASH / /",
    "BANG ! !",
    "BANG_EQUAL != !=",
    "EQUAL = =",
    "EQUAL_EQUAL == ==",
    "LESS < <",
    "LESS_EQUAL <= <=",
    "GREATER > >",
    "GREATER_EQUAL >= >=",
    "EOF  "
]

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# testing power and regular multiplication
input_text = "** *"
scanner = Scanner(input_text)
tokens = scanner.scan_all_tokens()

actual_output = []
for token in tokens:
    actual_output.append(str(token))

expected_output = [
    "POWER ** **",
    "STAR * *",
    "EOF  "
]

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# testing keywords
input_text = "and class else false fun for if nil or print return super this true var while"
scanner = Scanner(input_text)
tokens = scanner.scan_all_tokens()

actual_output = []
for token in tokens:
    actual_output.append(str(token))

expected_output = [
    "AND and None",
    "CLASS class None",
    "ELSE else None",
    "FALSE false None",
    "FUN fun None",
    "FOR for None",
    "IF if None",
    "NIL nil None",
    "OR or None",
    "PRINT print None",
    "RETURN return None",
    "SUPER super None",
    "THIS this None",
    "TRUE true None",
    "VAR var None",
    "WHILE while None",
    "EOF  "
]

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# testing strings and identifiers
input_text = '"hello world" "" beans beans6 _LargeBeans'
scanner = Scanner(input_text)
tokens = scanner.scan_all_tokens()

actual_output = []
for token in tokens:
    actual_output.append(str(token))

expected_output = [
    'STRING "hello world" hello world',
    'STRING "" ',
    "IDENTIFIER beans None",
    "IDENTIFIER beans6 None",
    "IDENTIFIER _LargeBeans None",
    "EOF  "
]

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# testing number edge cases
input_text = "0 12.3 12. . 12..3"
scanner = Scanner(input_text)
tokens = scanner.scan_all_tokens()

actual_output = []
for token in tokens:
    actual_output.append(str(token))

expected_output = [
    "NUMBER 0 0",
    "NUMBER 12.3 12.3",
    "NUMBER 12 12",
    "DOT . .",
    "DOT . .",
    "NUMBER 12 12",
    "DOT . .",
    "DOT . .",
    "NUMBER 3 3",
    "EOF  "
]

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# testing that comments are skipped
input_text = "/ 123 // ignore the rest of this line\n456"
scanner = Scanner(input_text)
tokens = scanner.scan_all_tokens()

actual_output = []
for token in tokens:
    actual_output.append(str(token))

expected_output = [
    "SLASH / /",
    "NUMBER 123 123",
    "NUMBER 456 456",
    "EOF  "
]

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# testing an unexpected character and checking that scanning continues
input_text = "@ 123"
scanner = Scanner(input_text)
tokens = scanner.scan_all_tokens()

actual_output = []
for token in tokens:
    actual_output.append(str(token))

expected_output = [
    "NUMBER 123 123",
    "EOF  "
]

print("Expected tokens:", expected_output)
print("Actual tokens:", actual_output)
print("The scanner should also print a warning for the @ character")

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# testing empty input
input_text = ""
scanner = Scanner(input_text)
tokens = scanner.scan_all_tokens()

actual_output = []
for token in tokens:
    actual_output.append(str(token))

expected_output = [
    "EOF  "
]

print("Expected:", expected_output)
print("Actual:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")


#========================================================


# testing a string with no closing quote
input_text = '"unfinished'
scanner = Scanner(input_text)

tokens = scanner.scan_all_tokens()

actual_output = []
for token in tokens:
    actual_output.append(str(token))

expected_output = ["EOF  "]

print("Expected tokens:", expected_output)
print("Actual tokens:", actual_output)

if actual_output == expected_output:
    print("PASS")
else:
    print("FAIL")