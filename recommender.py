import json
import time
import pickle
import numpy as np
import spacy
import webbrowser

SENTENCE_SIM_LIMIT = 100
CNT_RECOMMEND = 10
WEIGHTS_4_RECOMMEND_SCORE = [0.33, 0.33, 0.34]
WEIGHTS_4_PRESELECTION = [1, 0]
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


def get_value(xi, path: list):
  obj = xi[path[0]]
  for p in path[1:]:
    obj = obj[p]
  return obj


def get_prop_values(xi, props):
  l = []
  for p in props:
    if p['is_float']:
      l.append(float(get_value(xi, p['path'])))
    else:
      l.append(get_value(xi, p['path']))

  return l


def preselection(x):
  r = 0
  for i in range(len(WEIGHTS_4_PRESELECTION)):
    r += x['sim' + str(i)] * WEIGHTS_4_PRESELECTION[i]
  return r


def calculate_basic_sim(product_idx: int, x):
  prop_list = [
      {'is_float': False, 'path': ['category', 'google_shopping_api']},
      {'is_float': True, 'path': ['price', 'amount']}
  ]
  main_product = get_prop_values(x[product_idx], prop_list)

  similarity2MainProduct = []
  for i, xi in enumerate(x):
    if i == product_idx:
      continue
    candidate_product = get_prop_values(xi, prop_list)
    similarities = {}
    for j, p in enumerate(prop_list):
      sim = 0
      if p['is_float']:
        sim = num_sim(candidate_product[j], main_product[j])
      else:
        sim = substr_sim(candidate_product[j], main_product[j])
      similarities['sim' + str(j)] = sim
    similarities['product_idx'] = i
    similarity2MainProduct.append(similarities)

  # get only the top 100 similar ones because calculating similarity to each other takes 6-7 minutes for a product
  similarity2MainProduct = sorted(similarity2MainProduct, key=preselection, reverse=True)[
      :SENTENCE_SIM_LIMIT]
  return similarity2MainProduct


def get_recommand_score(obj):
  score = 0
  for i in range(len(WEIGHTS_4_RECOMMEND_SCORE)):
    score += obj['sim' + str(i)] * WEIGHTS_4_RECOMMEND_SCORE[i]
  return score


def recommend4(product_idx: int):
  """ product_idx is the index of the product to make suggestions
   x should be a list of all the products. (like products_1.json) """
  start_time = time.time()
  sim4TheProduct = calculate_basic_sim(product_idx, x)
  prop1 = ['description', 'long']
  for sim in sim4TheProduct:
    desc1 = get_value(x[product_idx], prop1)
    desc2 = get_value(x[sim['product_idx']], prop1)
    sim['sim2'] = german_sentence_sim(desc1, desc2)
    sim['recommend_score'] = get_recommand_score(sim)

  sim4TheProduct = sorted(
      sim4TheProduct, key=lambda x: x['recommend_score'], reverse=True)

  # prop2 = ['image', 'default']
  # webbrowser.open(get_value(x[product_idx], prop2), new=2)
  # for sim in sim4TheProduct[:10]:
  #   webbrowser.open(get_value(x[sim['product_idx']], prop2), new=2)

  return json.dumps(sim4TheProduct[:10])
