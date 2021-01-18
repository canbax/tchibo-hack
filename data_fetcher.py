import requests
import json
import time

url = 'https://api.hackathon.tchibo.com/api/v1/products'
params = {'sort': 'product_id'}
headers = {'Content-Type': 'application/json',
           'Accept': 'application/json'}
has_next = True
is_first = True
next_url = None
page_num = 1
start_time = time.time()

while has_next:
  resp = None
  if is_first:
    resp = requests.get(url, params=params, headers=headers)
  else:
    resp = requests.get(next_url, headers=headers)
  data = json.loads(resp.text)
  with open('products_{}.json'.format(page_num), 'w+') as f:
    f.write(json.dumps(data['data']))
  has_next = data['links']['next'] is not None
  next_url = data['links']['next']
  is_first = False
  page_num += 1
  if page_num % 20 == 0:
    end_time = time.time()
    print(str(page_num) + ' donwloaded in ' + str(end_time - start_time))
  time.sleep(1)
