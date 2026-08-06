# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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

import tests.textflow_
import texes
import textflow.path

ARCHIVE = utilo.join(
    texes.ROOT,
    'tests/textflow_/quotations/expected',
    exist=True,
)


@pytest.mark.parametrize('source, expected', [
    pytest.param(hoverpower.MASTER072_PDF, 'master072', id='master072'),
    pytest.param(hoverpower.MASTER083_PDF, 'master083', id='master083'),
])
@utilotest.nightly
def test_validate_quotations_x(source, expected, td, mp):
    QuotationValidate(
        source,
        pages=':',
        expected=expected,
        td=td,
        mp=mp,
    ).evaluate()


class QuotationValidate(utilotest.BaseLiner):

    def __init__(self, source, pages, expected, td, mp):
        super().__init__(
            program=functools.partial(
                tests.textflow_.run,
                mp=mp,
            ),
            step='quotation',
            source=source,
            pages=pages,
            workdir=td.tmpdir,
            index=expected,
            archive=ARCHIVE,
            loader=self.load_quotations,
        )

    def load_quotations(self, workdir):  # pylint:disable=R0201
        path = textflow.path.quotation(workdir)
        result = serializeraw.load_quotations(path)
        return result

    def raw(self, value) -> str:  # pylint:disable=R0201
        quotes = [
            f'{str(quote.page).zfill(3)} {quote.sentence}' for quote in value
        ]
        raw = utilo.NEWLINE.join(quotes).strip()
        return raw
