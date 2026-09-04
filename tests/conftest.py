# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import gennex
import hoverpower
import pytest
import utilotest
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

import texes

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = texes.PACKAGE

hoverpower.setup(texes.ROOT)

RESOURCES = [
    (hoverpower.DISS143_PDF, '0:50'),
    (hoverpower.DISS144_PDF, '0:50'),
    (hoverpower.DISS172_PDF, '30:70'),
    hoverpower.BACHELOR028_PDF,
    hoverpower.BACHELOR037_PDF,
    hoverpower.BACHELOR051_PDF,
    hoverpower.BACHELOR075_PDF,
    hoverpower.BACHELOR076_PDF,
    hoverpower.DOCU007_PDF,
    hoverpower.DOCU009_PDF,
    hoverpower.DOCU027_PDF,
    hoverpower.HOME043_PDF,
    hoverpower.MASTER072_PDF,
    hoverpower.MASTER075_PDF,
    hoverpower.MASTER083_PDF,
    hoverpower.MASTER091B_PDF,
    hoverpower.MASTER098_PDF,
    hoverpower.MASTER116_PDF,
    hoverpower.todo(hoverpower.BACHELOR056_PDF, '0:20', spacestation=True),
]
WORKER = utilotest.worker_count(12, onci=len(RESOURCES))


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    hoverpower.run()


def extract(resources):
    gennex.extract(
        files=resources,
        bibliography=True,
        detector=True,
        groupme=True,
        headlines=True,
        lists=True,
        magic=True,
        sections=True,
        words=True,
        pagenumber=True,
        footnote=True,
        headnote=True,
        cleanup=True,
        worker=WORKER,
        rawmaker=gennex.CONFIG.replace('--char_margin=3.1',
                                       '--char_margin=5.0'),
    )
