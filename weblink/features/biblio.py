# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw
import utila

import weblink.features.sentence


def work(bibliography: str) -> str:
    if not utila.exists(bibliography):
        return '[]'
    loaded = load_bibliography(bibliography)
    processed = weblink.features.sentence.process_sentences(loaded)
    dumped = serializeraw.dump_hyperlinks(processed)
    return dumped


def load_bibliography(bibliography: str) -> iamraw.PageContentTexts:
    """Convert bib table in existing data structure to reuse code."""
    bibliography = serializeraw.load_bibliography_reference(bibliography)
    result = []
    for reference in bibliography.references:
        result.append(
            iamraw.PageContentText(
                content=[
                    iamraw.TextSection(
                        content=[reference.raw],
                        pages=[reference.raw_pdfpage],
                    )
                ],
                page=reference.raw_pdfpage,
            ))
    return result
