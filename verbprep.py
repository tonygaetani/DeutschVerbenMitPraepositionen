import random
import operator
import human_curl as curl
import urllib
import json

translations_cache = {}
translations_host = "https://de.wiktionary.org"
translations_query_template = "w/api.php?action=query&prop=iwlinks&titles={}&iwprop=url&iwprefix=en&format=json&continue="


def get_translations(word):
    if word in translations_cache:
        return translations_cache[word]
    query = translations_query_template.format(urllib.quote(word))
    url = "{}/{}".format(translations_host, query)
    try:
        response = curl.get(url)
    except Exception:
        return ''
    if response.status_code != 200:
        return ''
    content = json.loads(response.content)
    pages = content['query']['pages']
    translations = []
    for page in pages:
        if 'iwlinks' not in pages[page]:
            continue
        for iwlinks in pages[page]['iwlinks']:
            data = iwlinks['*']
            translations.append(data[data.rfind('/') + 1:])
    ret = ', '.join(translations)
    if len(ret) == 0:
        return ''
    translations_cache[word] = ret
    return ret


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


def main():
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
                # allow no answer to learn, strip sich (if present) and get translations
                print get_translations(verb[len('sich '):] if verb.startswith('sich ') else verb)
                print
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


if __name__ == '__main__':
    main()
