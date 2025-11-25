# pendulum/numeric.py

from sympy import lambdify

def lambdify_expr(expr, variables):
    """
    Convert symbolic expression to numpy-callable function.
    """
    return lambdify(variables, expr, modules="numpy")
