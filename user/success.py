from flask import Blueprint, render_template, Flask, session

user = Blueprint("success",__name__,static_folder="static", template_folder="template")

@user.route('/')
def success():
	if "name" not in session:
		return "<h1><center>please login</center></h1>"
	else:
		return render_template('user.html',name = session['name'].lower())

# @user.route('')
