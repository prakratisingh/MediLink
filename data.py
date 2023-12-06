# importing the connector for setting up connection with mysql
import mysql.connector
class DataBase:
    
    # constructor of DataBase class
    def __init__(self):
        # setting up the connection
        self.conn = mysql.connector.connect(host='localhost',password='admin',user='root')
        if self.conn.is_connected():
            print("Connection is established...!")
        else:
            print("Connection is not established")
        
        # getting the cursor from the connection object
        self.cur = self.conn.cursor()

        # creating the database named 'majorproject' if it do not exist
        self.cur.execute("CREATE DATABASE IF NOT EXISTS majorproject;")
        
        self.cur.execute("USE majorproject;")
        # creating the table userdata
        # three columns: email, pass and hash
        self.cur.execute("CREATE TABLE IF NOT EXISTS userdata (email varchar(255) PRIMARY KEY, pass VARCHAR(16),hash CHAR(64));")

    # function to check whether the email is already present in database or not
    def isExistingUser(self,email):
        # query to fetch the result if that user exists in the table
        checkQuery = "SELECT * FROM userdata WHERE email = %s"
        self.cur.execute(checkQuery, (email,))
        existing_user = self.cur.fetchone()
        # if exists then true
        if existing_user :
            return True
        return False

    # function to insert a new record to the table
    def insertUser(self,email,password,hash):
        if self.isExistingUser(email):
            return False
        else:
            # Inserting new user into the table
            insert_query = "INSERT INTO userdata (email, pass,hash) VALUES (%s, %s,%s)"
            self.cur.execute(insert_query, (email, password,hash))
            self.conn.commit()
            return True

    # function to authenticate user
    def authenticateUser(self,email, password):
        # matching the user's credentials in the table
        query = "SELECT * FROM userdata WHERE email = %s AND pass = %s"
        self.cur.execute(query, (email, password))
        user = self.cur.fetchone()
        if user:
            return True
        return False
    
    # function to update the hash value in the table userdata
    def updateHash(self,email,hash):
        query = "UPDATE userdata SET hash = %s WHERE email = %s"
        self.cur.execute(query,(hash,email))
        self.conn.commit()
    
    # function to get the last hash present against that user 
    def last_hash(self,username):
        query = "SELECT hash from userdata where email = %s"
        self.cur.execute(query,(username,))
        result = self.cur.fetchall()
        res = ""
        for r in result:
            res = r
        return res[0]