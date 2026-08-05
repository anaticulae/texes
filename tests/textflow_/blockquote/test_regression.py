# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import serializeraw
import utilotest

import tests.textflow_
import textflow.path


def test_noblockquote_bachelor51page21(td, mp):
    detected = run_blockquote(
        hoverpower.BACHELOR051_PDF,
        td,
        mp,
        pages='21',
    )
    assert not detected


def run_blockquote(source, td, mp, pages=':'):
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    tests.textflow_.run(
        f'-i {source} --blockquote --pages={pages}',
        mp=mp,
    )
    path = textflow.path.blockquote(td.tmpdir)
    loaded = serializeraw.load_blockquotes(path)
    return loaded
