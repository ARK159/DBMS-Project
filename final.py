from flask import Flask,redirect,url_for,render_template,request
import mysql.connector
from mysql.connector import Error
import pandas as pd
import matplotlib.pyplot as plt
import uuid,sys
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
        


def execute_query(connection, query):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
    return cursor


connection=create_server_connection('localhost','root','')
query="drop database NEUER"
execute_query(connection,query)
create_database(connection,"Create Database NEUER")
connection=create_db_connection('localhost','root','','NEUER')


query="""Create Table Cart(
  Cart_id varchar(12) not null,
  primary key(Cart_id)
  )
"""
execute_query(connection,query)

query = """CREATE TABLE User(
    User_Name varchar(11) NOT NULL,
    User_Password varchar(13) NOT NULL,
    PRIMARY KEY (User_Name)   
);"""

execute_query(connection, query)


query="""CREATE TABLE Customer (
    Customer_id VARCHAR(6) NOT NULL,
    Name VARCHAR(20) NOT NULL,
    Address VARCHAR(20) NOT NULL,
    Pincode INT(6) NOT NULL,
    Phone_int_s BIGINT(20) NOT NULL,
    Email_address varchar(30) not null,
    PRIMARY KEY (Customer_id),
    Cart_id VARCHAR(7) NOT NULL,
    User_Name varchar(11) NOT NULL,
    FOREIGN KEY (Cart_id) REFERENCES Cart (Cart_id),
    FOREIGN KEY (User_Name) REFERENCES User (User_Name)
);"""
execute_query(connection,query)


query="""CREATE TABLE Seller
    (
        Seller_id VARCHAR(6) NOT NULL,
        s_pass VARCHAR(10) NOT NULL,
        Name VARCHAR(20) NOT NULL,
        Address VARCHAR(10) NOT NULL,
        PRIMARY KEY (Seller_id)
    );"""
execute_query(connection,query)

query="""CREATE TABLE Seller_Phone_num
    (
        Phone_num BIGINT(10) NOT NULL,
        Seller_id VARCHAR(6) NOT NULL,
        PRIMARY KEY (Phone_num, Seller_id),
        FOREIGN KEY (Seller_id) REFERENCES Seller(Seller_id)
        ON DELETE CASCADE
    );"""
execute_query(connection,query)

query="""CREATE TABLE Payment
    (
        payment_id VARCHAR(7) NOT NULL,
        payment_date DATE NOT NULL,
        Payment_type VARCHAR(10) NOT NULL,
        Customer_id VARCHAR(6) NOT NULL,
        Cart_id VARCHAR(7) NOT NULL,
        PRIMARY KEY (payment_id),
        FOREIGN KEY (Customer_id) REFERENCES Customer(Customer_id),
        FOREIGN KEY (Cart_id) REFERENCES Cart(Cart_id),
        total_amount numeric(6)
    );"""
execute_query(connection,query)

query="""CREATE TABLE Transaction (
    payment_id VARCHAR(7) NOT NULL,
    Customer_id VARCHAR(6) NOT NULL,
    CardHolder_name VARCHAR(11) NOT NULL,
    Card_Number BIGINT(16) NOT NULL,
    Expiration_date DATE NOT NULL,
    CVV INT(3) NOT NULL,
    Country VARCHAR(13) NOT NULL,
    PRIMARY KEY (payment_id), 
    FOREIGN KEY (Customer_id) REFERENCES Customer (Customer_id),
    FOREIGN KEY (payment_id) REFERENCES Payment (payment_id)
);
"""
cursor=execute_query(connection,query)

query="""CREATE TABLE Product
    (
        Product_id VARCHAR(7) NOT NULL,
        Type VARCHAR(7) NOT NULL,
        Color VARCHAR(15),
        P_Size VARCHAR(2),
        Gender CHAR(5) ,
        Cost INT(5) NOT NULL,
        Quantity INT(2) NOT NULL,
        Seller_id VARCHAR(6),
        PRIMARY KEY (Product_id),
        FOREIGN KEY (Seller_id) REFERENCES Seller(Seller_id)
    );
"""
execute_query(connection,query)


query="""CREATE TABLE Cart_item
    (
        Quantity_wished INT(1) check (Quantity_wished <> 0),
        Date_Added DATE NOT NULL,
        Cart_id VARCHAR(7) NOT NULL,
        Product_id VARCHAR(7) NOT NULL,
        purchased varchar(3) default 'NO',
        FOREIGN KEY (Cart_id) REFERENCES Cart(Cart_id),
        FOREIGN KEY (Product_id) REFERENCES Product(Product_id),
        Primary key(Cart_id,Product_id)
    );"""
execute_query(connection,query)

query="""
CREATE FUNCTION total_cost(cId VARCHAR(10))
RETURNS INT
BEGIN
    DECLARE total INT DEFAULT 0;
    
    SELECT SUM(cost) INTO total
    FROM Product
    JOIN cart_item ON Product.Product_id = Cart_item.Product_id
    WHERE Cart_item.Cart_id = cId;
    
    RETURN total;
END 
"""
cursor=execute_query(connection,query)
query="""
CREATE OR REPLACE TRIGGER before_pay_up
BEFORE INSERT ON Payment
FOR EACH ROW
BEGIN
    SET new.total_amount= total_cost(new.Cart_id);
END;
"""
cursor=execute_query(connection,query)


cursor=execute_query(connection,query)

query="""
CREATE OR REPLACE FUNCTION numCartId(cd VARCHAR(10))
    RETURNS INT
BEGIN
    DECLARE total INT DEFAULT 0;
    
    SELECT COUNT(*) INTO total
    FROM Cart_item
    WHERE Cart_id = cd;
    
    RETURN total;
END 
"""
cursor=execute_query(connection,query)

query="""
CREATE TRIGGER before_customer
BEFORE INSERT
ON Customer
FOR EACH ROW
BEGIN
    DECLARE c VARCHAR(10);
    DECLARE n INT;
    
    SET c = NEW.Cart_id;
    SET n = numCartId(c);
    
    IF n > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Sorry';
    END IF;
    
    INSERT INTO Cart VALUES (c);
END
"""
cursor=execute_query(connection,query)


cursor=connection.cursor()
query="insert into User values('admin','pass')"
cursor.execute(query)
query="select * from User "
cursor=execute_query(connection,query)
result=cursor.fetchall()

if __name__=='__main__':
    app.run(debug=True)