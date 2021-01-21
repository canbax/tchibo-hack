import json
import pickle
import time

start_time = time.time()

PAGE_CNT = 4154
# PAGE_CNT = 100
cnt = 1
all_data = []
while cnt <= PAGE_CNT:
  with open('data/products_{}.json'.format(cnt), 'r') as f:
    data = json.loads(f.read())
    all_data.extend(data)
  cnt += 1

with open('all_products.json', 'w+') as f:
  f.write(json.dumps(all_data))

# pickled data can be read nearly 2 times faster than JSON
with open('all_products_pickle', 'wb') as f:
  pickle.dump(all_data, f)     

print(str(PAGE_CNT) + ' donwloaded in ' + str(time.time() - start_time))
