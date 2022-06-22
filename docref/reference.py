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
import konrad
import utila

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
            verbose=True,
        )
        if not parsed:
            continue
        parsed, raws = parsed
        raws = [''.join(konrad.mark2str(item) for item in raw) for raw in raws]
        result.append(iamraw.DocRef(page, number, parsed, raw=raws))
    return result


def remove_invalid(items, text, validator: callable):
    lookup = docref.utils.sentence_lookup(text)
    result = []
    for item in items:
        sentence = lookup[item.page][item.sentence]
        # TODO: NOT REALY REQUIRED, SEE PARSE_TEXT()
        plain = docref.utils.sentence_plain(sentence, item.marked)
        for reference, mark in zip(plain, item.marked):
            if not validator(reference):
                utila.debug(f'docref:bib:invalid reference: {reference}')
                continue
            result.append(
                iamraw.DocRef(
                    item.page,
                    item.sentence,
                    [mark],
                    raw=[reference],
                ))
    return result
