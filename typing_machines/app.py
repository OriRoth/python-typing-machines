from sys import argv, stderr
from typing_machines.compilers.compiler_g import compile_g, compile_query_g
from typing_machines.compilers.compiler_r import compile_r, compile_query_r
from typing_machines.examples.machines import all_machines


def _help() -> None:
	print("Usage:", file=stderr)
	print("\tpython app.py [G,R] -m <machine_name>", file=stderr)
	print("\tpython app.py [G,R] -q <input word>", file=stderr)
	print("Example:", file=stderr)
	print("\tpython app.py R -m anbn > experiment.py", file=stderr)
	print("\tpython app.py R -q aaabbb >> experiment.py", file=stderr)
	print("\tmypy experiment.py", file=stderr)
	print("\t> Success: no issues found in 1 source file", file=stderr)
	print("\tsed -i '$ d' experiment.py  # delete previous query", file=stderr)
	print("\tpython app.py R -q aababb >> experiment.py", file=stderr)
	print("\tmypy experiment.py", file=stderr)
	print("\t> error: Incompatible types in assignment [...]", file=stderr)


def main() -> None:
	"""
	The main application.
	See `_help()` for details.
	"""
	if len(argv) not in [3, 4] or argv[1] not in ["G", "R"]:
		_help()
		return
	if argv[2] == "-m":
		machine_name: str = argv[3]
		if machine_name not in all_machines:
			print(f"No machine \"{machine_name}\". Available machines:")
			print(", ".join(all_machines.keys()))
			return
		if argv[1] == "G":
			print(compile_g(all_machines[machine_name]))
		else:
			print(compile_r(all_machines[machine_name]))
		return
	elif argv[2] == "-q":
		input_word: str = argv[3] if len(argv) == 4 else ""
		if argv[1] == "G":
			print(compile_query_g(input_word))
		else:
			print(compile_query_r(input_word))
		return
	_help()


if __name__ == "__main__":
	main()
