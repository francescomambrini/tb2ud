import logging
from tb2ud.queries.query import Query


def is_pred_co(node):
    # sreg_krasis = re.compile(r"([κχ])(?=\w?[ὐὖὔἰἴἀἂἄἈὠᾀᾆἠὢὤὦᾦ])")
    if node.misc['NodeType'] == 'Artificial' and node.deprel == 'PRED_CO':
        right_siblings = [n for n in node.parent.children if int(n.ord) > int(node.ord)]
        # logging.warning(f'Length: {len(right_siblings)}')
        for sib in right_siblings:
            if sib.misc['NodeType'] != 'Artificial' and node.deprel == 'PRED_CO':
                return True

class PredCo(Query):
    def __init__(self):
        super().__init__(is_pred_co, mark="Gapping")