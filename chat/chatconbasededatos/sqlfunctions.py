import mysql.connector

class Database:
    def __init__(self):
        pass
    @property
    def db_conn(self):
        self.mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="chatroom_q")
        return self.db
    @db_conn.setter
#log in
    @staticmethod
    def LogIn(username, password, db):
        try:
            db.cursor.execute("SELECT id FROM usuarios WHERE email = '"+ username +"'  AND pwd = '"+ password +"';")
            myresult = db.cursor.fetchall()
            print("Sesion iniciada")
            return myresult
        except: 
            print("Error de inicio de sesion")    
#sign in
    @staticmethod
    def SignIn(username, password, db):
        try:
            db.cursor.execute("SELECT email FROM usuarios WHERE email = '"+ username +"'")
            myresult = db.cursor.fetchall()
            if myresult != 0:
                try:
                    sql = "INSERT INTO usuarios (email, pwd) VALUES (%s, %s)"
                    val = (username, password)
                    db.cursor.execute(sql, val)
                    print("Usuario Creado")
                    try:
                        db.cursor.execute("SELECT id FROM usuarios WHERE email = '"+ username +"'")
                        myresult = db.cursor.fetchall()
                        print("Sesion iniciada")
                        return myresult    
                    except:
                        print("Error de base de datos - 3")
                except:
                    print("Error de base de datos - 2")
        except: 
            print("Error de base de datos - 1") 

#storemsg
    @staticmethod
    def StoreMsg():

        pass
#printmsgs
    @staticmethod
    def PrintMsg():
        pass


""" db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="chatroom_q")  
cursor = db.cursor()
cursor.execute("SELECT id FROM usuarios WHERE email = 'pepe'  AND pwd = '123';")
myresult = cursor.fetchall()"""
Database.db_conn.fget(Database).cursor().execute("SELECT id FROM usuarios WHERE email = 'pepe'  AND pwd = '123';")
print(Database.db_conn)
#Database.LogIn("pepe", "123", Database.cursor())