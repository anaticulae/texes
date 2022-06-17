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

RESOURCES = [
    (power.BACHELOR075_PDF, '14:70'),
    (power.BACHELOR076_PDF, ':'),
    (power.DISS143_PDF, '15:30'),
    (power.DISS172_PDF, '30:70'),
    (power.MASTER072_PDF, ':'),
    (power.MASTER075_PDF, ':'),
    (power.MASTER083_PDF, ':'),
    (power.MASTER098_PDF, ':'),
    (power.MASTER116_PDF, ':'),
]
RESOURCES = [
    pytest.param(source, page, id=utila.file_name(source))
    for source, page in RESOURCES
]


@utilatest.nightly
@pytest.mark.parametrize('source, pages', RESOURCES)
def test_bibref_validate(source, pages, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    Evaluate(
        source=source,
        pages=pages,
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()
    # TODO: USE SECTIONS TO SELECT PAGES


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, workdir, monkeypatch):
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
