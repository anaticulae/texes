# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import docref.path
import docref.utils
import tests.docref_


@utilatest.requires(power.MASTER091B_PDF)
def test_docref_bibliography_master91b(testdir, monkeypatch):
    """Do not parse overlapping words.

    Do not detect overlapping words twice. Some pattern are part of
    other pattern.
    """
    bibliography = extract_label(
        power.MASTER091B_PDF,
        testdir,
        monkeypatch,
        pages='9',
    )
    assert len(bibliography) == 2


def extract_label(source, testdir, monkeypatch, pages=':'):
    source = power.link(source)
    tests.docref_.run(
        f'-i {source} --bibliography --pages={pages}',
        monkeypatch=monkeypatch,
    )
    bibliography = docref.path.docref_bibliography(testdir.tmpdir)
    bibliography = serializeraw.load_docref(bibliography)
    return bibliography
