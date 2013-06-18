# encoding: utf-8

"""
This is a module docstring
"""

__author__ = "Marcin Nowak"
__copyright__ = "Copyright 2013"
__license__ = "Propertiary"
__maintainer__ = "Marcin Nowak"
__email__ = "marcin.j.nowak@gmail.com"


import decimal
import math


def value_as_words(value):
    value = decimal.Decimal(str(value))

    floor = int(math.floor(value))
    fraction = int((value-decimal.Decimal(floor))*100)

    txts = [
        u'jeden dwa trzy cztery pięć sześć siedem osiem dziewięć',
        u'dziesięć dwadzieścia trzydzieści czterdzieści pięćdziesiąt '\
            u'sześćdziesiąt siedemdziesiąt osiemdziesiąt dziewięćdziesiąt',
        u'sto dwieście trzysta czterysta pięćset sześćset siedemset osiemset '\
            u'dziewięćset',
    ]

    nascie = u'dziesięć jedenaście dwanaście trzynaście czternaście piętnaście '\
            u'szesnaście siedemnaście osiemnaście dziewiętnaście'.split(' ')

    words = map(lambda x: [' ']+x.split(' '), txts)
    ranks = [('','',''),
             (u' tysiąc', u' tysiące', u' tysięcy'),
             (u' milion', u' miliony', u' milionów'),
             (u' miliard', u' miliardy', u' miliardów'),
             (u' bilion', u' biliony', u' bilionów'),
             (u' biliard', u' biliardy', u' biliardów'),
         ]

    out_list = []

    step = 0
    while floor:
        idx = step % 3
        value, wordidx = divmod(floor, 10)
        if idx==0 and value % 10 == 1:
            word = nascie[wordidx]
            value, newwordidx = divmod(value, 10)
            step+=1
            rankidx = 2
        else:
            word = words[idx][wordidx]
            rankidx = 0 if wordidx < 2 else 1 if wordidx<5 else 2
        out_list.append(u'%s%s' % (word, ranks[step/3][rankidx] if idx==0 else ''))
        step+=1
        floor = value

    output = ' '.join(filter(lambda x: x.strip(),reversed(out_list)))

    if fraction:
        return u'%s %s/100' % (output, fraction)

    return output

