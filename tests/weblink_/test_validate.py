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

import tests
import tests.conftest
import tests.weblink_
import weblink
import weblink.path

ARCHIVE = utila.join(weblink.ROOT, 'tests/weblink_/expected', exist=True)

RESOURCES = utilatest.test_resources(tests.conftest.RESOURCES)


@pytest.mark.parametrize('source', RESOURCES)
def test_validate_hyperlinks(source, td, mp):
    utilatest.fixture_requires(source)
    Evaluate(
        source=source,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, workdir, mp):
        super().__init__(
            program=functools.partial(
                tests.weblink_.run,
                mp=mp,
            ),
            step='',
            pages=':',
            source=power.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
        )

    def frompath(self, workdir):  # pylint:disable=R0201
        result = []
        for loader in [
                weblink.path.weblink_bibliography,
                weblink.path.weblink_footer,
                weblink.path.weblink_sentence,
        ]:
            path = loader(workdir)
            loaded = serializeraw.load_hyperlinks(path)
            result.extend(loaded)
        return result

    def raw(self, value) -> str:
        value.sort(key=lambda x: x.page)
        result = []
        for hyperlink in value:
            raw = f'{str(hyperlink.page).zfill(3)} {hyperlink.href}'
            if hyperlink.visited:
                raw = f'{raw} {hyperlink.visited}'
            result.append(raw)
        raw = utila.NEWLINE.join(result)
        return raw
