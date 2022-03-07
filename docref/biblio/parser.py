# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

import docref.biblio.strategies.intext
import docref.biblio.strategies.tech


def parse(page: str) -> iamraw.BibliographyReferences:
    """\
    >>> parse('[10]')
    [BibliographyReference(...reference='10'...raw='[10]'...)]
    """
    parsed = docref.biblio.strategies.tech.parse(page)
    if parsed:
        return parsed
    parsed = docref.biblio.strategies.intext.parse(page)
    if parsed:
        return parsed
    return None
