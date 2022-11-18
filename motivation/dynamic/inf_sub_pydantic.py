# Python version: 3.9.5

# Pydantic version: 1.10.2
# Site: https://pydantic-docs.helpmanual.io/
# Verdict: no error
# Reason: from looking at the source, variance is probably not supported

from typing import TypeVar, Generic
from pydantic import BaseModel
from pydantic.generics import GenericModel
Z = TypeVar("Z", contravariant=True)
class N(GenericModel, Generic[Z]): ...
class C(N[N["C"]]): ...
class A(BaseModel): x: N[C]
A(x=C())
