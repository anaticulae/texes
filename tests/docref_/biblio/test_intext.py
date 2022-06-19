# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import docref.biblio.strategies.intext

RAW = """\
(Halbwachs 1985:71)
(ebd .:20)
(Nora 1990:12-13)
(Hahn ; Traba 2015:13)
(Koreik 2010:1482)
(Seydoux de Clausonne 1968:20)
(vgl. Darilek 2014)
(vgl. Defrance ; Pfeil 2014 ; vgl. Frank 2005)
"""

TODO = """\
"""


def test_parse_label():
    parsed = docref.biblio.strategies.intext.parse(RAW)
    expected = len(RAW.splitlines())
    assert len(parsed) == expected


def test_parse_not_working_yet():
    parsed = docref.biblio.strategies.intext.parse(TODO)
    expected = len(TODO.splitlines())
    assert len(parsed) == expected
