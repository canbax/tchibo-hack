import json
import time
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# we can use description, category, price and images to make a similarity matrix and recommomend the highest scoring ones

x = None
with open('all_products_pickle', 'rb') as f:
  x = pickle.load(f)

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


p1 = x[0]['category']['google_shopping_api']
p2 = float(x[0]['price']['amount'])

start_time = time.time()

docs = []
for xi in x:
  # print(substr_sim(p1, xi['category']['google_shopping_api']))
  # print(num_sim(p2, float(xi['price']['amount'])))
  # print(str(p2) + '  vs ' + xi['price']['amount'])
  if xi['description']['long'] is None:
    docs.append('')
  else:
    docs.append(xi['description']['long'])

vect = TfidfVectorizer()
tfidf = vect.fit_transform(docs)
pairwise_similarity = tfidf * tfidf.T
n, _ = pairwise_similarity.shape
pairwise_similarity[np.arange(n), np.arange(n)] = -1.0
# pairwise_similarity[2].argmax()
# print((np.sort(pairwise_similarity[2].toarray().flatten())[::-1])[:100])

with open('desc_long_pairwise_similarity', 'wb') as f:
  pickle.dump(pairwise_similarity, f)

print(' executed in ' + str(time.time() - start_time))
