from decimal import Decimal as long
from fractions import Fraction as fraction
from pyplus.tools.dec import dint,SimpleType,Calc

import math
import matplotlib
import numpy as np
import numpy

from sympy import *

def safe_formula_solver(formula, **variables):
    allowed_symbols = {k: symbols(k) for k in variables.keys()}
    try:
        expr = sympify(formula, locals=allowed_symbols)
        return float(expr.subs(variables))
    except SympifyError:
        raise ValueError("包含非法符号或函数")
