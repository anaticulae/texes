# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

# TODO: MOVED FROM WORDS, REMOVE LATER


def intindex(index: str) -> int:
    """Convert undefined index `'31u'` to int index `31.

    >>> intindex('31u')
    31
    >>> intindex('1') is None
    True
    """
    with contextlib.suppress(ValueError, IndexError):
        if index[-1] == 'u':
            return int(index[:-1])
    return None


def listindex(index: str) -> int:
    """Convert list index `'10l'` to int index `10.

    >>> listindex('10l')
    10
    """
    with contextlib.suppress(ValueError):
        if index[-1] == 'l':
            return int(index[:-1])
    return None
