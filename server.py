from recommender import recommend4
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/similars')
def similars():
  idx = int(request.args.get('product_idx'))
  return recommend4(idx)


if __name__ == '__main__':
  app.run()
