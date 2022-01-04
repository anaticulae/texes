# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import iamraw
import utila

PATTERN = r"""
    (vgl[.][ ])?
    (?P<author>
        (
            ebd[.]|
            \b[\w /\.]+?
        )
    )
    [ ]?
    (?P<year>\d{4})?
    (
        [:]                         # optional collon between author and year
        [ ]{0,3}                    # space between collon and pages
        (?P<pages>
            (
                \d+(a|b|c|d)[-]\d+(a|b|c|d)| # from x till y
                \d+[-]\d+|                   # from x till y
                \d+ff[.]|                    # single page with following
                \d+                          # single page
            )
        )
    )
"""

AUTHOR_AND_YEAR = r"""
    \(
        (vgl[.][ ])
        (?P<author>\b[\w/]+?)
        [ ]
        (?P<year>\d{4})
    \)
"""

REFERENCE_LONG = r"""
\(
    vgl\.
    [ ]
    (?P<author>.{8,100})
    ,
    [ ]
    (?P<pages>
        (S\.)?
        [ ]
        (
            \d+|                # single page
            \d+[ ]?ff\.?|       # single page with following
            \d+\-\d+            # from x till y
        )
    )
\)
"""


def parse(raw: str) -> iamraw.BibliographyReferences:
    result = []
    for pattern in [PATTERN, AUTHOR_AND_YEAR, REFERENCE_LONG]:
        parsed = parse_pattern(raw, pattern)
        result.extend(parsed)
    return result


def parse_pattern(raw: str, pattern: str) -> iamraw.BibliographyReferences:
    matched = re.finditer(pattern, raw, re.VERBOSE)
    if not matched:
        return []
    result = []
    for item in matched:
        raw = utila.extract_match(item)
        author = item['author']
        try:
            year = int(item['year'])
        except (IndexError, TypeError):
            year = None
        try:
            pages = item['pages']
        except IndexError:
            pages = None
        link = iamraw.BibliographyReference(
            authors=[author],
            year=year,
            page=pages,
            raw=raw,
        )
        result.append(link)
    return result
