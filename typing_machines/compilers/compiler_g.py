from typing import List, Union

from typing_machines.abstract_machines.turing_machine import TuringMachine, Direction


def _render_type(*types: str, stringify_argument=True) -> str:
    assert len(types) > 0
    if len(types) == 1:
        return types[0]
    quotation: str = "\"" if stringify_argument else ""
    return f"{types[0]}[{quotation}{_render_type(*types[1:], stringify_argument=False)}{quotation}]"


TAPE_END: str = "__TAPE_END__"


def compile_g(turing_machine: TuringMachine) -> str:
    """
    Compiles a Turing machine into Python type hints that simulate it.
    Implementation of Grigore's original construction, see here for more details:
    https://arxiv.org/abs/1605.05274
    """
    typing_machine: str = ""
    # render imports and type variable
    typing_machine += "from typing import TypeVar, Generic\n"
    typing_machine += "T = TypeVar(\"T\", contravariant=True)\n"
    # render Z / N / ML / MR
    typing_machine += "class Z: ...\n"
    typing_machine += "class N(Generic[T]): ...\n"
    typing_machine += "class ML(Generic[T]): ...\n"
    typing_machine += "class MR(Generic[T]): ...\n"
    # render L_s
    typing_machine += "\n".join(f"class L_{letter}(Generic[T]): ..." for letter in turing_machine.alphabet) + "\n"
    typing_machine += f"class L_{TAPE_END}(Generic[T]): ...\n"
    # render q_lr / q_rl
    typing_machine += "\n".join(f"class QLR_{state}(Generic[T]): ..." for state in turing_machine.states) + "\n"
    typing_machine += "\n".join(f"class QRL_{state}(Generic[T]): ..." for state in turing_machine.states) + "\n"
    # render E
    supers_e: List[str] = []
    supers_e += [_render_type(f"QLR_{state}", "N", f"QRW_{state}", "E", "E", "T") for state in turing_machine.states]
    supers_e += [_render_type(f"QRL_{state}", "N", f"QLW_{state}", "E", "E", "T") for state in turing_machine.states]
    super_clause: str = "" if len(supers_e) == 0 else ", " + ", ".join(supers_e)
    typing_machine += f"class E(Generic[T]{super_clause}): ...\n"
    # render q_lw / q_rw
    for state in turing_machine.states:
        supers_lw: List[str] = []
        supers_rw: List[str] = []
        supers_lw.append(_render_type("ML", "N", f"QL_{state}", "T"))
        supers_rw.append(_render_type("MR", "N", f"QR_{state}", "T"))
        supers_lw.append(_render_type("MR", "N", f"QLW_{state}", "MR", "N", "T"))
        supers_rw.append(_render_type("ML", "N", f"QRW_{state}", "ML", "N", "T"))
        supers_lw += [_render_type(f"L_{letter}", "N", f"QLW_{state}", f"L_{letter}", "N", "T")
                      for letter in turing_machine.alphabet + [TAPE_END]]
        supers_rw += [_render_type(f"L_{letter}", "N", f"QRW_{state}", f"L_{letter}", "N", "T")
                      for letter in turing_machine.alphabet + [TAPE_END]]
        if state != turing_machine.termination_state:
            supers_lw.append(_render_type("E", f"QLR_{state}", "N", "T"))
            supers_rw.append(_render_type("E", f"QRL_{state}", "N", "T"))
        else:
            supers_lw.append(_render_type("E", "E", "Z"))
            supers_rw.append(_render_type("E", "E", "Z"))
        super_clause: str = "" if len(supers_lw) == 0 else ", " + ", ".join(supers_lw)
        typing_machine += f"class QLW_{state}(Generic[T]{super_clause}): ...\n"
        super_clause = "" if len(supers_rw) == 0 else ", " + ", ".join(supers_rw)
        typing_machine += f"class QRW_{state}(Generic[T]{super_clause}): ...\n"
    # render q_l / q_r
    for state in turing_machine.states:
        supers_l: List[str] = []
        supers_r: List[str] = []
        for transition in turing_machine.transitions:
            if transition.source_state == state:
                if transition.read_letter != TuringMachine.BLANK:
                    if transition.move_direction == Direction.LEFT:
                        supers_l.append(_render_type(f"L_{transition.read_letter}", "N",
                                                     f"QLW_{transition.target_state}", "ML", "N",
                                                     f"L_{transition.write_letter}", "N", "T"))
                        supers_r.append(_render_type(f"L_{transition.read_letter}", "N",
                                                     f"QRW_{transition.target_state}", f"L_{transition.write_letter}",
                                                     "N", "ML", "N", "T"))
                    else:
                        supers_l.append(_render_type(f"L_{transition.read_letter}", "N",
                                                     f"QLW_{transition.target_state}", f"L_{transition.write_letter}",
                                                     "N", "MR", "N", "T"))
                        supers_r.append(_render_type(f"L_{transition.read_letter}", "N",
                                                     f"QRW_{transition.target_state}", "MR", "N",
                                                     f"L_{transition.write_letter}", "N", "T"))
                else:
                    if transition.move_direction == Direction.LEFT:
                        supers_l.append(_render_type(f"L_{TAPE_END}", "N", f"QLW_{transition.target_state}",
                                                     f"L_{TAPE_END}", "N", "ML", "N",
                                                     f"L_{transition.write_letter}", "N", "T"))
                        supers_r.append(_render_type(f"L_{TAPE_END}", "N", f"QRW_{transition.target_state}",
                                                     f"L_{TAPE_END}", "N", f"L_{transition.write_letter}",
                                                     "N", "ML", "N", "T"))
                    else:
                        supers_l.append(_render_type(f"L_{TAPE_END}", "N", f"QLW_{transition.target_state}",
                                                     f"L_{TAPE_END}", "N", f"L_{transition.write_letter}",
                                                     "N", "MR", "N", "T"))
                        supers_r.append(_render_type(f"L_{TAPE_END}", "N", f"QRW_{transition.target_state}",
                                                     f"L_{TAPE_END}", "N", "MR", "N",
                                                     f"L_{transition.write_letter}", "N", "T"))
        super_clause: str = "" if len(supers_l) == 0 else ", " + ", ".join(supers_l)
        typing_machine += f"class QL_{state}(Generic[T]{super_clause}): ...\n"
        super_clause = "" if len(supers_r) == 0 else ", " + ", ".join(supers_r)
        typing_machine += f"class QR_{state}(Generic[T]{super_clause}): ...\n"
    return typing_machine.rstrip()


def compile_query_g(input_word: Union[str, List[str]],
                    turing_machine: TuringMachine):
    """
    Compiles an input word into a variable assignments which invokes a
    subtyping query.
    """
    if isinstance(input_word, str):
        return compile_query_g(list(input_word), turing_machine)
    input_word = input_word[::-1]
    tape: List[str] = []
    tape.append(f"QRW_{turing_machine.initial_state}")
    tape.append(f"L_{TAPE_END}")
    tape.append("N")
    for letter in input_word:
        tape.append(f"L_{letter}")
        tape.append("N")
    tape.append("MR")
    tape.append("N")
    tape.append(f"L_{TAPE_END}")
    tape.append("N")
    tape.append("E")
    tape.append("E")
    tape.append("Z")
    tape_type: str = "[".join(tape) + "]" * (len(tape) - 1)
    return f"_: E[E[Z]] = {tape_type}()"
