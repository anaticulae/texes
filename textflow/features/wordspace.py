# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import utilo

import textflow.wordspace


def work(
    text: str,
    textpositions: str,
    sizeandborder: str,
    headerfooter: str,
    magic: str,
    wordspaces: str,
    pages: tuple,
) -> str:
    if not utilo.exists(wordspaces):
        utilo.error(f'wordspace does not exists: {wordspaces} skip --wordspace')
        return NO_WORDSPACE
    ptcns = serializeraw.ptcn_fromfile(
        text,
        textpositions,
        sizeandborder,
        headerfooter,
        pages=pages,
    )
    magic = serializeraw.load_types(
        magic,
        pages=pages,
    )
    wordspaces = serializeraw.load_wspaces(wordspaces, pages=pages)
    result = textflow.wordspace.extract(ptcns, magic, wordspaces)
    dumped = serializeraw.dump_wordspaces(result)
    return dumped


NO_WORDSPACE = serializeraw.dump_wordspaces([])
