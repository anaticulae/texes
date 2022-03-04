# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Bibliography Link
=================

This module enables to parse links to the bibliography sources out of text
flow.

See `footlink`.

Examples
--------

* [Pap15], [Wik07]
* (vgl. Havelock 1963: 166), (vgl. Ong 2012: 145).

Styles
------

Harvard
~~~~~~~

* (vgl. Havelock 1963: 166)
* (vgl. Havelock 1986: 77; Robinson/Hawpe 1986: 124)
* (ebd.: 18; vgl. hierzu auch Havelock 1963: 47)
* (vgl. Plat. Men.: 97a-98c)
* (vgl. ebd.: 6; Havelock 1982: 186; Murray/Wilson 2004: 1)
* (vgl. Dierse 1977: 2-6)
* (Meier 2007: 192)

Chicago
~~~~~~~

Like Harvard but located in the footer?

Technical
~~~~~~~~~

* [WAS19]

Numbers
~~~~~~~

* (144,13)

Location
--------

There are 2 location where bibliography links can be located. On the one
hand there can stand in the floating text to reference sentences or
pargraph. On the other hand footer can contain list of bibliography links

TODO: FOOTER
TODO: TECHNICAL
"""

import iamraw
import serializeraw
import utila

import docref.bibliography.parser
import docref.reference
import docref.utils


def work(sentences: str, headlines: str, pages: tuple = None) -> str:
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    sentences = serializeraw.load_text(
        sentences,
        headlines=headlines,
        pages=pages,
    )
    parsed = docref.reference.parse_text(
        sentences,
        pattern=PATTERN,
        compare_content=False,
    )
    parsed = remove_invalid(parsed, sentences)
    dumped = serializeraw.dump_docref(parsed)
    return dumped


def remove_invalid(items, text):
    lookup = docref.utils.sentence_lookup(text)
    result = []
    for item in items:
        sentence = lookup[item.page][item.sentence]
        # TODO: NOT REALY REQUIRED, SEE PARSE_TEXT()
        plain = docref.utils.sentence_plain(sentence, item.marked)
        for reference, mark in zip(plain, item.marked):
            if not valid(reference):
                utila.error(f'docref:bib:invalid reference: {reference}')
                continue
            result.append(
                iamraw.DocRef(
                    item.page,
                    item.sentence,
                    [mark],
                    raw=[reference],
                ))
    return result


NUMBERED_REFERENCE = r"""
\[
    [ ]{0,2}
    \d{1,3}
    (
        [ ]{0,2}
        \,
        [ ]{0,2}
        \d{1,3}
    )+
    [ ]{0,2}
\]
"""


def valid(item: str):
    """\
    >>> valid('[ 28 ]')
    True
    >>> valid('[28, 76, 59]')
    True
    """
    if docref.bibliography.parser.parse(item):
        return True
    if utila.match(NUMBERED_REFERENCE, item):
        return True
    return False


PATTERN = utila.splitlines("""
[Hof11, S. 309-311]
[Hof11, S. 314f]
[Mag13]
[RNB12, S. 62ff]
(Fornoff 2016: 53; Erll 2017: 11-12)
(Górny et al. 2012: 14)
(Hahn; Traba 2015: 17)
(Koreik 2010: 1478)
(Robbe 2009: 51-52)
([AM11], S. 239 f.)
([Ag12a])
([Bo06], S. 133 ff.)
([WIZ12])
([We05], S. 48)
(ebd.: 21; Fornoff 2016: 45-48)
(ebd.: 51)
(ebd.: 51-60)
(ebd: 51-60)
(vgl. Darilek 2014),
(vgl. Darilek 2014b),
(vgl. Defrance; Pfeil 2014; vgl. Frank 2005)
[1]
[25]
[123]
[11, 22]
[11, 22, 33]
""")
