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

import configo
import serializeraw
import utilo

import docref.biblio.parser
import docref.features
import docref.reference


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
    parsed = docref.reference.remove_invalid(
        parsed,
        sentences,
        validator=valid,
    )
    result = select(parsed)
    dumped = serializeraw.dump_docref(result)
    return dumped


SIMPLE_COUNT_MIN = configo.HV_INT_PLUS(default=10)

SIMPLE_RATE_MIN = configo.HV_PERCENT_PLUS(default=50)


def select(parsed: list) -> list:
    """Do not select COLON_SIMPLE if only a few items are parsed.

    If there are too few, this colons are no references, there are often
    part of math or something else.
    """
    complexs, simple = utilo.partition(
        items=parsed,
        key=lambda x: not any(item for item in x.raw
                              if COLON_SIMPLE.match(item)),
    )
    if len(simple) < SIMPLE_COUNT_MIN:
        utilo.debug(f'too few: {len(simple)}, {len(parsed)} disable simple')
        return complexs
    rate = utilo.rate_rel(len(simple), len(parsed))
    if rate < SIMPLE_RATE_MIN:
        utilo.debug(f'rate: {rate} {len(simple)}, {len(parsed)} disable simple')
        return complexs
    return parsed


NUMBERED_REFERENCE = utilo.compiles(r"""
\[
    [ ]{0,2}
    \d{1,3}
    (
        [ ]{0,2}
        \,
        [ ]{0,2}
        \d{1,3}
    ){0,5}
    [ ]{0,2}
\]
""")

COLON_SIMPLE = utilo.compiles(r"""
\(
    [ ]{0,2}
    \d{1,3}
    [ ]{0,2}
    (
        [ ]{0,2}
        \,
        [ ]{0,2}
        \d{1,3}
        [ ]{0,2}
    ){0,5}
\)
""")


@utilo.cacheme
def valid(item: str):
    """\
    >>> valid('[ 28 ]')
    True
    >>> valid('[28, 76, 59]')
    True
    >>> valid('(Bradley & Lang, 1994)')
    True
    >>> valid('(Irwin et al., 1996)')
    True
    >>> valid('(Wimmer & Hartmann, 2014, S. 11-12)')
    True
    >>> valid('(10)')
    True
    """
    if docref.biblio.parser.parse(item):
        return True
    if NUMBERED_REFERENCE.match(item):
        return True
    if COLON_SIMPLE.match(item):
        return True
    return False


PATTERN = utilo.splitlines("""
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
(vgl. Darilek 2014)
(vgl. Darilek 2014b)
(vgl. Defrance; Pfeil 2014; vgl. Frank 2005)
(vgl. BOBEK und FESL 1978: S. 228)
(vgl. BOBEK und FESL 1978, S. 141)
(vgl. BOBEK u. FESL 1978: S. 227)
(vgl. HEINRITZ, KLEIN und POPP (2003), S. 29)
(vgl. BEHRENS 1965, S. 41ff)
(vgl. BEHRENS 1965, S. 138)
(vgl. BOUS (1933), S. 3 ff)
(vgl. BOUS (1933), S. 3)
(vgl. KAMENZ 2001{{hn:2:nh}}, S. 137ff)
(Schnabel, 2011)
(vgl. Statistisches Bundesamt, Verkehrsunfälle 2013)
(Vollrath & Krems, 2011)
(Wimmer & Hartmann, 2014, S. 11-12)
(Irwin et al., 1996)
(Krüger et al., 2005, S. 59)
(Zylman, 1972, zit. nach Krüger et al., 2005, Seite 59)
(Techniker, 2013, S. 8)
(Techniker Krankenkasse, 2013, S. 8)
[1]
[25]
[123]
[11, 22]
[11, 22, 33]
[11, 22, 33, 44]
[11, 22, 33, 44, 55]
(1)
(11, 22)
(11, 22, 33)
(11, 22, 33, 44)
(11, 22, 33, 44, 55)
""")
PATTERN |= {utilo.compiles(r'\{\{hn\:\d{1,4}\:nh\}\}')}
