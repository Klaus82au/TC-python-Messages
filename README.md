# TC-python-Messages

This reads \n terminated 'packets' from the input file and
distributes them between receivers, loaded from json file.

usage:
First run swig_magic.sh script to compile the C library.
Then run ./parse.py    messages.txt    addressants.json
