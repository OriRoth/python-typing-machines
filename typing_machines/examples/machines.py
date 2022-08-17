"""
Turing machine examples.
"""

from typing_machines.abstract_machines.turing_machine import TuringMachine, Transition, Direction

anbn: TuringMachine = TuringMachine("q0", "q4", [
    Transition("q0", "a", "q1", "c", Direction.RIGHT),
    Transition("q1", "a", "q1", "a", Direction.RIGHT),
    Transition("q1", "b", "q1", "b", Direction.RIGHT),
    Transition("q1", TuringMachine.BLANK, "q2", "c", Direction.LEFT),
    Transition("q1", "c", "q2", "c", Direction.LEFT),
    Transition("q2", "b", "q3", "c", Direction.LEFT),
    Transition("q3", "a", "q3", "a", Direction.LEFT),
    Transition("q3", "b", "q3", "b", Direction.LEFT),
    Transition("q3", TuringMachine.BLANK, "q0", "c", Direction.RIGHT),
    Transition("q3", "c", "q0", "c", Direction.RIGHT),
    Transition("q0", TuringMachine.BLANK, "q4", "c", Direction.RIGHT),
    Transition("q0", "c", "q4", "c", Direction.RIGHT),
])
""" Recognizes { a^n b^n | n >=0 } """

palindromes: TuringMachine = TuringMachine("q0", "q8", [
    Transition("q0", "a", "q1", "c", Direction.RIGHT),
    Transition("q1", "a", "q2", "a", Direction.RIGHT),
    Transition("q1", "b", "q2", "b", Direction.RIGHT),
    Transition("q1", TuringMachine.BLANK, "q8", "c", Direction.RIGHT),
    Transition("q1", "c", "q8", "c", Direction.RIGHT),
    Transition("q2", "a", "q2", "a", Direction.RIGHT),
    Transition("q2", "b", "q2", "b", Direction.RIGHT),
    Transition("q2", TuringMachine.BLANK, "q3", "c", Direction.LEFT),
    Transition("q2", "c", "q3", "c", Direction.LEFT),
    Transition("q3", "a", "q4", "c", Direction.LEFT),
    Transition("q4", "a", "q4", "a", Direction.LEFT),
    Transition("q4", "b", "q4", "b", Direction.LEFT),
    Transition("q4", TuringMachine.BLANK, "q0", "c", Direction.RIGHT),
    Transition("q4", "c", "q0", "c", Direction.RIGHT),
    Transition("q0", "b", "q5", "c", Direction.RIGHT),
    Transition("q5", "a", "q6", "a", Direction.RIGHT),
    Transition("q5", "b", "q6", "b", Direction.RIGHT),
    Transition("q5", TuringMachine.BLANK, "q8", "c", Direction.RIGHT),
    Transition("q5", "c", "q8", "c", Direction.RIGHT),
    Transition("q6", "a", "q6", "a", Direction.RIGHT),
    Transition("q6", "b", "q6", "b", Direction.RIGHT),
    Transition("q6", TuringMachine.BLANK, "q7", "c", Direction.LEFT),
    Transition("q6", "c", "q7", "c", Direction.LEFT),
    Transition("q7", "b", "q4", "c", Direction.LEFT),
    Transition("q0", TuringMachine.BLANK, "q8", "c", Direction.RIGHT),
    Transition("q0", "c", "q8", "c", Direction.RIGHT),
])
""" Recognizes { w | w is a palindrome over {a,b} } """
