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
import utilatest

import tests.weblink_
import weblink


@pytest.mark.xfail(reason='softwareintegration')
def test_links_master75pages15(td, mp):
    loaded = hyperlinks(power.MASTER075_PDF, td, mp, 15)
    assert len(loaded) == 1
    hyperlink = loaded[0].href
    assert hyperlink.startswith('https')
    assert hyperlink.endswith('index.html')
    assert loaded[0].visited


def hyperlinks(source, td, mp, pages=':'):
    utilatest.fixture_requires(source)
    cmd = f'-i {power.link(source)} --sentence --pages={pages}'
    tests.weblink_.run(cmd, mp=mp)
    linkpath = weblink.path.weblink_sentence(td.tmpdir)
    loaded = serializeraw.load_hyperlinks(linkpath)
    return loaded
