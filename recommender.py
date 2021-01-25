import json
import time
import pickle
import numpy as np
import spacy
import webbrowser

SENTENCE_SIM_LIMIT = 100
CNT_RECOMMEND = 10
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


def recommend4(product_idx: int, x):
  """ product_idx is the index of the product to make suggestions
   x should be a list of all the products. (like products_1.json) """
  p1 = x[product_idx]['category']['google_shopping_api']
  p2 = float(x[product_idx]['price']['amount'])

  start_time = time.time()

  sim4TheProduct = []
  for idx, xi in enumerate(x):
    if idx == product_idx:
      continue
    sim = substr_sim(p1, xi['category']['google_shopping_api'])
    sim2 = num_sim(p2, float(xi['price']['amount']))
    sim4TheProduct.append({'sim1': sim, 'sim2': sim2, 'product_idx': idx})

  # get only the top 100 similar ones because calculating similarity to each other takes 6-7 minutes for a product
  sim4TheProduct = sorted(sim4TheProduct, key=lambda x: x['sim1'], reverse=True)[
      :SENTENCE_SIM_LIMIT]

  for sim in sim4TheProduct:
    desc1 = x[product_idx]['description']['long']
    desc2 = x[sim['product_idx']]['description']['long']
    sim['sim3'] = german_sentence_sim(desc1, desc2)
    sim['recommend_score'] = sim['sim1'] * 0.13 + \
        sim['sim2'] * 0.33 + + sim['sim3'] * 0.54
  
  sim4TheProduct = sorted(sim4TheProduct, key=lambda x: x['recommend_score'], reverse=True)

  webbrowser.open(x[product_idx]['image']['default'], new=2)
  for sim in sim4TheProduct[:10]:
    webbrowser.open(x[sim['product_idx']]['image']['default'], new=2)

  print(sim4TheProduct[:10])
  print(' executed in ' + str(time.time() - start_time))

recommend4(0, x)