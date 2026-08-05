# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import utilotest

import tests.textflow_
import textflow.features.lineending
import textflow.path


@utilotest.longrun
@utilotest.requires(hoverpower.MASTER072_PDF)
def test_textflow_lineendings(td, mp):
    source = hoverpower.link(hoverpower.MASTER072_PDF)
    tests.textflow_.run(
        f'-i {source} --pages=0:10 --lineending',
        mp=mp,
    )
    source = textflow.path.lineending(td.tmpdir)

    endings = textflow.features.lineending.load_lineendings(source)
    assert len(endings) == 10
