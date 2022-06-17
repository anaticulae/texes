# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest
import utila

import texas

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = texas.PACKAGE

power.setup(texas.ROOT)

RESOURCES = [
    (power.BACHELOR051_PDF, '15:30'),
    (power.DISS143_PDF, '0:50'),
    (power.DISS172_PDF, '30:70'),
    (power.MASTER091B_PDF, '0:20'),
    power.BACHELOR037_PDF,
    power.BACHELOR075_PDF,
    power.BACHELOR076_PDF,
    power.DOCU007_PDF,
    power.DOCU009_PDF,
    power.DOCU027_PDF,
    power.HOME040_PDF,
    power.MASTER072_PDF,
    power.MASTER075_PDF,
    power.MASTER083_PDF,
    power.MASTER098_PDF,
    power.MASTER116_PDF,
    power.todo(power.BACHELOR056_PDF, '0:20', spacestation=True),
]
WORKER = 4


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract(resources):
    utila.log(f'root: {power.REPOSITORY}')
    genex.extract(
        files=resources,
        destination=power.generated(),
        base=power.REPOSITORY,
        bibliography=True,
        detector=True,
        groupme=True,
        headlines=True,
        lists=True,
        magic=True,
        sections=True,
        words=True,
        worker=WORKER,
        pages=':',
        rawmaker=genex.CONFIG.replace('--char_margin=3.1', '--char_margin=5.0'),
    )
