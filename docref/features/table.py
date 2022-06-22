# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import utila

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
    )
    validated = docref.reference.remove_invalid(
        parsed,
        sentences,
        validator=valid,
    )
    dumped = serializeraw.dump_docref(validated)
    return dumped


VALID = utila.compiles(r"""
    (
        Tabelle|
        Tab\.|
        Table
    )
""")


@utila.cacheme
def valid(item: str) -> bool:
    """\
    >>> valid('(siehe Kapitel 3.1)')
    False
    """
    if VALID.search(item):
        return True
    return False


PATTERN = utila.splitlines("""
(s. Tab. 1)
(siehe Tab. 5)
(siehe Tabelle 2.2)
siehe Tab. 5
siehe Tabelle 1-4
siehe Tabelle 2.2
Tabelle 3.1
folgende Tabelle 3.1
folgende Tabelle 5
nachfolgende Tabelle 3.1
nachfolgende Tabelle 5
folgende Tabelle
unten stehende Tabelle
stehende Tabelle
""")
