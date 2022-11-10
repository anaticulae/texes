# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import texmex
import utila
import utilatest

import textflow.alignment.style


@pytest.mark.xfail(reason='softwareintegration')
@utilatest.longrun
@utilatest.requires(power.MASTER072_PDF)
def test_page_linealignments_expected_master72p4():
    source = power.link(power.MASTER072_PDF)
    pages = (4,)
    navigators = serializeraw.ptn_frompath(
        source,
        pages=pages,
    )
    page4 = navigators[0]
    current = textflow.alignment.style.page_linealignments_expected(page4)
    expected = [
        texmex.TextAlignment.BLOCK,
        texmex.TextAlignment.LEFT,
        texmex.TextAlignment.BLOCK,
        texmex.TextAlignment.RIGHT,
    ]
    assert current == expected, expected


@pytest.mark.xfail(reason='enable later')
@utilatest.longrun
@utilatest.requires(power.MASTER072_PDF)
def test_page_linealignments_expected_master72p6():
    source = power.link(power.MASTER072_PDF)
    pages = (6,)
    navigators = serializeraw.ptn_frompath(
        source,
        pages=pages,
    )
    page6 = navigators[0]
    current = textflow.alignment.style.page_linealignments_expected(page6)
    expected = [
        [
            texmex.TextAlignment.LEFT,
            texmex.TextAlignment.CENTER,
            texmex.TextAlignment.BLOCK,
        ],
        texmex.TextAlignment.BLOCK,
        [
            texmex.TextAlignment.CENTER,
            texmex.TextAlignment.BLOCK,
        ],
        texmex.TextAlignment.BLOCK,
        texmex.TextAlignment.BLOCK,
        texmex.TextAlignment.RIGHT,
    ]
    assert current == expected, expected


@pytest.mark.xfail(reason='softwareintegration')
@utilatest.requires(power.HOME043_PDF)
def test_page_linealignments_expected_homework40p3():
    source = power.link(power.HOME043_PDF)
    navigators = serializeraw.ptn_frompath(source)
    border = textflow.alignment.style.document_textfeed(navigators)
    # alignment
    current = textflow.alignment.style.page_linealignments_expected(
        utila.select_page(navigators, 3),
        border=border,
    )
    expected = [
        texmex.TextAlignment.CENTER,
        texmex.TextAlignment.LEFT,
        texmex.TextAlignment.LEFT,
        texmex.TextAlignment.LEFT,
        texmex.TextAlignment.LEFT,
        texmex.TextAlignment.BLOCK,
        texmex.TextAlignment.LEFT,
        texmex.TextAlignment.LEFT,
        texmex.TextAlignment.BLOCK,
    ]
    assert current[0:9] == expected, expected


@pytest.mark.xfail(reason='softwareintegration')
@utilatest.requires(power.HOME043_PDF)
def test_page_linealignments_expected_homework40p4():
    source = power.link(power.HOME043_PDF)
    navigators = serializeraw.ptn_frompath(source)
    border = textflow.alignment.style.document_textfeed(navigators)
    # alignment
    current = textflow.alignment.style.page_linealignments_expected(
        utila.select_page(navigators, page=4),
        border=border,
    )
    expected = [
        texmex.TextAlignment.CENTER,
        texmex.TextAlignment.LEFT,
        texmex.TextAlignment.LEFT,
        texmex.TextAlignment.LEFT,
        texmex.TextAlignment.LEFT,
        texmex.TextAlignment.LEFT,
    ]
    assert current[0:6] == expected, expected
