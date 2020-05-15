import json
common = {}

with open('static/dataset/new.json', encoding='utf-8', errors='ignore') as json_data:
    data = json.load(json_data, strict=False)

for i in data:
    dic = {}
    for j in i:
        if j != 'Title' and j != 'Summary' and j != 'YouTube Trailer' and j != 'Short Summary':
            dic.setdefault(j, i[j])
    common.setdefault(i['Title'], dic)
