# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCESS, TAB
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
#------------------------------------------------------------------------------
GLOBALS(globals())
#------------------------------------------------------------------------------
identifier = \
        (   POS(0)
        +   ANY(UCASE + LCASE)
        +   FENCE(SPAN("." + DIGITS + UCASE + "_" + LCASE) | ε())
        +   RPOS(0)
        )
assert True is ("Id_99" in identifier)
#------------------------------------------------------------------------------
real_number = \
        (   POS(0)
        +   (   (   SPAN(DIGITS) @ 'whole'
                +   (σ('.') + FENCE(SPAN(DIGITS) | ε()) @ 'fract' | ε())
                +   (σ('E') | σ('e'))
                +   (σ('+') | σ('-') | ε())
                +   SPAN(DIGITS) @ 'exp'
                )
            |   (   SPAN(DIGITS) @ 'whole'
                +   σ('.')
                +   FENCE(SPAN(DIGITS) | ε()) @ 'fract'
                )
            )
        +   RPOS(0)
        )
assert True is ("12.99E+3" in real_number)
#------------------------------------------------------------------------------
from SNOBOL4python import Σ, Π
test_one = Σ( POS(0) @ 'OUTPUT'
           ,  Π(σ('B') , σ('F') , σ('L') , σ('R')) @ 'OUTPUT'
           ,  Π(σ('E') , σ('EA')) @ 'OUTPUT'
           ,  Π(σ('D') , σ('DS')) @ 'OUTPUT'
           ,  RPOS(0) @ 'OUTPUT'
           )
assert True is ("BED" in test_one)
assert True is ("FED" in test_one)
assert True is ("LED" in test_one)
assert True is ("RED" in test_one)
assert True is ("BEAD" in test_one)
assert True is ("FEAD" in test_one)
assert True is ("LEAD" in test_one)
assert True is ("READ" in test_one)
assert True is ("BEDS" in test_one)
assert True is ("FEDS" in test_one)
assert True is ("LEDS" in test_one)
assert True is ("REDS" in test_one)
assert True is ("BEADS" in test_one)
assert True is ("FEADS" in test_one)
assert True is ("LEADS" in test_one)
assert True is ("READS" in test_one)
#------------------------------------------------------------------------------
# units = None
# romanXlat = '0,1I,2II,3III,4IV,5V,6VI,7VII,8VIII,9IX,'
# def Roman(n):
#     global units
#     if not MATCH_REPLACE(n, RPOS(1) + LEN(1) @ 'units', ''):
#         return ""
#     if not units, BREAK(',') @ 'units', globals()):
#         return None
#     return REPLACE(Roman(n),'IVXLCDM','XLCDM**') + units
# print(Roman(1))
# print(Roman(4))
# print(Roman(5))
# print(Roman(9))
# print(Roman(10))
#------------------------------------------------------------------------------
# BALEXP = NOTANY(' ( ) , ) I ' (' ARBNO( *BALEXP) ')'
# BAL BALEXP ARBNO(BALEXP)
# ALLBAL = BAL S OUTPUT FAIL
#------------------------------------------------------------------------------
Bal = POS(0) + BAL() @ 'OUTPUT' + RPOS(0)
assert False is ("" in Bal)
assert False is (")A+B(" in Bal)
assert False is ("A+B)" in Bal)
assert False is ("(A+B" in Bal)
assert True  is ("(A+B)" in Bal)
assert True  is ("A+B()" in Bal)
assert True  is ("A()+B" in Bal)
assert False is ("A+B())" in Bal)
assert False is ("((A+B)" in Bal)
assert True  is ("X" in Bal)
assert True  is ("XYZ" in Bal)
assert True  is ("(A+B)" in Bal)
assert True  is ("A(B*C) (E/F)G+H" in Bal)
assert True  is ("( (A+ ( B*C) ) +D)" in Bal)
assert True  is ("(0+(1*9))" in Bal)
assert True  is ("((A+(B*C))+D)" in Bal)
#------------------------------------------------------------------------------
Arb = POS(0) + ARB() @ 'OUTPUT' + RPOS(0)
assert True is ("" in Arb)
assert True is ("$" in Arb)
assert True is ("$$" in Arb)
assert True is ("$$$" in Arb)
#------------------------------------------------------------------------------
