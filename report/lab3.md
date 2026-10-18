# Lab 3: Parser

## Overview

The main thing I worked on for this lab was getting Yuck to take the tokens from the scanner and turn them into an expression tree. I already had the AST classes and printer from Lab 2, so I used those again instead of making new ones.

I made a recursive-descent parser. Basically, it uses a group of methods that call each other to work through the expression. It starts with `parse_input()` and eventually gets to `parse_primary()`, where it handles the basic pieces like literals and expressions inside parentheses. When the parser finds an operator, it builds a `Binary` or `Unary` node to represent that part of the expression.

One part I had to pay attention to was making sure expressions get grouped the way I intended. For example, `1 + 2 * 3` should keep the multiplication together inside the addition. I also made power work from the right, so `2 ** 3 ** 2` becomes
`(** 2 (** 3 2))`. Seeing those results printed as ASTs helped me tell whether the parser was putting the pieces in the right places or not.

I also added a check to make sure the parser had used all the input. That way, if there is another token after a complete expression somehow, it can report that instead of ignorning it and causing potential issues down the road. I tried a few invalid expressions too, including a missing operand, a missing closing parenthesis, and an extra token. I made it catch those as `SyntaxError` messages and and had it print them to let you know what went wrong more specifically.

## Expression Grammar Rules

I did not add new expression rules for Lab 3. I worked on making the parser follow those rules and build the AST. Here is the grammar as a reminder.

```text
expression -> logic_or

logic_or -> logic_and ( "or" logic_and )*

logic_and -> equality ( "and" equality )*

equality -> comparison ( ( "!=" | "==" ) comparison )*

comparison -> term ( ( ">" | ">=" | "<" | "<=" ) term )*

term -> factor ( ( "-" | "+" ) factor )*

factor -> unary ( ( "/" | "*" ) unary )*

power -> primary ( "**" power )?

unary -> ( "!" | "-" ) unary
       | power

primary -> NUMBER
         | STRING
         | "true"
         | "false"
         | "nil"
         | "(" expression ")"
```

## Syntax Tree Example

For the input `1 + 2 * 3`, the syntax tree is:

```text
        +
       / \
      1   *
         / \
        2   3
```

My AST printer shows the same hierarchy like this:

```text
(+ 1 (* 2 3))
```

The `+` is at the top because it is the main expression. Its left side is `1`, and its right side is the `*` expression. That shows that `2 * 3` stays together as the right side of the addition.

## Setup and Running It

I used Python and I did not need to install anything extra. I ran the commands from the main project folder.

To run the parser tests, I used:
`python test/lab3/test_parser.py`

To run a source file, I used:
`python src/yuck.py test/lab3/sample.yuck`

To start interactive mode, I used:
`python src/yuck.py`

## Parser Tests

I wrote the tests using input strings that go through the scanner, parser, and AST printer. For each expression, I compared the printer's output with the output I expected it to be. The tests cover different expression types, operator precedence and associativity, and nested grouping. I also tested the syntax errors for invalid input.

After testing the parser, I tried running Yuck with a source sample file and in interactive mode. File mode printed the AST for a valid expression and showed an error for invalid input. In interactive mode, I entered an invalid expression followed by a valid one, and the program kept going after reporting the error.

I wrote several test expressions to check different parts of the parser. Below, I explain what each input is testing. After that, I included the results in the same order. For valid expressions, I show what I expected the AST printer to print and what it actually printed. For invalid expressions, I show the error message the parser gave me.

```text
===================================================
---TESTING SIMPLE NUMARIC EXPRESSION---
===================================================
Expected: 123
Actual: 123
PASSED - Expression matched what was expected
===================================================

---TESTING EXPRESSION WITH ADDITION AND MULTIPLICATION---
===================================================
Expected: (+ 1 (* 2 3))
Actual: (+ 1 (* 2 3))
PASSED - Multiplication stayed inside addition
===================================================

---TESTING EXPRESSION WITH POWER---
===================================================
Expected: (** 2 (** 3 2))
Actual: (** 2 (** 3 2))
PASSED - Exponentiation grouped from the right
===================================================

---TESTING A 'NOT' EXPRESSION WITH A GROUPED EXPRESSION---
===================================================
Expected: (! (group expression: (+ 1 2)))
Actual: (! (group expression: (+ 1 2)))
PASSED - Unary not and grouping worked
===================================================

---TESTING A UNARY MINUS EXPRESSION---
===================================================
Expected: (- 123)
Actual: (- 123)
PASSED - Unary minus worked
===================================================

---TESTING 'AND' & 'OR'---
===================================================
Expected: (or true (and false true))
Actual: (or true (and false true))
PASSED - And stayed grouped inside or
===================================================

---TESTING OPPERATORS WITH A COMPARISON---
===================================================
Expected: (>= (+ 1 (* 2 3)) 7)
Actual: (>= (+ 1 (* 2 3)) 7)
PASSED - Arithmetic stayed grouped inside the comparison
===================================================

---TESTING A STRING LITERAL---
===================================================
Expected: greetings and salutations my good sir
Actual: greetings and salutations my good sir
PASSED - String literal worked
===================================================

---TESTING A NIL LITERAL---
===================================================
Expected: nil
Actual: nil
PASSED - Nil literal worked
===================================================

---TESTING EQUALITY WITH ADDITION---
===================================================
Expected: (== (+ 1 2) 3)
Actual: (== (+ 1 2) 3)
PASSED - Addition stayed grouped inside equality
===================================================

---TESTING SUBTRACTION INSIDE DIVISION---
===================================================
Expected: (/ (group expression: (- 10 6)) 2)
Actual: (/ (group expression: (- 10 6)) 2)
PASSED - Subtraction stayed grouped inside division
===================================================

---TESTING GREATER THAN---
===================================================
Expected: (> 3 2)
Actual: (> 3 2)
PASSED - Greater than worked
===================================================

---TESTING LESS THAN---
===================================================
Expected: (< 1 4)
Actual: (< 1 4)
PASSED - Less than worked
===================================================

---TESTING LESS THAN OR EQUAL---
===================================================
Expected: (<= 2 9)
Actual: (<= 2 9)
PASSED - Less than or equal worked
===================================================

---TESTING NOT EQUAL---
===================================================
Expected: (!= 6 7)
Actual: (!= 6 7)
PASSED - Not equal worked
===================================================

---TESTING SUBTRACTION ASSOCIATIVITY---
===================================================
Expected: (- (- 10 3) 2)
Actual: (- (- 10 3) 2)
PASSED - Subtraction grouped from the left
===================================================

---TESTING UNARY MINUS WITH POWER---
===================================================
Expected: (- (** 2 2))
Actual: (- (** 2 2))
PASSED - Unary minus and power grouped as expected
===================================================

---TESTING NESTED GROUPING---
===================================================
Expected: (group expression: (* (group expression: (+ 1 2)) 3))
Actual: (group expression: (* (group expression: (+ 1 2)) 3))
PASSED - Nested grouping worked
===================================================

---TESTING EXTRA TOKENS---
Expected an angry message for the extra token

Actual error:
 My guyyyy, I finished the expression, but found 456 on line 1. That's an extra token. You go fix now, ok?
PASSED - Extra token was reported
===================================================

---TESTING A MISSING OPERAND---
Expected to be yelled at for a missing operand

Actual error:
 Hey smart guy, take a peek on line 1. There should be an expression but I dont see one. You go fix now, ok?

PASSED - Missing operand was reported
===================================================

---TESTING A MISSING CLOSING PARENTHESIS---
Expected to be chewed out for a missing a closing parenthesis

Actual error:
 Woah bro, im over here at line 1 looking for a ')'
 and guess what I cant find... Thats right, your ')'. You should go fix that

PASSED - Missing closing parenthesis was reported and feelings were hurt
===================================================
```

## Limitations

My parser handles expressions, but it does not execute them. It also does not parse full programs with statements or variables yet. For this lab, I focused on parsing expressions and reporting the syntax errors I tested.
