# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german
import iamraw
import serializeraw
import texmex
import utilo


def work(word: str, pages: tuple = None) -> str:
    word = serializeraw.load_text(
        word,
        pages=pages,
    )
    collected = collect_quotations(word)
    dumped = serializeraw.dump_quotations(collected)
    return dumped


def collect_quotations(word) -> iamraw.ExtractedQuotations:
    result = []
    for page, index, sentence, splitted in sentences(word):
        lang = german.lang(splitted).language
        extracted = german.extract_quotes(sentence, lang=lang)
        if not extracted:
            continue
        for item in extracted:
            if item[0] is None or item[1] is None:
                utilo.error(f'not fully closed quotation {splitted}')
        extracted = [
            item for item in extracted
            if item[0] is not None and item[1] is not None
        ]
        quote = german.raw_quotation(splitted, extracted)
        for item in quote:
            result.append((page, index, item))
    return result


def sentences(word) -> iamraw.ExtractedQuotations:
    for word_section in word:
        page, pagecontent = word_section.page, word_section.content
        sentence_index = 0
        for _, content in pagecontent:
            for sentence in content:
                if texmex.is_list(sentence):
                    sentence = texmex.list_split(sentence)
                    # list
                    sentence = sentence[0]
                elif texmex.is_formula(sentence):
                    # skip formula
                    continue
                splitted = german.word_tokenize(
                    sentence,
                    validate_sentences=False,
                )
                if splitted:
                    yield page, sentence_index, sentence, splitted
                sentence_index = sentence_index + 1
