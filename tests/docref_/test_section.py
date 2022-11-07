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

import docref.path
import tests.docref_


@pytest.mark.xfail(reason='softwareintegration')
@utilatest.requires(power.MASTER075_PDF)
def test_section_master75page25_50(td, mp):
    source = power.link(power.MASTER075_PDF)
    cmd = f'-i {source} --section --pages=25:50'
    tests.docref_.run(cmd, mp=mp)

    path = docref.path.docref_section(td.tmpdir)
    loaded = serializeraw.load_docref(path)
    assert len(loaded) in {8, 9, 10, 12, 13}  # TODO: VALIDATE LATER
