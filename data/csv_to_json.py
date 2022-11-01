import csv
import json

ADS = 'ad'
CATEGORY = 'category'
LOC = 'location'
USER = 'user'


def convert_file(csv_file, json_file, model):
    result = []
    with open(csv_file, encoding='utf-8') as csv_f:
        for row in csv.DictReader(csv_f):
            to_add = {'model': model, 'pk': int(row['Id'] if 'Id' in row else row['id'])}
            if 'id' in row:
                del row['id']
            else:
                del row['Id']

            if 'location_id' in row:
                row['location'] = [int(row['location_id'])]
                del row['location_id']

            if 'is_published' in row:
                if row['is_published'] == 'TRUE':
                    row['is_published'] = True
                else:
                    row['is_published'] = False

            if 'price' in row:
                row['price'] = int(row['price'])

            to_add['fields'] = row
            result.append(to_add)

    with open(json_file, 'w', encoding='utf-8') as jf:
        jf.write(json.dumps(result, ensure_ascii=False))


convert_file(f"{ADS}.csv", f"{ADS}.json", 'ads.ad')
convert_file(f"{CATEGORY}.csv", f"{CATEGORY}.json", 'ads.category')
convert_file(f"{USER}.csv", f"{USER}.json", 'users.user')
convert_file(f"{LOC}.csv", f"{LOC}.json", 'users.location')
