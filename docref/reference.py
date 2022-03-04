# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german
import iamraw

import docref.utils


def parse_text(
    text,
    pattern: set,
    compare_content: bool = True,
) -> iamraw.DocRefs:
    result = []
    for page, number, sentence in docref.utils.sentences(text, numbers=True):
        parsed = german.searches(
            pattern,
            sentence,
            compare_content=compare_content,
            overlapping_remove=True,
        )
        if not parsed:
            continue
        result.append(iamraw.DocRef(page, number, parsed))
    return result
