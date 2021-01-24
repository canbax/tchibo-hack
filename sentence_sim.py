import spacy
import pickle
import time

x = None
with open('all_products_pickle', 'rb') as f:
  x = pickle.load(f)

start_time = time.time()
sentence1 = x[0]['description']['long']
for xi in x[:100]:
  print(german_sentence_sim(sentence1, xi['description']['long']))

print(' executed in ' + str(time.time() - start_time))
