from Twilio_Class import *
import schedule
import time

def main():
    run = Twilio()
    
    schedule.every(5).seconds.do(run.Schedule)


    while(True):
        schedule.run_pending()
        time.sleep(5)
    





if __name__ == "__main__":
    main()
