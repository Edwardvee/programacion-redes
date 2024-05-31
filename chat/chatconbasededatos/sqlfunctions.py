import mysql.connector



class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="chatroom_q")
        self.cursor = self.db.cursor()
    db =  mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="chatroom_q")
    cursor = db.cursor()
#get user 
    @staticmethod
    def GetUser(uid, cursor):
        try:
            sql = "SELECT id, email FROM usuarios WHERE email = %s;"
            val = (uid)
            cursor.execute(sql, val)
            myresult = cursor.fetchall()
            if myresult != []:
                print("Se obtuvo " + myresult)
                return myresult
            else:
                return -1
        except: 
            print("Error")   
#log in
    @staticmethod
    def LogIn(username, password, cursor):
        try:
            sql = "SELECT email FROM usuarios WHERE email = %s AND pwd = %s;"
            val = (username,password)
            cursor.execute(sql, val)
            myresult = cursor.fetchall()
            if myresult != []:
                print(myresult)
                print("Sesion iniciada")
                return myresult
            else:
                print("No se ha encontrado usuario")
                return -1
        except: 
            print("Error de inicio de sesion")  
#sign in
    @staticmethod
    def SignIn(username, password, cursor, db):
        try:
            myresult = Database.GetUser(username, Database.cursor)
            if myresult == []:
                try:
                    sql = "INSERT INTO usuarios (email, pwd) VALUES (%s, %s)"
                    val = (username, password)
                    cursor.execute(sql, val)
                    db.commit()
                    print("Usuario Creado")
                    try:
                        myresult = Database.LogIn(username, password, Database.cursor)
                        return myresult 
                    except:
                        print("Error de base de datos - 3")
                        return -1
                except:
                    print("Error de base de datos - 2")
                    return -1
        except: 
            print("Error nombre de usuario ya elegido") 
            return -1

#storemsg
    @staticmethod
    def StoreMsg():  
        pass
#printmsgs
    @staticmethod
    def PrintMsg():
        pass

#print(Database.GetUser("pepe", Database.cursor))
#print(Database.SignIn("pepe553355","123", Database.cursor, Database.db))
#Database.db_conn.fget(Database).cursor().execute("SELECT id FROM usuarios WHERE email = 'pepe'  AND pwd = '123';")
#print(Database.db_conn)
#print(Database.LogIn("pep54354354e", "1345323", Database.cursor))

