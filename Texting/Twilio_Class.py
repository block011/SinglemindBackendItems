#twilio class
from DB_Class import *
from twilio.rest import Client


class Twilio:




    def Send_Text(self, EventName, EventDesc, PhoneNumber):
        account_sid = ""
        auth_token = ""
        client = Client(account_sid, auth_token)

        message = client.messages.create(
                body= "Your event is soon!" + EventName + ":" + EventDesc,
                from_='+19514827423',
                to=PhoneNumber
                )

    def Schedule(self):
        result = self.__DB.Grab_Most_Recent_Notifications()
        if result is None:
            return;
        for notify in result:
            eventdata = self.__DB.Grab_Event_Data(notify[1])
            self.Send_Text(eventdata[0], eventdata[1], self.__DB.Grab_User_PhoneNumber(notify[0])) 
        return; 



    def __init__(self):
        self.__DB = database()
