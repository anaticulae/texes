# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import weblink

DESCRIPTION = ''

WORKPLAN = [
    utilo.create_step(
        'biblio',
        inputs=[
            utilo.ResultFile('bibliography', 'result_result'),
        ],
        output=('biblio',),
    ),
    utilo.create_step(
        'footer',
        inputs=[
            utilo.ResultFile('groupme', 'hefopa_result'),
        ],
        output=('footer',),
    ),
    utilo.create_step(
        'sentence',
        inputs=[
            utilo.ResultFile('words', 'sentences_sentences'),
        ],
        output=('sentence',),
    ),
]


def main():
    utilo.featurepack(
        root=weblink.ROOT,
        workplan=WORKPLAN,
        featurepackage='weblink.features',
        config=utilo.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=weblink.PROCESS,
            pages=True,
            version=weblink.__version__,
        ),
    )
