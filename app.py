from flask import Flask,render_template,request,jsonify
from interface import interface
from jsonify import common
from Engine.booktest import BookEngine
from omdb import OMDBClient
from Engine.movietestRun import MovieEngine
from flask.helpers import url_for

app = Flask(__name__, static_folder='static')
ob = interface(BookEngine(), MovieEngine())

client = OMDBClient(apikey='e181a4c1')

def checkurlcontent(title):
  res = url_for('static', filename = 'images/nan.jpg')
  set_path = res
  try:
      res = client.get(title,year=dict(common.get(title)).get('Year'))[:1][0].get('poster')
  except Exception as x:
      if x:
          pass
  return res if res != 'N/A' else set_path

@app.route('/')
def index():
  return render_template('main.html')
      
@app.route('/recommended_contents',methods=['POST'])
def viewcontents():
  arr = request.form['myInput']
  arr = arr.split('|')
  M_val = arr[0].strip()
  B_val = arr[1].strip()
  contents = ob.controller(M_val, B_val)
  return render_template("main.html", len=len(contents), contents=contents, common=common, check=checkurlcontent)

if __name__ == '__main__':
  app.run(debug=True)