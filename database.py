import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="miniamazon"
)
mycursor = mydb.cursor()


#mycursor.execute("create table customers(name varchar(30), address varchar(50))")

#sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
#val = [("trial", "village"),
#		("trial2", "village2")]
#mycursor.executemany(sql, val)

#mydb.commit()



#print(mycursor.rowcount, "was inserted.")
#print("1 record inserted, ID:", mycursor.lastrowid)

# mycursor.execute("select * from customers")
# allData = (mycursor.fetchall())
# for c in allData:
	# print(c)
	
	
# mycursor.execute("describe customers")

# print(mycursor.fetchall()) #returns tuple of 6 values


# mycursor.execute("delete from customers")

# mydb.commit()

# mycursor.execute("select * from customers")

# print(mycursor.fetchall())











