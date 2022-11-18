# Python version: 3.9.5

# Pytypes version: 1.0b10
# Site: https://pypi.org/project/pytypes/
# Verdict: run time error
# Reason: refers to isinstance which does not support generic types

from typing import TypeVar, Generic
from pytypes import is_subtype, resolve_fw_decl
Z = TypeVar("Z", contravariant=True)
class N(Generic[Z]): ...
class C(N[N["C"]]): ...
assert not is_subtype(resolve_fw_decl(C), resolve_fw_decl(N[C]))
