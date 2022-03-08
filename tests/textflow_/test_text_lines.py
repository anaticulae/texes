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
import utilatest

import textflow.alignment.style

TextAlignment = texmex.TextAlignment


@pytest.mark.parametrize('source, expected', [
    pytest.param(power.MASTER072_PDF, TextAlignment.BLOCK, id='master72'),
    pytest.param(power.BACHELOR037_PDF, TextAlignment.BLOCK, id='bachelor37'),
    pytest.param(power.DOCU007_PDF, TextAlignment.BLOCK, id='docu009'),
    pytest.param(power.HOME040_PDF, TextAlignment.LEFT, id='home040'),
])
@utilatest.nightly
def test_document_alignment(source, expected):
    source = power.link(source)
    utilatest.fixture_requires(source)
    content_navigators = serializeraw.ptn_frompath(
        source,
        prefix='oneline',
    )
    alignment = textflow.alignment.style.document_alignment(content_navigators)
    assert alignment == expected, alignment


@utilatest.requires(power.HOME040_PDF)
def test_page_linealignment_homework40p4():
    navigators = serializeraw.ptn_frompath(
        power.link(power.HOME040_PDF),
        prefix='oneline',
    )
    left, right = textflow.alignment.style.document_textfeed(navigators)
    page4 = navigators[4]
    linealignments = textflow.alignment.style.page_linealignments(
        page4,
        left,
        right,
    )
    assert linealignments[0] == TextAlignment.CENTER
    assert linealignments[1] == TextAlignment.LEFT
    assert linealignments[-1] == TextAlignment.RIGHT


@utilatest.longrun
@utilatest.requires(power.MASTER072_PDF)
def test_page_linealignment_master72p4():
    navigators = serializeraw.ptn_frompath(
        power.link(power.MASTER072_PDF),
        prefix='oneline',
    )
    left, right = textflow.alignment.style.document_textfeed(navigators)
    page4 = navigators[4]
    linealignments = textflow.alignment.style.page_linealignments(
        page4,
        left,
        right,
    )
    assert linealignments[0] == TextAlignment.BLOCK
    assert linealignments[2] == TextAlignment.LEFT
    assert linealignments[3] == TextAlignment.LEFT
    assert linealignments[4] == TextAlignment.BLOCK
    assert linealignments[-1] == TextAlignment.RIGHT


@utilatest.longrun
@utilatest.requires(power.MASTER072_PDF)
def test_page_linealignment_master72p15():
    navigators = serializeraw.ptn_frompath(
        power.link(power.MASTER072_PDF),
        prefix='oneline',
    )
    left, right = textflow.alignment.style.document_textfeed(navigators)
    page15 = navigators[15]
    linealignments = textflow.alignment.style.page_linealignments(
        page15,
        left,
        right,
    )
    # CENTER marks the end of BLOCK_CENTER
    # LEFT marks the end of BLOCK
    assert linealignments[0] == TextAlignment.BLOCK_CENTER
    assert linealignments[1] == TextAlignment.BLOCK_CENTER
    assert linealignments[2] == TextAlignment.BLOCK_CENTER
    assert linealignments[3] == TextAlignment.CENTER

    assert linealignments[7] == TextAlignment.BLOCK_CENTER
    assert linealignments[8] == TextAlignment.BLOCK_CENTER
    assert linealignments[9] == TextAlignment.CENTER
