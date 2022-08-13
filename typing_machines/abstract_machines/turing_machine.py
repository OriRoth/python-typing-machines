from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from typing import List


class Direction(Enum):
	"""
	Machine head move direction.
	"""
	LEFT = 1
	RIGHT = 2


@dataclass
class Transition:
	"""
	Turing machine transition.
	When the machine is in state `source_state` and
	and the current tape cell contains the letter `read_letter`,
	the machine moves to state `target_state`, writes letter
	`write_letter` in the current cell, and moves the machine
	head according to `move_direction`.
	"""
	source_state: str
	read_letter: str
	target_state: str
	write_letter: str
	move_direction: Direction


@dataclass
class TuringMachine:
	"""
	Turing machine specifications.
	Accepts the input word immediately when reaching its single accepting state.
	"""
	BLANK = "@"
	initial_state: str
	termination_state: str
	transitions: List[Transition]
	
	@cached_property
	def alphabet(self) -> List[str]:
		"""
		Returns the machine alphabet, i.e., the set of machine letters.
		"""
		alphabet = []
		for transition in self.transitions:
			if transition.read_letter not in alphabet and transition.read_letter != TuringMachine.BLANK:
				alphabet.append(transition.read_letter)
			if transition.write_letter not in alphabet and transition.write_letter != TuringMachine.BLANK:
				alphabet.append(transition.write_letter)
		return alphabet
	
	@cached_property
	def states(self) -> List[str]:
		"""
		Returns the set of machine states.
		"""
		states = [self.initial_state]
		for transition in self.transitions:
			if transition.source_state not in states:
				states.append(transition.source_state)
			if transition.target_state not in states:
				states.append(transition.target_state)
		if self.termination_state not in states:
			states.append(self.termination_state)
		return states
