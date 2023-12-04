import mysql.connector
class DataBase:
    def __init__(self):
        self.conn = mysql.connector.connect(host='localhost',password='',user='root')
        if self.conn.is_connected():
            print("Connection is established...!")
        else:
            print("Connection is not established")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE DATABASE IF NOT EXISTS majorproject;")
        self.cur.execute("USE majorproject;")
        self.cur.execute("CREATE TABLE IF NOT EXISTS userdata (email varchar(255) PRIMARY KEY, pass VARCHAR(16),hash CHAR(64));")

    def isExistingUser(self,email):
        checkQuery = "SELECT * FROM userdata WHERE email = %s"
        self.cur.execute(checkQuery, (email,))
        existing_user = self.cur.fetchone()
        if existing_user :
            return True
        return False

    def insertUser(self,email,password,hash):
        if self.isExistingUser(email):
            return False
        else:
            # Insert new user into the database
            insert_query = "INSERT INTO userdata (email, pass,hash) VALUES (%s, %s,%s)"
            self.cur.execute(insert_query, (email, password,hash))
            self.conn.commit()
            return True

    def authenticateUser(self,email, password):
        # Check if user exists and credentials match
        query = "SELECT * FROM userdata WHERE email = %s AND pass = %s"
        self.cur.execute(query, (email, password))
        user = self.cur.fetchone()
        if user:
            return True
        return False
    
    def updateHash(self,email,hash):
        query = "UPDATE userdata SET hash = %s WHERE email = %s"
        self.cur.execute(query,(hash,email))
        self.conn.commit()
    
    def last_hash(self,username):
        query = "SELECT hash from userdata where email = %s"
        self.cur.execute(query,(username,))
        result = self.cur.fetchall()
        res = ""
        for r in result:
            res = r
        return res[0]
