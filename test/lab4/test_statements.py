# START OF AI CODE
import sys
sys.path.insert(0, ".")
# END OF AI CODE

from src.yuck import Scanner
from src.yuck import Parser
from src.yuck import Interpreter


# testing an expression statement
print("===================================================")
print("---TESTING AN EXPRESSION STATEMENT---")
scanner = Scanner("4 + 2;")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)

print("Expected: Nothing should print")
print("Actual:")

statements = parser.parse_program()
interpreter = Interpreter()
interpreter.interpret(statements)

print("===================================================\n")


# testing a string print statement
print("---TESTING A STRING PRINT STATEMENT---")
scanner = Scanner('print "one";')
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)

print("===================================================")
print("Expected: one")
print("Actual:")

statements = parser.parse_program()
interpreter = Interpreter()
interpreter.interpret(statements)

print("===================================================\n")


# testing a number print statement
print("---TESTING A NUMBER PRINT STATEMENT---")
scanner = Scanner("print 123;")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)

print("===================================================")
print("Expected: 123")
print("Actual:")

statements = parser.parse_program()
interpreter = Interpreter()
interpreter.interpret(statements)

print("===================================================\n")


# testing a true print statement
print("---TESTING A TRUE PRINT STATEMENT---")
scanner = Scanner("print true;")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)

print("===================================================")
print("Expected: true")
print("Actual:")

statements = parser.parse_program()
interpreter = Interpreter()
interpreter.interpret(statements)

print("===================================================\n")


# testing a false print statement
print("---TESTING A FALSE PRINT STATEMENT---")
scanner = Scanner("print false;")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)

print("===================================================")
print("Expected: false")
print("Actual:")

statements = parser.parse_program()
interpreter = Interpreter()
interpreter.interpret(statements)

print("===================================================\n")


# testing a nil print statement
print("---TESTING A NIL PRINT STATEMENT---")
scanner = Scanner("print nil;")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)

print("===================================================")
print("Expected: nil")
print("Actual:")

statements = parser.parse_program()
interpreter = Interpreter()
interpreter.interpret(statements)

print("===================================================\n")


# testing a print statement with addition
print("---TESTING ADDITION IN A PRINT STATEMENT---")
scanner = Scanner("print 1 + 2;")
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)

print("===================================================")
print("Expected: 3")
print("Actual:")

statements = parser.parse_program()
interpreter = Interpreter()
interpreter.interpret(statements)

print("===================================================\n")


# testing recovery after a missing semicolon
print("---TESTING RECOVERY AFTER A MISSING SEMICOLON---")
scanner = Scanner('''"one"
print "recovered";''')
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)

print("===================================================")
print("Expected: A missing-semicolon error, then recovered")
print("Actual:")

statements = parser.parse_program()
interpreter = Interpreter()
interpreter.interpret(statements)

print("===================================================\n")


# testing recovery after a missing expression
print("---TESTING RECOVERY AFTER A MISSING EXPRESSION---")
scanner = Scanner('''print 2 + ;
print "recovered";''')
tokens = scanner.scan_all_tokens()

parser = Parser(tokens)

print("===================================================")
print("Expected: A missing-expression error, then recovered")
print("Actual:")

statements = parser.parse_program()
interpreter = Interpreter()
interpreter.interpret(statements)

print("===================================================\n")