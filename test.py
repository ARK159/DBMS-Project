from flask import Flask,redirect,url_for,render_template,request
import mysql.connector
from mysql.connector import Error
import pandas as pd
import matplotlib.pyplot as plt
import uuid,sys,datetime

app=Flask(__name__)


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_database(connection, query):
    cursor = connection.cursor(buffered=True)
    
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")
        


def execute_query(connection, query,list=None):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query,list)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
    return cursor



connection=create_server_connection('localhost','root','')
# query="drop database NEUER"
# execute_query(connection,query)
# create_database(connection,"Create Database NEUER")
connection=create_db_connection('localhost','root','','NEUER')


@app.route('/')
def welcome():
    return render_template('login.html')

@app.route('/home/<username>')
def home(username):
    return render_template('homepage.html',username=username)

@app.route('/products/<username>')
def products(username):
    return render_template('products.html',username=username)

@app.route('/payment/<username>')
def payment(username):
    return render_template('payment.html',username=username)


@app.route('/categories/<username>' ,methods=['GET'])
def categories(username):

        if request.method=='GET':
            category=request.args .get('category')
            print(category)

            if category=='groceries':
                query="select Product_id,Type,Color,P_Size,Gender,Cost,Quantity,Product.Seller_id,Image,Product.Name from Seller,Product where Type='Grocery' and Product.Seller_id=Seller.Seller_id and Product.Quantity>0"
                cursor=execute_query(connection,query)
                result=cursor.fetchall()
                columns=list(cursor.column_names)
                query=""" 
                        SELECT Seller.Name,Address from Seller inner join Product on Product.Seller_id=Seller.Seller_id and Type='Grocery'
                  """
                cursor=execute_query(connection,query)
                result1=cursor.fetchall()
                # result1=[row[1:] for row in result1]
                columns1=cursor.column_names
                print(columns)
                # print(result1,"hello")
                return render_template('groceries.html',username=username,product=result,columns=columns,result1=result1,columns1=list(columns1))

            elif(category=='fashion'):
                category=request.args .get('category')
                print(category)

                if category=='fashion':
                    query="select Product_id,Type,Color,P_Size,Gender,Cost,Quantity,Product.Seller_id,Image,Product.Name from Seller,Product where Type='Fashion' and Product.Seller_id=Seller.Seller_id and Product.Quantity>0"
                    cursor=execute_query(connection,query)
                    result=cursor.fetchall()
                    columns=list(cursor.column_names)
                    query=""" 
                            SELECT Seller.Name,Address from Seller inner join Product on Seller.Seller_id=Product.Seller_id and Type='Fashion'
                    """
                    cursor=execute_query(connection,query)
                    result1=cursor.fetchall()
                    # result1=[row[1:] for row in result1]
                    columns1=cursor.column_names
                    # print(result1,"hello")
                    return render_template('fashion.html',username=username,product=result,columns=columns,result1=result1,columns1=list(columns1))
            elif category=='electronics':
                category=request.args .get('category')
                print(category)

                if category=='electronics':
                    query="select Product_id,Type,Color,P_Size,Gender,Cost,Quantity,Product.Seller_id,Image,Product.Name from Seller,Product where Type='Electronics' and Product.Seller_id=Seller.Seller_id and Product.Quantity>0"
                    cursor=execute_query(connection,query)
                    result=cursor.fetchall()
                    columns=list(cursor.column_names)
                    query=""" 
                            SELECT Seller.Name,Address from Seller inner join Product on Seller.Seller_id=Product.Seller_id and Type='Electronics'
                    """
                    cursor=execute_query(connection,query)
                    result1=cursor.fetchall()
                    # result1=[row[1:] for row in result1]
                    columns1=cursor.column_names
                    # print(result1,"hello")
                    return render_template('electronics.html',username=username,product=result,columns=columns,result1=result1,columns1=list(columns1))
            else:
                category=request.args .get('category')
                print(category)

                if category=='sports':
                    query="select Product_id,Type,Color,P_Size,Gender,Cost,Quantity,Product.Seller_id,Image,Product.Name from Seller,Product where Type='Sports' and Product.Seller_id=Seller.Seller_id and Product.Quantity>0"
                    cursor=execute_query(connection,query)
                    result=cursor.fetchall()
                    columns=list(cursor.column_names)
                    query=""" 
                            SELECT Seller.Name,Address from Seller inner join Product on Seller.Seller_id=Product.Seller_id and Type='Sports'
                    """
                    cursor=execute_query(connection,query)
                    result1=cursor.fetchall()
                    columns1=cursor.column_names
                    # print(result1,"hello")
                    return render_template('sports.html',username=username,product=result,columns=columns,result1=result1,columns1=list(columns1))
       

@app.route('/cart/<username>/<product_id>' ,methods=['GET','POST'])
def cart (username,product_id):
    if request.method=='POST':
        try:
            quantity=request.form['quantity']
            # print(type(product_id))
            query="select Quantity from Product where Product_id=(%s) and Quantity  >= (%s)"
            cursor=execute_query(connection,query,list=(product_id,quantity))
            result=cursor.fetchall()
            if len(result):
                query="select Cart_id from Customer where User_Name=(%s)"
                print(username)
                cursor=execute_query(connection,query,(username,))
                cart_id=cursor.fetchall()
                query="Select count(*) from Cart_item where Cart_id=(%s) and Product_id=(%s)"
                cursor=execute_query(connection,query,(str(cart_id[0][0]),product_id))
                count=cursor.fetchall()
                count=count[0][0]
                if(count):
                    return "PRODUCT ALREADY IN CART"
                else:
                    query="Insert into Cart_item values (%s,%s,%s,%s,%s)"
                    cursor=execute_query(connection,query,(quantity,datetime.date.today(),str(cart_id[0][0]),product_id,'NO'))
                    query="Update  Product set Quantity=Quantity-(%s) where Product_id=(%s)"
                    cursor=execute_query(connection,query,(quantity,product_id))
                    return "PRODUCT ADDED TO CART"
                # query="select * from Product where Product_id in (select Product.Product_id from Product inner join Cart_item on Product.Product_id=Cart_item.Product_id)"
                # cursor=execute_query(connection,query)
                # result=cursor.fetchall()
                # print(result)
                # columns=list(cursor.column_names)
               
                # return render_template('cart.html',username=username,quantity=int(quantity),product=result,columns=columns)
                 
            else:
                return f"Sorry,Not enough Items,{username}"
        except Exception as e:
            print("Error:",e)
            sys.exit()  
    return "Hello"




@app.route('/carti/<username>')
def carti(username):
    total=0
    print(username)
    query="Select Cart_id from Customer,User where Customer.User_Name=(%s) and User.User_Name=(%s)"
    cursor=execute_query(connection,query,(username,username))
    cart_id=(cursor.fetchall())[0][0]
    query="select * from Product where Product_id in (select Product.Product_id from Product inner join Cart_item on Product.Product_id=Cart_item.Product_id and Cart_item.Cart_id=(%s) and purchased='NO')"
    cursor=execute_query(connection,query,(cart_id,))
    result=cursor.fetchall()
    columns=list(cursor.column_names)
    query="Select Quantity_wished from Cart_item where Cart_id=(%s)"
    cursor=execute_query(connection,query,(cart_id,))
    quantity=cursor.fetchall()
    quantity=[ x[0] for x in quantity]
    
    for i in range(len(result)):
        total+=result[i][5]*quantity[i]
    return render_template('cart.html',username=username,quantity=quantity,product=result,columns=columns,total=total)

@app.route('/check/<username>')
def check(username):
    return username
@app.route('/transaction/<username>',methods=['GET','POST'])
def transaction(username):
    if request.method=='GET':
        try:
            query="Select Cart_id from Customer,User where Customer.User_Name=(%s) and User.User_Name=(%s)"
            cursor=execute_query(connection,query,(username,username))
            cart_id=(cursor.fetchall())[0][0]
            query="Select Customer_id from Customer,User where Customer.User_Name=User.User_Name"
            cursor=execute_query(connection,query)
            customer_id=(cursor.fetchall())[0][0]

            name=request.args.get('name')
            number=request.args.get('number')
            cvv=request.args.get('cvv')
            expiry=request.args.get('expiration')
            country=request.args.get('country')

            query="select Balance from Card where Name=(%s) and Number=(%s) and CVV=(%s) and Expiry_date=(%s) and Country=(%s)"
            cursor=execute_query(connection,query,(name,number,cvv,expiry,country))
            money=(cursor.fetchall())
            if(len(money)):
                money=float(money[0][0])
                print(name,number,cvv,expiry,country)
                query="select sum(Quantity_wished*Cost)as Total from Product,Cart_item where Product.Product_id=Cart_item.Product_id and Cart_id=(%s)"
                cursor=execute_query(connection,query,(cart_id,))
                total=cursor.fetchall()[0][0]
                print((money),(total))
                print(total)
                if money<total:
                    return "Card Declined.Try again"
                else:
                    payment_id='#'+str(uuid.uuid4())[0:5]
                    payment_date=datetime.date.today()
                    query="Insert into Payment (payment_id,payment_date,Customer_id,Cart_id) values(%s,%s,%s,%s)"
                    cursor=execute_query(connection,query,(payment_id,payment_date,customer_id,cart_id))
                    query="update Cart_item SET purchased='YES' where Cart_id=(%s)"
                    print(cart_id)
                    cursor=execute_query(connection,query,(cart_id,))
                    query="delete from Cart_item where Cart_id=(%s)"
                    cursor=execute_query(connection,query,(cart_id,))
                    query="insert into Transaction values (%s,%s,%s,%s,%s,%s,%s)"
                    cursor=execute_query(connection,query,(payment_id,customer_id,name,number,expiry,cvv,country))
                    query="update Card set Balance=Balance-(%s) where Number=(%s)"
                    cursor=execute_query(connection,query,(total,number))
                    return "Payment successfull"
            else:
                return "Invalid Card"
            
        except Error as e:
            print("Error: ",e)
            sys.exit()
    return "bye"
    

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        username=request.form['username']
        name=request.form['name']
        address=request.form['address']
        pincode=request.form['pincode']
        phone=request.form['phone']
        email=request.form['email']
        query = f"SELECT * FROM User WHERE User_Name = '{username}';"
        cursor = execute_query(connection, query)
        result=cursor.fetchall()
        if(len(result)):
            return render_template('register.html')
        else:
            try:
                user_Password=request.form['user_password']
                query = f"INSERT INTO User VALUES ('{username}','{user_Password}');"
                cursor = execute_query(connection, query)
                cid='#'+str(uuid.uuid4())[:5]
                caid='#'+str(uuid.uuid4())[:5]
                query=f"INSERT INTO Customer VALUES ('{cid}','{name}','{address}',{pincode},{phone},'{email}','{caid}','{username}');"
                cursor=execute_query(connection,query)
            except Exception as e:
                print(e)
                query="rollback"
                cursor=execute_query(connection,query)
                sys.exit()
            return redirect(url_for('home',username=username))    



@app.route('/user', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_Password = request.form['user_password']
        print(user_Password," ",user_id)
        query = f"SELECT * FROM User WHERE User_Name = '{user_id}' and User_Password='{user_Password}';"
        cursor = execute_query(connection, query)
        
        result = cursor.fetchall()
        if(len(result)<=0):
            return render_template('register.html')
        else:
            return redirect(url_for('home',username=user_id))

    return render_template('login.html')


if __name__=='__main__':
    app.run(debug=True)





