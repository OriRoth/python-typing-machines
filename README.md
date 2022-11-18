# Python Type Hints Are Turing Complete

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7004898.svg)](https://doi.org/10.5281/zenodo.7004898)

We present a reduction from Turing machines to Python type hints. The Turing machine accepts its input if and only if
the Python program is correctly typed.

## How did it happen?

[Python enhancement proposal (PEP) 484](https://peps.python.org/pep-0484/)
added optional type hints to the Python programming language. One of the features of the proposed type system is
[nominal subtyping with variance](https://peps.python.org/pep-0484/#covariance-and-contravariance). Radu Grigore showed
that [this particular form of subtyping is Turing complete](https://arxiv.org/abs/1605.05274)
by describing a reduction from Turing machines to class tables. This project applies Radu's construction with Python
type hints.

## How can I try it?

Here is one possible script (also found in `typing_machines/app.py`):

```python
from typing_machines.app import *  # import application
with open("example.py", "w") as python_file:  # write palindromes machine and input "abbabba"
    python_file.write(encode(Algorithm.Grigore, palindromes, "abbabba"))
sleep(1)  # wait for write operation
with Popen(["mypy", "example.py"]) as p:  # run mypy
    retcode = p.wait(timeout=10)
assert retcode == 0  # compiles successfully, "abbabba" is a palindrome
with open("example.py", "w") as python_file:  # write palindromes machine and input "abbbaba"
    python_file.write(encode(Algorithm.Grigore, palindromes, "abbbaba"))
sleep(1)  # wait for write operation
with Popen(["mypy", "example.py"]) as p:  # run mypy
    retcode = p.wait(timeout=10)
assert retcode != 0  # does not compile, "abbbaba" is not a palindrome
```

The `palindromes` Turing machine is defined in `typing_machines/examples/machines.py`. You can add new machines in this
file.

## Wait, so `mypy` can get into an infinite loop?

Kind of. As with many other compilers, the subtyping algorithm implemented in `mypy` is recursive, so, recursion +
infinite loop = *stack overflow*. In fact, even this simple program makes `mypy` throw a segmentation fault:

```python
from typing import TypeVar, Generic
T = TypeVar("T", contravariant=True)
class N(Generic[T]): ...
class C(N[N["C"]]): ...
_: N[C] = C()
```

This is *not* a `mypy` bug. The problem of verifying Python type hints is undecidable, so `mypy` getting stuck for
certain programs is unavoidable.

## What's new?

We introduce an alternative construction that is supposed to compile much faster for large inputs. You can try the new
construction by using `Algorithm.Roth` instead of
`Algorithm.Grigore` in the script above.
