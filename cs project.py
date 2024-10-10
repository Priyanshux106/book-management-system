# Importing mysql connector module
import mysql.connector
# Making MySQL connection object
mycon = mysql.connector.connect(
	host='localhost3306', user='root',
	password='Ryuk@3102006',
	database='theatre')
# Making MySQL cursor object
mycur = mycon.cursor()
def space():  
    for i in range(1):
        print()

# To check if a customer of a given ID exists or not
def check():
	# Query to select all customer IDs
	# from the table
	qry = 'select cust_id from customer;'
	
	mycur.execute(qry)
	''' Return a list where each element
	in the list is a tuple
	fetched from each record in table
	Each tuple contains a single element
	as only customer IDs are fetched
	from cust_id column of each record'''

	d = mycur.fetchall()
	# To create a list of all customer IDs in the table
	list_of_ids = []
	for ids in d:
		# A list of all customer IDs in table
		list_of_ids.append(ids[0])
		
	return list_of_ids

# To create a new account for the customer
def cust_ac():
	ask = 'Y'
	list_of_ids = check()
	while ask in 'yY':
		custid = int(input('Enter your customer id... '))
		# to check if a customer already exists with this ID
		if custid in list_of_ids:
			print('This Customer Id already exists....\
Try creating a new one')
		else:
		# Tuple to contain details of the customer
			c_det = ()
			cnam = input('First Name : ')
			
			cphno = input('Phone Number : ')
			movie = input("enter movie")
			c_det = (custid, cnam, cphno, movie)
			
			''' Values inserted in the table and default NULL value are 
				provided for booked product at the time of creation 
				of customer account '''

			qry = 'insert into customer values(%s,%s,%s,%s,%s,NULL);'
			
			# value of the fields to be entered with the query
			val = c_det
			
			mycur.execute(qry, val)
			mycon.commit()
			print('Customer details entered')
			ask = input('Do you want to continue (Y/N) ')
			if ask not in ('Yy'):
				space()
				break
# To select all booked movie of
# a given customer from the table
def get_bkd_mov(cust_id):
	qry = 'select bkd_mov from customer\
where cust_id=%s;'
	mycur.execute(qry, (cust_id,))
	bm = mycur.fetchone()
	bkd_mov = bm[0]
	return bkd_mov
def sign_in():
	try:
		ask = int(input('Enter customer ID to sign in : '))
		# Using check function to check whether this account exists or not
		list_of_ids = check()
		if ask in list_of_ids:
			while True:
				print(''' Do you want to :																 
						1) View Bookings
						2) Book a movie
						3) Update Self Details
						4) Cancel booked movie 
							enter 'back' to exit ''')
				# Take choice of the customer
				ccc = input('enter choice - ')
				if ccc == '1':
					# Get booked movie function is used where cutomer ID
					# is passed as an argument

					s = get_bkd_mov(ask)
					# To check if the column has any value
					if s is None or s == ' ':
						print('you have not booked products yet')
					else:
						''' If more than one products are booked,
						their IDs are stored as a single value
						separated by '_' so we have to split the
						string to print each product ID.'''
						
						# d is a list containing movie names
						d = s.split('_')
						
						print('Booked movie')
						for bkdmovie in d:
							print(bkdmovie)

				if ccc == '2':

					# check if the product to be booked exists or not
					qry = 'select mov_name from movie;'
					mycur.execute(qry)
					mov_list = mycur.fetchall()
					''' contains a list where each element is a tuple fetched
					from each record, the tuple contains values in the
					column named mov_nam from movie table.'''

					# empty list to store product IDs
					list_of_movie = []
					for i in mov_list:
						list_of_movie.append(i[0])

					# Take ID and quantity of movies to be booked
					mov_name = input('Enter the movie name to book movie : ')
					# To add booked movie in the column,we first
					# need to check if it already contains a value in it
					if mov_name in list_of_movie:
						# Customer ID is given as value along with
						# query to fetch booked movie for the given ID
						qry = 'select bkd_mov from customer where cust_id=%s;'
						mycur.execute(qry, (ask,))
						pr = mycur.fetchone()
						# prl is value fetched from table
						prl = pr[0] 
						# When the column is empty the new movie is to stored
						if prl is None or prl == ' ':
							qry = 'update customer set bkd_mov=%s where cust_id=%s;'				
							val = (mov_name+'_', ask)
							mycur.execute(qry, val)
							mycon.commit()
							print('Your Movie is booked !!')
						else:
							prl1 = prl+mov_name
							qry2 = 'update customer set bkd_movie=%s where cust_id=%s;'
							# val2 is the new value containing all booked movies
							# to be stored in the column
							val2 = (prl1+'_', ask)
							mycur.execute(qry2, val2)
							mycon.commit()
							print('Your Movie is booked !!')
					else:
						 print('This movie is not available')

                if ccc == '3':

					qry = 'select cust_id,c_nam,c_phno,movie\
						from customer where cust_id =%s'
					mycur.execute(qry, (ask,))
					# clist contains list of all values fetched
					# in the form of a tuple for this customer ID
					clist = mycur.fetchone()
					# list of fields to be updated
					flds = ['Name', 'Ph.No', 'Movie']
					dic = {}
					print("Your existing record is :")
					# The fetched details are stored in the form of key
					# value pair in a dictionary
					for i in range(4):
						dic[flds[i]] = clist[i+1]
						print(i+1, ' ', flds[i], ' : ', clist[i+1])

               
					for i in range(len(clist)):
						updtc = int(input('enter choice to update '))
						upval = input('enter'+flds[updtc-1]+' ')
					# Change the value corresponding to the required field
						dic[flds[updtc-1]] = upval
						yn = input(
							'Do you want to update other details? y or n ')
						if yn in 'Nn':
							break
					qry = 'update customer set c_nam=%s,c_phno=%s,\
					c_movie=%s where cust_id=%s;'

					updtl = tuple(dic.values())+(ask,)
					# The value to be passed along with the query is a tuple
					# containing updated details of the given customer ID
					val = (updtl)
					mycur.execute(qry, val)
					mycon.commit()
					print('Your details are updated ')

			    if ccc == '4':

					try:
						# To get the existing bookings
						# Booked products in the table
						bkd_movie = get_bkd_mov(ask)
						print('Your Booking(s) : \n ', bkd_movie)
						if bkd_movie is None or bkd_movie == ' ':
							print('you have no bookings to cancel')
						else:
							cw = input("To cancel all bookingd; enter A \nOR \
enter the movie name to cancel : ")
							if cw in 'Aa':
								qry = 'update customer set bkd_movie=NULL\
								where cust_id=%s'

								mycur.execute(qry, (ask,))
								mycon.commit()
								print('All bookings deleted')
							elif cw in bkd_movie:
								# If more than one products entered,
								# split them on the basis of '_'
								# x is a list containing all booked movie
								x = (bkd_movie[0:-1]).split('_')
								
								# Delete the required movie name
								x.remove(cw)
								updt_mov = ''
								# Again concatenate each movie name
								# in the list to store in the table
								for item in x:
									updt_mov = updt_mov+item+'_'
								qry = 'update customer set bkd_movie=%s where cust_id=%s'
								val = (updt_mov, ask)
								mycur.execute(qry, val)
								mycon.commit()
								print('Booking Cancelled !')
					except Exception:
						print('Some problem in updating details.Try again')
					if ccc.lower() == 'back':
						print("Successfully logged out")
						space()
					 
					
				
					
		else:
			print('This Account does not exist. ')
	except Exception:
		print('Some error occurred. Try Again')

					
					
					   
# To fetch values from all columns of 
# movie table to get movie details
def view_movie():
	qry = 'select * from movie;'
	mycur.execute(qry)
	d = mycur.fetchall()
	# contains list of all records
	dic = {}
	# Each record fetched is separated into a key value pair
	# and stored in the dictionary where product ID is the key
	for i in d:
		dic[i[0]] = i[1:]
	print('_'*80)
# Printing the dictionary in the form of a table
	print("{:<17} {:<22} {:<23} {:<19}".format(
		'mov_name', 'mov_num', 'mov_price', 'mov_time'))
	print('_'*80)
	for k, v in dic.items():
		a, b, c = v
		print("{:<17} {:<22} {:<23} {:<19}".format(k, a, b, c))
	print('_'*80)

# To add a new movie in movie table
def addmov():
	# Display list of products
	view_movie() 
	n = int(input('Enter no of movie to insert '))
	for j in range(n):
		# Initialize tuple to store
		# product details.
		t = ()
		movnum = int(input("movie No. "))
		movname = input('movie number : ')
		movprice = int(input('Price : '))
		movtime = int(input('Stock : '))
		t = (movnum, movname, movprice, movtime)
		# Using MySql query
		qry = 'insert into movie values(%s,%s,%s,%s);'
		val = t
		mycur.execute(qry, val)
		mycon.commit()
		print("movie Added")

		# To remove a movie from the table
def delmov():
	view_movie()
	delt = input("Enter name of movie to be deleted")
	qry = 'delete from movie where mov_name=%s;'
	mycur.execute(qry, (delt,))
	mycon.commit()
	print("movie is removed")

print('WELCOME !')
# Running a infinite loop
while True:
	print('''Are you a :												 
(A). Customer
enter e to exit ''')
	ch = input('Enter - ')
	try:
		if ch in 'aA':
			print(" 1. Create Account\n 2.Sign In into existing account")
			choice = input('enter- ')
			if choice == '1':
				cust_ac()
			elif choice == '2':
				sign_in()
			else:
				print('no account found')
				print("Thankyou for visiting !")
		
			    
		break
	except Exception:
		print('Give the right input')
	space()


