from flask import Blueprint, render_template, Flask, session

user = Blueprint("success",__name__,static_folder="static",template_folder="template")

@user.route('/')
def success():
	if "name" not in session:
		return "please login"
	else:
		return "<h1>BLUPRINT CALLED</h1>"