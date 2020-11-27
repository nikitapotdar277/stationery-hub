from flask import Blueprint, render_template, Flask, session, flash, redirect

user = Blueprint("success",__name__,static_folder="static", template_folder="template")

@user.route('/')
def success():
	if "name" not in session:
		flash("Please Login to continue","info")
		return redirect('/login')
	else:
		return render_template('user.html',name = session['name'].lower())
