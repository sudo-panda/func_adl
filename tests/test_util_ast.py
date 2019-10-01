# Tests for ast_util.py

# Now the real test code starts.
from func_adl.util_ast import lambda_is_identity, lambda_test, lambda_is_true, lambda_unwrap, lambda_body_replace
import ast

# Identity
def test_identity_is():
    assert lambda_is_identity(ast.parse('lambda x: x')) == True

def test_identity_isnot_body():
    assert lambda_is_identity(ast.parse('lambda x: x+1')) == False

def test_identity_isnot_args():
    assert lambda_is_identity(ast.parse('lambda x,y: x')) == False

def test_identity_isnot_body_var():
    assert lambda_is_identity(ast.parse('lambda x: x1')) == False

# Is this a lambda?
def test_lambda_test_expression():
    assert lambda_test(ast.parse("x")) == False

def test_lambda_assure_expression():
    try:
        lambda_test(ast.parse("x"))
        assert False
    except:
        pass

def test_lambda_assure_lambda():
    try:
        lambda_test(ast.parse("lambda:x : x+1"))
        assert False
    except:
        pass

def test_lambda_simple_ast_expr():
    assert lambda_test(ast.Not()) == False

def test_lambda_test_lambda_module():
    assert lambda_test(ast.parse('lambda x: x')) == True

def test_lambda_test_raw_lambda():
    rl = ast.parse('lambda x: x').body[0].value
    assert lambda_test(rl) == True

# Is this lambda always returning true?
def test_lambda_is_true_yes():
    assert lambda_is_true(ast.parse("lambda x: True")) == True

def test_lambda_is_true_no():
    assert lambda_is_true(ast.parse("lambda x: False")) == False

def test_lambda_is_true_expression():
    assert lambda_is_true(ast.parse("lambda x: x")) == False

def test_lambda_is_true_non_lambda():
    assert lambda_is_true(ast.parse("True")) == False

# Replacement
def test_lambda_replace_simple_expression():
    a1 = ast.parse("lambda x: x")

    nexpr = ast.parse("lambda y: y + 1")
    expr = lambda_unwrap(nexpr).body

    a2 = lambda_body_replace(lambda_unwrap(a1), expr)
    a2_txt = ast.dump(a2)
    assert "op=Add(), right=Num(n=1))" in a2_txt