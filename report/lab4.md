# Lab 4: Statements

## Overview

For this lab, I added expression statements and print statements to Yuck. I also made an evaluator that figures out the value of expressions. An expression statement like `4 + 2;` gets evaluated, but it does not print the answer. A print statement like `print 4 + 2;` gets evaluated and shows the answer.

I also added panic-mode error recovery. When the parser hits a syntax error, it shows a message and skips ahead so it can try reading another statement. This lets it keep going after a mistake instead of stopping the whole program.

## How Statements Work

An expression statement has an expression followed by a semicolon. For example:

```text
4 + 2;
```

The evaluator figures out the answer, but the interpreter does not print it.

A print statement starts with `print` and ends with a semicolon:

```text
print 4 + 2;
```

The evaluator figures out the answer, and the interpreter prints it. It also uses Yuck's words `true`, `false`, and `nil` instead of Python's versions.

## Panic-Mode Error Recovery

When the parser cant read a statement, it shows a syntax error and tries to recover. It skips tokens until it finds a semicolon or something that looks like the start of another statement. If it finds a semicolon, it moves past it. If it finds another statement start, it leaves that token for the parser to read.

I tested this with a missing semicolon and a missing expression. In both tests, Yuck showed an error and then ran a later valid print statement.

## Setup and Running It

I used Python and did not need to install anything extra. I ran these commands from the main project folder.

To run my Lab 4 tester, I used:

```powershell
python test/lab4/test_statements.py
```

To run the valid-statements input file, I used:

```powershell
python src/yuck.py test/lab4/statements.yuck
```

To run the recovery input file, I used:

```powershell
python src/yuck.py test/lab4/recovery.yuck
```

## Statement Tests

In `test/lab4/test_statements.py` each test makes a scanner, gets the tokens, makes a parser, and runs the statements with the interpreter. I printed what I expected and compared it with what the actual result output was.

The tester checks an expression statement, different print values, addition in a print statement, and recovery after two kinds of syntax errors. Here is what I saw when I ran it:

```text
===================================================
---TESTING AN EXPRESSION STATEMENT---
Expected: Nothing should print
Actual:
===================================================

---TESTING A STRING PRINT STATEMENT---
===================================================
Expected: one
Actual:
one
===================================================

---TESTING A NUMBER PRINT STATEMENT---
===================================================
Expected: 123
Actual:
123
===================================================

---TESTING A TRUE PRINT STATEMENT---
===================================================
Expected: true
Actual:
true
===================================================

---TESTING A FALSE PRINT STATEMENT---
===================================================
Expected: false
Actual:
false
===================================================

---TESTING A NIL PRINT STATEMENT---
===================================================
Expected: nil
Actual:
nil
===================================================

---TESTING ADDITION IN A PRINT STATEMENT---
===================================================
Expected: 3
Actual:
3
===================================================

---TESTING RECOVERY AFTER A MISSING SEMICOLON---
===================================================
Expected: A missing-semicolon error, then recovered
Actual:

uh ohhh, you made a little syntax error:
 Expected a ';' after the expression statement on line 2.
recovered
===================================================

---TESTING RECOVERY AFTER A MISSING EXPRESSION---
===================================================
Expected: A missing expression error, then recovered
Actual:

uh ohhh, you made a little syntax error:
 Hey smart guy, take a peek on line 1. There should be an expression but I dont see one. You go fix now, ok?
recovered
===================================================
```

## Lab 4 Test Inputs

### Valid Statements

I used this input to check that an expression statement does not print its answer, but print statements do.

Input from `test/lab4/statements.yuck`:

```text
4 + 2;
print "one";
print true;
print 1 + 2;
print nil;
```

Expected output:

```text
one
true
3
nil
```

The expression statement `4 + 2;` should not print anything.

Actual output:

```text
one
true
3
nil
```

Result: Pass. The expression statement did not print, and the print statements showed their answers.

### Syntax-Error Recovery

I used this input to check that the parser shows syntax errors and keeps going to later statements.

Input from `test/lab4/recovery.yuck`:

```text
"one"
true;
print 2 + ;
4 + 2;
print "one";
print true;
print 1 + 2;
print nil;
```

The first expression is missing a semicolon. The `print 2 + ;` statement is missing an expression after `+`. The later statements check if the parser can recover and keep going.

Actual output:

```text
uh ohhh, you made a little syntax error:
 Expected a ';' after the expression statement on line 2.

uh ohhh, you made a little syntax error:
 Hey smart guy, take a peek on line 3. There should be an expression but I dont see one. You go fix now, ok?
one
true
3
nil
```

Result: Pass. The parser showed both errors and kept going. The expression statement did not print, and the later print statements showed `one`, `true`, `3`, and `nil`.

## Limitations

Yuck can evaluate expressions, run expression statements, print values, and recover from the syntax errors I tested. It still does not have things like variables or control flow statements but I believe that is next.

## Conclusion

For this lab, I added expression statements and print statements, and made an evaluator to figure out expression values. I also added panic mode error recovery so the parser can keep going after syntax errors. My tests showed that expression statements do not print their answers, print statements do, and later valid statements can still run after the errors I tried
