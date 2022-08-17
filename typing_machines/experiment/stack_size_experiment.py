from os import remove
from random import Random
from resource import RLIMIT_STACK, setrlimit
from subprocess import Popen, DEVNULL
from time import sleep
from typing import Callable, List, Tuple, Iterable

import matplotlib.pyplot as plt

from typing_machines.app import encode, Algorithm
from typing_machines.examples.machines import palindromes


def binary_search(le: Callable[[int], bool]) -> int:
    """
    Finds a natural number according to the given "lower equals" predicate.
    Returns -1 if no number is found.
    """
    l: int = -1
    u: int = 1
    while le(u):
        l = u
        u *= 2
    u -= 1
    while l < u:
        m: int = (l + u) // 2 + (l + u) % 2
        if le(m):
            l = m
        else:
            u = m - 1
    return l


def get_random_palindrome(n: int) -> str:
    """
    Returns a random palindrome over {a, b} of length n.
    Always returns the same word for a given n.
    """
    random: Random = Random(n)
    palindrome: str = ""
    while n > 0:
        l: str = "a" if random.getrandbits(1) else "b"
        palindrome = l + palindrome + l
        n -= 1
    return palindrome


def get_stack_size(algorithm: Algorithm, input_word: str) -> int:
    """
    Get the call stack size mypy requires to compile the palindromes typing machine with the given
    algorithm and input palindrome.
    """

    def compiles(n: int) -> bool:
        with open("test.py", "w") as python_file:
            python_file.write(encode(algorithm, palindromes, input_word))
        sleep(1)
        stack_size: int = (n + 5) * 1000000
        with Popen(["mypy", "test.py"], preexec_fn=lambda: setrlimit(RLIMIT_STACK, (stack_size, stack_size)),
                   stdout=DEVNULL, stderr=DEVNULL) as p:
            retcode = p.wait(timeout=10)
        remove("test.py")
        return retcode != 0

    depth: int = binary_search(compiles)
    depth = 5 if depth == -1 else depth + 5
    return depth


def run_experiment(algorithm: Algorithm, input_lengths: Iterable[int]) -> List[Tuple[int, int]]:
    """
    Find mypy stack sizes for given algorithm and input lengths.
    """
    results: List[Tuple[int, int]] = []
    for n in input_lengths:
        s: int = get_stack_size(algorithm, get_random_palindrome(n))
        results.append((n * 2, s))
        print(f"mypy requires {s}M stack size with algorithm {algorithm.name} and palindrome of length {n * 2}")
    return results


if __name__ == '__main__':
    grigore_results: List[Tuple[int, int]] = run_experiment(Algorithm.Grigore, range(5, 9))
    print("Grigore's results:")
    for n, s in grigore_results:
        print(f"Grigore\t{n}\t{s}")
    roth_results: List[Tuple[int, int]] = run_experiment(Algorithm.Roth, range(5, 46, 5))
    print("Roth's results:")
    for n, s in roth_results:
        print(f"Roth\t{n}\t{s}")
    plt.plot([n for n, _ in grigore_results], [s for _, s in grigore_results], color="blue", label="Grigore")
    plt.scatter([n for n, _ in grigore_results], [s for _, s in grigore_results], color="blue", marker="o")
    plt.plot([n for n, _ in roth_results], [s for _, s in roth_results], color="green", label="Roth")
    plt.scatter([n for n, _ in roth_results], [s for _, s in roth_results], color="green", marker="x")
    plt.legend(loc="upper right")
    plt.show()
