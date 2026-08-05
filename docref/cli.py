# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import docref

DESCRIPTION = """\
Docref parses all in-doc-refrences which connect text elements(siehe
Abbildung 5) with structure elements(figure, table, etc.).
"""

WORKPLAN = [
    utilo.create_step(
        'bibliography',
        inputs=[
            utilo.ResultFile('words', 'sentences_sentences'),
            utilo.ResultFile('headlines', 'result_result'),
        ],
        output=('parsed',),
    ),
    utilo.create_step(
        'figure',
        inputs=[
            utilo.ResultFile('words', 'sentences_sentences'),
            utilo.ResultFile('headlines', 'result_result'),
        ],
        output=('parsed',),
    ),
    utilo.create_step(
        'section',
        inputs=[
            utilo.ResultFile('words', 'sentences_sentences'),
            utilo.ResultFile('headlines', 'result_result'),
        ],
        output=('parsed',),
    ),
    utilo.create_step(
        'table',
        inputs=[
            utilo.ResultFile('words', 'sentences_sentences'),
            utilo.ResultFile('headlines', 'result_result'),
        ],
        output=('parsed',),
    ),
]


def main():
    utilo.featurepack(
        root=docref.ROOT,
        workplan=WORKPLAN,
        featurepackage='docref.features',
        config=utilo.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=docref.PROCESS,
            pages=True,
            version=docref.__version__,
        ),
    )
