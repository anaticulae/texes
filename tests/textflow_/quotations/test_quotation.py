# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw
import serializeraw
import utilo
import utilotest

import tests
import textflow.path


@utilotest.nightly
def test_textflow_quotation_master72p10t20(td, mp):
    current = extract_quotations(
        hoverpower.MASTER072_PDF,
        '10:21',
        td,
        mp,
    )
    assert current
    assert len(current) >= 30, str(current)
    dumped = serializeraw.dump_quotations(current)
    loaded = serializeraw.load_quotations(dumped)
    assert loaded == current


@utilotest.longrun
def test_textflow_quotation_bachelor76(td, mp):
    quotations = extract_quotations(
        hoverpower.BACHELOR076_PDF,
        '4,5',
        td,
        mp,
    )
    expected = 5
    assert len(quotations) == expected


# TODO: ADJUST EXPECTED AFTER IMPROVING PARSER
BACHELOR76_EXPECTED = """\
„ Digitalisierung “

„ Gesetzen der Digitalisierung “

„ Alles , was digitalisiert und in Informationen verwandelt werden kann , wird\
 digitalisiert und in Informationen verwandelt “

„ Was automatisiert werden kann , wird automatisiert “

„ Jede Technologie , die zum Zweck der Überwachung und Kontrolle \
kolonisiert werden kann , wird , was immer auch ihr ursprünglicher \
Zweck war , zum Zwecke der Überwachung und Kontrolle kolonisiert “

„ Digitalisierung und Industrie 4.0 im Mittelstand – Gestaltungsmöglichkeiten \
der digitalen Infrastruktur entlang der Wertschöpfungskette “

„ Unter dem Begriff Digitalisierung verstehen wir die Transformation von \
Geschäftsmodellen mit Hilfe von Informations - und Kommunikationstechnologien \
zur Reduktion von Schnittstellen , zur funktionsübergreifenden Vernetzung und\
 zur Erhöhung der Effektivität und Effizienz . “

„ Industrie 4.0 “"""

# „ digitale Revolution ”

# „ Cyber - Physischen Systemen ”

# „ In - dustrie 4.0 ”"""


@utilotest.longrun
def test_textflow_quotation_validate_bachelor76p4_10(td, mp):
    quotations = extract_quotations(
        hoverpower.BACHELOR076_PDF,
        '4:10',
        td,
        mp,
    )
    expected = utilo.splitlines(BACHELOR76_EXPECTED, pattern='\n\n')
    assert len(quotations) == len(expected)
    raw = (2 * utilo.NEWLINE).join([item.sentence for item in quotations])
    assert raw == BACHELOR76_EXPECTED


@utilotest.longrun
def test_textflow_quotation_validate_bachelor76p8(td, mp):
    quotations = extract_quotations(
        hoverpower.BACHELOR076_PDF,
        '8',
        td,
        mp,
    )
    assert len(quotations) == 2  # VALIDATED


def extract_quotations(
    source,
    pages: str,
    td,
    mp,
) -> iamraw.ExtractedQuotations:
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    tests.textflow_.run(
        f'-i {source} -i {td.tmpdir} --pages={pages} --quotation',
        mp=mp,
    )
    path = textflow.path.quotation(td.tmpdir)
    result = serializeraw.load_quotations(path)
    return result
