import random
import operator


def parseline(line):
    if line.startswith("#"):
        return None
    parsedline = tuple(line.split(','))
    if len(parsedline) == 3:
        (verb, prep, case) = parsedline
        preps = ((prep, case),)
    elif len(parsedline) == 5:
        (verb, prep1, case1, prep2, case2) = parsedline
        preps = ((prep1, case1), (prep2, case2),)
    else:
        print "Fehler: {}".format(line)
        return None
    return verb, preps


def notnone(x):
    return True if x is not None else False


def getprogresscount(responses):
    total = 0
    for count in responses.itervalues():
        total += count
    return total


def printsummary(responses):
    for word, count in responses:
        print "{}: {}".format(word, count)


def addresponse(responses, response, verb):
    try:
        responses[response][verb] += 1
    except KeyError:
        responses[response][verb] = 1


with open('words.txt', 'r') as f:
    lines = filter(notnone, map(parseline, f.readlines()))

responses = {True: {}, False: {}}
try:
    while True:
        index = random.randint(0, len(lines) - 1)
        verb, preps = lines[index]
        response = raw_input("{} ".format(verb))
        correct = False
        for prep, case in preps:
            print "{} {} + {}".format(verb, prep, case)
            correct = correct or response == prep
        if not len(response):
            # allow no answer to learn
            continue
        addresponse(responses, correct, verb)
        print "Richtig: {}".format(getprogresscount(responses[True]))
        print "Falsch: {}".format(getprogresscount(responses[False]))
        print
except KeyboardInterrupt:
    print
    print "Korrekt Total:"
    printsummary(sorted(responses[True].items(), key=operator.itemgetter(1)))
    print
    print "Falsch Total:"
    printsummary(reversed(sorted(responses[False].items(), key=operator.itemgetter(1))))
    print
