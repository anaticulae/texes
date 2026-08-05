# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import german
import iamraw
import serializeraw
import utilo


def work(sentences: str, pages: tuple = None) -> str:
    if not utilo.exists(sentences):
        utilo.log(f'skip weblink sentences, missing: {sentences}')
        return '[]'
    sentences = serializeraw.load_text(content=sentences, pages=pages)
    processed = process_sentences(sentences)
    dumped = serializeraw.dump_hyperlinks(processed)
    return dumped


def process_sentences(texts):
    result = []
    for page, sentence in sentences_iter(texts):
        extracted = process_chunk(sentence)
        for item in extracted:
            item.page = page
        result.extend(extracted)
    return result


LOOK_FORWARD = configo.HV_INT_PLUS(default=30)


def process_chunk(sentence):
    result = []
    hyperlinks = german.links(sentence, position=True)
    if hyperlinks:
        hyperlinks = try_merge(sentence)
    for hyperlink, starting in hyperlinks:
        date = lookaround(
            sentence,
            start=starting,
            end=starting + len(hyperlink),
            collector=german.dates,
            after=LOOK_FORWARD,
        )
        date = date[0] if date else None
        result.append(iamraw.ExtractedHyperLink(href=hyperlink, visited=date))
    return result


def lookaround(
    text: str,
    start: int,
    end: int,
    collector: callable,
    before: int = 0,
    after: int = 0,
):
    """Try to parse pattern `collector` before and or after parsed item.

    Check the neighborhood.
    """
    before = text[start - before:start]
    after = text[end:end + after]
    result = []
    for item in [before, after]:
        parsed = collector(item)
        if not parsed:
            continue
        result.extend(parsed)
    return result


def try_merge(sentence: str) -> list:
    """\
    >>> try_merge('(Quelle: https://www.menschen _und_gesellschaft/'
    ... ' bevoelkerung/_geschlecht/index.html - aufgerufen am 15.03.2017)')
    [('https://www.menschen_und_gesellschaft/bevoelkerung/_geschlecht/index.html', 9)]
    """
    # TODO: MOVE TO GERMAN MERGE METHOD
    # TODO: SUPPORT MORE THAN ONE FORWARD MERGE
    result = []
    hyperlinks = german.links(sentence, position=True)
    for hyperlink, starting in hyperlinks:
        index = starting + len(hyperlink)
        raw_sentence = sentence[index:]
        merged = merge_forward(hyperlink, raw_sentence)
        if merged:
            # TODO: SUPPORT MORE THAN ONE HYPERLINK IN ONE SENTENCE
            assert len(merged) == 1, str(merged)
            result.append((merged[0], starting))
            continue
        if plain_word(raw_sentence):
            # next word seams not content of hyperlink
            result.append((hyperlink, starting))
            continue
        # connecting is not possible
        result.append((hyperlink, starting))
    return result


def merge_forward(before, text) -> list:
    splitted = text.split()
    current = None
    joined = before
    for item in splitted:
        current = german.links(joined)
        if item == '-':
            break
        joined = joined + item
        parsed = german.links(joined)
        if not parsed:
            break
        if parsed[0] != joined:
            break
    return current


def plain_word(text: str) -> bool:
    """\
    >>> plain_word('Hesus one')
    True
    >>> plain_word('_geschlec')
    False
    >>> plain_word('ht/index.html')
    False
    """
    return all(item.isalpha() for item in text.split())


def sentences_iter(texts, numbers: bool = False):
    number, current = 0, None
    for chunk in texts:
        for section in chunk.content:
            for page, sentence in zip(section.pages, section.content):
                if not numbers:
                    yield page, sentence
                else:
                    if current != page:
                        number = 0
                        current = page
                    else:
                        number += 1
                    yield page, number, sentence
