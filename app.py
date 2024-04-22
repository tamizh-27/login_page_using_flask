from flask import Flask, render_template, request
import mysql.connector as mc
import pickle
import pandas as pd

app = Flask(__name__)
db = mc.connect(host="localhost",user="root",password="sql@123",database="ml_cat2")

query = '''
create table login
(username varchar(20),
 password varchar(20))
'''

cursor = db.cursor(query)

cursor.execute(query)

model = pickle.load(open("model.pkl","rb"))

@app.route('/')
def home():
    return render_template("webpage.html")

@app.route('/signin', methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("mail")
        password = request.form.get("pwd")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM login WHERE username=%s AND password=%s", (email, password))
        result = cursor.fetchone()
        if result:
            return render_template("ml_model.html")
        else:
            return render_template("webpage.html", msg="Invalid username or password")
    else:
        return render_template("webpage.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("mail")
        password = request.form.get("pwd")
        cursor = db.cursor()
        cursor.execute("INSERT INTO login (username, password) VALUES (%s, %s)", (email, password))
        db.commit()
        return render_template("webpage.html", msg="Signed up successfully")
    else:
        return render_template("webpage.html")
    
@app.route('/pred', methods=["GET", "POST"])
def pred():
    if request.method == "POST":
        inp1 = request.form.get("input1")
        inp2 = request.form.get("input2")
        inp3 = request.form.get("input3")
        inp4 = request.form.get("input4")
        inp5 = request.form.get("input5")
        inp6 = request.form.get("input6")
        inp7 = request.form.get("input7")
        test = [[inp1,inp2,inp3,inp4,inp5,inp6,inp7]]
        pred = model.predict(test)    
        pred = pd.Series(pred)    
        pred = pred.replace({0:"Female",1:"Male"})
        return render_template("prediction.html",out="The gender is : " + pred[0])
    else:
        return render_template("ml_model.html")

if __name__ == "__main__":
    app.run()
