import sys


class Token:
    def __init__(self, token_type, raw_token, string_token, line_number):
        self.token_type = token_type
        self.raw_token = raw_token
        self.string_token = string_token
        self.line_number = line_number
       

    def __str__(self):
        return f'{self.token_type} {self.raw_token} {self.string_token}'

# each type of token so i can easily reference them in the scanner
# this is refered to as 'lexeme' but it is easier for me to think of it as a token type
class TokenType:
    # raw token type = string token type
    # single character tokens
    LEFT_PAREN = 'LEFT_PAREN'
    RIGHT_PAREN = 'RIGHT_PAREN'
    LEFT_BRACE = 'LEFT_BRACE'
    RIGHT_BRACE = 'RIGHT_BRACE'
    COMMA = 'COMMA'
    DOT = 'DOT'
    MINUS = 'MINUS'
    PLUS = 'PLUS'
    SEMICOLON = 'SEMICOLON'
    SLASH = 'SLASH'
    STAR = 'STAR'
    NUMBER = 'NUMBER'
    EOF = 'EOF'
    POWER = 'POWER'

    # one or two character tokens
    BANG = 'BANG'
    BANG_EQUAL = 'BANG_EQUAL'
    EQUAL = 'EQUAL'
    EQUAL_EQUAL = 'EQUAL_EQUAL'
    LESS = 'LESS'
    LESS_EQUAL = 'LESS_EQUAL'
    GREATER = 'GREATER'
    GREATER_EQUAL = 'GREATER_EQUAL'

    # keywords
    AND = 'AND'
    CLASS = 'CLASS'
    ELSE = 'ELSE'
    FALSE = 'FALSE'
    FUN = 'FUN'
    FOR = 'FOR'
    IF = 'IF'
    NIL = 'NIL'
    OR = 'OR'
    PRINT = 'PRINT'
    RETURN = 'RETURN'
    SUPER = 'SUPER'
    THIS = 'THIS'
    TRUE = 'TRUE'
    VAR = 'VAR'
    WHILE = 'WHILE'

    # literals
    IDENTIFIER = 'IDENTIFIER'
    STRING = 'STRING'
    NUMBER = 'NUMBER'

# This is going to be the class for storing the literal value from the literal expression
class Literal:
    def __init__(self, value):
        self.value = value

# This is going to be the class for storing my expression inside of parentheses 
class Grouping:
    def __init__(self, expression):
        self.expression = expression

# This class is going to be the operator and the expression that is tied to that like "-123." operator is the token and right is the expression for it
class Unary:
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

# This class is going to be the class that has a left expression, an operator, and a right expression. 
class Binary:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

# this class is going to be the expression statement that will hold the expression and will be used in the interpreter to evaluate it
class ExpressionStatement:
    def __init__(self, expression):
        self.expression = expression

# this class is going to be the print statement that will hold the expression used in the interpreter to evaluate it and print it
class PrintStatement:
    def __init__(self, expression):
        self.expression = expression


# This class is going to be my printer that prints the actual AST expression as text and yells at you if its not recognized/supported
class AstPrinter:
    def magic_printer(self, expression):
        if isinstance(expression, Literal): # if its a literal expression
            if expression.value is None:
                return "nil"
            if expression.value is True:
                return "true"
            if expression.value is False:
                return "false"
            return str(expression.value)
        
        elif isinstance(expression, Grouping): # if the expression is a group
            return "(group expression: " + self.magic_printer(expression.expression) + ")" # recursively prints the inner expression

        elif isinstance(expression, Unary): # if its an operator type like ! = + - 
            return "(" + expression.operator.raw_token + " " + self.magic_printer(expression.right) + ")"

        elif isinstance(expression, Binary): # prints the operator first, left, then right expression
            return "(" + expression.operator.raw_token + " " + self.magic_printer(expression.left) + " " + self.magic_printer(expression.right) + ")"

        
        else: # if its strange
            raise TypeError(f"uhhhh, not quite sure what this is: {type(expression).__name__}")



class Evaluator:
    def evaluate(self, expression):
        if isinstance(expression, Literal):
            return expression.value

        if isinstance(expression, Grouping):
            return self.evaluate(expression.expression)

        if isinstance(expression, Unary):
            right_value = self.evaluate(expression.right)

            if expression.operator.token_type == TokenType.BANG:
                if right_value is None or right_value is False:
                    return True
                else:
                    return False

            if expression.operator.token_type == TokenType.MINUS:
                if isinstance(right_value, bool) or not isinstance(right_value, (int, float)):
                    # Unary minus
                    raise TypeError("Unary minus only works on numbers. This value isn't a number, go take a peek.")

                return -right_value


        if isinstance(expression, Binary):
            left_value = self.evaluate(expression.left)
            operator_type = expression.operator.token_type

            if operator_type == TokenType.AND:
                if left_value is None or left_value is False:
                    return left_value
                else:
                    return self.evaluate(expression.right)

            if operator_type == TokenType.OR:
                if left_value is None or left_value is False:
                    return self.evaluate(expression.right)
                else:
                    return left_value

            right_value = self.evaluate(expression.right)

            if operator_type == TokenType.PLUS:
                if isinstance(left_value, (int, float)) and not isinstance(left_value, bool):
                    if isinstance(right_value, (int, float)) and not isinstance(right_value, bool):
                        return left_value + right_value

                if isinstance(left_value, str) and isinstance(right_value, str):
                    return left_value + right_value

                # Addition
                raise TypeError("The + operator can add two numbers or join two strings. These values don't fit either pair.")

            if operator_type == TokenType.MINUS:
                if isinstance(left_value, (int, float)) and not isinstance(left_value, bool):
                    if isinstance(right_value, (int, float)) and not isinstance(right_value, bool):
                        return left_value - right_value

                # Subtraction
                raise TypeError("Subtraction needs two numbers. One of these values isn't numeric.")

            if operator_type == TokenType.STAR:
                if isinstance(left_value, (int, float)) and not isinstance(left_value, bool):
                    if isinstance(right_value, (int, float)) and not isinstance(right_value, bool):
                        return left_value * right_value

                # Multiplication
                raise TypeError("Looks like * got a non-number. It needs a number on both sides.")

            if operator_type == TokenType.SLASH:
                if isinstance(left_value, (int, float)) and not isinstance(left_value, bool):
                    if isinstance(right_value, (int, float)) and not isinstance(right_value, bool):
                        return left_value / right_value

                # Division
                raise TypeError("Can't divide these values as they are; division needs two numbers.")
            if operator_type == TokenType.POWER:
                if isinstance(left_value, (int, float)) and not isinstance(left_value, bool):
                    if isinstance(right_value, (int, float)) and not isinstance(right_value, bool):
                        return left_value ** right_value

                # Exponentiation
                raise TypeError("For **, both the base and the exponent need to be numbers.")

            if (operator_type == TokenType.GREATER
                    or operator_type == TokenType.GREATER_EQUAL
                    or operator_type == TokenType.LESS
                    or operator_type == TokenType.LESS_EQUAL):
                if (isinstance(left_value, (int, float))
                        and not isinstance(left_value, bool)
                        and isinstance(right_value, (int, float))
                        and not isinstance(right_value, bool)):

                    if operator_type == TokenType.GREATER:
                        return left_value > right_value

                    if operator_type == TokenType.GREATER_EQUAL:
                        return left_value >= right_value

                    if operator_type == TokenType.LESS:
                        return left_value < right_value

                    if operator_type == TokenType.LESS_EQUAL:
                        return left_value <= right_value

                raise TypeError("Comparisons need two numbers. These values aren't both numbers.")

            if (operator_type == TokenType.EQUAL_EQUAL
                    or operator_type == TokenType.BANG_EQUAL):

                if (isinstance(left_value, (int, float))
                        and not isinstance(left_value, bool)
                        and isinstance(right_value, (int, float))
                        and not isinstance(right_value, bool)):
                    values_are_equal = left_value == right_value
                else:
                    values_are_equal = (
                        type(left_value) == type(right_value)
                        and left_value == right_value
                    )

                if operator_type == TokenType.EQUAL_EQUAL:
                    return values_are_equal
                else:
                    return not values_are_equal



        raise TypeError(f"I don't know how to evaluate this expression: {type(expression).__name__}")




# START OF AI HELP
# Pseudocode for interpreting statements:
# - Go through each statement in order.
# - For an expression statement, evaluate its expression and do not display the result.
# - For a print statement, evaluate its expression and display the result.
# - Convert true, false, and nil to the words Yuck uses.
#
# The statement type decides whether its value should be printed.
# END OF AI HELP


# this is going to evaluate every expression statement and will handle when it will be displayed
class Interpreter:
    def __init__(self):
        self.evaluator = Evaluator()

    def interpret(self, statements):
        for statement in statements:
            if isinstance(statement, ExpressionStatement):
                self.evaluator.evaluate(statement.expression)

            elif isinstance(statement, PrintStatement):
                value = self.evaluator.evaluate(statement.expression)
                print(self.stringify(value))

    def stringify(self, value):
        if value is None:
            return "nil"

        if value is True:
            return "true"

        if value is False:
            return "false"

        return str(value)



# my scanner will scan the text from the input and make a list of the tokens it sees so we can
# use them later when making the parcer. It also keeps track of the line number for error reference
class Scanner:
    def __init__(self, input_text):
        self.input_text = input_text
        self.token_list = []
        self.start_index = 0
        self.current_index = 0
        self.line_number = 1
         # added this dictionary to check whether a word is a keyword or a regular identifier
        self.keywords = {
        'and': TokenType.AND,
        'class': TokenType.CLASS,
        'else': TokenType.ELSE,
        'false': TokenType.FALSE,
        'fun': TokenType.FUN,
        'for': TokenType.FOR,
        'if': TokenType.IF,
        'nil': TokenType.NIL,
        'or': TokenType.OR,
        'print': TokenType.PRINT,
        'return': TokenType.RETURN,
        'super': TokenType.SUPER,
        'this': TokenType.THIS,
        'true': TokenType.TRUE,
        'var': TokenType.VAR,
        'while': TokenType.WHILE
        }

    def scan_all_tokens(self):
        while self.current_index < len(self.input_text):
            self.start_index = self.current_index
            self.check_token()
        self.token_list.append(Token(TokenType.EOF, '', '', self.line_number))
        return self.token_list

    def check_token(self):
        character = self.input_text[self.current_index]
        self.current_index += 1

        # checking for special characters like new line, whitespace, tab, return and whatever I can think of that I dont want in the token list
        if character in ' \r\t':
            return None
        
        if character == '\n':
            self.line_number += 1
            return None

        # checking for digits and making them into a number token
        # I asked AI here to help with the psudocode and the syntax for appending the tokens for each type. Im exhausted and needed the mental assistance
        """
        Syntax for appending tokens to the token list:

        self.token_list.append(
        Token(token_type, original_text, interpreted_value, line_number)
        )""" 
        # NOTE: I should probably just make this append action into a function later to help with readability

        # START OF AI HELP (I replaced the psudocode it gave me with my code)
        # After making all of my 'if' statements, I relized that I didn't account for the double characters and went back and imbedded that logic in the 'if' statement I needed to

        # single character tokens
        if character == '(':
            self.token_list.append(Token(TokenType.LEFT_PAREN, character, character, self.line_number))

        if character == ')':
            self.token_list.append(Token(TokenType.RIGHT_PAREN, character, character, self.line_number))

        if character == '{':
            self.token_list.append(Token(TokenType.LEFT_BRACE, character, character, self.line_number))

        if character == '}':
            self.token_list.append(Token(TokenType.RIGHT_BRACE, character, character, self.line_number))

        if character == ',':
            self.token_list.append(Token(TokenType.COMMA, character, character, self.line_number))

        if character == '.':
            self.token_list.append(Token(TokenType.DOT, character, character, self.line_number))

        if character == '-':
            self.token_list.append(Token(TokenType.MINUS, character, character, self.line_number))

        if character == '+':
            self.token_list.append(Token(TokenType.PLUS, character, character, self.line_number))

        if character == ';':
            self.token_list.append(Token(TokenType.SEMICOLON, character, character, self.line_number))

        # added logic and handling to check for comments 
        if character == '/':
            if self.current_index < len(self.input_text) and self.input_text[self.current_index] == '/':
                while self.current_index < len(self.input_text) and self.input_text[self.current_index] != '\n':
                    self.current_index += 1
                return None
            else:
                self.token_list.append(Token(TokenType.SLASH, character, character, self.line_number))
            
        # checking if we have multiplcation or power - NOTE reminder to edit test_scanner.py to test this after dinner!!!!!
        if character == '*':
            if self.current_index < len(self.input_text) and self.input_text[self.current_index] == '*':
                self.current_index += 1
                self.token_list.append(Token(TokenType.POWER, character + '*', character + '*', self.line_number))
            else:
                self.token_list.append(Token(TokenType.STAR, character, character, self.line_number))

        # checking if ! and if the next character is '=' then it is BANG_EQUAL, else its just BANG. Same thing for the other 2 character tokens
        if character == '!':
            if self.current_index < len(self.input_text) and self.input_text[self.current_index] == '=':
                self.current_index += 1
                self.token_list.append(Token(TokenType.BANG_EQUAL, character + '=', character + '=', self.line_number))
            else:
                self.token_list.append(Token(TokenType.BANG, character, character, self.line_number))
                

        if character == '=':
            if self.current_index < len(self.input_text) and self.input_text[self.current_index] == '=':
                self.current_index += 1
                self.token_list.append(Token(TokenType.EQUAL_EQUAL, character + '=', character + '=', self.line_number))
            else:
                self.token_list.append(Token(TokenType.EQUAL, character, character, self.line_number))

        if character == '<':
            if self.current_index < len(self.input_text) and self.input_text[self.current_index] == '=':
                self.current_index += 1
                self.token_list.append(Token(TokenType.LESS_EQUAL, character + '=', character + '=', self.line_number))
            else:
                self.token_list.append(Token(TokenType.LESS, character, character, self.line_number))

        if character == '>':
            if self.current_index < len(self.input_text) and self.input_text[self.current_index] == '=':
                self.current_index += 1
                self.token_list.append(Token(TokenType.GREATER_EQUAL, character + '=', character + '=', self.line_number))
            else:
                self.token_list.append(Token(TokenType.GREATER, character, character, self.line_number))


        # checking for digits
        if character.isdigit():
            # while the file is not empty, check the current character
            while self.current_index < len(self.input_text) and self.input_text[self.current_index].isdigit():
                self.current_index += 1

            # checking for decimal point and if the next character is a digit, then it is a decimal

            # START OF AI CODE (I had asked it to help me write this. I spent too long trying to follow in my head. its been 7 hours of working on this)
            if self.current_index < len(self.input_text) and self.input_text[self.current_index] == '.' and self.current_index + 1 < len(self.input_text) and self.input_text[self.current_index + 1].isdigit():
                self.current_index += 1
                while self.current_index < len(self.input_text) and self.input_text[self.current_index].isdigit():
                    self.current_index += 1

            # if we found a decimal then it needs to be a float, otherwise it needs to be an int
            number_string = self.input_text[self.start_index:self.current_index]
            if '.' in number_string:
                number_value = float(number_string)
            else:
                number_value = int(number_string)

            self.token_list.append(Token(TokenType.NUMBER, number_string, number_value, self.line_number))
            # END OF AI CODE

        # checking for double quotes 
        if character == '"':
            # while there is text and the next character is not a double quote, look at the next character.
            while self.current_index < len(self.input_text) and self.input_text[self.current_index] != '"':
                # if the next character is a new line, change the line number and check the next character. keeping track of line number for error reference
                if self.input_text[self.current_index] == '\n':
                    self.line_number += 1
                self.current_index += 1

            # if we found run out of text and didnt find the closing double quote, tell them they are silly and to check the line number
            if self.current_index >= len(self.input_text):
                print(f'Error: take a peek at line {self.line_number}. See that? I dont either... You should check that out and maybe add that closing double quote')
                return None

            # moving onto the next character to rinse and reapeat the process of checking
            self.current_index += 1

            # we have our completed string and are adding it to the token list
            # I relized that i needed to add a second value for the string with the quotes
            no_quote_string = self.input_text[self.start_index + 1:self.current_index - 1]
            string_value = self.input_text[self.start_index:self.current_index]
            self.token_list.append(Token(TokenType.STRING, string_value, no_quote_string, self.line_number))
        
        # checking for letters and making them into an identifier token
        if character.isalpha() and character.isascii() or character == '_':
            # while there is text to see
            while self.current_index < len(self.input_text):
                # look to the next character
                next_character = self.input_text[self.current_index]
                # if thats a letter, number, or_ then keep looking at the next character
                if next_character.isalnum() and next_character.isascii() or next_character == '_':
                    self.current_index += 1
                else:
                    # when the next character isnt what we are looking for, break
                    break

            # assigning the string we just found to our variable and adding that to the token list
            identifier_value = self.input_text[self.start_index:self.current_index]
            # referencing the dictionary of keywords to check if its a keyword or just a regualat identifier
            token_type = self.keywords.get(identifier_value, TokenType.IDENTIFIER)
            self.token_list.append(Token(token_type, identifier_value, None, self.line_number))
            return
        # END OF AI HELP

        # checking for invalid characters
        valid_characters = (
            character in '(){}.,-+;/*!<=>'
            or character == '"'
            or character.isdigit()
            or (character.isalpha() and character.isascii())
            or character == '_'
        )
        if not valid_characters:
            print(f"Woah there, what on earth is this: {character!r} look at line {self.line_number} and maybe try and fix that")

        
#NOTE: Add parser here eventually. It will need to be 'Recursive Descent Parsing'
# There are many techniques: LL(k), LR(1), LALR 
"""
Here is a helpful note from lecture

expression → equality ;
equality → comparison ( ( "!=" | "==" ) comparison )* ;
comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term → factor ( ( "-" | "+" ) factor )* ;
factor → unary ( ( "/" | "*" ) unary )* ;
unary → ( "!" | "-" ) unary
| primary ;
primary → NUMBER | STRING | "true" | "false" | "nil"
| "(" expression ")" ;

"""
# I asked AI to help with a play by play on what I needed to do to get this going
# START OF AI HELP
# 1. Start with the tokens from the scanner. The parser needs those tokens
#    so it can read the input one piece at a time.
#
# 2. Keep track of which token you are currently reading. Add small helper
#    methods to look at the current token, move to the next token, and check
#    whether the current token is the one you need.
#
# 3. Write a method for the simplest parts of an expression first. This
#    method should recognize literals like numbers, strings, true, false,
#    and nil. It should also recognize an opening parenthesis, parse the
#    expression inside it, and look for the closing parenthesis.
#
# 4. Build the AST as you read. Put literal values in Literal nodes,
#    parenthesized expressions in Grouping nodes, unary expressions in
#    Unary nodes, and expressions with two sides in Binary nodes.
#
# 5. Add a parsing method for each operator-precedence level. Start with
#    the methods for operators that bind most tightly, then have each next
#    method call the tighter level beneath it. This makes multiplication
#    stay grouped inside addition, for example.
#
# 6. For operators that group from the left, use a loop: parse the left
#    expression, find an operator, parse the right expression, and combine
#    them into a Binary node. Keep combining while there are more operators
#    at that level.
#
# 7. For an operator that groups from the right, like **, parse its right
#    side by calling the same parsing method again. This makes
#    2 ** 3 ** 2 group as 2 ** (3 ** 2).
#
# 8. Make the main expression method start at the lowest-precedence level.
#    The parser will then work down through the tighter levels until it
#    reaches a literal or a grouped expression.
#
# 9. Make an entry-point method parse the expression and then check that
#    the next token is EOF. If it is not, report the leftover token as an
#    error instead of ignoring it.
#
# 10. Connect the parser to the program: scan the input, pass the tokens
#     to the parser, then send the finished AST to the printer. Test both
#     valid expressions and invalid input so you can check the AST shape
#     and make sure errors are reported.
# END OF AI HELP

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens # the list returned by our scanner
        self.current = 0 # starting position

    # allowing us to look at the current token type without moving forward
    def look_at_current_token(self):
        return self.tokens[self.current]

    # checks to see if the current token is EOF
    def check_for_eof(self):
        return self.look_at_current_token().token_type == TokenType.EOF

    # allows us to save the current token and move onto the next token but only if its not a EOF token
    def move_to_next_token(self):
        current_token = self.look_at_current_token()

        if not self.check_for_eof():
            self.current += 1

        return current_token


    # checks to see if the current token is the token type we want then moves on
    def token_we_want(self, token_type):
        if self.look_at_current_token().token_type == token_type:
            self.move_to_next_token()
            return True
        else:
            return False

    # saves the current token first becasue matching a token moves to the next one
    # for numbers and strings it puts the scanners valye into a literal value and for true, false, and nil it turns them into True, False, and None
    # for parentheseis, it goes through the expression insdie and wraps it in a Grouping
    def parse_primary(self):
        token = self.look_at_current_token()

        if self.token_we_want(TokenType.NUMBER):
            return Literal(token.string_token)

        if self.token_we_want(TokenType.STRING):
            return Literal(token.string_token)

        if self.token_we_want(TokenType.TRUE):
            return Literal(True)

        if self.token_we_want(TokenType.FALSE):
                    return Literal(False)

        if self.token_we_want(TokenType.NIL):
                    return Literal(None)

        if self.token_we_want(TokenType.LEFT_PAREN):
            expression = self.parse_expression()

            if not self.token_we_want(TokenType.RIGHT_PAREN):
                raise SyntaxError(f"Woah bro, im over here at line {token.line_number} looking for a ')'\n and guess what I cant find... Thats right, your ')'. You should go fix that")

            return Grouping(expression)
        else:
            raise SyntaxError(f"Hey smart guy, take a peek on line {token.line_number}. There should be an expression but I dont see one. You go fix now, ok?")

    # reads the left side, if the token is POWER, it saves that then calls the function again to read the right side
    # that allows us to make a chained powers group like 2 ** (3 ** 2)
    def parse_power(self):
        left_expression = self.parse_primary()

        if self.look_at_current_token().token_type == TokenType.POWER:
            operator = self.move_to_next_token()
            right_expression = self.parse_power()

            return Binary(left_expression, operator, right_expression)
        else:
            return left_expression


    # checks if the current toke is an ! or - then saves it as the operator, goes through the expression after it and makes a unary node
    # if theres no unary operator then it moves onto looking through a power expression
    def parse_unary(self):
        token_type = self.look_at_current_token().token_type

        if token_type == TokenType.BANG or token_type == TokenType.MINUS:
            operator = self.move_to_next_token()
            right_expression = self.parse_unary()
            return Unary(operator, right_expression)

        else:
            return self.parse_power()


    # reads the left side. each time it sees a * or / it saves it as the operator, reads the next unary expression and builds a binary node
    # the purpose of making a while loop lets something like 2 * 3 / 4 be read from left to right
    def parse_factor(self):
        left_expression = self.parse_unary()

        while(self.look_at_current_token().token_type == TokenType.STAR or self.look_at_current_token().token_type == TokenType.SLASH):
            operator = self.move_to_next_token()
            right_expression = self.parse_unary()
            left_expression = Binary(left_expression,operator,right_expression)

        return left_expression

    # This has the same concept as parse_factor but checking for + or -
    # it calls parse_factor for each side so multiplication and division have a higher priotirty than addition and subtraction (PEMDAS)
    def parse_plus_and_minus(self):
        left_expression = self.parse_factor()

        while(self.look_at_current_token().token_type == TokenType.PLUS or self.look_at_current_token().token_type == TokenType.MINUS):
            operator = self.move_to_next_token()
            right_expression = self.parse_factor()
            left_expression = Binary(left_expression,operator,right_expression)

        return left_expression


    # reads from left to right then combines more expressions when it sees <, <=, >, >=
    # because it calls parese_plus_or_minus for each side, each expressions stays together before it builds the comparison
    def parse_comparison(self):
        left_expression = self.parse_plus_and_minus()

        while(self.look_at_current_token().token_type == TokenType.GREATER
              or self.look_at_current_token().token_type == TokenType.GREATER_EQUAL
              or self.look_at_current_token().token_type == TokenType.LESS
              or self.look_at_current_token().token_type == TokenType.LESS_EQUAL):

            operator = self.move_to_next_token()
            right_expression = self.parse_plus_and_minus()
            left_expression = Binary(left_expression,operator,right_expression)

        return left_expression


    # reads a comparison expression then combinese ith with another comparison when it finds == or != and also follows the PEMDAS heirachy
    def parse_equality(self):
        left_expression = self.parse_comparison()

        while(self.look_at_current_token().token_type == TokenType.EQUAL_EQUAL
              or self.look_at_current_token().token_type == TokenType.BANG_EQUAL):

            operator = self.move_to_next_token()
            right_expression = self.parse_comparison()
            left_expression = Binary(left_expression,operator,right_expression)

        return left_expression


    # reads the equality expression then combines it with another one whenever it sees and
    def parse_and(self):
        left_expression = self.parse_equality()

        while(self.look_at_current_token().token_type == TokenType.AND):
            operator = self.move_to_next_token()
            right_expression = self.parse_equality()
            left_expression = Binary(left_expression,operator,right_expression)

        return left_expression


    # same logic as 'parse_and' reads the left and right side and will make sure expressions follow their grammer rule
    def parse_or(self):
            left_expression = self.parse_and()
    
            while(self.look_at_current_token().token_type == TokenType.OR):
                operator = self.move_to_next_token()
                right_expression = self.parse_and()
                left_expression = Binary(left_expression,operator,right_expression)
    
            return left_expression


    # main parser that starts with the top level 'or' logic grammer rule and will work down through the grammer tree
    def parse_expression(self):
        return self.parse_or()


    # START OF AI HELP
    # Pseudocode for reading one statement:
    # - Check whether the statement starts with the print keyword.
    # - If it does, read the expression and require a semicolon.
    # - If it does not, read an expression and require a semicolon.
    # - Return the matching statement node so the interpreter knows what to do.
    #
    # The semicolon marks where this statement ends.
    # END OF AI HELP

    # goes through the input and sees if the first token is a print statement and if it is then it will parse the expression right after it and make sure theres a ; at the end
    # If its not a print then it will just make sure theres a ; at the end of the expression and return the whole thing as an expression statement
    def parse_statement(self):
            if self.token_we_want(TokenType.PRINT):
                expression = self.parse_expression()

                if not self.token_we_want(TokenType.SEMICOLON):
                    token = self.look_at_current_token()
                    raise SyntaxError(
                        f"Expected a ';' after the print statement on line {token.line_number}."
                    )

                return PrintStatement(expression)

            expression = self.parse_expression()

            if not self.token_we_want(TokenType.SEMICOLON):
                token = self.look_at_current_token()
                raise SyntaxError(
                    f"Expected a ';' after the expression statement on line {token.line_number}."
                )

            return ExpressionStatement(expression) 




    # START OF AI HELP
    # Pseudocode for reading a whole program:
    # - Make an empty list for the statements.
    # - Keep reading statements until the input reaches EOF.
    # - If a statement has a syntax error, show the error and try to recover.
    # - Return the statements that were read successfully.
    #
    # This lets the parser keep going instead of stopping at the first bad statement.
    # END OF AI HELP

    # this is going though parse_statement() until it reached the EOF then returns the list of them
    def parse_program(self):
        statements = []

        while not self.check_for_eof():
            try:
                statement = self.parse_statement()
                statements.append(statement)
            except SyntaxError as error:
                print("\nuh ohhh, you made a little syntax error:\n", error)
                self.recover()

        return statements





    # START OF AI HELP
    # Pseudocode for recovering after a syntax error:
    # - Move through the tokens until reaching EOF, a semicolon, or a likely
    #   start of the next statement.
    # - If a semicolon is found, move past it because it ended the bad statement.
    # - If a likely statement start is found, leave it there so parsing can try again.
    #
    # Skipping ahead helps one mistake from stopping the rest of the program.
    # END OF AI HELP


    # this is going to skip to a ; or will leave the next statement 'start' token thats ready for parsing
    def recover(self):
        while not self.check_for_eof():
            token_type = self.look_at_current_token().token_type

            if token_type == TokenType.SEMICOLON:
                self.move_to_next_token()
                return

            if (token_type == TokenType.PRINT
                    or token_type == TokenType.NUMBER
                    or token_type == TokenType.STRING
                    or token_type == TokenType.TRUE
                    or token_type == TokenType.FALSE
                    or token_type == TokenType.NIL
                    or token_type == TokenType.LEFT_PAREN
                    or token_type == TokenType.BANG
                    or token_type == TokenType.MINUS):
                return

            self.move_to_next_token()


    # goes through the input expression then cheks for an EOF. if its not, then there is an extra token and yell at the user for their mistake
    def parse_input(self):
        expression = self.parse_expression()

        if not self.check_for_eof():
            token = self.look_at_current_token()
            raise SyntaxError(f"My guyyyy, I finished the expression, but found {token.raw_token} on line {token.line_number}. That's an extra token. You go fix now, ok?")
        else:
            return expression

# End of parser


# START OF AI HELP
# Pseudocode for running Yuck input:
# - Scan the source text into tokens.
# - Give the tokens to the parser to get a list of statements.
# - Give the statements to the interpreter to run them.
# - Catch syntax and runtime errors and show the message.
# END OF AI HELP

def run(input_text):
    scanner = Scanner(input_text)
    tokens = scanner.scan_all_tokens()
    parser = Parser(tokens)

    try:
        statements = parser.parse_program()
        interpreter = Interpreter()
        interpreter.interpret(statements)

    except SyntaxError as error:
        print("\nuh ohhh, you made a little syntax error:\n", error)

    except (TypeError, ZeroDivisionError) as error:
        print("\nuh ohhh, there was a runtime error:\n", error)

#Takes the file path as an argument and runs the file
def open_file(path):
    with open(path, 'r') as file:
        input_text = file.read()

    run(input_text)

#Takes user file input and runs the input
def print_prompt():
    try:
        while True:
            input_text = input('> ') # This made it easier to follow with a '>'  vs having it blank
            print(f'{input_text}')
            run(input_text)
    except KeyboardInterrupt: # exits with Ctrl+C
        print()
        
def main():
    if len(sys.argv) == 1:   #If there is only one argument in the command line
        print_prompt()

    elif len(sys.argv) == 2:   #If there are two arguments in the command line, the second argument is the file path
        open_file(sys.argv[1])

    else:
        print('Usage: python src/yuck.py [script]')


if __name__ == "__main__":
    main()