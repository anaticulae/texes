#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utilo

import textflow

DESCRIPTION = """\
Textflow extracts the text alignment, spaces between words and line
 endings for every line.
"""

WORKPLAN = [
    utilo.create_step(
        'alignment',
        inputs=[
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
        ],
        output=('current', 'expected'),
    ),
    utilo.create_step(
        'lineending',
        inputs=[
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
        ],
        output=('lastchar',),
    ),
    utilo.create_step(
        'quotation',
        inputs=[
            utilo.ResultFile('words', 'sentences_sentences'),
        ],
        output=('quotation',),
    ),
    utilo.create_step(
        'blockquote',
        inputs=[
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('groupme', 'footer_footerheader'),
        ],
        output=('blockquote',),
    ),
    utilo.create_step(
        'wordspace',
        inputs=[
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('groupme', 'footer_footerheader'),
            utilo.ResultFile('magic', 'content_content'),
            utilo.ResultFile('spacestation', 'wspace_wspace', optional=True),
        ],
        output=('wordspace',),
    ),
]


def main():
    utilo.featurepack(
        root=textflow.ROOT,
        workplan=WORKPLAN,
        featurepackage='textflow.features',
        config=utilo.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=textflow.PROCESS,
            pages=True,
            version=textflow.__version__,
        ),
    )
