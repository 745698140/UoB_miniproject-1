import json


with open('./test/Tst2022-01-04LOBs.json') as f:
    j_son = json.load(f)
    print(j_son[750])