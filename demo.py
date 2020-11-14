from flask import Flask, redirect, url_for, render_template, request
import mysql.connector
from user.success import user


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="miniamazon"
)
mycursor = mydb.cursor()

app = Flask(__name__)
app.register_blueprint(user,url_prefix='/user')

#table -> registration

@app.route('/<anything>')
def defaultpg(anything):
	return f"<h1>This the bad url</h1>"

@app.route('/login',methods=["GET","POST"])
def login():
	if request.method == "POST":
		
		email = request.form["username"]
		password = request.form["user_pass"]
		
		sql = "select password from registration where email= '" + email + "';"
		
		mycursor.execute(sql)
		
		db_pass = mycursor.fetchone()
		if db_pass == None or db_pass[0] != password:
			return "<h1>Incorrect Email/password</h1>"
		elif db_pass[0] == password:
			return redirect("/user")#f"<h1>Login successfully {email[:email.find('@')]}</h1>"
		
		
		return f"<h1>TRUE</h1>"
	else:
		
		return render_template('sign_in.html')
	

@app.route('/register',methods=['GET','POST'])
def register():
	
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
			return redirect("login")
	else:
		return render_template('register.html')

@app.route('/')
@app.route('/home')
def home():
	return render_template("index.html")
	

if __name__ == "__main__":
	app.debug = True
	app.run()