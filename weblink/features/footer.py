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


def work(footers: str, pages: tuple = None) -> str:
    if not utila.exists(footers):
        return '[]'
    loadeded = load_footnotes(
        footers,
        pages=pages,
    )
    processed = weblink.features.sentence.process_sentences(loadeded)
    dumped = serializeraw.dump_hyperlinks(processed)
    return dumped


def load_footnotes(
    footers: str,
    pages: tuple = None,
) -> iamraw.PageContentTexts:
    footers = serializeraw.load_footnotes(
        footers,
        pages=pages,
    )
    result = []
    for page in footers:
        collected = [item.text for item in page.content]
        result.append(
            iamraw.PageContentText(
                content=[
                    iamraw.TextSection(
                        content=collected,
                        pages=[page.page] * len(collected),
                    )
                ],
                page=page.page,
            ))
    return result
