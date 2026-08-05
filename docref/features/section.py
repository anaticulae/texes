# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import utilo

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


VALID = utilo.compiles(r"""
    (
        Abschnitt|
        Anhang|
        Bereich|
        Chapter|
        Kapitel|
        Kap\.|
        Link|
        Paragraph|
        Part|
        Point|
        Punkt|
        Section|
        Weblink
    )
""")


@utilo.cacheme
def valid(item: str) -> bool:
    """\
    >>> valid('Industrie 4.0')
    False
    """
    if VALID.search(item):
        return True
    return False


PATTERN = utilo.splitlines("""
(siehe Abs. 5)
(siehe Abschnitt 7.1.1)
(siehe Abschnitt A.1.1)
(siehe Kapitel 2.2)
(siehe Kapitel A.2)
(siehe Kap. 2)
(Abschnitte 1.4 bis 1.7)
(Abschnitte 1 bis 5)
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
(vgl. Kap. 1.2)
Im nachfolgenden Abschnitt
Im nachfolgenden Kapitel
""")
