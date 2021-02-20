import json

with open('/Users/charleshjpearce/Desktop/UoB/UoB_miniproject/data/TstB02_2022-01-04LOBs.json') as f:
    j_son = json.load(f)

s = 0
processed_json = []
for i, lob in enumerate(j_son):
    if lob['ask'] == j_son[i-1]['ask'] and lob['bid'] == j_son[i-1]['bid']:
        s += 1
        continue
    else:
        processed_json.append(lob)

with open('/Users/charleshjpearce/Desktop/UoB/UoB_miniproject/data/test_dup_removed.json', 'wt') as out:
    json.dump(processed_json, out)

print(f'number of duplicate lobs: {s}')
print(f'total proportion of duplicate lobs: {s/len(j_son)}')