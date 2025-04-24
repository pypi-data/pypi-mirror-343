# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------------------------------------------------
# SNOBOL4 string pattern matching
#> python -m pip install build
#> python -m pip install twine
#> python -m pip install --upgrade pip
#> python -m pip install --upgrade setuptools wheel build
#> python src/SNOBOL4python/SNOBOL4patterns.py
#> python -m build
#> python -m pip install ./dist/snobol4python-0.4.5.tar.gz
#> python -m pip install ./dist/snobol4python-0.4.5-py3-none-any.whl
#> python -m pip install --index-url https://test.pypi.org/simple SNOBOL4python
#> python -m twine check ./dist/*
#> python -m twine upload ./dist/*
#> python tests/test_01.py
#> python tests/test_json.py
#> python tests/test_arbno.py
#> python tests/test_re_simple.py
#> python ENG-685/transl8r_pop3.py > ENG-685/pop3.py
#----------------------------------------------------------------------------------------------------------------------
import re
import copy
import logging
from pprint import pprint, pformat
#----------------------------------------------------------------------------------------------------------------------
class F(Exception): pass
#----------------------------------------------------------------------------------------------------------------------
class PATTERN(object):
    def __init__(self):             self.generator = self.γ()
    def __iter__(self):             self.generator = self.γ(); return self.generator
    def __next__(self):             return next(self.generator)
    def __invert__(self):           return π(self) # pi, unary '~', optional, zero or one
    def __add__(self, other):       # SIGMA, binary +, subsequent -----------------------------------------------------
                                    if isinstance(other, str):      other = σ(str(other))
                                    if isinstance(self, Σ):         return Σ(*self.AP, other)
                                    else:                           return Σ(self, other)
    def __or__(self, other):        # PI, binary |, alternate ---------------------------------------------------------
                                    if isinstance(other, str):      other = σ(str(other))
                                    if isinstance(self, Π):         return Π(*self.AP, other)
                                    else:                           return Π(self, other)
    def __and__(self, other):       # rho, binary &, conjunction ------------------------------------------------------
                                    if isinstance(other, str):      other = σ(str(other))
                                    if isinstance(self, ρ):         return ρ(*self.AP, other)
                                    else:                           return ρ(self, other)
    def __deepcopy__(self, memo):   return type(self)() # -------------------------------------------------------------
    def __matmul__(self, other):    return δ(self, other) # delta, binary @, immediate assignment
    def __mod__(self, other):       return Δ(self, other) # DELTA, binary %, conditional assignment
    def __eq__(self, other):        return SEARCH(other, self, exc=True) # equal == operator, returns slice
    def __contains__(self, other):  return SEARCH(other, self, exc=False) # comparison in operator, returns bool
#----------------------------------------------------------------------------------------------------------------------
class STRING(str):
    def __repr__(self):             return str.__repr__(self)
    def __add__(self, other):       # SIGMA
                                    if isinstance(other, Σ):        return Σ(σ(self), *other.AP)
                                    elif isinstance(other, str):    return STRING(super().__add__(other))
                                    else:                           return Σ(σ(self), other)
    def __radd__(self, other):      # SIGMA
                                    if isinstance(other, Σ):        return Σ(*other.AP, σ(self))
                                    elif isinstance(other, str):    return STRING(other.__add__(self))
                                    else:                           return Σ(other, σ(self))
    def __or__(self, other):        # PI
                                    if isinstance(other, Π):        return Π(σ(self), *other.AP)
                                    else:                           return Π(σ(self), other)
    def __xor__(self, other):       # PI
                                    if isinstance(other, Π):        return Π(*other.AP, σ(self))
                                    else:                           return Π(other, σ(self))
    def __contains__(self, other):  # in operator
                                    if isinstance(other, PATTERN):  return other.__contains__(self)
                                    else:                           return super().__contains__(other)
#----------------------------------------------------------------------------------------------------------------------
class Ϩ(STRING): pass
globals()['NULL'] = STRING('')
#----------------------------------------------------------------------------------------------------------------------
class ε(PATTERN): # epsilon, null string, zero-length string
    def __init__(self): super().__init__()
    def __repr__(self): return "ε()"
    def γ(self): global Ϣ; yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
#----------------------------------------------------------------------------------------------------------------------
class FAIL(PATTERN):
    def __init__(self): super().__init__()
    def __repr__(self): return "FAIL()"
    def γ(self): return
#----------------------------------------------------------------------------------------------------------------------
class ABORT(PATTERN):
    def __init__(self): super().__init__()
    def __repr__(self): return "ABORT()"
    def γ(self): raise F("ABORT()")
#----------------------------------------------------------------------------------------------------------------------
class SUCCESS(PATTERN):
    def __init__(self): super().__init__()
    def __repr__(self): return "SUCCESS()"
    def γ(self):
        global Ϣ
        while True:
            yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
#----------------------------------------------------------------------------------------------------------------------
class α(PATTERN):
    def __init__(self): super().__init__();
    def __repr__(self): return "α()"
    def γ(self):
        global Ϣ
        if  (Ϣ[-1].pos == 0) or \
            (Ϣ[-1].pos > 0 and Ϣ[-1].subject[Ϣ[-1].pos-1:Ϣ[-1].pos] == '\n'):
            yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
#----------------------------------------------------------------------------------------------------------------------
class ω(PATTERN):
    def __init__(self): super().__init__();
    def __repr__(self): return "ω()"
    def γ(self):
        global Ϣ
        if  (Ϣ[-1].pos == len(Ϣ[-1].subject)) or \
            (Ϣ[-1].pos < len(Ϣ[-1].subject) and Ϣ[-1].subject[Ϣ[-1].pos:Ϣ[-1].pos + 1] == '\n'):
            yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
#----------------------------------------------------------------------------------------------------------------------
class REM(PATTERN):
    def __init__(self): super().__init__()
    def __repr__(self): return "REM()"
    def γ(self):
        global Ϣ; pos0 = Ϣ[-1].pos
        Ϣ[-1].pos = len(Ϣ[-1].subject)
        yield slice(pos0, Ϣ[-1].pos)
        Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
class ARB(PATTERN): # ARB
    def __init__(self): super().__init__()
    def __repr__(self): return "ARB()"
    def γ(self):
        global Ϣ; pos0 = Ϣ[-1].pos
        while Ϣ[-1].pos <= len(Ϣ[-1].subject):
            yield slice(pos0, Ϣ[-1].pos)
            Ϣ[-1].pos += 1
        Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
class MARB(ARB): pass
#----------------------------------------------------------------------------------------------------------------------
class ζ(PATTERN):
    def __init__(self, N): super().__init__(); self.N = N
    def __repr__(self): return f"ζ({pformat(self.N)})"
    def __deepcopy__(self, memo): return ζ(self.N)
    def γ(self):
        if not isinstance(self.N, str):
            if callable(self.N): self.P = self.N()
            else: self.P = _globals[str(self.N)]
        else: self.P = _globals[self.N]
        yield from copy.deepcopy(self.P)
#----------------------------------------------------------------------------------------------------------------------
class nPush(PATTERN):
    def __init__(self): super().__init__()
    def __repr__(self): return "nPush()"
    def γ(self):
        global Ϣ
        logger.info("nPush() SUCCESS")
        Ϣ[-1].cstack.append(f"Ϣ[-1].itop += 1")
        Ϣ[-1].cstack.append(f"Ϣ[-1].istack.append(0)")
        yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
        logger.warning("nPush() backtracking...")
        Ϣ[-1].cstack.pop()
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
class nInc(PATTERN):
    def __init__(self): super().__init__();
    def __repr__(self): return "nInc()"
    def γ(self):
        global Ϣ
        logger.info("nInc() SUCCESS")
        Ϣ[-1].cstack.append(f"Ϣ[-1].istack[Ϣ[-1].itop] += 1")
        yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
        logger.warning("nInc() backtracking...")
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
class nPop(PATTERN):
    def __init__(self): super().__init__();
    def __repr__(self): return "nPop()"
    def γ(self):
        global Ϣ
        logger.info("nPop() SUCCESS")
        Ϣ[-1].cstack.append(f"Ϣ[-1].istack.pop()")
        Ϣ[-1].cstack.append(f"Ϣ[-1].itop -= 1")
        yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
        logger.warning("nPop() backtracking...")
        Ϣ[-1].cstack.pop()
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
class Shift(PATTERN):
    def __init__(self, t=None, v=None): super().__init__(); self.t = t; self.v = v
    def __repr__(self): return f"Shift({pformat(self.t)}, {pformat(self.v)})"
    def __deepcopy__(self, memo): return Shift(self.t, self.v)
    def γ(self):
        global Ϣ
        logger.info("Shift(%r, %r) SUCCESS", self.t, self.v)
        if self.t is None:   Ϣ[-1].cstack.append(f"Ϣ[-1].shift()")
        elif self.v is None: Ϣ[-1].cstack.append(f"Ϣ[-1].shift('{self.t}')")
        else:                Ϣ[-1].cstack.append(f"Ϣ[-1].shift('{self.t}', {self.v})")
        yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
        logger.warning("Shift(%r, %r) backtracking...", self.t, self.v)
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
class Reduce(PATTERN):
    def __init__(self, t, n=-1): super().__init__(); self.t = t; self.n = n
    def __repr__(self): return f"Reduce({pformat(self.t)}, {pformat(self.n)})"
    def __deepcopy__(self, memo): return Reduce(self.t, self.n)
    def γ(self):
        global Ϣ
        if type(self.t).__name__ == 'function': self.t = self.t()
        logger.info("Reduce(%r, %r) SUCCESS", self.t, self.n)
        if   self.n == -2: self.n = "Ϣ[-1].istack[Ϣ[-1].itop + 1]"
        elif self.n == -1: self.n = "Ϣ[-1].istack[Ϣ[-1].itop]"
        Ϣ[-1].cstack.append(f"Ϣ[-1].reduce('{self.t}', {self.n})")
        yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
        logger.warning("Reduce(%r, %r) backtracking...", self.t, self.n)
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
class Pop(PATTERN):
    def __init__(self, v): super().__init__(); self.v = v
    def __repr__(self): return f"Pop({pformat(self.v)})"
    def __deepcopy__(self, memo): return Pop(self.v)
    def γ(self):
        global Ϣ
        logger.info("Pop(%s) SUCCESS", self.v)
        Ϣ[-1].cstack.append(f"{self.v} = Ϣ[-1].pop()")
        yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
        logger.warning("Pop(%s) backtracking...", self.v)
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
class BAL(PATTERN): # BAL
    def __init__(self): super().__init__()
    def __repr__(self): return "BAL()"
    def γ(self):
        global Ϣ; pos0 = Ϣ[-1].pos; nest = 0
        Ϣ[-1].pos += 1
        while Ϣ[-1].pos <= len(Ϣ[-1].subject):
            ch = Ϣ[-1].subject[Ϣ[-1].pos-1:Ϣ[-1].pos]
            match ch:
                case '(': nest += 1
                case ')': nest -= 1
            if nest < 0: break
            elif nest > 0 and Ϣ[-1].pos >= len(Ϣ[-1].subject): break
            elif nest == 0: yield slice(pos0, Ϣ[-1].pos)
            Ϣ[-1].pos += 1
        Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
class FENCE(PATTERN): # FENCE and FENCE(P)
    def __init__(self, P:PATTERN=None): super().__init__(); self.P:PATTERN = P
    def __repr__(self): return f"FENCE({pformat(self.P)})"
    def __deepcopy__(self, memo): return FENCE(copy.deepcopy(self.P))
    def γ(self):
        global Ϣ
        if self.P:
            logger.info("FENCE(%s) SUCCESS", pformat(self.P))
            yield from self.P
            logger.warning("FENCE(%s) backtracking...", pformat(self.P))
        else:
            logger.info("FENCE() SUCCESS")
            yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
            logger.warning("FENCE() backtracking...")
#----------------------------------------------------------------------------------------------------------------------
class POS(PATTERN):
    def __init__(self, n): super().__init__(); self.n = n
    def __repr__(self): return f"POS({pformat(self.n)})"
    def __deepcopy__(self, memo): return POS(self.n)
    def γ(self):
        global Ϣ
        self.pos = self.n
        if not isinstance(self.pos, int):
            if callable(self.pos): self.pos = int(self.pos())
            else: self.pos = self.n = int(self.pos)
        if Ϣ[-1].pos == self.pos:
            logger.info("POS(%d) SUCCESS(%d,%d)=", self.pos, Ϣ[-1].pos, 0)
            yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
            logger.warning("POS(%d) backtracking...", self.pos)
#----------------------------------------------------------------------------------------------------------------------
class RPOS(PATTERN):
    def __init__(self, n): super().__init__(); self.n = n
    def __repr__(self): return f"RPOS({pformat(self.n)})"
    def __deepcopy__(self, memo): return RPOS(self.n)
    def γ(self):
        global Ϣ
        self.pos = self.n
        if not isinstance(self.pos, int):
            if callable(self.pos): self.pos = int(self.pos())
            else: self.pos = self.n = int(self.pos)
        if Ϣ[-1].pos == len(Ϣ[-1].subject) - self.pos:
            logger.info("RPOS(%d) SUCCESS(%d,%d)=", self.pos, Ϣ[-1].pos, 0)
            yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
            logger.warning("RPOS(%d) backtracking...", self.pos)
#----------------------------------------------------------------------------------------------------------------------
class LEN(PATTERN):
    def __init__(self, n): super().__init__(); self.n = n
    def __repr__(self): return f"LEN({pformat(self.n)})"
    def __deepcopy__(self, memo): return LEN(self.n)
    def γ(self):
        global Ϣ
        self.len = self.n
        if not isinstance(self.len, int):
            if callable(self.len): self.len = int(self.len())
            else: self.len = self.n = int(self.len)
        if Ϣ[-1].pos + self.len <= len(Ϣ[-1].subject):
            logger.info("LEN(%d) SUCCESS(%d,%d)=%s", self.len, Ϣ[-1].pos, self.len, Ϣ[-1].subject[Ϣ[-1].pos:Ϣ[-1].pos + self.len])
            Ϣ[-1].pos += self.len
            yield slice(Ϣ[-1].pos - self.len, Ϣ[-1].pos)
            Ϣ[-1].pos -= self.len
            logger.warning("LEN(%d) backtracking(%d)...", self.len, Ϣ[-1].pos)
#----------------------------------------------------------------------------------------------------------------------
class TAB(PATTERN):
    def __init__(self, n): super().__init__(); self.n = n
    def __repr__(self): return f"TAB({pformat(self.n)})"
    def __deepcopy__(self, memo): return TAB(self.n)
    def γ(self):
        global Ϣ
        self.pos = self.n
        if not isinstance(self.pos, int):
            if callable(self.pos): self.pos = int(self.pos())
            else: self.pos = self.n = int(self.pos)
        if self.pos <= len(Ϣ[-1].subject):
            if self.pos >= Ϣ[-1].pos:
                pos0 = Ϣ[-1].pos
                Ϣ[-1].pos = self.pos
                yield slice(pos0, self.pos)
                Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
class RTAB(PATTERN):
    def __init__(self, n): super().__init__(); self.n = n
    def __repr__(self): return f"RTAB({pformat(self.n)})"
    def __deepcopy__(self, memo): return RTAB(self.n)
    def γ(self):
        global Ϣ
        self.pos = self.n
        if not isinstance(self.pos, int):
            if callable(self.pos): self.pos = int(self.pos())
            else: self.pos = self.n = int(self.pos)
        if self.pos <= len(Ϣ[-1].subject):
            self.pos = len(Ϣ[-1].subject) - self.pos
            if self.pos >= Ϣ[-1].pos:
                pos0 = Ϣ[-1].pos
                Ϣ[-1].pos = self.pos
                yield slice(pos0, self.pos)
                Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
class σ(PATTERN): # sigma, σ, sequence of characters, string patttern
    def __init__(self, s): super().__init__(); self.s = s
    def __repr__(self): return f"σ({pformat(self.s)})"
    def __deepcopy__(self, memo): return σ(self.s)
    def γ(self):
        global Ϣ; pos0 = Ϣ[-1].pos
        self.lit = self.s
        if not isinstance(self.lit, str):
            if callable(self.lit): self.lit = str(self.lit())
            else: self.lit = str(self.lit) # might need to raise an exception
        logger.debug("σ(%r) trying(%d)", self.lit, pos0)
        if pos0 + len(self.lit) <= len(Ϣ[-1].subject):
            if self.lit == Ϣ[-1].subject[pos0:pos0 + len(self.lit)]:
                logger.info("σ(%r) SUCCESS(%d,%d)=", self.lit, Ϣ[-1].pos, len(self.lit))
                Ϣ[-1].pos += len(self.lit)
                yield slice(pos0, Ϣ[-1].pos)
                logger.warning("σ(%r) backtracking(%d,%d)...", self.lit, pos0, Ϣ[-1].pos)
                Ϣ[-1].pos = pos0
        return None
#----------------------------------------------------------------------------------------------------------------------
class ANY(PATTERN):
    def __init__(self, chars): super().__init__(); self.chars = chars
    def __repr__(self): return f"ANY({pformat(self.chars)})"
    def __deepcopy__(self, memo): return ANY(self.chars)
    def γ(self):
        global Ϣ
        self.characters = self.chars
        if not isinstance(self.characters, str):
            if not isinstance(self.characters, set):
                if callable(self.characters):
                    self.characters = self.characters()
                else: self.characters = str(self.characters)
        logger.debug("ANY(%r) trying(%d)", self.characters, Ϣ[-1].pos)
        if Ϣ[-1].pos < len(Ϣ[-1].subject):
            if Ϣ[-1].subject[Ϣ[-1].pos] in self.characters:
                logger.info("ANY(%r) SUCCESS(%d,%d)=%s", self.characters, Ϣ[-1].pos, 1, Ϣ[-1].subject[Ϣ[-1].pos])
                Ϣ[-1].pos += 1
                yield slice(Ϣ[-1].pos - 1, Ϣ[-1].pos)
                logger.warning("ANY(%r) backtracking(%d,%d)...", self.characters, Ϣ[-1].pos - 1, Ϣ[-1].pos)
                Ϣ[-1].pos -= 1
#----------------------------------------------------------------------------------------------------------------------
class NOTANY(PATTERN):
    def __init__(self, chars): super().__init__(); self.chars = chars
    def __repr__(self): return f"NOTANY({pformat(self.chars)})"
    def __deepcopy__(self, memo): return NOTANY(self.chars)
    def γ(self):
        global Ϣ
        self.characters = self.chars
        if not isinstance(self.characters, str):
            if not isinstance(self.characters, set):
                if callable(self.characters):
                    self.characters = self.characters()
                else: self.characters = str(self.characters)
        logger.debug("NOTANY(%r) trying(%d)", self.characters, Ϣ[-1].pos)
        if Ϣ[-1].pos < len(Ϣ[-1].subject):
            if not Ϣ[-1].subject[Ϣ[-1].pos] in self.characters:
                logger.info("NOTANY(%r) SUCCESS(%d,%d)=%s", self.characters, Ϣ[-1].pos, 1, Ϣ[-1].subject[Ϣ[-1].pos])
                Ϣ[-1].pos += 1
                yield slice(Ϣ[-1].pos - 1, Ϣ[-1].pos)
                logger.warning("NOTANY(%r) backtracking(%d,%d)...", self.characters, Ϣ[-1].pos - 1, Ϣ[-1].pos)
                Ϣ[-1].pos -= 1
#----------------------------------------------------------------------------------------------------------------------
class SPAN(PATTERN):
    def __init__(self, chars): super().__init__(); self.chars = chars
    def __repr__(self): return f"SPAN({pformat(self.chars)})"
    def __deepcopy__(self, memo): return SPAN(self.chars)
    def γ(self):
        global Ϣ; pos0 = Ϣ[-1].pos
        self.characters = self.chars
        if not isinstance(self.characters, str):
            if not isinstance(self.characters, set):
                if callable(self.characters):
                    self.characters = self.characters()
                else: self.characters = str(self.characters)
        logger.debug("SPAN(%r) trying(%d)", self.characters, pos0)
        while True:
            if Ϣ[-1].pos >= len(Ϣ[-1].subject): break
            if Ϣ[-1].subject[Ϣ[-1].pos] in self.characters:
                Ϣ[-1].pos += 1
            else: break
        if Ϣ[-1].pos > pos0:
            logger.info("SPAN(%r) SUCCESS(%d,%d)=%s", self.characters, pos0, Ϣ[-1].pos - pos0, Ϣ[-1].subject[pos0:Ϣ[-1].pos])
            yield slice(pos0, Ϣ[-1].pos)
            logger.warning("SPAN(%r) backtracking(%d,%d)...", self.characters, pos0, Ϣ[-1].pos)
            Ϣ[-1].pos = pos0
        return None
#----------------------------------------------------------------------------------------------------------------------
class BREAK(PATTERN):
    def __init__(self, chars): super().__init__(); self.chars = chars
    def __repr__(self): return f"BREAK({pformat(self.chars)})"
    def __deepcopy__(self, memo): return BREAK(self.chars)
    def γ(self):
        global Ϣ; pos0 = Ϣ[-1].pos
        self.characters = self.chars
        if not isinstance(self.characters, str):
            if not isinstance(self.characters, set):
                if callable(self.characters):
                    self.characters = self.characters()
                else: self.characters = str(self.characters)
        logger.debug("BREAK(%r) SUCCESS(%d)", self.characters, pos0)
        while True:
            if Ϣ[-1].pos >= len(Ϣ[-1].subject): break
            if not Ϣ[-1].subject[Ϣ[-1].pos] in self.characters:
                Ϣ[-1].pos += 1
            else: break
        if Ϣ[-1].pos < len(Ϣ[-1].subject):
            logger.info("BREAK(%r) SUCCESS(%d,%d)=%s", self.characters, pos0, Ϣ[-1].pos - pos0, Ϣ[-1].subject[pos0:Ϣ[-1].pos])
            yield slice(pos0, Ϣ[-1].pos)
            logger.warning("BREAK(%r) backtracking(%d,%d)...", self.characters, pos0, Ϣ[-1].pos)
            Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
class BREAKX(BREAK): pass
#----------------------------------------------------------------------------------------------------------------------
# Immediate cursor assignment during pattern matching
class Θ(PATTERN):
    def __init__(self, N):
        super().__init__()
        self.N = N
    def __repr__(self): return f"Θ({pformat(self.N)})"
    def __deepcopy__(self, memo):
        return Θ(self.N)
    def γ(self):
        global Ϣ, _globals
        self.N = str(self.N)
        if self.N == "OUTPUT":
            Ϣ[-1].nl = True
            print(Ϣ[-1].pos, end='·');
        logger.info("Θ(%s) SUCCESS", self.N)
        _globals[self.N] = Ϣ[-1].pos
        yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
        logger.warning("Θ(%s) backtracking...", self.N)
#----------------------------------------------------------------------------------------------------------------------
# Conditional cursor assignment (after successful complete pattern match)
class θ(PATTERN):
    def __init__(self, N):
        super().__init__()
        self.N = N
    def __repr__(self): return f"θ({pformat(self.N)})"
    def __deepcopy__(self, memo):
        return θ(self.N)
    def γ(self):
        global Ϣ
        self.N = str(self.N)
        if self.N == "OUTPUT":
            Ϣ[-1].nl = True
            print(Ϣ[-1].pos, end='·')
        logger.info("θ(%s) SUCCESS", self.N)
        Ϣ[-1].cstack.append(f"{self.N} = {Ϣ[-1].pos}")
        yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
        logger.warning("θ(%s) backtracking...", self.N)
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
# Immediate match assignment during pattern matching (permanent)
class δ(PATTERN): # delta, binary '@', SNOBOL4: P $ N
    def __init__(self, P:PATTERN, N): super().__init__(); self.P:PATTERN = P; self.N = N
    def __repr__(self): return f"δ({pformat(self.P)}, {pformat(self.N)})"
    def __deepcopy__(self, memo): return δ(copy.deepcopy(self.P), self.N)
    def γ(self):
        global _globals; self.N = str(self.N)
        logger.debug("δ(%s, %s)", pformat(self.P), self.N)
        for _1 in self.P:
            assert _1 != ""
            v = Ϣ[-1].subject[_1]
            if self.N == "OUTPUT":
                Ϣ[-1].nl = True
                print(v, end='·')
            logger.debug("%s = δ(%r)", self.N, v)
            _globals[self.N] = STRING(v)
            yield _1
#----------------------------------------------------------------------------------------------------------------------
# Conditional match assignment (after successful complete pattern match)
class Δ(PATTERN): # DELTA, binary '%', SNOBOL4: P . N
    def __init__(self, P:PATTERN, N): super().__init__(); self.P:PATTERN = P; self.N = N
    def __repr__(self): return f"Δ({pformat(self.P)}, {pformat(self.N)})"
    def __deepcopy__(self, memo): return Δ(copy.deepcopy(self.P), self.N)
    def γ(self):
        global Ϣ; self.N = str(self.N)
        logger.debug("Δ(%s, %s)", pformat(self.P), self.N)
        for _1 in self.P:
            assert _1 != ""
            logger.info("%s = Δ(%r) SUCCESS", self.N, _1)
            if self.N == "OUTPUT":
                Ϣ[-1].cstack.append(f"print(Ϣ[-1].subject[{_1.start}:{_1.stop}])")
            else: Ϣ[-1].cstack.append(f"{self.N} = STRING(Ϣ[-1].subject[{_1.start}:{_1.stop}])")
            yield _1
            logger.warning("%s = Δ(%r) backtracking...", self.N, _1)
            Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
# Immediate evaluation as test during pattern matching
class Λ(PATTERN): # lambda, P *eval(), *EQ(), *IDENT(), P $ tx $ *func(tx)
    def __init__(self, expression): super().__init__(); self.expression = expression
    def __repr__(self): return f"Λ({pformat(self.expression)})"
    def __deepcopy__(self, memo): return Λ(self.expression)
    def γ(self):
        global Ϣ, _globals
        match type(self.expression).__name__:
            case 'str':
                logger.debug("Λ(%r) evaluating...", self.expression)
                try:
                    if eval(self.expression, _globals):
                        logger.info("Λ(%r) SUCCESS", self.expression)
                        yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
                        logger.warning("Λ(%r) backtracking...", self.expression)
                    else: logger.warning("Λ(%r) FAIL!", self.expression)
                except Exception as e:
                    logger.error("Λ(%r) EXCEPTION evaluating. (%r) FAIL!", self.expression, e)
            case 'function':
                logger.debug("Λ(function) evaluating...")
                try:
                    if self.expression():
                        logger.info("Λ(function) SUCCESS")
                        yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
                        logger.warning("Λ(function) backtracking...")
                    else: logger.warning("Λ(function) FAIL!")
                except Exception as e:
                    logger.error("Λ(function) EXCEPTION evaluating. (%r) FAIL!", e)
#----------------------------------------------------------------------------------------------------------------------
# Conditional match execution (after successful complete pattern match)
class λ(PATTERN): # LAMBDA, P . *exec(), P . tx . *func(tx)
    def __init__(self, command): super().__init__(); self.command = command
    def __repr__(self): return f"λ({pformat(self.command)})"
    def __deepcopy__(self, memo): return λ(self.command)
    def γ(self):
        global Ϣ
        logger.debug("λ(%r) compiling...", self.command)
        if self.command:
            if compile(self.command, '<string>', 'exec'): # 'single', 'eval'
                logger.info("λ(%r) SUCCESS", self.command)
                Ϣ[-1].cstack.append(self.command)
                yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
                logger.warning("λ(%r) backtracking...", self.command)
                Ϣ[-1].cstack.pop()
            else: logger.error("λ(%r) Error compiling. FAIL", self.command)
        else: yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
#----------------------------------------------------------------------------------------------------------------------
# Regular Expression pattern matching (with immediate assignments)
_rexs = dict()
class Φ(PATTERN):
    def __init__(self, r): super().__init__(); self.r = r
    def __repr__(self): return f"Φ({pformat(self.r)})"
    def __deepcopy__(self, memo): return Φ(self.r)
    def γ(self):
        global Ϣ, _rexs
        self.rex = self.r
        if not isinstance(self.rex, str):
            if callable(self.rex): self.rex = str(self.rex())
            else: self.rex = str(self.rex) # should possibly be exception
        if self.rex not in _rexs:
            _rexs[self.rex] = re.compile(self.rex, re.MULTILINE)
        if matches := _rexs[self.rex].match(Ϣ[-1].subject, pos = Ϣ[-1].pos, endpos = len(Ϣ[-1].subject)):
            pos0 = Ϣ[-1].pos
            if pos0 == matches.start():
                Ϣ[-1].pos = matches.end()
                for (N, V) in matches.groupdict().items():
                    _globals[N] = STRING(V)
                yield slice(pos0, Ϣ[-1].pos)
                Ϣ[-1].pos = pos0
            else: raise Exception("Yikes! Internal error.")
#----------------------------------------------------------------------------------------------------------------------
# Regular Expression pattern matching (with conditional assignments)
class φ(PATTERN):
    def __init__(self, r): super().__init__(); self.r = r
    def __repr__(self): return f"φ({pformat(self.r)})"
    def __deepcopy__(self, memo): return φ(self.r)
    def γ(self):
        global Ϣ, _rexs
        self.rex = self.r
        if not isinstance(self.rex, str):
            if callable(self.rex): self.rex = str(self.rex())
            else: self.rex = str(self.rex) # should possibly be exception
        if self.rex not in _rexs:
            _rexs[self.rex] = re.compile(self.rex, re.MULTILINE)
        if matches := _rexs[self.rex].match(Ϣ[-1].subject, pos = Ϣ[-1].pos, endpos = len(Ϣ[-1].subject)):
            pos0 = Ϣ[-1].pos
            if pos0 == matches.start():
                Ϣ[-1].pos = matches.end()
                push_count = 0
                for item in matches.re.groupindex.items():
                    N = item[0]
                    span = matches.span(item[1])
                    if span != (-1, -1):
                        push_count += 1
                        Ϣ[-1].cstack.append(f"{N} = STRING(Ϣ[-1].subject[{span[0]}:{span[1]}])")
                yield slice(pos0, Ϣ[-1].pos)
                for i in range(push_count):
                    Ϣ[-1].cstack.pop()
                Ϣ[-1].pos = pos0
            else: raise Exception("Yikes! Internal error.")
#----------------------------------------------------------------------------------------------------------------------
class ρ(PATTERN): # rho, AND, conjunction
    def __init__(self, P:PATTERN, Q:PATTERN): super().__init__(); self.P = P; self.Q = Q
    def __repr__(self): return  "ρ(*{0})".format(len(self.AP))
    def __deepcopy__(self, memo): return ρ(copy.deepcopy(self.P), copy.deepcopy(self.Q))
    def γ(self):
        global Ϣ; Ϣ[-1].depth += 1; pos0 = Ϣ[-1].pos
        for _1 in self.P:
            pos1 = Ϣ[-1].pos
            try:
                Ϣ[-1].pos = pos0
                next(self.Q)
                if (Ϣ[-1].pos == pos1):
                    yield _1
                    Ϣ[-1].pos = pos0
            except StopIteration:
                Ϣ[-1].pos = pos0
        Ϣ[-1].depth -= 1
#----------------------------------------------------------------------------------------------------------------------
class π(PATTERN): # pi, π, optional, SNOBOL4: P | epsilon
    def __init__(self, P:PATTERN): super().__init__(); self.P = P
    def __repr__(self): return f"π({pformat(self.P)})"
    def __deepcopy__(self, memo): return π(copy.deepcopy(self.P))
    def γ(self):
        global Ϣ
        Ϣ[-1].depth += 1
        yield from self.P
        yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
        Ϣ[-1].depth -= 1
#----------------------------------------------------------------------------------------------------------------------
class Π(PATTERN): # PI, Π, possibilities, alternates, alternatives, SNOBOL4: P | Q | R | S | ...
    def __init__(self, *AP:PATTERN): super().__init__(); self.AP = AP
    def __repr__(self): return  "Π(*{0})".format(len(self.AP))
    def __deepcopy__(self, memo): return Π(*(copy.deepcopy(P) for P in self.AP))
    def γ(self):
        global Ϣ
        logger.debug("Π(%s) trying(%d)...", " ".join([pformat(P) for P in self.AP]), Ϣ[-1].pos)
        Ϣ[-1].depth += 1
        for P in self.AP: yield from P
        Ϣ[-1].depth -= 1
#----------------------------------------------------------------------------------------------------------------------
class Σ(PATTERN): # SIGMA, Σ, sequence, subsequents, SNOBOL4: P Q R S T ...
    def __init__(self, *AP:PATTERN): super().__init__(); self.AP = AP
    def __repr__(self): return  "Σ(*{0})".format(len(self.AP))
    def __deepcopy__(self, memo): return Σ(*(copy.deepcopy(P) for P in self.AP))
    def γ(self):
        global Ϣ; Ϣ[-1].depth += 1; pos0 = Ϣ[-1].pos
        logger.debug("Σ(%s) trying(%d)...", " ".join([pformat(P) for P in self.AP]), pos0)
        highmark = 0
        cursor = 0
        while cursor >= 0:
            if cursor >= len(self.AP):
                logger.info("Σ(*) SUCCESS(%d,%d)=%s", pos0, Ϣ[-1].pos - pos0, Ϣ[-1].subject[pos0:Ϣ[-1].pos])
                yield slice(pos0, Ϣ[-1].pos)
                logger.warning("Σ(*) backtracking(%d,%d)...", pos0, Ϣ[-1].pos)
                cursor -= 1
            if cursor >= highmark:
                iter(self.AP[cursor])
                highmark += 1
            try:
                next(self.AP[cursor])
                cursor += 1
            except StopIteration:
                highmark -= 1
                cursor -= 1
        Ϣ[-1].depth -= 1
#----------------------------------------------------------------------------------------------------------------------
class ARBNO(PATTERN):
    def __init__(self, P:PATTERN): super().__init__(); self.P = P
    def __repr__(self): return  "ARBNO({0})".format(pformat(self.P))
    def __deepcopy__(self, memo): return ARBNO(copy.deepcopy(self.P))
    def γ(self):
        global Ϣ; Ϣ[-1].depth += 1; pos0 = Ϣ[-1].pos
        logger.debug("ARBNO(%s) trying(%d)...", pformat(self.P), pos0)
        highmark = 0
        cursor = 0
        AP = []
        while cursor >= 0:
            if cursor >= len(AP):
                logger.info("ARBNO(%s) SUCCESS(%d,%d)=%s", pformat(self.P), pos0, Ϣ[-1].pos - pos0, Ϣ[-1].subject[pos0:Ϣ[-1].pos])
                yield slice(pos0, Ϣ[-1].pos)
                logger.warning("ARBNO(%s) backtracking(%d)...", pformat(self.P), pos0)
            if cursor >= highmark:
                AP.append((Ϣ[-1].pos, copy.deepcopy(self.P)))
                iter(AP[cursor][1])
                highmark += 1
            try:
                next(AP[cursor][1])
                cursor += 1
            except StopIteration:
                highmark -= 1
                cursor -= 1
                AP.pop()
        Ϣ[-1].depth -= 1
#----------------------------------------------------------------------------------------------------------------------
class MARBNO(ARBNO): pass
#----------------------------------------------------------------------------------------------------------------------
def _push(lyst): Ϣ[-1].vstack.append(lyst)
def _pop(): return Ϣ[-1].vstack.pop()
def _shift(t='', v=None):
    if v is None:
        _push([t])
    else: _push([t, v])
def _reduce(t, n):
    if n == 0 and t == 'Σ':
        _push(['ε'])
    elif n != 1 or t not in ('Σ', 'Π', 'ρ', 'snoExprList', '|', '..'):
        x = [t]
        for i in range(n):
            x.insert(1, _pop())
        _push(x)
#----------------------------------------------------------------------------------------------------------------------
class DEBUG_formatter(logging.Formatter):
    def window(self, size):
        global Ϣ
        if len(Ϣ) > 0:
            left  = Ϣ[-1].subject[max(0, Ϣ[-1].pos - size) : Ϣ[-1].pos]
            right = Ϣ[-1].subject[Ϣ[-1].pos : min(Ϣ[-1].pos + size, len(Ϣ[-1].subject))]
            pad_left  = ' ' * max(0, size - len(left))
            pad_right = ' ' * max(0, size - len(right))
            return f"{pformat(pad_left+left)}|{Ϣ[-1].pos:4d}|{pformat(right+pad_right)}"
        else: return " " * (6 + 2 * size)
    def format(self, record):
        global Ϣ, _window_size
        original_message = super().format(record)
        if len(Ϣ) > 0:
            formatted_message = "{0:s} {1:s}".format(self.window(_window_size // 2), original_message) # {2:s} # '  ' * Ϣ[-1].depth,
        else: formatted_message = original_message
        return formatted_message
#----------------------------------------------------------------------------------------------------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
logger.handlers.clear()
logger.propagate = False
handler = logging.StreamHandler()
handler.setLevel(logging.ERROR)
handler.setFormatter(DEBUG_formatter("%(message)s"))
logger.addHandler(handler)
#----------------------------------------------------------------------------------------------------------------------
class SNOBOL:
    __slots__ = ['pos', 'subject', 'depth', 'cstack', 'itop', 'istack', 'vstack', 'nl' , 'shift', 'reduce', 'pop']
    def __repr__(self): return f"('SNOBOL', {self.depth}, {self.pos}, {len(self.subject)}, {pformat(self.subject)}, {pformat(self.cstack)})"
    def __init__(self, pos:int, subject:str):
        self.pos:int        = pos
        self.subject:str    = subject
        self.depth:int      = 0
        self.cstack:list    = []
        self.itop:int       = -1
        self.istack:list    = []
        self.vstack:list    = []
        self.nl:bool        = False
        self.shift          = _shift
        self.reduce         = _reduce
        self.pop            = _pop
#----------------------------------------------------------------------------------------------------------------------
Ϣ = [] # SNOBOL stack
_globals = None # global variables
_window_size = 24 # size of sliding window display for tracing
#----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import SNOBOL4functions
    from SNOBOL4functions import GLOBALS as F_GLOBALS
else: from .SNOBOL4functions import GLOBALS as F_GLOBALS
def GLOBALS(g:dict): F_GLOBALS(g); global _globals; _globals = g
#----------------------------------------------------------------------------------------------------------------------
def TRACE(level:int=None, window:int=None):
    global _window_size, logger, handler
    if window is not None:
        _window_size = window
    if level is not None:
        logger.setLevel(level)
        handler.setLevel(level)
#----------------------------------------------------------------------------------------------------------------------
def MATCH     (S, P:PATTERN, exc=False) -> slice: return SEARCH(S, POS(0) + P, exc)
def FULLMATCH (S, P:PATTERN, exc=False) -> slice: return SEARCH(S, POS(0) + P + RPOS(0), exc)
def SEARCH    (S, P:PATTERN, exc=False) -> slice:
    global _globals, Ϣ; S = str(S)
    if _globals is None:
        _globals = globals()
    slyce = None
    command = None
    Ϣ.append(None)
    for cursor in range(0, 1+len(S)):
        TRY = copy.deepcopy(P)
        iter(TRY)
        try:
            Ϣ[-1] = SNOBOL(cursor, S)
            slyce = next(TRY)
            if Ϣ[-1].nl: print()
            logger.info(f'SEARCH(): "{S}" ? "{slyce}"')
            for command in Ϣ[-1].cstack:
                logger.debug('SEARCH(): %r', command)
            try:
                _globals['Ϣ'] = Ϣ
                _globals['STRING'] = STRING
                for command in Ϣ[-1].cstack:
                    exec(command, _globals)
            except Exception as e:
                logger.error("SEARCH(): Exception: %r, command: %r", e, command)
            break
        except StopIteration:
            if Ϣ[-1].nl: print()
        except F as e:
            if Ϣ[-1].nl: print()
            logger.error("SEARCH(): FAILURE: %r", e)
            Ϣ.pop()
            raise
        except Exception as e:
            if Ϣ[-1].nl: print()
            logger.critical("SEARCH(): Exception: %r", e)
            Ϣ.pop()
            raise
    Ϣ.pop()
    if exc == True and not slyce: raise F("FAIL")
    return slyce
#-----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import SNOBOL4functions
    from SNOBOL4functions import ALPHABET, DIGITS, UCASE, LCASE
    from SNOBOL4functions import DEFINE, REPLACE, SUBSTITUTE
    from SNOBOL4functions import END, RETURN, FRETURN, NRETURN
    GLOBALS(globals())
    TRACE(50)
#   --------------------------------------------------------------------------------------------------------------------
    if "SNOBOL4" in POS(0) + (SPAN("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + σ('4')) % "name" + RPOS(0):
        print(name)
    if "SNOBOL4" in POS(0) + (BREAK("0123456789") + σ('4')) % "name" + RPOS(0):
        print(name)
    if "001_01C717AB.5C51AFDE ..." in φ(r"(?P<name>[0-9]{3}(_[0-9A-F]{4})?_[0-9A-F]{8}\.[0-9A-F]{8})"):
        print(name)
#   --------------------------------------------------------------------------------------------------------------------
    exit(0)
#-----------------------------------------------------------------------------------------------------------------------
