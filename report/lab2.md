# Lab 2: AST Printer

## Expression Grammar

I started with expression rules that are, once again, pretty close to Lox because just like last time I wanted to focus on making the logic work before changing a lot of the language. I split the grammar into levels so you are able to see how the different parts of an expression piece together too. It's helpful for me to be able to visualize it like that versus trying to follow it all in your head

## Expression Rules

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

I felt comfortable enough with what I have so far and wanted Yuck to have something that Lox didnt, so I added `**` for exponentiation. I made sure to give it its own `power` rule because I wanted it to have its own spot in the expression order

because `power` uses `power` again on the right side, something like `2 ** 3 ** 2` should group in theory as `2 ** (3 ** 2)`

## Design Choices and Differences from Lox

I kept most of the expression rules fairly similar to Lox because it gave me a good reference point to follow. I didnt want to change a bunch of things, like I mentioned earlier, just in the effort to make Yuck look different. Adding `**` felt like a small enough change that was one, different from Lox, and two, that I wouldnt get super confused or frustraded trying to write the logic

I used the same `Binary` class for `**` as I did for `+` and `*`. They all need a left expression, an operator, and a right expression, so I didnt think I needed a separate class just for exponentiation. That seemed like it would be a waste of space and redundent

I also changed the scanner so it checks whether another `*` comes after the first one. If there is another one, it makes a `POWER` token. If there is not, it makes a regular `STAR` token

## AST Classes and Printer

I made four classes for the different expression types

- `Literal` holds a value, like a number, string, `true`, `false`, or `nil`
- `Grouping` holds the expression inside the parentheses
- `Unary` holds an operator and the expression it goes with
- `Binary` holds a left expression, an operator, and a right expression

After I made the classes, I added a printer so I could see what the expressions looked like. It checks what kind of expression it gets and prints the parts in parentheses. When one expression is inside another, the output shows that nesting too

I decided to print a group like this: `(group expression: 45.67)`. I kept `expression:` in there because I thought it made it clearer that the number is the expression inside the group

I know that python uses `True`, `False`, and `None`, so I made the printer show them as Yucks versions `true`, `false`, and `nil`. String values print without quotation marks

## Setup and Running the Tests

I once again used Python 3 and did not need to install anything extra

I ran the AST tests by typing this into the terminal:

```powershell
python test/lab2/test_ast.py
```

I made each expression directly in the test file, then printed it and compared the result with what I expected. The test prints `PASS` when the two outputs match

I also ran the scanner tests with this just to verify my `POWER` logic worked:

```powershell
python test/lab1/test_scanner.py
```

It had `**` and `*` to check that the scanner makes a `POWER` token for two stars and a `STAR` token for one star

## AST Printer Tests

### 1. Grouping a Number

I started with a number inside a group. I wanted to see if the printer kept the group visible and printed the number inside it

**Hard-coded AST:**

```python
number = Literal(45.67)
grouped_number = Grouping(number)
```

**Expected output:**

```text
(group expression: 45.67)
```

**Actual output:**

```text
(group expression: 45.67)
```

**Result:** Pass. The output matched what I expected

### 2. Unary Minus

Next, I tried a unary expression. I made a minus token and gave it a number to go with

**Hard-coded AST:**

```python
number_for_unary = Literal(123)
minus_token = Token(TokenType.MINUS, "-", None, 1)
negative_number = Unary(minus_token, number_for_unary)
```

**Expected output:**

```text
(- 123)
```

**Actual output:**

```text
(- 123)
```

**Result:** Pass. The output matched what I expected

### 3. Exponentiation

I wanted to check that I could put one power expression inside another. I made the inside one first, then used it as the right side of the outside one. This is going to turn out to be `2 ** (3 ** 2)`

**Hard-coded AST:**

```python
first_number = Literal(2)
second_number = Literal(3)
third_number = Literal(2)

power_token = Token(TokenType.POWER, "**", None, 1)

inner_power = Binary(second_number, power_token, third_number)
full_power = Binary(first_number, power_token, inner_power)
```

**Expected output:**

```text
(** 2 (** 3 2))
```

**Actual output:**

```text
(** 2 (** 3 2))
```

**Result:** Pass. The output matched what I expected. This test makes the `POWER` token directly, so it checks the printer and not the scanner

### 4. String Literal

I tried testing a string next

**Hard-coded AST:**

```python
message = Literal("Why did you make this language")
```

**Expected output:**

```text
Why did you make this language
```

**Actual output:**

```text
Why did you make this language
```

**Result:** Pass. The output matched what I expected

### 5. True Literal

I used Python's `True` to check that the printer changed it to Yuck's lowercase `true`

**Hard-coded AST:**

```python
true_value = Literal(True)
```

**Expected output:**

```text
true
```

**Actual output:**

```text
true
```

**Result:** Pass. The output matched what I expected

### 6. False Literal

I did the same thing with Python's `False` and checked that it printed as Yucks lowercase `false`

**Hard-coded AST:**

```python
false_value = Literal(False)
```

**Expected output:**

```text
false
```

**Actual output:**

```text
false
```

**Result:** Pass. The output matched what I expected

### 7. Nil Literal

For Yucks `nil`, I used Python's `None`. I wanted to make sure the printer showed `nil` instead of `None`

**Hard-coded AST:**

```python
nil_value = Literal(None)
```

**Expected output:**

```text
nil
```

**Actual output:**

```text
nil
```

**Result:** Pass. The output matched what I expected

### 8. Addition with Multiplication

I put multiplication inside an addition to see if the printer showed which expression was inside the other one

**Hard-coded AST:**

```python
one = Literal(1)
two = Literal(2)
three = Literal(3)

multiply_token = Token(TokenType.STAR, "*", None, 1)
add_token = Token(TokenType.PLUS, "+", None, 1)

multiplication = Binary(two, multiply_token, three)
addition = Binary(one, add_token, multiplication)
```

**Expected output:**

```text
(+ 1 (* 2 3))
```

**Actual output:**

```text
(+ 1 (* 2 3))
```

**Result:** Pass. The output matched what I expected

### 9. Subtraction Inside Division

I put subtraction inside division so I could check both operators and see if the inner subtraction stayed grouped

**Hard-coded AST:**

```python
ten = Literal(10)
six = Literal(6)
two = Literal(2)

minus_token = Token(TokenType.MINUS, "-", None, 1)
divide_token = Token(TokenType.SLASH, "/", None, 1)

subtraction = Binary(ten, minus_token, six)
division = Binary(subtraction, divide_token, two)
```

**Expected output:**

```text
(/ (- 10 6) 2)
```

**Actual output:**

```text
(/ (- 10 6) 2)
```

**Result:** Pass. The output matched what I expected

### 10. Greater Than

I made a simple `>` expression to check that the operator and numbers printed in the right order

**Hard-coded AST:**

```python
three = Literal(3)
two = Literal(2)
greater_token = Token(TokenType.GREATER, ">", None, 1)
greater_expression = Binary(three, greater_token, two)
```

**Expected output:**

```text
(> 3 2)
```

**Actual output:**

```text
(> 3 2)
```

**Result:** Pass. The output matched what I expected

### 11. Less Than

I checked `<` the same way

**Hard-coded AST:**

```python
one = Literal(1)
four = Literal(4)
less_token = Token(TokenType.LESS, "<", None, 1)
less_expression = Binary(one, less_token, four)
```

**Expected output:**

```text
(< 1 4)
```

**Actual output:**

```text
(< 1 4)
```

**Result:** Pass. The output matched what I expected

### 12. Equal To

I checked `==` to make sure the printer showed the operator and both values

**Hard-coded AST:**

```python
five_left = Literal(5)
five_right = Literal(5)
equal_token = Token(TokenType.EQUAL_EQUAL, "==", None, 1)
equal_expression = Binary(five_left, equal_token, five_right)
```

**Expected output:**

```text
(== 5 5)
```

**Actual output:**

```text
(== 5 5)
```

**Result:** Pass. The output matched what I expected

### 13. Not Equal To

Then I checked `!=`

**Hard-coded AST:**

```python
six = Literal(6)
seven = Literal(7)
not_equal_token = Token(TokenType.BANG_EQUAL, "!=", None, 1)
not_equal_expression = Binary(six, not_equal_token, seven)
```

**Expected output:**

```text
(!= 6 7)
```

**Actual output:**

```text
(!= 6 7)
```

**Result:** Pass. The output matched what I expected

### 14. Greater Than or Equal To

I checked `>=` too because I wanted to make sure both characters showed up in the output

**Hard-coded AST:**

```python
eight = Literal(8)
four = Literal(4)
greater_equal_token = Token(TokenType.GREATER_EQUAL, ">=", None, 1)
greater_equal_expression = Binary(eight, greater_equal_token, four)
```

**Expected output:**

```text
(>= 8 4)
```

**Actual output:**

```text
(>= 8 4)
```

**Result:** Pass. The output matched what I expected

### 15. Less Than or Equal To

I also checked `<=`

**Hard-coded AST:**

```python
two = Literal(2)
nine = Literal(9)
less_equal_token = Token(TokenType.LESS_EQUAL, "<=", None, 1)
less_equal_expression = Binary(two, less_equal_token, nine)
```

**Expected output:**

```text
(<= 2 9)
```

**Actual output:**

```text
(<= 2 9)
```

**Result:** Pass. The output matched what I expected

### 16. Unary Logical Not

I used `!` with `false` to check another unary expression

**Hard-coded AST:**

```python
false_value = Literal(False)
not_token = Token(TokenType.BANG, "!", None, 1)
not_expression = Unary(not_token, false_value)
```

**Expected output:**

```text
(! false)
```

**Actual output:**

```text
(! false)
```

**Result:** Pass. The output matched what I expected

### 17. Or with And Inside It

I put an `and` expression inside an `or` expression so I could check both operators and see the nesting in the output

**Hard-coded AST:**

```python
true_value = Literal(True)
false_value = Literal(False)
another_true_value = Literal(True)

and_token = Token(TokenType.AND, "and", None, 1)
or_token = Token(TokenType.OR, "or", None, 1)

and_expression = Binary(false_value, and_token, another_true_value)
or_expression = Binary(true_value, or_token, and_expression)
```

**Expected output:**

```text
(or true (and false true))
```

**Actual output:**

```text
(or true (and false true))
```

**Result:** Pass. The output matched what I expected

## Scanner Test for Exponentiation

I also added a scanner test because I wanted to make sure the scanner could tell `**` apart from `*`. I gave it both operators and checked the tokens it returned

**Input:**

```text
** *
```

**Expected tokens:**

```text
POWER ** **
STAR * *
EOF
```

**Actual tokens:**

```text
POWER ** **
STAR * *
EOF
```

**Result:** Pass. `**` came out as one `POWER` token, and `*` came out as one `STAR` token

## Known Limitations

- I made the AST objects directly in the test program becasue I havent made the parser yet
- The printer shows the expression tree, but it does not calculate or run the expressions
- The exponent AST test makes a `POWER` token directly. The scanner test separately checks that the scanner recognizes `**`
- String values print without quotation marks

## Conclusion

I started with a few AST examples and kept adding more until I had examples for the expression types and operators in my grammar. It took me some time, a handfull of google searches, and a youtube video for me to understand the syntax and grammer logic but in the end, all 17 AST examples passed, and my scanner test for `**` passed too. Although this lab took a ton of time and effort to plan out, it has been very helpful with my behind the scenes understanding of programming and has also helped me gain some of my coding confidence back. On a transparency note, I had AI help write the markdown like I did in lab 1 too
