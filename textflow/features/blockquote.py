# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""BlockQuotes

.. todo:: think about block quotes without quotation marks

"""

import configo
import german
import iamraw
import serializeraw
import texmex
import utila

BLOCK_QUOTE_DIST_MIN = configo.HV_FLOAT_PLUS(default=5.0)

BLOCK_QUOTE_LINE_LENGTH_MAX = configo.HV_FLOAT_PLUS(default=15)


def work(
    text: str,
    textpositions: str,
    sizeandborder: str,
    headerfooter: str,
    pages: tuple,
) -> str:
    ptcns = serializeraw.ptcn_fromfile(
        text,
        textpositions,
        sizeandborder,
        headerfooter,
        pages=pages,
    )
    textsize = texmex.document_textsize(ptcns)

    result = [analyze_page(page, textsize=textsize) for page in ptcns]

    # remove empty pages
    result = [item for item in result if item.content]
    dumped = serializeraw.dump_blockquotes(result)
    return dumped


def analyze_page(
    ptcn: texmex.PageTextContentNavigator,
    textsize: float,
) -> iamraw.PageContentBlockQuotes:
    grouped = texmex.group_linedistances_complex(ptcn)

    bounds = texmex.textbounds(ptcn, contentborder=ptcn.content)
    boundsgroups = group_todata(grouped, bounds)
    datagroups = group_todata(grouped, ptcn)

    result = []
    for index, (group, bounds) in enumerate(zip(datagroups, boundsgroups)):
        if not any((
                iscitation_group(bounds),
                iscitation_group_intention(bounds),
                iscitation_group_right_bounded(group, bounds, textsize),
        )):
            continue
        if len(group) > BLOCK_QUOTE_LINE_LENGTH_MAX:
            # TODO: ADD WARNING ABOUT VERY LONG CITATION, DO WE REQUIRE A
            # BETTER STRATEGY?
            continue
        result.append((grouped[index], [item.text.strip() for item in group]))
    return iamraw.PageContentBlockQuotes(page=ptcn.page, content=result)


def group_todata(index, navigator):
    if not index:
        return []
    result = []
    for group in index:
        collected = [navigator[index] for index in group]
        result.append(collected)
    return result


RIGHT_MAX = configo.HV_FLOAT_PLUS(default=3.0)

LEFT_MAX = configo.HV_FLOAT_PLUS(default=20.0)


def iscitation_group_right_bounded(group, bounds, textsize) -> bool:
    if len(bounds) < 3:
        # bock quote must have at least 3 lines
        return False
    left, right = group_distance(bounds)
    blocksize = texmex.textsize_frompage(group)
    if blocksize >= textsize:
        return False
    if right > RIGHT_MAX:
        return False
    if left <= LEFT_MAX:
        # left feeded text
        return False
    left = utila.groupby_diff(
        [item.bounds.leftdist for item in bounds],
        maxdiff=1.5,
    )
    if len(left) > 1:
        # more than one different text feed on the left side
        return False
    return True


def iscitation_group_intention(bounds) -> bool:
    """Check that group is indentend and contains some quotation
    marks."""
    left, right = group_distance(bounds)
    if left < BLOCK_QUOTE_DIST_MIN:
        return False
    if right < BLOCK_QUOTE_DIST_MIN:
        return False
    lines = [
        german.word_tokenize(item.text, validate_sentences=False)
        for item in bounds
    ]
    marks = [word for word in lines if german.contain_quotation_marks(word)]
    marks = utila.flatten(marks)
    # TODO: COUNT QUOTATION SIGNS?
    contains_quotation = any(marks)
    return contains_quotation


def iscitation_group(bounds) -> bool:
    """Group starts and ends with quotation mark."""
    text = ' '.join([item.text.strip() for item in bounds])
    marks = german.word_tokenize(text, validate_sentences=False)
    if len(marks) < 2:
        return False
    if not german.contain_quotation_marks([marks[0]]):
        return False
    # 0:3 add some tolerance to ignore, dots or highnotes
    if not german.contain_quotation_marks(marks[-3:]):
        return False
    return True


def group_distance(group):
    if not group:
        return None
    left = [item.bounds.leftdist for item in group]
    right = [item.bounds.rightdist for item in group]
    left = utila.roundme(left, digits=0, convert=False)
    right = utila.roundme(right, digits=0, convert=False)
    left, right = utila.mode(left), utila.mode(right)
    return left, right
