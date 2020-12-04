from flask import Blueprint, render_template, Flask, session

user = Blueprint("success",__name__,static_folder="static", template_folder="template")

@user.route('/')
def success():
	if "name" not in session:
		return "<h1><center>please login</center></h1>"
	
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
		sql = """insert into cart(product_email,item_name,img,cart_holder) values(%s,%s,%s,%s)"""
		mycursor.execute(sql, (seller_email, item_name, image,session["email"]))
		mydb.commit()
		flash("Insert into cart successfully done")
		return redirect('/')
	except :
		#print("ERRORR")
		redirect('/somethingwentwrong')

@user.route('cartD/<int:id>',methods=['POST'])
def CartD(id):
	try:
		sql = f"""delete from cart where item_id = {id}"""
		mycursor.execute(sql)
		mydb.commit()
		flash("DELETION successfully done")
		return redirect('/user/mycart')
	except :
		#print("ERRORR")
		redirect('/somethingwentwrong')

@user.route('/sell',methods=['POST'])
def sell():
	return render_template("sell.html")

@user.route('/sell1',methods=['POST'])
def sell1():
	email = session["name"] + "@gmail.com"
	item_name = request.form["item"]
	price = request.form["price"]
	description=request.form["description"]
	file = request.files['sellitem'] # name
	#print(file)
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
	#print(os.getcwd())
	img_name = ['static/user_pg/image_dy/'+i for i in os.listdir(r"./user/static/user_pg/image_dy/")]
	#print(img_name)
	for i in range(len(img_name)):
		prices.append((i+1)*100)
		review.append((i+1))
	return render_template("user1.html",img_name=img_name,prices=prices,review=review,slider=img_name,history=img_name)

	
@user.route('/wishlist',methods=['GET','POST'])
def wishlist():
	return render_template('wishlist.html',name=session["name"])


@user.route('/myorders',methods=['POST'])
def myorders():
	return render_template('orderHistory.html',title=session["name"])

@user.route('/mycart',methods=['POST'])
def mycart():
	sql = f""" select cart.product_email,cart.item_name,items.price,cart.cart_holder,cart.img,cart.item_id from cart join items on cart.img = items.img and cart.cart_holder = '{session['email']}' order by cart.img;"""
	mycursor.execute(sql)
	db_search = mycursor.fetchall()
	#print (db_search)
	value = {
			0:"IN STOCK",
			1:"NOT IN STOCK"
			}

			# ()
			# ()
			# [hello,hi,bye]
			# index,val
# 6,7,1,8 --->file_name
# 1,6,7,8 ---->val
	link,file_name = path_finder()
	list_ = []
	fname = []
	print("Loop begins")

	print(db_search)
	#(db_search.sort(key=lambda x:x[-1]))
	#print(db_search)
	#file_name
	# list1, list2 = zip(*sorted(zip(file_name,link)))
	# print("List1 starts")
	# print(list1)
	# print(list2)
	# print("List2 end")

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
		total += i[2]

	sql = f""" select count(*) from cart where cart_holder='{session['email']}';"""
	mycursor.execute(sql)
	count = int(mycursor.fetchone()[0])
	return render_template('cart.html', db_search = enumerate(db_search),list_=list_,file_name=file_name,total=total,count=count)
		
	#return render_template('cart.html')

@user.route('/emptyCart',methods=['POST'])
def emptyCart():
	sql = """truncate cart;"""
	mycursor.execute(sql)
	mydb.commit()
	return redirect('/user/mycart')

