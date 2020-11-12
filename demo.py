from flask import Flask, redirect, url_for, render_template, request
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="miniamazon"
)
mycursor = mydb.cursor()

app = Flask(__name__)

#table -> registration

@app.route('/<anything>')
def defaultpg(anything):
	return f"<h1>This the bad url</h1>"


@app.route('/login',methods=['GET','POST'])
def login():
	
	if request.method == "POST":
	
	
		email = request.form["email"]
		branch = request.form["branch"]
		year = request.form["year"]
		password = request.form["psw"]
		sql = "select * from registration where email ='" + email + "';" 
		#print(sql)
		mycursor.execute(sql)
		#mydb.commit()
		if ((mycursor.fetchone())== None) and (request.form["psw"] == request.form["psw-repeat"]):
			sql = "insert into registration(email,branch,year,password) values(%s, %s, %s, %s);"
			val = (email,branch,year,password)
			#print(sql)
			mycursor.execute(sql,val)
			mydb.commit()
			return f"<h1>You have successfully entered the right data</h1>"
		else:
			return redirect("/login")
	else:
	
	#print(email)
	#if email == "yugandharyelai@gmail.com":
	#	return f"<h1>successfull login</h1>"
		return render_template('register.html')

@app.route('/')
def home():
	return render_template("index.html")
	

if __name__ == "__main__":
	app.run(debug = True)