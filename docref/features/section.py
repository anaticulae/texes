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


VALID = utila.compiles(r"""
    (
        Abschnitt|
        Anhang|
        Bereich|
        Chapter|
        Kapitel|
        Link|
        Paragraph|
        Part|
        Point|
        Punkt|
        Section|
        Weblink
    )
""")


@utila.cacheme
def valid(item: str) -> bool:
    """\
    >>> valid('Industrie 4.0')
    False
    """
    if VALID.search(item):
        return True
    return False


PATTERN = utila.splitlines("""
(siehe Abs. 5)
(siehe Abschnitt 7.1.1)
(siehe Kapitel 2.2)
Abs. 5
Abschnitt 1
Abschnitt 1.
Kapitel 2.
Punkt 4.1.4
siehe Abs. 5
siehe Abschnitt 7.1.1
siehe Kapitel 2.
siehe Punkt 4.2.2.
siehe Punkt 4.7
siehe auch Punkt 4.3.2.
in section 3.1.2
in section 2
in section 1.1
""")
