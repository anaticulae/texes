# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import weblink

DESCRIPTION = ''

WORKPLAN = [
    utila.create_step(
        'biblio',
        inputs=[
            utila.ResultFile('detector', 'bibliography_detected'),
        ],
        output=('biblio',),
    ),
    utila.create_step(
        'footer',
        inputs=[
            utila.ResultFile('groupme', 'footer_footerheader'),
        ],
        output=('footer',),
    ),
    utila.create_step(
        'sentence',
        inputs=[
            utila.ResultFile('words', 'sentences_sentences'),
        ],
        output=('sentence',),
    ),
]


def main():
    utila.featurepack(
        root=weblink.ROOT,
        workplan=WORKPLAN,
        featurepackage='weblink.features',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=weblink.PROCESS,
            pages=True,
            version=weblink.__version__,
        ),
    )
