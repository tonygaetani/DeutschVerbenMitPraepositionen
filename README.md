# DeutschVerbenMitPraepositionen
Interactive way to learn which prepositions to use with German verbs

# Requirements
python 2.7

python modules: human_curl, urllib

# Usage
## Run the program
`python verbprep.py`
## Answer
Only answer with a preposition, if there are two correct answers and you know them both, just pick one!
Alternatively, if you do not know the answer then you can enter no answer. In this case the program will
print out the correct answer(s) and a translation for the verb (if available).

# `words.txt` file format
verb,preposition,case-for-preposition
or
verb,preposition,case-for-preposition,second-preposition,case-for-second-preposition

lines that begin with `#` are ignored
