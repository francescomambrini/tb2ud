import logging

logger = logging.getLogger()


def _check_item(nodes, item):
    return [n for n in nodes if n.udeprel == item]


def get_first_in_priority(nodes, priority_list):
    # Advmod is prioritized over csubj; that works OK for noun-advmod, but what about adverbs or conjunctions?
    # that's why we create a quarantine: it something matches amod but is an adverb, a conj or a preposition,
    # it goes to quarantine and is evaluated only in the end, if nothing else shows up

    quarantine = []
    for i in priority_list:
        nds = _check_item(nodes, i)
        if len(nds) >= 1:
            if nds[0].udeprel == 'advmod' and nds[0].xpos[0] in ['c', 'd', 'r']:
                quarantine.append(nds[0])
                continue
            if len(nds) == 1:
                return nds[0]
            elif len(nds) > 1:
                logger.warning(f'More than 1 node in priority list for node {nds[0].parent.address()}! Returning the first')
                return nds[0]

        if quarantine:
            return quarantine[0]
