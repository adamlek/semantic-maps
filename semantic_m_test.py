#!/usr/bin/env python3
from itertools import *
from toolz import *
from pprint import pprint
from collections import namedtuple, defaultdict
from operator import *

Entry = namedtuple('Entry', ['index', 'sentence'])

# func, args, kwargs -> func
def partial(func, *args, **kwargs):
    def newf(*fargs, **fkwargs):
        newkw = kwargs.copy()
        newkw.update(fkwargs)
        return func(*args, *fargs, **fkwargs)
    newf.args = args
    newf.kwargs = kwargs
    return newf

# path -> list
def read_file(pth, fnct):
    with open(pth) as f:
        return fnct(filter(lambda x: first(x)>7,
                    enumerate(f.read().lower().split('\n'))))

# list -> iter
def clean_lines(lst):
    for line in lst:
        yield Entry(list(islice(second(line).split(), None, 1))[0],
                    list(filter(lambda w: w.isalpha(),
                                    islice(second(line).split(), 1, None))))

# int, list[list] -> iter
def get_ngrams(size, text):
    return sliding_window(size, text)

# given word pairs from two languages, (w1,w2), find the number of sentences in which they co-occur
def get_correlation_pairs(sent_mapping, correlation_pairs):
    pos_pairs = []
    neg_pairs = []
    for en_sent, fr_sent in sent_mapping:
        for en_w, fr_w in correlation_pairs:
            if en_w in en_sent.sentence:
                if fr_w in fr_sent.sentence:
                    pos_pairs.append((en_sent, fr_sent))
                else:
                    neg_pairs.append((en_sent, fr_sent))
    return pos_pairs, neg_pairs

# from a word w, get all target sentences in which any of the target words appear
def get_targetwords(mapping, source_word, target_words):
    corr_dict = defaultdict(int)
    o = list(filter(lambda x: source_word in x[0].sentence, mapping))

    for en_s, fr_s in o:
        for w in target_words:
            if w in fr_s.sentence:
                corr_dict[w] += 1
    return corr_dict

# main controller
def main():
    paths = ['./eng-x-bible-kingjames.txt',
            './fra-x-bible-kingjames.txt']

    correlation_pairs = [('go', 'aller'), ('come', 'venir')]
    s_word = 'enter'
    t_words = ['aller', 'venir', 'de', 'entrer']

    texts = list(map(lambda p: read_file(p, clean_lines), paths))

    en, fr = list(texts[0]), list(texts[1])

    mapping = []
    for i, entry in enumerate(en):
        for entry2 in fr[i:]:
            if entry.index == entry2.index:
                print(entry, entry2)
                mapping.append((entry, entry2))

    pos_pairs, neg_pairs = get_correlation_pairs(mapping,
                                                 correlation_pairs)
    target_words = get_targetwords(mapping,
                        s_word,
                        t_words)
    pprint(target_words)

if __name__ == '__main__':
    main()
    
