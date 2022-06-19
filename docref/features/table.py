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

import docref.features.bibliography
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
    validated = docref.features.bibliography.remove_invalid(
        parsed,
        sentences,
        validator=valid,
    )
    dumped = serializeraw.dump_docref(validated)
    return dumped


@utila.cacheme
def valid(item: str) -> bool:
    """\
    >>> valid('(sieheKapitel3.1)')
    False
    """
    item = item.lower()
    if 'kapitel' in item:
        return False
    if 'punkt' in item:
        return False
    return True


PATTERN = utila.splitlines("""
(s. Tab. 1)
(siehe Tab. 5)
(siehe Tabelle 2.2)
siehe Tab. 5
siehe Tabelle 2.2
""")
