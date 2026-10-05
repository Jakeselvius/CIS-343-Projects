# Lab 1: Yuck Scanner

## What My Language Does

My language is called Yuck. For this lab, I made the scanner. It reads the code and makes tokens from it. It does not parse or run the code.

I used the same keywords as Lox for now. I wanted to focus on getting the scanner to work before I started changing a lot of the language rules.

My keywords are `and`, `class`, `else`, `false`, `fun`, `for`, `if`, `nil`, `or`, `print`, `return`, `super`, `this`, `true`, `var`, and `while`.

My punctuation tokens are `(`, `)`, `{`, `}`, `,`, `.`, and `;`. My operators are `+`, `-`, `*`, `/`, `!`, `!=`, `=`, `==`, `<`, `<=`, `>`, and `>=`.

A name starts with an English letter or `_`. After that, it can have letters, numbers, or `_`. A number can be a whole number or a decimal. The decimal point is part of the number only when a digit comes after it.

Strings start and end with double quotes. The scanner keeps the quotes in the lexeme, but takes them off for the string value. Strings do not have escape sequences. The scanner currently lets a string continue onto another line.

Spaces, tabs, and carriage returns are ignored. New lines are ignored as tokens, but the scanner counts them for line numbers. A `//` comment makes the scanner skip the rest of that line.

## Regular Expressions

Number:

```text
[0-9]+(\.[0-9]+)?
```

String:

```text
"[^"]*"
```

Identifier:

```text
[A-Za-z_][A-Za-z0-9_]*
```

The string expression allows new lines because my scanner currently allows multiline strings. I did not add escape sequences.

The number expression shows digits from `0` to `9`. My code uses Python's `isdigit()` method, which can also treat some other characters like digits I found out. I have not handled every one of those cases yet.

## How Yuck Is Different From Lox

Right now, Yuck uses the same keyword spellings and operators as Lox. I chose that because I wanted to get the scanner working first. So far, the main difference is really only that I named my language Yuck. I have not added custom keyword spellings yet but plan to later down the road.

## Setup and Running It

I used Python 3. I did not install any extra libraries because I only used Python's built-in features.

I ran the commands from the main repository folder. To check the Python version, I used:

```powershell
python --version
```

To scan a source file, I used:

```powershell
python src/yuck.py test/lab1/test_scanner.yuck
```

To start interactive mode, I used:

```powershell
python src/yuck.py
```

To run my test script, I used:

```powershell
python test/lab1/test_scanner.py
```

## Tests

### Broad Scanner Test

Purpose: I used this to test multiple token types together, like punctuation, operators, numbers, strings, names, keywords, comments, and an unexpected character.

Source input from `test/lab1/test_scanner.yuck`:

```text
(){}.,-+;/* 
123
! != = == < <= > >=
123 45.67 89.
"hello world" ""
beans beans6 _LargeBeans
if iffy true trueish
/ 123 // ignore the rest of this line
456
@
123
```

Expected result: The scanner should print the tokens in order. It should skip the words after `//`, report `@` with its line number, keep going, and finish with EOF.

Actual scanner output:

```text
Woah there, what on earth is this: '@' look at line 10 and maybe try and fix that
LEFT_PAREN ( (
RIGHT_PAREN ) )
LEFT_BRACE { {
RIGHT_BRACE } }
DOT . .
COMMA , ,
MINUS - -
PLUS + +
SEMICOLON ; ;
SLASH / /
STAR * *
NUMBER 123 123
BANG ! !
BANG_EQUAL != !=
EQUAL = =
EQUAL_EQUAL == ==
LESS < <
LESS_EQUAL <= <=
GREATER > >
GREATER_EQUAL >= >=
NUMBER 123 123
NUMBER 45.67 45.67
NUMBER 89 89
DOT . .
STRING "hello world" hello world
STRING "" 
IDENTIFIER beans None
IDENTIFIER beans6 None
IDENTIFIER _LargeBeans None
IF if None
IDENTIFIER iffy None
TRUE true None
IDENTIFIER trueish None
SLASH / /
NUMBER 123 123
NUMBER 456 456
NUMBER 123 123
EOF  
```

Result: Pass. The comment text did not turn into tokens, the scanner reported `@` on line 10, and it kept scanning after the error.

### Keyword Test

Purpose: I used this to check all the keywords in my list.

Source input from `test/lab1/keywords.yuck`:

```text
and class else false fun for if nil or print return super this true var while
```

Expected result: I expected one token for each keyword, followed by EOF.

Actual scanner output from `python src/yuck.py test/lab1/keywords.yuck`:

```text
AND and None
CLASS class None
ELSE else None
FALSE false None
FUN fun None
FOR for None
IF if None
NIL nil None
OR or None
PRINT print None
RETURN return None
SUPER super None
THIS this None
TRUE true None
VAR var None
WHILE while None
EOF  
```

Result: Pass. Each word became the keyword token I expected.

### Number Edge Test

Purpose: I used this to check whole numbers, decimals, and dots next to numbers.

Source input from `test/lab1/number_edges.yuck`:

```text
0 12.3 12. . 12..3
```

Expected result: `12.3` should be one NUMBER token. In `12.` and `12..3`, the dots should be separate DOT tokens.

Actual scanner output from `python src/yuck.py test/lab1/number_edges.yuck`:

```text
NUMBER 0 0
NUMBER 12.3 12.3
NUMBER 12 12
DOT . .
DOT . .
NUMBER 12 12
DOT . .
DOT . .
NUMBER 3 3
EOF  
```

Result: Pass. The scanner only included a decimal point when a digit came after it.

### Unexpected Character and Recovery Test

Purpose: I used this to check that the scanner reports a character it does not recognize and keeps going.

Source input from `test/lab1/unexpected_character.yuck`:

```text
@
123
```

Expected result: I expected an error for `@` on line 1, then a NUMBER token for `123`, followed by EOF.

Actual scanner output from `python src/yuck.py test/lab1/unexpected_character.yuck`:

```text
Woah there, what on earth is this: '@' look at line 1 and maybe try and fix that
NUMBER 123 123
EOF  
```

Result: Pass. The scanner printed the error and still scanned the next line.

### Unterminated String Test

Purpose: I used this to check what happens when I forget the closing quote.

Source input from `test/lab1/unterminated_string.yuck`:

```text
"unfinished
```

Expected result: I expected an error message with the line number, then EOF.

Actual scanner output from `python src/yuck.py test/lab1/unterminated_string.yuck`:

```text
Error: take a peek at line 1. See that? I dont either... You should check that out and maybe add that closing double quote
EOF  
```

Result: Pass. The scanner reported the missing quote and finished without stopping with an exception.

### Empty Input Test

Purpose: I used this to check what happens if the input file has nothing in it.

Source input: `test/lab1/empty.yuck` is empty.

Expected result: I expected the scanner to print EOF.

Actual scanner output from `python src/yuck.py test/lab1/empty.yuck`:

```text
EOF  
```

Result: Pass.

### Interactive Mode Test

Purpose: I used this to check that interactive mode still works after a scanner error.

What I did: I ran `python src/yuck.py`, entered `@`, then entered `123` at the next prompt. I pressed Ctrl+C to leave.

Expected result: I expected an error message for `@`, then a NUMBER token for `123` on the next input.

Actual interactive output (the lines I typed are shown after each prompt):

```text
> @
@
Woah there, what on earth is this: '@' look at line 1 and maybe try and fix that
EOF  
> 123
123
NUMBER 123 123
EOF  
```

What happened: After EOF, the program showed its next prompt. I pressed Ctrl+C there, and interactive mode exited.

Result: Pass.

### Test Script Result

I ran `python test/lab1/test_scanner.py`. It printed:

```text
PASS: punctuation and operators
PASS: comments
PASS: strings and identifiers
PASS: keywords
PASS: number edge cases
PASS: unexpected character and recovery
PASS: unterminated string
PASS: empty input
All tests passed.
```

Result: Pass.

## Limitations

- This lab only scans tokens. It does not parse or run Yuck code.
- Strings do not have escape sequences.
- The scanner lets strings continue across lines in a source file.
- The number expression uses ASCII digits, but Python's `isdigit()` can also treat some other characters like digits. I have not handled every one of those cases yet but plan to later down the road.
- Yuck currently uses the same keyword spellings and operators as Lox. I wanted to do that first so I could really understand the functionalty of it all before I changed thigs too much. Im sorry if this is not allowed but it is what helped me learn and understand the most.
- The tests I made cover the main cases I tried, but they do not check every possible input. Im sure you could break it if you tried.
