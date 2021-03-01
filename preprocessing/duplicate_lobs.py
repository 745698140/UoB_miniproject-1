import json
from tqdm import tqdm

def remove_dup_null(string_in):
    print('Removing duplicate lobs and null vals')
    j_son = json.loads(string_in)
    processed_json = []
    for i, lob in enumerate(j_son):
        if (lob['ask'] == j_son[i-1]['ask'] and lob['bid'] == j_son[i-1]['bid']) \
        or not lob['ask'] or not lob['bid']:
            continue
        else:
            processed_json.append(lob)
    return processed_json