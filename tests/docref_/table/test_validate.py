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
import tests.docref_

ARCHIVE = utila.join(
    docref.ROOT,
    'tests/docref_/table/expected',
    exist=True,
)


@utilatest.nightly
@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.BACHELOR037_PDF, ':', 'bachelor037', id='bachelor037'),
])
def test_tableref_validate(source, pages, expected, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    Evaluate(
        source=source,
        pages=pages,
        expected=expected,
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, expected, workdir, monkeypatch):
        super().__init__(
            program=functools.partial(
                tests.docref_.run,
                monkeypatch=monkeypatch,
            ),
            step='table',
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
        path = docref.path.docref_table(path)
        references = serializeraw.load_docref(path)
        return references

    def raw(self, value) -> str:
        collected = [
            f'{item.page} {item.sentence} {"   ".join(item.raw)}'
            for item in value
        ]
        result = utila.NEWLINE.join(collected)
        return result
