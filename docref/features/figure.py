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
        Abb\.|
        Abbildung|
        Figure|
        Fig\.|
        Image|
        Img\.
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
(Abb. 100 und 101)
(s. Abb. 3a)
(s. Abb. 3)
(siehe Abb. 100 und 101)
(siehe Abb. 100)
(siehe Abbildung 2.12)
(siehe Abbildung 100)
s. Abb. 8a und 8b
s. Abb. 8 und 8a
s. Abb. 8a und 8
s. Abb. 3b
s. Abb. 3
siehe Abbildung 2.12.3
siehe Abbildung 2.12
siehe Abbildung 10
Abb. 100 und 1001
Abb. 100 und Abb. 101
Abbildung 2.1
Abbildungen 100 und 1001
Abb. 3
in Abb. 3
nachfolgenden Abbildung
folgenden Abbildung
folgende Abbildung
""")
