from flask import Flask,render_template,request,jsonify
from interface import interface
from Engine.booktest import BookEngine
from Engine.movietest import MovieEngine
import requests
import omdb
app = Flask(__name__)


@app.route('/')
def index():
  return render_template('main.html')

@app.route('/pass_val',methods=['POST'])
def pass_val():
  arr = request.form['myInput']
  arr = arr.split('|')
  M_val = arr[0].split('-')[1].strip()
  B_val = arr[1].split('-')[1].strip()
  contents = ob.controller(M_val, B_val)
  return render_template("main.html", len=len(contents), contents=contents)

@app.route('/routed')
def movieinfo():
  response = requests.get('https://www.omdbapi.com/?apikey=e181a4c1&plot=short&r=json&s=iron man')
  return response.text

if __name__ == '__main__':
  book = BookEngine()
  movie = MovieEngine()
  ob = interface(book, movie)
  app.run(debug=True)