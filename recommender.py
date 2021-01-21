import json
import time
import pickle
# we can use description, category, price and images to make a similarity matrix and recommomend the highest scoring ones

start_time = time.time()
x = None
with open('all_products_pickle', 'rb') as f:
  x = pickle.load(f)

# with open('all_products.json', 'r') as f:
#   x = json.loads(f.read())

print(' read all data in ' + str(time.time() - start_time))

# for xi in x:
#   print(xi['category']['google_shopping_api'])


