# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import utila

PAGES = r"""
    (S\.)?
    [ ]{0,2}
    (?P<pages>
        (
            (                                           # from x till y
                \d{1,4}[ ]{0,2}(a|b|c|d)
                [ ]{0,2}[-][ ]{0,2}
                \d{1,4}[ ]{0,2}(a|b|c|d)
            )|
            \d{1,4}[ ]{0,2}[-][ ]{0,2}\d{1,4}|          # from x till y
            \d{1,4}[ ]{0,2}(ff|f)[ ]{0,2}\.?|           # single page with following
            \d{1,4}                                     # single page
        )
    )
"""

YEAR = r"""
(
    \(?
        (?P<year>
            (
                20[012]\d|
                1[789]\d\d
            )
        )
    \)?
)
"""

AUTHOR = r"""
(
    (?P<author>
        (
            ebd\.|
            \b.{4,100}?
        )
    )
)
"""

PATTERN = utila.compiles(r"""
    (vgl[.][ ]{0,2})?
    (?P<author>
        (
            ebd\.|
            \b[\w\ /\.]+?
        )
    )
    [ ]{0,2}
    %(year)s?
    (
        # if year matches : and , is possible, if no year matches : is possible
        (?(year)[:,]|[:])           # optional collon between author and year
        [ ]{0,3}                    # space between collon and pages
        %(pages)s
    )
""" % dict(year=YEAR, pages=PAGES))

AUTHOR_AND_YEAR = utila.compiles(r"""
\(
    vgl\.
    [ ]{0,2}
    %(author)s
    [ ]{0,2}
    %(year)s
\)
""" % dict(author=AUTHOR, year=YEAR))

REFERENCE_LONG = utila.compiles(r"""
\(
    vgl\.
    [ ]{0,2}
    %(author)s
    [,:]
    [ ]{0,2}
    %(pages)s
\)
""" % dict(author=AUTHOR, pages=PAGES))

AUTHOR_COMMA_YEAR = utila.compiles(r"""
\(
    [ ]{0,2}
    %(author)s
    [ ]{0,2}
    [,]
    [ ]{0,2}
    %(year)s
    (
        [ ]{0,2}
        [,]?
        [ ]{0,2}
        %(pages)s
    ){0,1}
    [ ]{0,2}
\)
""" % dict(author=AUTHOR, year=YEAR, pages=PAGES))

HIGHNOTE = utila.compiles(r"""
    (?P<author>
        \{\{hn\:\d{1,4}\:nh\}\}
    )
""")

PATTERNS = (
    HIGHNOTE,
    PATTERN,
    AUTHOR_AND_YEAR,
    REFERENCE_LONG,
    AUTHOR_COMMA_YEAR,
)


def parse(raw: str) -> iamraw.BibliographyReferences:
    result = []
    for pattern in PATTERNS:
        parsed = parse_pattern(raw, pattern)
        raw = utila.ghost_replace(
            text=raw,
            pattern=[item.raw for item in parsed],
        )
        result.extend(parsed)
    return result


def parse_pattern(raw: str, pattern: str) -> iamraw.BibliographyReferences:
    matched = pattern.finditer(raw)
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
