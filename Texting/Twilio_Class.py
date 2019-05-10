#twilio class
from DB_Class import *
from twilio.rest import Client


class Twilio:

    def schedule():
        result = __DB.Grab_Most_Recent_Notification()
        if result is None:
            return;
        for notify in result:
            print("test")
        return; 



    def __init__(self):
        __DB = database()
