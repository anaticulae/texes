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
import texmex
import utila
import utilatest

import tests.textflow_
import textflow.features.alignment
import textflow.path


@utilatest.longrun
@utilatest.requires(power.MASTER072_PDF)
def test_textflow_alignment_expected(td, mp):
    source = power.link(power.MASTER072_PDF)
    tests.textflow_.run(
        f'-i {source} --pages=10:20 --alignment',
        mp=mp,
    )
    source = textflow.path.alignment(td.tmpdir)
    current = textflow.features.alignment.load_alignment(source)
    assert current
    assert len(current) == 10, str(current)


@pytest.mark.xfail(reason='unsupported block_end')
@utilatest.longrun
@utilatest.requires(power.MASTER098_PDF)
def test_alignment_master98_page2(td, mp):
    source = power.link(power.MASTER098_PDF)
    tests.textflow_.run(
        f'-i {source} --pages=2 --alignment',
        mp=mp,
    )
    source = textflow.path.alignment(td.tmpdir)
    current = textflow.features.alignment.load_alignment(source)
    content = utila.select_content(current, 2)
    assert content[4] == texmex.TextAlignment.BLOCK_END
