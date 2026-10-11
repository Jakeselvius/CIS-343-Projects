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
class Parser:
    pass

# End of parser




def run(input_text):
    scanner = Scanner(input_text)
    tokens = scanner.scan_all_tokens()

    for current_token in tokens:
        print(current_token)

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