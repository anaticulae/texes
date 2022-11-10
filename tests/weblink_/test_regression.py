# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import weblink.features.sentence


def test_try_merge():
    raw = 'unter: file:///C:/Users/user/Downloads/MEMO-16-2265_DE.pdf'
    merged = weblink.features.sentence.try_merge(raw)
    assert len(merged) == 1
    merged = weblink.features.sentence.try_merge(raw)
    assert len(merged) == 1
    merged = weblink.features.sentence.try_merge(raw)
    assert len(merged) == 1
