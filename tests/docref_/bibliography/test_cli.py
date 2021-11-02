# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import pytest
import serializeraw
import utila
import utilatest

import docref.path
import docref.utils
import tests.docref_


def extract_label(source, testdir, monkeypatch, pages=':'):
    source = power.link(source)
    tests.docref_.run(
        f'-i {source} --bibliography --pages={pages}',
        monkeypatch=monkeypatch,
    )
    bibliography = docref.path.docref_bibliography(testdir.tmpdir)
    bibliography = serializeraw.load_docref(bibliography)
    return bibliography


def extract_label_plain(pdf, testdir, monkeypatch, pages=None):
    bibliography = extract_label(
        pdf,
        testdir,
        monkeypatch,
        pages=utila.simplify_pages(pages),
    )
    source = power.link(pdf)
    path = os.path.join(source, 'words__sentences_sentences.yaml')
    headlines = serializeraw.load_headlines(source, pages=pages)
    text = serializeraw.load_text(path, headlines=headlines, pages=pages)
    plain = docref.utils.references_plain(bibliography, text)
    flat = utila.flatten(plain)
    return flat


@utilatest.nightly
@utilatest.requires(power.MASTER116_PDF)
def test_docref_bibliography_master116(testdir, monkeypatch):
    # TODO: Changes after support more tech label
    bibliography = extract_label(
        power.MASTER116_PDF,
        testdir,
        monkeypatch,
        pages='8:93',
    )
    assert len(bibliography) == 91  # NOT VALIDATED YET


@pytest.mark.xfail(reason='[33] is missing')
@utilatest.longrun
@utilatest.requires(power.BACHELOR075_PDF)
def test_docref_bibliography_bachelor075(testdir, monkeypatch):
    bibliography = extract_label(
        power.BACHELOR075_PDF,
        testdir,
        monkeypatch,
    )
    source = power.link(power.BACHELOR075_PDF)
    headlines = serializeraw.load_headlines(source)
    path = os.path.join(source, 'words__sentences_sentences.yaml')
    text = serializeraw.load_text(path, headlines=headlines)
    plain = docref.utils.references_plain(bibliography, text)
    flat = utila.flatten(plain)
    unique = utila.sort(*utila.make_unique(flat))
    # TODO: VALIDATED ALL MULTIPLE REFERENCES
    assert len(unique) == 41  # VALIDATED: 41


@utilatest.requires(power.MASTER091B_PDF)
def test_docref_bibliography_master91b(testdir, monkeypatch):
    """Do not parse overlapping words. Do not detect overlapping words
    twice. Some pattern are part of other pattern."""
    bibliography = extract_label(
        power.MASTER091B_PDF,
        testdir,
        monkeypatch,
        pages='9',
    )
    assert len(bibliography) == 2


@utilatest.nightly
@utilatest.requires(power.MASTER098_PDF)
def test_docref_bibliography_master98(testdir, monkeypatch):
    bibliography = extract_label(power.MASTER098_PDF, testdir, monkeypatch)
    assert len(bibliography) == 272  # NOT VALIDATED YET


@utilatest.longrun
def test_docref_bibliography_diss143(testdir, monkeypatch):
    flat = extract_label_plain(
        power.DISS143_PDF,
        testdir,
        monkeypatch,
        pages=utila.ranged_tuple(15, 30),
    )
    assert len(flat) == 30  # NOT VALIDATED YET
