from flask import Flask,render_template,request,jsonify
from interface import interface
from Engine.booktest import BookEngine
from Engine.movietest import MovieEngine

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

book = BookEngine()
movie = MovieEngine()
ob = interface(book, movie)
if __name__ == '__main__':
  app.run(debug=True)