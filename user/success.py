from flask import Blueprint, render_template, Flask

user = Blueprint("success",__name__,static_folder="static",template_folder="template")

@user.route('/')
def success():
	return "<h1>BLUPRINT CALLED</h1>"