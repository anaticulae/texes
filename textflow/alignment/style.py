# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Line Style
==========

Feed
----

* left
* right

Style
-----

* left
* right
* block
* center
* block-center
"""

import configo
import texmex
import utilo

BLOCK_TEXT_DIFF = configo.HV_FLOAT_PLUS(default=10.0)


def document_alignment(navigators: texmex.PTNs) -> texmex.TextAlignment:
    result = []
    left, right = document_textfeed(navigators)
    for page in navigators:
        # left, right = page.content.left, page.content.right
        style = page_linealignments(page, left, right)
        result.extend(style)
    return utilo.modes(result)


def document_textfeed(navigators):
    left = texmex.document_textfeed(navigators)
    right = texmex.document_textfeed(navigators, left=False)
    return left, right


TEXT_BORDER_NOISE = configo.HV_FLOAT_PLUS(default=15.0)
# A center block must have a minimal width to exclude page numbers or very
# short centered text as beeing a center text block.
BLOCK_CENTER_WIDTH_MIN = configo.HV_FLOAT_PLUS(default=300.0)

BLOCK_EUQAL_BORDER_DIFF_MAX = configo.HV_FLOAT_PLUS(default=5.0)

PAGE_LINEALIGNMENTS_DIFF_MAX = configo.HV_FLOAT_PLUS(default=3.0)


def page_linealignments(
    navigator,
    left_alignment,
    right_alignment,
) -> texmex.TextAlignments:
    result = []
    border_left, border_right = leftright(
        navigator,
        left_alignment,
        right_alignment,
    )
    for left, right in zip(border_left, border_right):
        width = navigator.width - left - right
        if utilo.near(right, 0.0, diff=PAGE_LINEALIGNMENTS_DIFF_MAX):
            if left > 100:
                result.append(texmex.TextAlignment.RIGHT)
            elif left <= 50:
                result.append(texmex.TextAlignment.BLOCK)
            continue
        if right >= 20:
            if left >= 20:
                if utilo.near(right, left, BLOCK_EUQAL_BORDER_DIFF_MAX)\
                   and width >= BLOCK_CENTER_WIDTH_MIN:
                    # left and right textfeed is equal
                    result.append(texmex.TextAlignment.BLOCK_CENTER)
                else:
                    result.append(texmex.TextAlignment.CENTER)
            else:
                result.append(texmex.TextAlignment.LEFT)
            continue
        if left <= 50:
            result.append(texmex.TextAlignment.LEFT)
        else:
            # ?
            result.append(texmex.TextAlignment.BLOCK)
    return result


def document_linealignments_expected(navigators):
    border = document_textfeed(navigators)
    result = [(
        navigator.page,
        page_linealignments_expected(navigator, border=border),
    ) for navigator in navigators]
    return result


def page_linealignments_expected(navigator, border=None):
    if border is None:
        border = document_textfeed([navigator])
    grouped = texmex.group_linedistances_complex(navigator)
    content = groupby(navigator, grouped)
    result = []
    for group in content:
        # TODO: MOVE TO SEPARATE METHOD
        nav = texmex.PTN(pagesize=(
            navigator.width,
            navigator.height,
        ))
        nav.data = group
        alignments = page_linealignments(nav, *border)
        if not alignments:
            continue
        alignment = utilo.modes(alignments)
        result.append(alignment)
    return result


def groupby(navigator, grouped):
    result = [[navigator[item] for item in group] for group in grouped]
    return result


def leftright(navigator, left, right):
    left = feed_left(navigator, left)
    left = [utilo.threshold(item, diff=TEXT_BORDER_NOISE) for item in left]
    right = feed_right(navigator, right)
    right = [utilo.threshold(item, diff=TEXT_BORDER_NOISE) for item in right]
    return left, right


def feed_left(navigator, left):
    diff = [item.bounding[0] - left for item in navigator]
    diff = utilo.roundme(diff, convert=False)
    return diff


def feed_right(navigator: texmex.PTN, right: float) -> list:
    """Determine distance to right pagefeed(distance to right paper border).

    Args:
        navigator(PTN): content of one page
        right(float): distance to the right paper side
    Returns:
        List of distances to paper page feed for every line.
    """
    # absolute coordinate measured from left paper as origin
    expected = navigator.width - right
    diff = [expected - item.bounding[2] for item in navigator]
    diff = utilo.roundme(diff, convert=False)
    return diff
