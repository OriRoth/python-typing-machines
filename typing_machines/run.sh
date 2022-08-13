export PYTHONPATH="../$PYTHONPATH:$PWD"      # register project
python3 app.py G -m palindromes > example.py # print "palindromes" typing machine
python3 app.py G -q abbabba >> example.py    # print input "abbabba" (palindrome)
sleep 1                                      # wait for write operation to finish...
mypy example.py                              # compiles successfully
sed -i '$ d' example.py                      # delete previous input
python3 app.py G -q abbaaba >> example.py    # print input "abbaaba" (not a palindrome)
sleep 1                                      # wait for write operation to finish...
mypy example.py                              # does not compile
