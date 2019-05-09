import mysql.connector


class database:

    #initializes connection
    def Establish_Connection(self):

        self.__con = mysql.connector.connect (
            host= "localhost",
            user="root",
            passwd = "root",
            database = "SingleMind",
            auth_plugin = 'mysql_native_password'
            )

        self.__cur = self.__con.cursor()
        

    #grabs a user by UserID
    def Grab_User_Data(self,UserID):
        print("Grabs users info from "+UserID)

    def Grab_Event_Data(self,EventID):
        print("Grabs event info from " + EventID)

    def Grab_Most_Recent_Notifications(self):
        print("Grabs most recent notification info")
    #initialize DB
    def __init__(self):
        self.Establish_Connection()

    
