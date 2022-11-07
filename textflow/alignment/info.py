# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


class AlignmentInfo:

    def __init__(self, oneline, alignment):
        msg = f'{len(oneline)} == {len(alignment)}'
        assert len(oneline) == len(alignment), msg
        self.oneline = PageTextAdapter(layout=oneline)
        self.data = alignment

    def alignment(self, page, bounding):
        # TODO: ADD MORE DOCS HERE
        centered = center(bounding)
        inside = self.oneline.inside(page=page, bounding=centered)
        if not inside:
            return None
        selected = utila.select_page(self.data, page=page)
        if not selected:
            return None
        try:
            result = [selected.content[index] for index, _ in inside]
        except IndexError:
            # TODO: INVESTIGATE HOW THIS CAN HAPPEN
            utila.debug(f'alignment, out of bounds: {page}; {inside}')
            return []
        return result


class PageTextAdapter:

    def __init__(self, layout):
        self.layout = layout

    def inside(self, page, bounding):
        selected = utila.select_page(self.layout, page=page)
        if not selected:
            utila.error(f'adapter: could not select page {page}')
            return None
        result = [(index, item)
                  for index, item in enumerate(selected)
                  if utila.rect_inside(item.bounding, bounding)]
        return result


def center(bounding):
    # TODO: VERIFY THE SENCE OF THIS METHOD
    x0, y0, x1, y1 = bounding
    result = (
        (x1 + x0) / 2,
        (y1 + y0) / 2,
        (x1 + x0) / 2,
        (y1 + y0) / 2,
    )
    return result
