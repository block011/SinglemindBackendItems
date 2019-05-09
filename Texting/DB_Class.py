import mysql.connector


class database:

    def Establish_Connection(self):

        self.__con = mysql.connector.connect (
            host= "localhost",
            user="root",
            passwd = "root",
            database = "SingleMind",
            auth_plugin = 'mysql_native_password'
            )



    def __init__(self):
        Establish_Connection()

