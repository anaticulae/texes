# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import power
import pytest
import serializeraw
import utila
import utilatest

import docref
import docref.path
import tests
import tests.docref_

ARCHIVE = utila.join(
    docref.ROOT,
    'tests/docref_/biblio/expected',
    exist=True,
)


@utilatest.nightly
@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.BACHELOR075_PDF, ':', 'bachelor075', id='bachelor075'),
    pytest.param(power.BACHELOR076_PDF, ':', 'bachelor076', id='bachelor076'),
    pytest.param(power.DISS143_PDF, '15:30', 'diss143', id='diss143'),
    pytest.param(power.DISS172_PDF, '30:70', 'diss172', id='diss172'),
    pytest.param(power.MASTER072_PDF, ':', 'master072', id='master072'),
    pytest.param(power.MASTER075_PDF, ':', 'master075', id='master075'),
    pytest.param(power.MASTER083_PDF, ':', 'master083', id='master083'),
    pytest.param(power.MASTER098_PDF, ':', 'master098', id='master098'),
    pytest.param(power.MASTER116_PDF, ':', 'master116', id='master116'),
])
def test_bibref_validate(source, pages, expected, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    Evaluate(
        source=source,
        pages=pages,
        expected=expected,
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()
    # TODO: USE SECTIONS TO SELECT PAGES


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, expected, workdir, monkeypatch):
        super().__init__(
            program=functools.partial(
                tests.docref_.run,
                monkeypatch=monkeypatch,
            ),
            step='bibliography',
            pages=pages,
            source=power.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
            index=expected,
        )
        self.headlines = power.link(source)

    def frompath(self, path):  # pylint:disable=R0201
        path = docref.path.docref_bibliography(path)
        references = serializeraw.load_docref(path)
        return references

    def raw(self, value) -> str:
        collected = [
            f'{item.page} {item.sentence} {"   ".join(item.raw)}'
            for item in value
        ]
        result = utila.NEWLINE.join(collected)
        return result
