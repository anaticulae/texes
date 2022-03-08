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


def load_bibliography(bibliography: str):
    # TODO: STRANGE DATA STRUCTURE AS A RESULT OF REUSING CODE
    bibliography = serializeraw.load_bibliography_reference(bibliography)
    result = []
    for item in bibliography:
        result.append(
            iamraw.PageContentText(
                content=[
                    iamraw.TextSection(
                        content=[item.raw],
                        pages=[item.raw_pdfpage],
                    )
                ],
                page=item.raw_pdfpage,
            ))
    return result
