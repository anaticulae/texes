# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import power
import pytest
import utila
import utilatest

import tests.textflow_
import texas
import textflow.path
import textflow.quotation.serialize

ARCHIVE = utila.join(
    texas.ROOT,
    'tests/textflow_/quotations/expected',
    exist=True,
)


@pytest.mark.parametrize('source, expected', [
    pytest.param(power.MASTER072_PDF, 'master072', id='master072'),
    pytest.param(power.MASTER083_PDF, 'master083', id='master083'),
])
@utilatest.nightly
def test_validate_quotations_x(source, expected, testdir, monkeypatch):
    QuotationValidate(
        source,
        pages=':',
        expected=expected,
        testdir=testdir,
        monkeypatch=monkeypatch,
    ).evaluate()


class QuotationValidate(utilatest.BaseLiner):

    def __init__(self, source, pages, expected, testdir, monkeypatch):
        super().__init__(
            program=functools.partial(
                tests.textflow_.run,
                monkeypatch=monkeypatch,
            ),
            step='quotation',
            source=source,
            pages=pages,
            workdir=testdir.tmpdir,
            index=expected,
            archive=ARCHIVE,
            loader=self.load_quotations,
        )

    def load_quotations(self, workdir):  # pylint:disable=R0201
        path = textflow.path.quotation(workdir)
        result = textflow.quotation.serialize.load_quotations(path)
        return result

    def raw(self, value) -> str:  # pylint:disable=R0201
        quotes = [
            f'{str(quote.page).zfill(3)} {quote.sentence}' for quote in value
        ]
        raw = utila.NEWLINE.join(quotes).strip()
        return raw
