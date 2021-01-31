from recommender import recommend4, x, get_settings, update_settings
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


@app.route('/setconfig', methods=['POST'])
def update_config():
  data = json.loads(request.data.decode('ascii'))
  update_settings(data['preselection_size'], data['cnt_recommend'],
                  data['weights_4_recommend_score'], data['weights_4_preselection'])
  return ''


@app.route('/getconfig')
def get_config():
  return json.dumps(get_settings())


if __name__ == '__main__':
  app.run()
