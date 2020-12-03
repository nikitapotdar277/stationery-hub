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

def path_finder():
	paths = []
	
	for i,j,k in os.walk(r"C:\Users\College\Documents\GitHub\dbms\static\image\uploads" ):
		
		if k != []:
			paths.append([(i+'\\'+file) for file in k])
	actual = []
	for i in (paths):
		for j in i:
			actual.append(j)
			

	url_,file_name = [],[]
	for i in actual:
		url_.append('/'.join(i.split('\\')[6:]))
		file_name.append(i.split('\\')[-1])
	return url_,file_name

def insert_image(file):
	if file and allowed_file(file.filename):
		image = secure_filename(file.filename)
		path_ = os.path.join(app.config['UPLOAD_FOLDER']+session["year"]+'/'+session["branch"]+'/'+session["name"]+'/')
		if not os.path.exists(path_):
			os.makedirs(path_)

		sql = "select item_id from items order by item_id desc LIMIT 1;" #LIMIT DESC
		mycursor.execute(sql)
		try:
			index_= int(mycursor.fetchone()[0]) + 1
		except:
			index_ = 1
		file.save(path_ + '/' + str(index_)+'.jpg')
		return 1,(str(index_)+'.jpg')
	else:
		return 0, 'null'

	

@user.route('/')
def success():
	if "name" not in session:
		flash("Please Login To Continue!")
		return  redirect('/login')
	else:
		# try:

			sql =f"""select * from items where email not in ('{session["email"]}');"""  #LIKE USED
			#print(search_item,type(search_item))
			mycursor.execute(sql)
			db_search = mycursor.fetchall()
			#print (db_search)
			value = {
			0:"IN STOCK",
			1:"NOT IN STOCK"
			}

			link,file_name = path_finder()
			list_ = []
			# print("START__________")
			# print(link)
			# print(file_name)
			# print("END____________")
			#print("DEBUGGING")
			fname = []
			for index,val in enumerate(file_name):
				for row in db_search:
					if val in row[-2]:
						list_.append(link[index])
						#print(link[index])
						fname.append(val)

			return render_template('user2.html', db_search = enumerate(db_search),value=value,list_=list_,filename=fname,name=session["name"].lower())
		#except Exception as e:
			# print(e)
			# app.logger.info(f"Exception occured while encountering search :{request.url,e}")

			# return redirect('/somethingwentwrong')
		#return render_template('user2.html', name = session['name'].lower())

@user.route('/rent',methods=['POST'])
def rent():
	return render_template("rent.html")

@user.route('/rentitems',methods=['POST'])
def rentitems():
	email = session["name"] + "@gmail.com"
	item_name = request.form["item"]
	price = request.form["price"]
	item_type = "rent"
	file = request.files['rentitem']
		
# select branch,year from registration join items on registration.email = items.email;


	insert_success,image = insert_image(file)
	if not insert_success:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		print(request.url)
		return render_template("rent.html")

	sql = "insert into items(email,item_name,price,item_type,img,sold) values(%s, %s, %s, %s,%s,%s);"
	val = (email,item_name,price,item_type,image,0)
	mycursor.execute(sql, val)
	mydb.commit()
	flash("You have successfully Inserted The Details!")
	return redirect("/user")

@user.route('cart/<string:seller_email>/<string:item_name>/<string:image>')
def Cart(seller_email,item_name,image):
	try:
		sql = """insert into cart(email,item_name,img) values(%s,%s,%s)"""
		mycursor.execute(sql, (seller_email, item_name, image))
		mydb.commit()
		flash("Insert into cart successfully done")
		return redirect('/')
	except :
		print("ERRORR")
		redirect('/somethingwentwrong')

@user.route('/sell',methods=['POST'])
def sell():
	return render_template("sell.html")

@user.route('/sell1',methods=['POST'])
def sell1():
	email = session["name"] + "@gmail.com"
	item_name = request.form["item"]
	price = request.form["price"]
	file = request.files['sellitem'] # name
	print(file)
	insert_success,image = insert_image(file)
	if not insert_success:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		print(request.url)
		return render_template("sell.html")
	
	item_type = "sell"
	sql = "insert into items(email,item_name,price,item_type,img, sold) values(%s, %s, %s, %s, %s, %s);"
	val = (email,item_name,int(price),item_type,image,0)
	mycursor.execute(sql, val)
	mydb.commit()
	flash("You have successfully Inserted The Details!")
	return redirect("/user")

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


img_name,prices,review,history=[],[],[],[]

locations = {
	""
}

@user.route('/test')
def test():
	return render_template("user2.html",name="LOGIN")

@user.route('/product')
def product():
	return render_template("product.html")

@user.route('/user3')
def user3():
	return render_template("user3.html")



@user.route('/main')
def trial():
	print(os.getcwd())
	img_name = ['static/user_pg/image_dy/'+i for i in os.listdir(r"./user/static/user_pg/image_dy/")]
	print(img_name)
	for i in range(len(img_name)):
		prices.append((i+1)*100)
		review.append((i+1))
	return render_template("user1.html",img_name=img_name,prices=prices,review=review,slider=img_name,history=img_name)

	
@user.route('/wishlist',methods=['POST'])
def wishlist():
	return render_template('wishlist.html')


@user.route('/myorders',methods=['POST'])
def myorders():
	return render_template('orderHistory.html',title=session["name"])

@user.route('/mycart',methods=['GET'])
def mycart():
	sql = """select cart.email,cart.item_name,items.price,cart.img from cart join items on cart.img = items.img;"""
	mycursor.execute(sql)
	db_search = mycursor.fetchall()
	#print (db_search)
	value = {
			0:"IN STOCK",
			1:"NOT IN STOCK"
			}

	link,file_name = path_finder()
	list_ = []
	# print("START__________")
	# print(link)
	# print(file_name)
	# print("END____________")
	#print("DEBUGGING")
	fname = []
	for index,val in enumerate(file_name):
		for row in db_search:
			if val in row[-1]:
				print("Inside loop")
				list_.append(link[index])
				print(link[index])
				fname.append(val)

	return render_template('cart.html', db_search = enumerate(db_search),list_=list_)
		
	#return render_template('cart.html')