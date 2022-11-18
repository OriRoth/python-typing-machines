# Python version: 3.9.5

# Typeguard version: 2.13.3
# Site: https://typeguard.readthedocs.io
# Verdict: no error
# Reason: from looking at the source, variance is probably not supported

from typing import TypeVar, Generic, Any
from typeguard import typechecked
Z = TypeVar("Z", contravariant=True)
class N(Generic[Z]): ...
X = TypeVar("X")
class C(Generic[X], N[N["C[C[X]]"]]): ...
_: N[C[Any]] = C[Any]()
@typechecked
def f(_: N[C[Any]]): ...
f(C[Any]())
