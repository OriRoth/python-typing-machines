from typing import List, Union, Optional
from typing_machines.abstract_machines.turing_machine import TuringMachine, Direction


def _render_type(*types: str, stringify_argument=True) -> str:
	assert len(types) > 0
	if len(types) == 1:
		return types[0]
	quotation: str = "\"" if stringify_argument else ""
	return f"{types[0]}[{quotation}{_render_type(*types[1:], stringify_argument=False)}{quotation}]"


TAPE_END: str = "__TAPE_END__"


def compile_r(turing_machine: TuringMachine) -> str:
	"""
	Compiles a Turing machine into Python type hints that simulate it
	in real time.
	"""
	typing_machine: str = ""
	# render imports and type variable
	typing_machine += "from typing import TypeVar, Generic, Any\n"
	typing_machine += "T = TypeVar(\"T\", contravariant=True)\n"
	# render Z
	typing_machine += "class Z: ...\n"
	# render L_s
	typing_machine += "\n".join(f"class L_{letter}(Generic[T]): ..." for letter in turing_machine.alphabet) + "\n"
	typing_machine += f"class L_{TAPE_END}(Generic[T]): ...\n"
	# render q_l / q_r
	for state in turing_machine.states:
		if state == turing_machine.termination_state:
			continue
		supers_l = []
		supers_r = []
		for transition in turing_machine.transitions:
			if transition.source_state == state:
				if transition.read_letter != TuringMachine.BLANK:
					if transition.move_direction == Direction.LEFT:
						supers_l.append(_render_type(f"L_{transition.read_letter}", "N",
													 f"QL_{transition.target_state}",
													 f"L_{transition.write_letter}", "N", "T"))
						supers_r.append(_render_type(f"L_{transition.read_letter}",
													 f"QWRL_{transition.target_state}",
													 "N", f"L_{transition.write_letter}", "N", "T"))
					else:
						supers_l.append(_render_type(f"L_{transition.read_letter}",
													 f"QWLR_{transition.target_state}",
													 "N", f"L_{transition.write_letter}", "N", "T"))
						supers_r.append(_render_type(f"L_{transition.read_letter}", "N",
													 f"QR_{transition.target_state}",
													 f"L_{transition.write_letter}", "N", "T"))
				else:
					if transition.move_direction == Direction.LEFT:
						supers_l.append(_render_type(f"L_{TAPE_END}", f"QLSL_{transition.target_state}",
													 "N", f"L_{transition.write_letter}", "N", "T"))
						supers_r.append(_render_type(f"L_{TAPE_END}", f"QRSL_{transition.target_state}",
													 "N", f"L_{transition.write_letter}", "N", "T"))
					else:
						supers_l.append(_render_type(f"L_{TAPE_END}", f"QLSR_{transition.target_state}",
													 "N", f"L_{transition.write_letter}", "N", "T"))
						supers_r.append(_render_type(f"L_{TAPE_END}", f"QRSR_{transition.target_state}",
													 "N", f"L_{transition.write_letter}", "N", "T"))
		super_clause: str = "" if len(supers_l) == 0 else ", " + ", ".join(supers_l)
		typing_machine += f"class QL_{state}(Generic[T]{super_clause}): ...\n"
		super_clause = "" if len(supers_r) == 0 else ", " + ", ".join(supers_r)
		typing_machine += f"class QR_{state}(Generic[T]{super_clause}): ...\n"
	supers_hl = []
	supers_hr = []
	for letter in turing_machine.alphabet + [TAPE_END]:
		supers_hl.append(_render_type(f"L_{letter}", "N", "Any"))
		supers_hr.append(_render_type(f"L_{letter}", "N", "Any"))
	super_clause: str = "" if len(supers_hl) == 0 else ", " + ", ".join(supers_hl)
	typing_machine += f"class QL_{turing_machine.termination_state}(Generic[T]{super_clause}): ...\n"
	super_clause = "" if len(supers_hr) == 0 else ", " + ", ".join(supers_hr)
	typing_machine += f"class QR_{turing_machine.termination_state}(Generic[T]{super_clause}): ...\n"
	# render q_wl / q_wr
	for state in turing_machine.states:
		supers_wl = []
		supers_wr = []
		for letter in turing_machine.alphabet:
			supers_wl.append(_render_type(f"L_{letter}", "N", f"QL_{state}", f"L_{letter}", "N", "T"))
			supers_wr.append(_render_type(f"L_{letter}", "N", f"QR_{state}", f"L_{letter}", "N", "T"))
		super_clause: str = "" if len(supers_wl) == 0 else ", " + ", ".join(supers_wl)
		typing_machine += f"class QWL_{state}(Generic[T]{super_clause}): ...\n"
		super_clause = "" if len(supers_wr) == 0 else ", " + ", ".join(supers_wr)
		typing_machine += f"class QWR_{state}(Generic[T]{super_clause}): ...\n"
	# render q_rl / q_lr / q_wlr / q_wrl / q_lsl / q_rsr / q_lsr / q_rsl
	for state in turing_machine.states:
		typing_machine += f"class QRL_{state}(Generic[T]): ...\n"
		typing_machine += f"class QLR_{state}(Generic[T]): ...\n"
		typing_machine += f"class QWLR_{state}(Generic[T]): ...\n"
		typing_machine += f"class QWRL_{state}(Generic[T]): ...\n"
		typing_machine += f"class QLSL_{state}(Generic[T]): ...\n"
		typing_machine += f"class QRSR_{state}(Generic[T]): ...\n"
		typing_machine += f"class QLSR_{state}(Generic[T]): ...\n"
		typing_machine += f"class QRSL_{state}(Generic[T]): ...\n"
	# render N
	supers_n = []
	for state in turing_machine.states:
		supers_n.append(_render_type(f"QWLR_{state}", "N", f"QWR_{state}", "T"))
		supers_n.append(_render_type(f"QWRL_{state}", "N", f"QWL_{state}", "T"))
		supers_n.append(_render_type(f"QLSL_{state}", f"QRL_{state}", "N", f"L_{TAPE_END}", "N", "T"))
		supers_n.append(_render_type(f"QRSR_{state}", f"QLR_{state}", "N", f"L_{TAPE_END}", "N", "T"))
		supers_n.append(_render_type(f"QLSR_{state}", "N", f"QWR_{state}", f"L_{TAPE_END}", "N", "T"))
		supers_n.append(_render_type(f"QRSL_{state}", "N", f"QWL_{state}", f"L_{TAPE_END}", "N", "T"))
		supers_n.append(_render_type(f"QLR_{state}", "N", f"QR_{state}", "T"))
		supers_n.append(_render_type(f"QRL_{state}", "N", f"QL_{state}", "T"))
	super_clause: str = "" if len(supers_n) == 0 else ", " + ", ".join(supers_n)
	typing_machine += f"class N(Generic[T]{super_clause}): ..."
	return typing_machine


def compile_query_r(input_word: Union[str, List[str]],
					turing_machine: Optional[TuringMachine] = None):
	"""
	Compiles an input word into a variable assignments which invokes a
	subtyping query.
	"""
	if isinstance(input_word, str):
		return compile_query_r(list(input_word), turing_machine)
	tape: List[str] = []
	for letter in input_word:
		tape.append(f"L_{letter}")
		tape.append("N")
	tape.append(f"L_{TAPE_END}")
	tape.append("N")
	tape.append("Z")
	initial_state: str = turing_machine.initial_state if turing_machine else 'q0'
	value: str = _render_type(f"QR_{initial_state}", f"L_{TAPE_END}", "N", "Z")
	return f"_: {_render_type(*tape)} = {value}()"
