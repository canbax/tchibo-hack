import spacy
import pickle
import time

nlp = spacy.load('de_core_news_lg')


def german_sentence_sim(s1: str, s2: str):
  d1 = nlp(s1)
  # print([(w.text, w.pos_) for w in d1])
  d2 = nlp(s2)
  return d1.similarity(d2)


x = None
with open('all_products_pickle', 'rb') as f:
  x = pickle.load(f)

start_time = time.time()
sentence1 = x[0]['description']['long']
for xi in x[:100]:
  print(german_sentence_sim(sentence1, xi['description']['long']))

print(' executed in ' + str(time.time() - start_time))
