# Python version: 3.9.5

# Typical version: 2.8.0
# Site: https://python-typical.org/
# Verdict: run time error
# Reason: refers to isinstance which does not support generic types

from typing import TypeVar, Generic, Any
import typic
Z = TypeVar ("Z", contravariant=True)
class N(Generic[Z]): ...
X = TypeVar("X")
class C(Generic[X], N[N["C[C[X]]"]]): ...
_: N[C[Any]] = C[Any]()

@typic.al
def f(x: N[C[Any]]): ...
#f(C())
