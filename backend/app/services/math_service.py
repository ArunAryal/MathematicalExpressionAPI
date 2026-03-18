# uses SymPy to solve/simplify expressions

from sympy.parsing.latex import parse_latex
from sympy import solve,Eq
from sympy.core.relational import Relational
import logging

#parse_latex convers latex stirng into Sumpy object ,solve finds solution of an equation and EQ cretes SymPy equation object that represents an equation in sympy like EQ(x+2,5) menas x+2=5,  Relational represents any expression with a relationship used to check if the parse latex is an equation or just an expression.

# parse_latex runs first to get out of string-world into SymPy-world, and then Eq runs after to neatly reconstruct the equation from the SymPy objects that parse_latex produced.



# Create a logger named after the current module. When logs appear, you can tell exactly which file they came from.
logger=logging.getLogger(__name__)

INTEGRAL_TOKENS = (r"\int", r"\iint", r"\oint")
DERIVATIVE_TOKENS = (r"\frac{d}{d",)

class MathService:
    @staticmethod
    def process(latex:str) -> tuple[bool,str| None]: 
        #returns is_eqn,solution if it exits else None
        try:
            sympy_obj=parse_latex(latex)
        except Exception as e:
            logger.warning("Failed to parse LaTeX input '%s' :%s",latex,e)
            return False,None
            
        # integral
        if any(token in latex for token in INTEGRAL_TOKENS):
            try:
                result = sympy_obj.doit()
                return False, str(result)
            except Exception as e:
                logger.error("Failed to evaluate integral from '%s': %s", latex, e)
                return False, None

        # derivative
        if any(token in latex for token in DERIVATIVE_TOKENS):
            try:
                result = sympy_obj.doit()
                return False, str(result)
            except Exception as e:
                logger.error("Failed to evaluate derivative from '%s': %s", latex, e)
                return False, None

        #equation
        if isinstance(sympy_obj,Relational):
            try:
                solution=solve(Eq(sympy_obj.lhs-sympy_obj.rhs,0))
                evaluated=[s.doit() if hasattr(s,"doit") else s for s in solution]
                return True,str(evaluated)
            except Exception as e:
                logger.error("Failed to solve equation from input '%s': %s",latex,e)
                return True , None

        #plain expression
        return False,None