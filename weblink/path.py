# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def weblink_bibliography(path: str, prefix: str = '') -> str:
    return utila.pathconnector(path, 'weblink', 'biblio_biblio', prefix)


def weblink_footer(path: str, prefix: str = '') -> str:
    return utila.pathconnector(path, 'weblink', 'footer_footer', prefix)


def weblink_sentence(path: str, prefix: str = '') -> str:
    return utila.pathconnector(path, 'weblink', 'sentence_sentence', prefix)
