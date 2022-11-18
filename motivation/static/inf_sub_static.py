# Python version: 3.9.5

# Mypy version: 0.991
# Site: http://mypy-lang.org/
# Verdict: segmentation fault

# Pyre version: 0.9.17
# Note: download typeshed-main (https://github.com/python/typeshed) and place it in motivation/
# Site: https://pyre-check.org/
# Verdict: internal error

# Pyright version: 1.1.279
# Site: https://github.com/microsoft/pyright
# Verdict: type error
# Reason: ???

# Pytype version: 2022.11.10
# Site: https://google.github.io/pytype/
# Verdict: variance not supported

# Pyanalyze version: 0.8.0
# Site: https://pyanalyze.readthedocs.io
# Verdict: no error
# Reason: from looking at the source, variance is probably not supported

from typing import TypeVar, Generic, Any
Z = TypeVar ("Z", contravariant=True)
class N(Generic[Z]): ...
X = TypeVar("X")
class C(Generic[X], N[N["C[C[X]]"]]): ...
_: N[C[Any]] = C[Any]() # infinite subtyping
