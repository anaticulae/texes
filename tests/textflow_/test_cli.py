# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import serializeraw
import utilotest

import tests
import tests.textflow_


def test_textflow_cli(mp):
    tests.textflow_.run('--help', mp=mp)


@utilotest.nightly
@utilotest.requires(hoverpower.DOCU027_PDF)
def test_textflow_alignments_docu027(td, mp):
    """Ensure that document with empty page is parsed correctly."""
    source = hoverpower.link(hoverpower.DOCU027_PDF)
    tests.textflow_.run(
        f'-i {source} -o {td.tmpdir}',
        mp=mp,
    )


@pytest.mark.parametrize('source', [
    pytest.param(hoverpower.MASTER072_PDF, id='master072'),
    pytest.param(hoverpower.DOCU009_PDF, id='docu009'),
])
@utilotest.nightly
def test_textflow_alignments(source, td, mp):
    """Ensure that document with empty page is parsed correctly."""
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    tests.textflow_.run(
        f'-i {source} -o {td.tmpdir}',
        mp=mp,
    )


@utilotest.longrun
@utilotest.requires(hoverpower.BACHELOR056_PDF)
def test_textflow_wordspace_bachelor56page4(td, mp):
    source = hoverpower.link(hoverpower.BACHELOR056_PDF)
    tests.textflow_.run(
        f'-i {source} --wordspace --pages=4',
        mp=mp,
    )
    loaded = serializeraw.load_wordspaces(td.tmpdir)
    dumped = serializeraw.dump_wordspaces(loaded)
    again = serializeraw.load_wordspaces(dumped)
    assert again == loaded
