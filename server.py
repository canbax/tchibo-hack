from recommender import recommend4, x
from flask import Flask, render_template, request
import json

app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/similars')
def similars():
  idx = int(request.args.get('product_idx'))
  similar_products = recommend4(idx)
  for p in similar_products:
    p['product_data'] = x[p['product_idx']]

  return json.dumps(similar_products)


@app.route('/product')
def product_info():
  idx = int(request.args.get('product_idx'))
  return json.dumps(x[idx])


if __name__ == '__main__':
  app.run()
