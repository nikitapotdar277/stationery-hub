
#DONE--> Sakshi Pathak
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
app.config['MAIL_USERNAME'] = os.environ.get("USERNAME_")
app.config['MAIL_PASSWORD'] = os.environ.get("PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 

app.config['UPLOAD_FOLDER'] = 'static/image/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

user = Blueprint("success",__name__,static_folder="static", template_folder="template")

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def order(seller_email, item_name, item_type):
	sql1 = "select * from items where email = %s and item_name = %s;"
	mycursor.execute(sql1, (seller_email, item_name))
	db_val = mycursor.fetchone()

	if int(db_val[-1]) == 0:
		sql2 = "insert into orders(email, item_name, price, seller) values (%s, %s, %s, %s);"
		val = (session["name"] + "@gmail.com", item_name, int(db_val[3]), seller_email)
		mycursor.execute(sql2, val)
		mydb.commit()

		sql3 = "update items set sold = 1 where email = %s and item_name = %s;"
		mycursor.execute(sql3, (seller_email, item_name))
		mydb.commit()

		seller_msg = Message(
			'Hello',
			sender=os.environ.get("USERNAME_"),
			recipients=[seller_email]
		)
		seller_msg.body = 'Hello! the user ' + session["email"] + ' needs ' + item_name + '. They\'ll contact you soon. Thank you!'
		print("USERNAME_--->",os.environ.get("USERNAME_"))
		print(seller_msg.body)
		mail.send(seller_msg)
		buyer_msg = Message(
			'Hello',
			sender= os.environ.get("USERNAME_"),
			recipients=[session["name"] + '@gmail.com']
		)
		buyer_msg.body = 'Hello!, the user ' + seller_email +  ' has been notified about your stationery needs. You may contact them on the above email id. Thank you!'
		print(buyer_msg.body)
		mail.send(buyer_msg)
		return 1
	else:
		flash(f"Sorry The product {item_name} Is out of stock",category="danger")
		return 0

# @user.route('/search/<string:page>/<string:search_item>/<int:sort>',methods=['GET',"POST"])
def search(page,search_item,sort=0):

		scan = {

		"user": "items",
		"wishlist" :"wishlist",
		"cart" :"cart"

		}
		link,file_name = path_finder()
		list_ = []

		value = {
		0:"IN STOCK",
		1:"OUT OF STOCK"
		}
		link = sorted(link, key = lambda x: file_name[link.index(x)])
		file_name.sort()
		total = 0
		count = 0
		if page == "user":
			
			if "name" not in session:
				sql = f"""select * from {scan[page]} where item_name LIKE %s;"""   #LIKE USED
				mycursor.execute(sql, ("%" + search_item + "%",))
				name = "LOGIN"
				db_search = mycursor.fetchall()
				for index,val in enumerate(file_name):
					for row in (db_search):
						if val in row[5]:
							list_.append(link[index])

			else:
				sql = f"""select * from {scan[page]} where email not in ('{session["email"]}') and item_name like '%{search_item}%';"""
				mycursor.execute(sql)
				name = session["name"]
				db_search = mycursor.fetchall()
				for index,val in enumerate(file_name):
					for row in (db_search):
						if val in row[5]:
							list_.append(link[index])
		else:
			sql = f""" select {scan[page]}.product_email,{scan[page]}.item_name,items.price,{scan[page]}.cart_holder,{scan[page]}.img,items.sold,items.item_id,{scan[page]}.item_id from {scan[page]} join items on {scan[page]}.img = items.img and {scan[page]}.cart_holder = '{session['email']}' and {scan[page]}.item_name like '%{search_item}%' order by {scan[page]}.img;"""
		
			# sql = f"""select {scan[page]}.product_email,{scan[page]}.item_name,items.price,{scan[page]}.img,items.sold,items.item_id from {scan[page]} join items on {scan[page]}.img = items.img and {scan[page]}_holder='{session["email"]}' and {scan[page]}.item_name like '%{search_item}%' order by {scan[page]}.img;"""
			mycursor.execute(sql)
			name = session["name"]
			#print(search_item,type(search_item))
			db_search = mycursor.fetchall()
			for i in db_search:
				total += i[2]
			sql = f""" select count(*) from {scan[page]} join items on {scan[page]}.item_name = items.item_name and cart_holder='{session["email"]}' and {scan[page]}.item_name like '%{search_item}%' order by {scan[page]}.img;"""
			mycursor.execute(sql)
			count = int(mycursor.fetchone()[0])
		
		
			print ("Search->",db_search)

			for index,val in enumerate(file_name):
				for row in (db_search):
					if val in row[4]:
						list_.append(link[index])

		if sort == 1:
			list_ = list_[::-1]
			file_name = file_name[::-1]
			db_search = db_search[::-1]
					
		return db_search,value,list_,name,file_name,total,count

# @user.route('/Search/<string:page>/<int:sort>')
def Search(page,sort):


	db_search,value,list_,name,file_name,total,count = search(page,"",sort)
	if page == "user":
		page = "user2"
	return render_template(f'{page}.html', db_search = enumerate(db_search),value=value,list_=list_,name=name,filename=file_name,total=total,count=count)
	


def path_finder():
	paths = []
	
	for i,j,k in os.walk(os.environ.get('MINIAMAZONPATH')):
		
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
			1:"OUT OF STOCK"
			}

			link,file_name = path_finder()
			list_ = []
			fname = []

			# for i in file_name:
			# 	s = i.split('.jpg')
			# 	try:
			# 		fname.append(int(s[0]))
			# 	except :
			# 		pass
			# # fname.sort()
			# temp = []
			# for i in db_search:
			# 	temp.append(i[5])


			# print("Before sorting(link)--->",link)
			# print("Before sorting(file_name)--->",file_name)
			#file_name.sort()
			#fname.sort()
			# DO NOT TOUCH
			#fname.sort()
			link = sorted(link, key = lambda x: file_name[link.index(x)])
			file_name.sort()
			# link = sorted(file_name, key = lambda x: fname[file_name.index(x)])
			# fname.sort()

			# print("After sorting(link)--->",link)
			# print("After sorting(file_name)--->",file_name)

			print("USER---->",db_search)
			print("\nFilename--->",file_name)
			total = 0
			for index,val in enumerate(file_name):
				for row in (db_search):
					if val in row[-2]:
						list_.append(link[index])
						print("list--->",link[index])
						#fname.append(val)
						print("Fname-->",val)



			# for index,val in enumerate(file_name):
			# 	for row in db_search:
			# 		if val in row[-2]:
			# 			list_.append(link[index])
			# 			#print(link[index])
			# 			fname.append(val)

			return render_template('user2.html', db_search = enumerate(db_search),value=value,list_=list_,filename=file_name,name=session["name"].lower())
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
	flash("You have successfully Inserted The Details!",category="success")
	return redirect("/user")

@user.route('cart/<string:seller_email>/<string:item_name>/<string:image>')
def Cart(seller_email,item_name,image):
	try:

# 		INSERT INTO table_listnames (name, address, tele)
# SELECT * FROM (SELECT 'Rupert', 'Somewhere', '022') AS tmp
# WHERE NOT EXISTS (
#     SELECT name FROM table_listnames WHERE name = 'Rupert'
# ) LIMIT 1;

		if "name" in session:
			sql = """insert into cart(product_email,item_name,img,cart_holder) 
			select * from (SELECT %s,%s,%s,%s) as temp
			where not exists (
				select img,cart_holder from cart where img = %s and cart_holder = %s
			) limit 1;"""
			mycursor.execute(sql, (seller_email, item_name, image,session["email"],image,session["email"]))
			mydb.commit()
			flash("Insert into cart successfully done",category="success")
			return redirect('/')
		else:
			flash('Please Sign-in to Continue')
			return redirect('/login')
	except :
		#print("ERRORR")
		return redirect('/somethingwentwrong')

@user.route('cartD/<int:id>',methods=['POST'])
def CartD(id):
	try:
		sql = f"""delete from cart where item_id = {id}"""
		mycursor.execute(sql)
		mydb.commit()
		flash("DELETION successfully done",category="success")
		return redirect('/user/mycart')
	except:
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
	#description=request.form['description']
	#print(file)
	insert_success,image = insert_image(file)
	if not insert_success:
		flash('Allowed image types are -> png, jpg, jpeg, gif',category="danger")
		print(request.url)
		return render_template("sell.html")
	
	item_type = "sell"
	sql = "insert into items(email,item_name,price,item_type,img, sold) values(%s, %s, %s, %s, %s, %s);"
	val = (email,item_name,int(price),item_type,image,0)
	mycursor.execute(sql, val)
	mydb.commit()
	flash("You have successfully Inserted The Details!",category="success")
	return redirect("/user")

@user.route('/order/<string:seller_email>/<string:item_name>/<string:item_type>')
def ord(seller_email,item_name,item_type):
	if "name" in session:
		stat = order(seller_email,item_name,"item_type")
		if stat == 1:
			flash('Ordered! Please check your mail',category="success")
		return redirect('/')
	else:
		flash("Please Sign-in to Continue")
		return redirect("/login")



# @user.route('/product')
# def product():
# 	return render_template("product.html")

@user.route('product/<int:id>')
def product(id):
	# try:
		sql = """select * from items where item_id = %s;"""
		mycursor.execute(sql,(int(id),))
		db_search = mycursor.fetchone()
		print("PRODUCT--->",db_search)
		stock = {
		0 : "In stock",
		1 : "Sold"
		}
		img = ''
		link,file_name = path_finder()
		for i,file in enumerate(file_name):
			if file == db_search[-2]:
				img = link[i]
				break
		if "name" not in session:
			name = "LOGIN"
		else:
			name = session["name"]
		return render_template('product.html',database=db_search,stock=stock,img=img,name=name)
	# except Exception as e :
	# 	#print("ERRORR")
	# 	return redirect('/somethingwentwrong')



@user.route('/user3')
def user3():
	return render_template("user3.html")



@user.route('/main')
def trial():
	#print(os.getcwd())
	img_name = ['static/user_pg/image_dy/'+i for i in os.listdir(r"./user/static/user_pg/image_dy/")]
	#print(img_name)
	for i in range(len(img_name)):
		prices.append((i+1)*100)
		review.append((i+1))
	return render_template("user1.html",img_name=img_name,prices=prices,review=review,slider=img_name,history=img_name)

	
@user.route('/wishlist',methods=['POST'])
def liked():
	if "name" in session:
		sql = f""" select wishlist.product_email,wishlist.item_name,items.price,wishlist.cart_holder,wishlist.img,items.sold,items.item_id,wishlist.item_id from wishlist join items on wishlist.img = items.img and wishlist.cart_holder = '{session['email']}' order by wishlist.img;"""
		# sql = f""" select wishlist.product_email,wishlist.item_name,items.price,wishlist.cart_holder,wishlist.img,wishlist.item_id from wishlist join items on wishlist.img = items.img and wishlist.cart_holder = '{session['email']}' order by wishlist.img;"""
		mycursor.execute(sql)
		db_search = mycursor.fetchall()
		#print (db_search)
		value = {
				0:"IN STOCK",
				1:"OUT OF STOCK"
				}

		link,file_name = path_finder()
		list_ = []
		fname = []
		print("Loop begins")

		print(db_search)

		# DO NOT TOUCH
		link = sorted(link, key = lambda x: file_name[link.index(x)])
		file_name.sort()
		# DO NOT TOUCH
		total = 0
		for index,val in enumerate(file_name):
			for row in (db_search):
				if val in row[4]:
					list_.append(link[index])
					print("list--->",link[index])
					fname.append(val)
					print("Fname-->",val)
		print("Loop ends")

		return render_template('wishlist.html', db_search = enumerate(db_search),list_=list_,name=session["name"])
	else:
		flash("Please Sign-in to Continue",category="danger")
		return redirect('/login')


@user.route('wishlist/<string:seller_email>/<string:item_name>/<string:image>')
def wishlist(seller_email,item_name,image):
	try:

		sql = """insert into wishlist(product_email,item_name,img,cart_holder) 
		select * from (SELECT %s,%s,%s,%s) as temp
		where not exists (
		select img,cart_holder from wishlist where img = %s and cart_holder = %s
		) limit 1;"""
		mycursor.execute(sql, (seller_email, item_name, image,session["email"],image,session["email"]))
		mydb.commit()
		flash("Added to the wishlist",category="success")
		return redirect('/')
	except :
		#print("ERRORR")
		redirect('/somethingwentwrong')



@user.route('/myorders',methods=['GET','POST'])
def myorders():
	if "name" in session:

		sql = f""" select * from items where email = '{session['email']}' order by img;"""
		mycursor.execute(sql)
		db_search = mycursor.fetchall()
		#print (db_search)
		value = {
				0:"IN STOCK",
				1:"OUT OF STOCK"
				}

		link,file_name = path_finder()
		list_ = []
		fname = []
		print("Loop begins")

		print(db_search)

		# DO NOT TOUCH
		link = sorted(link, key = lambda x: file_name[link.index(x)])
		file_name.sort()
		# DO NOT TOUCH
		total = 0
		for index,val in enumerate(file_name):
			for row in (db_search):
				if val in row[-2]:
					list_.append(link[index])
					print("list--->",link[index])
					fname.append(val)
					print("Fname-->",val)
		print("Loop ends")
		for i in db_search:
			total += i[3]

		sql = f""" select count(*) from items where email='{session['email']}';"""
		mycursor.execute(sql)
		count = int(mycursor.fetchone()[0])
		return render_template('orderHistory.html', db_search = enumerate(db_search),list_=list_,file_name=file_name,total=total,count=count,name=session["name"],value=value)
			






		# return render_template('orderHistory.html',name=session["name"])
	else:
		flash("Please Sign-in to Continue",category="danger")
		return redirect('/login')
@user.route('/mycart',methods=['GET'])
def mycart():
	if "name" not in session:
		flash("Please Sign-in",category="danger")
		return redirect('/login')
	else:
		sql = f""" select cart.product_email,cart.item_name,items.price,cart.cart_holder,cart.img,items.sold,items.item_id,cart.item_id from cart join items on cart.img = items.img and cart.cart_holder = '{session['email']}' order by cart.img;"""
		mycursor.execute(sql)
		db_search = mycursor.fetchall()
		#print (db_search)
		value = {
				0:"IN STOCK",
				1:"OUT OF STOCK"
				}

		link,file_name = path_finder()
		list_ = []
		fname = []
		print("Loop begins")

		print(db_search)

		# DO NOT TOUCH
		link = sorted(link, key = lambda x: file_name[link.index(x)])
		file_name.sort()
		# DO NOT TOUCH
		total = 0
		for index,val in enumerate(file_name):
			for row in (db_search):
				if val in row[4]: #
					list_.append(link[index])
					print("list--->",link[index])
					fname.append(val)
					print("Fname-->",val)
		print("Loop ends")
		for i in db_search:
			total += i[2]

		sql = f""" select count(*) from cart join items on cart.img = items.img and cart.cart_holder = '{session['email']}' order by cart.img;"""
		mycursor.execute(sql)
		count = int(mycursor.fetchone()[0])
		return render_template('cart.html', value=value,db_search = enumerate(db_search),list_=list_,file_name=file_name,total=total,count=count,name=session["name"])
			

@user.route('/emptyCart',methods=['POST'])
def emptyCart():
	sql = f"""delete  from cart where cart_holder = '{session["email"]}';"""
	mycursor.execute(sql)
	mydb.commit()
	return redirect('/user/mycart')

@user.route('/checkout',methods=["POST"])
def checkout():
	sql = f""" select cart.product_email,cart.item_name,items.price,cart.cart_holder,cart.img,cart.item_id from cart join items on cart.img = items.img and cart.cart_holder = '{session['email']}' order by cart.img;"""
	mycursor.execute(sql)
	db_search = mycursor.fetchall()
	#0 seller 3 buyer
	print(db_search)
	seller,buyer = [],[]
	for row in db_search:
		
		order(row[0],row[1],"item_type")

	return redirect('/')

@user.route('removeItems/<int:id>',methods=["POST"])
def itemsD(id):
	try:
		sql = f"""delete from items where item_id = {id}"""
		mycursor.execute(sql)
		mydb.commit()
		flash("DELETION successfully done",category="info")
		return redirect('/user/myorders')
	except:
		redirect('/somethingwentwrong')

