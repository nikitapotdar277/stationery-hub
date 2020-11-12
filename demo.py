from flask import Flask, redirect, url_for, render_template, request


app = Flask(__name__)

#table -> registration

@app.route('/<anything>')
def defaultpg(anything):
	return f"<h1>This the bad url</h1>"


@app.route('/login',methods=['GET','POST'])
def login():
	#email = request.form["email"]
	if request.method == "POST":
		if request.form["email"] == "yugandharyelai@gmail.com":
			return f"<h1>You have successfully entered the right data</h1>"
		else:
			return f"<h1>User id doesnt match(Try again)</h1>"
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