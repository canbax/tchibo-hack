import json
import time
import pickle
import numpy as np
import spacy

# we can use description, category, price and images to make a similarity matrix and recommomend the highest scoring ones

x = None
with open('all_products_pickle', 'rb') as f:
  x = pickle.load(f)

nlp = spacy.load('de_core_news_lg')

# with open('all_products.json', 'r') as f:
#   x = json.loads(f.read())


def substr_sim(s1: str, s2: str):
  """ calculates a similarity score between 2 strings based on their common leftstring size """
  if s1 is None or s2 is None:
    return 0
  s1 = s1.strip()
  s2 = s2.strip()
  cnt = 0
  size1 = len(s1)
  size2 = len(s2)

  for i in range(min(size1, size2)):
    if s1[i] == s2[i]:
      cnt += 1
    else:
      break
  return 2 * cnt / (size1 + size2)


def num_sim(n1, n2):
  """ calculates a similarity score between 2 numbers """
  return 1 - abs(n1 - n2) / (n1 + n2)


def german_sentence_sim(s1: str, s2: str):
  d1 = nlp(s1)
  # print([(w.text, w.pos_) for w in d1])
  d2 = nlp(s2)
  return d1.similarity(d2)


product_idx = 0
p1 = x[product_idx]['category']['google_shopping_api']
p2 = float(x[product_idx]['price']['amount'])

start_time = time.time()

category_sims = []
for idx, xi in enumerate(x):
  if idx == product_idx:
    continue
  category_sims.append(substr_sim(p1, xi['category']['google_shopping_api']))
  # print(num_sim(p2, float(xi['price']['amount'])))
  # print(str(p2) + '  vs ' + xi['price']['amount'])

category_sims = sorted(category_sims, reverse=True)
print(category_sims[:100])
print(' executed in ' + str(time.time() - start_time))
