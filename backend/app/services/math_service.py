# uses SymPy to solve/simplify expressions

from sympy.parsing.latex import parse_latex
from sympy import solve,Eq
from sympy.core.relational import Relational

class MathService:
    @staticmethod
    def process(latex:str) -> tuple[bool,str| None]:
        try:
            expr=parse_latex(latex)
        except Exception:
            return False,None
        
        if isinstance(expr,Relational):
            try:
                solution=solve(Eq(expr.lhs-expr.rhs,0))
                return True,str(solution)
            except Exception:
                return True , None
        return False,None