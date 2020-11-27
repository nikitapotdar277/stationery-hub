from flask import Blueprint,Flask, redirect, url_for, render_template, request, session, flash
import mysql.connector
from flask_mail import Mail, Message
import sys
from werkzeug.utils import secure_filename
import base64
import os


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=sys.argv[1],
  database="miniamazon"
)
mycursor = mydb.cursor()

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'stationeryhub123@gmail.com'
app.config['MAIL_PASSWORD'] = 'snydbmsshub'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 

app.config['UPLOAD_FOLDER'] = 'static/image/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

user = Blueprint("success",__name__,static_folder="static", template_folder="template")

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	

@user.route('/')
def success():
	if "name" not in session:
		flash("Please Login to continue","info")
		return redirect('/login')
	else:
		return render_template('user.html', name = session['name'].lower())

@user.route('/lend',methods=['POST'])
def lend():
	return render_template("lend.html")

@user.route('/lenditems',methods=['POST'])
def lenditems():
	email = session["name"] + "@gmail.com"
	item_name = request.form["item"]
	price = request.form["price"]
	item_type = "lend"
	file = request.files['rentitem']
	
	if file and allowed_file(file.filename):
		image = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], image))

	else: 
		flash('Allowed image types are -> png, jpg, jpeg, gif')


	sql = "insert into items(email,item_name,price,item_type,img,sold) values(%s, %s, %s, %s,%s,%s);"
	val = (email,item_name,price,item_type,image,0)
	mycursor.execute(sql, val)
	mydb.commit()
	return render_template("index.html")


@user.route('/sell',methods=['POST'])
def sell():
	return render_template("sell.html")

@user.route('/sell1',methods=['POST'])
def sell1():
	email = session["name"] + "@gmail.com"
	item_name = request.form["item"]
	price = request.form["price"]
	file = request.files['sellitem']
	
	if file and allowed_file(file.filename):
		image = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], image))

	else: 
		flash('Allowed image types are -> png, jpg, jpeg, gif')
	
	item_type = "sell"
	sql = "insert into items(email,item_name,price,item_type,img, sold) values(%s, %s, %s, %s, %s, %s);"
	val = (email,item_name,int(price),item_type,image,0)
	mycursor.execute(sql, val)
	mydb.commit()
	return ('success')

@user.route('/order/<string:seller_email>/<string:item_name>/<string:item_type>')
def order(seller_email, item_name, item_type):
	sql1 = "select * from items where email = %s and item_name = %s and item_type = %s;"
	mycursor.execute(sql1, (seller_email, item_name, item_type))
	db_val = mycursor.fetchone()

	# img = img
	sql2 = "insert into orders(email, item_name, price, seller) values (%s, %s, %s, %s);"
	val = (session["name"] + "@gmail.com", item_name, db_val[3], seller_email)
	mycursor.execute(sql2, val)
	mydb.commit()

	sql3 = "update items set sold = 1 where email = %s and item_name = %s and item_type = %s;"
	mycursor.execute(sql3, (seller_email, item_name, item_type))
	mydb.commit()

	seller_msg = Message(
		'Hello',
		sender='stationeryhub123@gmail.com',
		recipients=[seller_email]
	)
	seller_msg.body = 'Hello! the user ' + session["name"] + '@gmail.com needs ' + item_name + '. They\'ll contact you soon. Thank you!'
	mail.send(seller_msg)
	buyer_msg = Message(
		'Hello',
		sender='stationeryhub123@gmail.com',
		recipients=[session["name"] + '@gmail.com']
	)
	buyer_msg.body = 'Hello! the user ' + seller_email + '@gmail.com has been notified about your stationery needs. You may contact them on the above email id. Thank you!'
	mail.send(buyer_msg)
	return('Ordered! Please check your mail')
