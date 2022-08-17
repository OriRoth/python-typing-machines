from enum import Enum
from os import remove
from subprocess import Popen
from time import sleep
from typing import Union, List

from typing_machines.abstract_machines.turing_machine import TuringMachine
from typing_machines.compilers.compiler_g import compile_g, compile_query_g
from typing_machines.compilers.compiler_r import compile_r, compile_query_r
from typing_machines.examples.machines import palindromes


class Algorithm(Enum):
    """
    Supported encoding algorithms by author name.
    """
    Grigore = 1
    Roth = 2


def encode_machine(algorithm: Algorithm, machine: TuringMachine) -> str:
    """
    Encode a Turing machine as a Python class table with given algorithm.
    """
    if algorithm == Algorithm.Grigore:
        return compile_g(machine)
    elif algorithm == Algorithm.Roth:
        return compile_r(machine)
    else:
        raise Exception(f"unrecognized algorithm {algorithm}")


def encode_query(algorithm: Algorithm, machine: TuringMachine, input_word: Union[str, List[str]]) -> str:
    """
    Encode an input word as a Python subtyping query with given algorithm.
    """
    if algorithm == Algorithm.Grigore:
        return compile_query_g(input_word, machine)
    elif algorithm == Algorithm.Roth:
        return compile_query_r(input_word, machine)
    else:
        raise Exception(f"unrecognized algorithm {algorithm}")


def encode(algorithm: Algorithm, machine: TuringMachine, input_word: Union[str, List[str]]) -> str:
    """
    Encode a Turing machine and its input using Python typing hints with given algorithm.
    """
    return encode_machine(algorithm, machine) + "\n" + encode_query(algorithm, machine, input_word)


if __name__ == '__main__':
    print("Is 'abbabba' a palindrome?")
    with open("example.py", "w") as python_file:
        python_file.write(encode(Algorithm.Grigore, palindromes, "abbabba"))
    sleep(1)
    with Popen(["mypy", "example.py"]) as p:
        retcode = p.wait(timeout=10)
    assert retcode == 0  # abbabba is a palindrome
    print("Is 'abbbaba' a palindrome?")
    with open("example.py", "w") as python_file:
        python_file.write(encode(Algorithm.Grigore, palindromes, "abbbaba"))
    sleep(1)
    with Popen(["mypy", "example.py"]) as p:
        retcode = p.wait(timeout=10)
    assert retcode != 0  # abbbaba is not a palindrome
    remove("example.py")
