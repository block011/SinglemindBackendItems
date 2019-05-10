#twilio class
from DB_Class import *
from twilio.rest import Client


class Twilio:




    def Send_Text(self, EventName, EventDesc, PhoneNumber):
        account_sid = "ACf4a101bd3abc4f0793033e4b64e19ed9"
        auth_token = "7796ab060c5c53cadc893ec7aa00cf2e"
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
            print("test")
        return; 



    def __init__(self):
        __DB = database()
