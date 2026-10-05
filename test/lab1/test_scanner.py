import os
import subprocess
import sys


project_folder = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

test_folder = os.path.dirname(os.path.abspath(__file__))
scanner_file = os.path.join(project_folder, "src", "yuck.py")


def run_test(test_name, input_file, expected_parts):
    input_path = os.path.join(test_folder, input_file)

    result = subprocess.run(
        [sys.executable, scanner_file, input_path],
        cwd=project_folder,
        capture_output=True,
        text=True
    )

    output = result.stdout
    test_passed = result.returncode == 0

    for expected_part in expected_parts:
        if expected_part not in output:
            test_passed = False
            print("Missing expected output:", expected_part)

    if test_name == "comments":
        if "ignore the rest" in output:
            test_passed = False
            print("The scanner incorrectly scanned text inside a comment.")

    if test_passed:
        print("PASS:", test_name)
    else:
        print("FAIL:", test_name)
        print("Scanner output:")
        print(output)
        if result.stderr:
            print("Error output:")
            print(result.stderr)

    return test_passed


all_tests_passed = True

if not run_test(
    "punctuation and operators",
    "test_scanner.yuck",
    [
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
        "STAR * *",
        "BANG ! !",
        "BANG_EQUAL != !=",
        "EQUAL = =",
        "EQUAL_EQUAL == ==",
        "LESS < <",
        "LESS_EQUAL <= <=",
        "GREATER > >",
        "GREATER_EQUAL >= >=",
        "EOF"
    ]
):
    all_tests_passed = False

if not run_test(
    "comments",
    "test_scanner.yuck",
    [
        "NUMBER 456 456",
        "EOF"
    ]
):
    all_tests_passed = False

if not run_test(
    "strings and identifiers",
    "test_scanner.yuck",
    [
        'STRING "hello world" hello world',
        'STRING ""',
        "IDENTIFIER beans None",
        "IDENTIFIER beans6 None",
        "IDENTIFIER _LargeBeans None"
    ]
):
    all_tests_passed = False

if not run_test(
    "keywords",
    "keywords.yuck",
    [
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
        "EOF"
    ]
):
    all_tests_passed = False

if not run_test(
    "number edge cases",
    "number_edges.yuck",
    [
        "NUMBER 0 0",
        "NUMBER 12.3 12.3",
        "NUMBER 12 12",
        "NUMBER 3 3",
        "DOT . .",
        "EOF"
    ]
):
    all_tests_passed = False

if not run_test(
    "unexpected character and recovery",
    "unexpected_character.yuck",
    [
        "'@'",
        "line 1",
        "NUMBER 123 123",
        "EOF"
    ]
):
    all_tests_passed = False

if not run_test(
    "unterminated string",
    "unterminated_string.yuck",
    [
        "Error:",
        "line",
        "closing double quote",
        "EOF"
    ]
):
    all_tests_passed = False

if not run_test(
    "empty input",
    "empty.yuck",
    [
        "EOF"
    ]
):
    all_tests_passed = False

if all_tests_passed:
    print("All tests passed.")
else:
    print("Some tests failed.")
    sys.exit(1)