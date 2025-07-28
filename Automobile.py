import mysql.connector as con
import random
from datetime import datetime
def setup_connection():
	try:
		connect=con.connect(host='localhost',user='root',password='Ashaz@321')
		return connect
	except con.Error as e:
		print('connection error:',e)


def setup_database(connect,cursor):
    cursor.execute('create database if not exists automobile')
    cursor.execute('use automobile')
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            id  char(3) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            category ENUM('Car', 'Bike') NOT NULL,
            brand VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            stock INT NOT NULL
        )
    """)

def product_entry(connect,cursor):
	id=input('Product ID:')
	name=input('Product name:')
	category=input('Product category:')
	brand=input('Product brand:')
	price=float(input('Product price:'))
	stock=input('Product stock:')
	cursor.execute('insert into product values (%s,%s,%s,%s,%s,%s)',(id,name,category,brand,price,stock)),
	connect.commit()
	print('Product added successfully')

def product_deletion(connect,cursor):
	id=input('Enter product ID to Delete:')
	cursor.execute('select * from product where id=%s',(id,))
	data=cursor.fetchone()
	if not data:
		print('No Id found:')
		
	else:
		cursor.execute('delete from product where id=%s',(id,))
		connect.commit()
		print('Product deleted successfully')


def product_updation(connect,cursor):
	id=input('Enter product id to update:')
	cursor.execute('select * from product where id=%s',(id,))
	data=cursor.fetchone()
	
	if not data:
		print('No Id found')

	else:
		print('1. Update price')
		print('2. Update stock')
		print('3. Upadate name')
		print('4. Update brand')
		ch=int(input('Enter your choice'))
		
		if ch == 1:
			price=float(input('Enter updated price:'))
			cursor.execute('update product set price =%s where id=%s',(price,id))
			connect.commit()
			print('Price updated Successfully')
		elif ch == 2:
			stock=float(input('Enter updated stock:'))
			cursor.execute('update product set stock =%s where id=%s',(stock,id))
			connect.commit()
			print('Stock updated Successfully')

		elif ch == 3:
			name=input('Enter updated name:')
			cursor.execute('update product set name=%s where id=%s',(name,id))
			connect.commit()
			print('Name updated successfully')

		elif ch == 4:
			brand=input('Enter the brand')
			cursor.execute('update product set brand=%s where id=%s',(brand,id))
			connect.commit()
			print('Brand updated successfully')
			
		else:
			print('Invalid choice:')


def search_record(connect,cursor):
	
	id=int(input('Enter Id to search record:'))
	cursor.execute('select * from product where id=%s',(id,))
	records=cursor.fetchone()
	heading=[desc[0] for desc in cursor.description]
	if not records:
		print('No rocord Exist with this Id')
	else:
		print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<11}'.format(*heading))
		print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<11}'.format(*records))


def product_details(connect,cursor):
	cursor.execute('select * from product')
	records=cursor.fetchall()
	heading=[desc[0] for desc in cursor.description]
	if not records:
		print('No records Exists')
	else:
		print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<11}'.format(*heading))
		for record in records:
			print('{:<10} {:<15} {:<15} {:<15} {:<15} {:<11}'.format(*record))

def generate_bill(connect,cursor):
	print("Enter product Ids and quantity (type 'done' to  finish):")
	cart=[]
	while True:
		p_id=input('Enter product Id')
		if p_id.lower() == 'done':
			break
			
		quantity=int(input('Enter quantity:'))
		cart.append((int(p_id), quantity))
					 
	total=0
	count=0
	bill_details=[]
	for p_id,quantity in cart:
		cursor.execute('select name,price,stock  from product where id=%s',(p_id,))
		product=cursor.fetchone()
		if product:
			name,price,stock=product
			if stock >= quantity:
				amount = price*quantity
				total += amount
				count += 1
				bill_details.append((count,name,price,quantity,amount))
				cursor.execute('Update product set stock= stock - %s where id=%s',(quantity,p_id))
			else:
				print(f'Insufficient stock {name}. available: {stock}')
			
		else:
			print(f'Product{p_id}. not found')
			
	connect.commit()
	print('\n'*5)
	print(f'{'':<25}\033[1mSHAKIB AUTOMOBILE\033[0m')
	print(f'bill no {random.randint(1000,2000)}{'':<40}date:{datetime.now().strftime('%d-%m-%y')}')
	print('-'*70)
	print(f'\033[1m{'sr.no':<7} {'name':<15}{'price':<15}{'quantity':<15}{'amount':<15}\033[0m')
	print('-'*70)
	for count,name,price,quantity,amount in bill_details:
		print(f'{count:<7}{name:<16}{price:<16}{quantity:<16}{amount:.2f}')
	print('-'*70)		
	gst=float(total)*5.5/100
	grand_total=gst+float(total)
	print(f'{'':<40} sub_total ={'':<2}{float(total):.2f}')
	print(f'{'':<40} gst(5.5%) ={'':<2}{gst:.2f}')
	print(f'{'':<40} grand_total ={'':<2}{grand_total:.2f}')
	print('\n'*5)
