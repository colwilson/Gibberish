#!/usr/bin/env python
import string
import re
from collections import defaultdict, Counter
from random import choice, randrange, randint
import textwrap

class Gibberish(object):

    def __init__(self, text, n=4):
        # n controls the length of the tuples
        self.n = n
        self.markov = defaultdict(Counter)

        text = " ".join(textwrap.wrap(text))
        word_list  = text.split()
        text = " ".join(word_list)

        capitalized = {}
        for ix, word in enumerate(word_list):
            # remove quotes, commas, periods ...
            word = word.replace('"', '')
            word = word.replace(',', '')
            word = word.replace('.', '')
            if ix > 0 and word[0].isupper():# and word_list[ix-1][-1:] != '.':
                capitalized[word] = True
        self.capitalized = [ k + " " for k in capitalized.keys() if len(k) >= n ]

        def sliced(listin,n):
            # non-overlapping slices, n elements at a time from listin,returned thru an iterator
            i=0
            len_listin=len(listin)
            while (i<len_listin ):
                yield "".join(listin[i:min(len_listin,i+n)])
                i+=n

        def pairwise(iterable):
            it = iter(iterable)
            last = next(it)
            for curr in it:
                yield last, curr
                last = curr

        for p, q in pairwise(sliced(text, n)):
            self.markov[p][q] += 1

    def generate(self, n):
        curr = choice(list(self.capitalized))
        yield curr[:len(curr)-self.n] # start of a random capitalized word from the text
        curr = curr[-self.n:]

        for i in xrange(n):
            yield curr
            if curr not in self.markov:   # handle case where there is no known successor
                curr = choice(list(self.markov))
            d = self.markov[curr]
            target = randrange(sum(d.values()))
            cumulative = 0
            for curr, cnt in d.items():
                cumulative += cnt
                if cumulative > target:
                    break

    def generate_sentence(self):
        text = self.generate(200)
        text = "".join(text)
        text += "."
        text = text.split(".")[0]
        text += "."
        text = text.replace('  ', '')
        return text

    def generate_paragraph(self):
        sentences = []
        for s in range(1, randint(1, 12)):
            sentences.append(self.generate_sentence())
        return " ".join(sentences)
