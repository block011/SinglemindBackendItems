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
    def Grab_User_PhoneNumber(self,UserID):
        query = "SELECT PhoneNumber FROM User_Table WHERE UserID = " + str(UserID)
        self.__cur.execute(query)
        result = self.__cur.fetchone()
        return(result[0])

    #grabs an event by EventID
    def Grab_Event_Data(self,EventID):
        query = "SELECT EventName, EventDesc FROM Event_Table WHERE EventID = " + str(EventID)
        self.__cur.execute(query)
        result = self.__cur.fetchone()
        return(result)

    #grabs most recent notifications
    def Grab_Most_Recent_Notifications(self):
        query = "SELECT UserID, EventID FROM Notification_Table WHERE HasNotified = 0 AND NotifyTime <= DATE_ADD(NOW(), INTERVAL 1 HOUR)"
        self.__cur.execute(query)
        result = self.__cur.fetchall()
        query = "DELETE FROM Notification_Table WHERE HasNotified = 0 AND NotifyTime <= DATE_ADD(NOW(), INTERVAL 1 HOUR)"
        self.__cur.execute(query)
        self.__con.commit()
        return result

    #initialize DB
    def __init__(self):
        self.Establish_Connection()
    
