from flask import Flask,render_template,redirect,url_for,request
import pymongo
import pandas as pd
import random

app = Flask(__name__)


idList = list(pd.read_csv("/Users/mu/Downloads/Personality_Lab/idList.csv",sep=","))
client = pymongo.MongoClient('localhost',27017)
db = client.personality
collection = db.personalityCollection

@app.route('/submit',methods=["POST"])
def submit():
	collection.insert({"id":request.form['id'],"type":request.form['type']})
	return redirect(url_for('homepage'))

@app.route('/homepage')
def homepage():
	id_in_db_set = set([doc['id'] for doc in collection.find()])
	id_list_set = set(idList)
	if (id_list_set - id_in_db_set):
		unclassfied_id = random.choice(list(id_list_set - id_in_db_set))
		return render_template('template.html',youtube_id=unclassfied_id)
	else:
		return "All finished"

if __name__ == '__main__':
	app.run(debug=True)
