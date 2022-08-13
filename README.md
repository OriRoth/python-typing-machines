# Python Type Hints are Turing Complete

We present a reduction from Turing machines to Python type hints.
The Turing machine accepts its input if and only if the Python
program is correctly typed.

## How did it happen?

[Python enhancement proposal (PEP) 484](https://peps.python.org/pep-0484/)
added optional type hints  to the Python programming language.
One of the features of the proposed type system is
[nominal subtyping with variance](https://peps.python.org/pep-0484/#covariance-and-contravariance).
Radu Grigore showed that [this particular form of
subtyping is Turing complete](https://arxiv.org/abs/1605.05274)
by describing a reduction from  Turing machines to class tables.
This project applies Radu's construction with Python type hints.

## How can I try it?

Here is one possible script (also found in `typing_machines/run.sh`):
```bash
export PYTHONPATH="../$PYTHONPATH:$PWD"      # register project
python3 app.py G -m palindromes > example.py # print "palindromes" typing machine
python3 app.py G -q abbabba >> example.py    # print input "abbabba" (palindrome)
sleep 1                                      # wait for write operation to finish...
mypy example.py                              # compiles successfully
sed -i '$ d' example.py                      # delete previous input
python3 app.py G -q abbaaba >> example.py    # print input "abbaaba" (not a palindrome)
sleep 1                                      # wait for write operation to finish...
mypy example.py                              # does not compile
```
The `palindromes` Turing machine is defined in `typing_machines/examples/machines.py`.
You can add new machines in this file.

## Wait, so `mypy` can get into an infinite loop?

Kind of.
As with many other compilers, the subtyping algorithm implemented
in `mypy` is recursive, so, recursion + infinite loop = *stack overflow*.
In fact, the following simple program (also found in `typing_machines/motivation/mypy_u_ok.py`)
makes `mypy` throw a segmentation  fault:
```python
from typing import TypeVar, Generic
T = TypeVar("T", contravariant=True)
class N(Generic[T]): ...
class C(N[N["C"]]): ...
_: N[C] = C()
```
This is *not* a `mypy` bug.
The problem of verifying Python type hints is undecidable,
so `mypy` getting stuck for certain programs is unavoidable.

## What's new?

We introduce an  alternative construction that
is supposed to compile much faster for large inputs.
You can try the new construction by typing `R` instead of
`G` in the first argument to `app.py`.
