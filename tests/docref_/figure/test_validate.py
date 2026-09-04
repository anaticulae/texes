# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import hoverpower
import pytest
import serializeraw
import utilo
import utilotest

import docref
import docref.path
import tests.conftest
import tests.docref_

ARCHIVE = utilo.join(
    docref.ROOT,
    'tests/docref_/figure/expected',
    exist=True,
)

RESOURCES = [
    pytest.param(
        hoverpower.pdf(source),
        hoverpower.ctext(hoverpower.pdf(source), default=':'),
        id=utilo.file_name(hoverpower.pdf(source)),
    ) for source in tests.conftest.RESOURCES
]


@utilotest.nightly
@pytest.mark.parametrize('source, pages', RESOURCES)
def test_validate_figureref(source, pages, td, mp):
    utilotest.fixture_requires(source)
    # TODO: ENABLE LATER
    return
    # pylint:disable=W0101
    Evaluate(
        source=source,
        pages=pages,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


class Evaluate(utilotest.BaseLiner):

    def __init__(self, source, pages, workdir, mp):
        super().__init__(
            program=functools.partial(
                tests.docref_.run,
                mp=mp,
            ),
            step='figure',
            pages=pages,
            source=hoverpower.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
        )
        self.headlines = hoverpower.link(source)

    def frompath(self, path):  # pylint:disable=R0201
        path = docref.path.docref_figure(path)
        references = serializeraw.load_docref(path)
        return references

    def raw(self, value) -> str:
        collected = [
            f'{item.page} {item.sentence} {"   ".join(item.raw)}'
            for item in value
        ]
        result = utilo.NEWLINE.join(collected)
        return result
