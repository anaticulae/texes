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
import tests.conftest
import tests.docref_

ARCHIVE = utila.join(
    docref.ROOT,
    'tests/docref_/table/expected',
    exist=True,
)

RESOURCES = [
    pytest.param(
        power.pdf(source),
        power.ctext(power.pdf(source), default=':'),
        id=utila.file_name(power.pdf(source)),
    ) for source in tests.conftest.RESOURCES
]


@utilatest.nightly
@pytest.mark.parametrize('source, pages', RESOURCES)
def test_validate_tableref(source, pages, td, mp):
    utilatest.fixture_requires(source)
    Evaluate(
        source=source,
        pages=pages,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, workdir, mp):
        super().__init__(
            program=functools.partial(
                tests.docref_.run,
                mp=mp,
            ),
            step='table',
            pages=pages,
            source=power.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
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
