from flask import Flask, jsonify, abort, make_response, request
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

#Database variables
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'SingleMind'
app.config['MYSQL_DATABASE_HOST'] = '10.142.0.5'


#Initializing connection and cursor
mysql.init_app(app)
con = mysql.connect()
cur = con.cursor()

#----------------------------------------------------------
#Creating a user
@app.route('/singlemind/users', methods=['POST'])
def create_task():

    #just a brief check to make sure payload is alright
    if not request.json or not 'Username' in request.json:
        abort(404)


    #our info
    #info can be None (except Username, Email, and Phone Number)
    user ={
    'Username':request.json.get('Username'),
    'Email':request.json.get('Email'),
    'FirstName':request.json.get('FirstName'),
    'LastName':request.json.get('LastName'),
    'PhoneNumber':request.json.get('PhoneNumber'),
    'BirthDate':request.json.get('BirthDate')
            }

    #Defining our error payload
    status_message = {
            'found_error':False,
            'message':"preexisting item in database!",
            'username_in_use':False,
            'email_in_use':False,
            'phone_number_in_use':False
            }


    #Checks if username is in use
    checkquery = "SELECT * FROM User_Table WHERE Username = '"+user['Username']+"';"
    cur.execute(checkquery)
    if (cur.rowcount != 0):
        status_message['found_error'] = True
        status_message['username_in_use'] = True
        
        
    #Checks if email is in use
    checkquery = "SELECT * FROM User_Table WHERE Email = '"+user['Email']+"';"
    cur.execute(checkquery)
    if (cur.rowcount != 0):
        status_message['found_error'] = True
        status_message['email_in_use'] = True

    
    #Checks if email is in use
    checkquery = "SELECT * FROM User_Table WHERE PhoneNumber = '"+user['PhoneNumber']+"';"
    cur.execute(checkquery)
    if (cur.rowcount != 0):
        status_message['found_error'] = True
        status_message['phone_number_in_use'] = True


    #Checking error flag
    if(status_message['found_error']):
        #Returning with error
        return jsonify ({'error': status_message})


    #Enter if there is no errors

    #Creating our mysql string
    query1 = "INSERT INTO User_Table(CreationDate, "
    query2 = "VALUES(NOW(),"

    for x in user.keys():
        if user[x] is not None:
            query1 += x + ", "
            query2 += "'" +  user[x] + "', "
    query1=query1[0:len(query1)-2]
    query2=query2[0:len(query2)-2]

    query1 += ") "
    query2 += ");"
    query1 += query2

    cur.execute(query1)
    con.commit()
    
    #Success return 201
    return jsonify({'user': user}), 201



#-------------------------------------------------------------
#Returns all users
@app.route('/singlemind/users', methods=['GET'])
def get_tasks():
    
    #Grabbing parameter username
    username = request.args.get('username')


    #If no username parameter, it will send back all users
    if username is not None:
        query = "SELECT * FROM User_Table WHERE '" + username + "'=Username"
    else:
        query = "SELECT * FROM User_Table" 

    cur.execute(query)

    #If no users are found
    if(cur.rowcount == 0):
        abort(404)

    #Creating dictionary to convert to JSON
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'users':r})



#---------------------------------------------------------------
#Returns a user by userid
@app.route('/singlemind/users/<int:user_id>', methods=['GET'])
def get_task_by_id(user_id):
  
    #Queries by UserID
    query = "SELECT * FROM User_Table WHERE UserID=" + str(user_id)
    cur.execute(query)

    #Checks if no UserID is found
    if(cur.rowcount == 0):
        abort(404)

    #Creating dictionary to convert to JSON
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'users':r})

#--------------------------------------------------------------------
#Updating a user
@app.route('/singlemind/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    
    #Queries by UserID
    query = "SELECT * FROM User_Table WHERE UserID=" + str(user_id)
    cur.execute(query)

    #Checks if no UserID is found
    if(cur.rowcount == 0):
        abort(404)

    #our info
    #info can be None (except Username, Email, and Phone Number)
    user ={
    'Username':request.json.get('Username'),
    'Email':request.json.get('Email'),
    'FirstName':request.json.get('FirstName'),
    'LastName':request.json.get('LastName'),
    'PhoneNumber':request.json.get('PhoneNumber'),
    'BirthDate':request.json.get('BirthDate')
            }

    #Defining our error payload
    status_message = {
            'found_error':False,
            'message':"preexisting item in database!",
            'username_in_use':False,
            'email_in_use':False,
            'phone_number_in_use':False
            }



    if user['Username'] is not None:
        #Checks if username is in use
        checkquery = "SELECT * FROM User_Table WHERE Username = '"+user['Username']+"';"
        cur.execute(checkquery)
        if (cur.rowcount != 0):
            status_message['found_error'] = True
            status_message['username_in_use'] = True
        
    if user['Email'] is not None:    
        #Checks if email is in use
        checkquery = "SELECT * FROM User_Table WHERE Email = '"+user['Email']+"';"
        cur.execute(checkquery)
        if (cur.rowcount != 0):
            status_message['found_error'] = True
            status_message['email_in_use'] = True

    if user['PhoneNumber']:
        #Checks if email is in use
        checkquery = "SELECT * FROM User_Table WHERE PhoneNumber = '"+user['PhoneNumber']+"';"
        cur.execute(checkquery)
        if (cur.rowcount != 0):
            status_message['found_error'] = True
            status_message['phone_number_in_use'] = True







    #Checking error flag
    if(status_message['found_error']):
        #Returning with error
        return jsonify ({'error': status_message})


    query1 = "UPDATE User_Table SET "
    query2 = " WHERE UserID = " + str(user_id) + ";"

    for x in user.keys():
        if user[x] is not None:
            query1 += x + "='" + user[x] + "', "
    query1=query1[0:len(query1)-2]
    query1 += query2
    cur.execute(query1)
    con.commit()
    return jsonify({'user':user}),200
    

#-------------------------------------------------------------------
#Deleting a user
@app.route('/singlemind/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    #Queries by UserID
    query = "SELECT * FROM User_Table WHERE UserID=" + str(user_id)
    cur.execute(query)

    #Checks if no UserID is found
    if(cur.rowcount == 0):
        abort(404)

    #Query to delete UserID
    query1 = "DELETE FROM User_Table WHERE UserID=" + str(user_id) + ";"
    cur.execute(query1)
    con.commit()

    return jsonify({'status':'deleted'})



#--------------------------------------------------
#---------------------------------------------------

#






#
#
#	EVENT REST CALLS
#
#


#----------------------------------------------------
#----------------------------------------------------



#------------------------------------------------
#Creating an Event
@app.route('/singlemind/events', methods=['POST'])
def create_event():
    
    #just a brief check to make sure payload is alright
    if not request.json or not 'UserID' in request.json:
        abort(404)

    #our info
    #EventDesc can be None which gets replaced with "No Description"
    event = {
    'UserID':request.json.get('UserID'),
    'EventName':request.json.get('EventName'),
    'EventDesc':request.json.get('EventDesc'),
    'EventDate':request.json.get('EventDate')
    }


    #Checks if Event Description is in place or not
    if event['EventDesc'] is None:
        event['EventDesc'] = "No description."

    #Error check to make sure all categories are there
    for x in event.keys():
        if event[x] is None:
            return make_response(jsonify({'error':'Invalid Payload'}, 404))

    #Creating mysql string
    #NOTE When refactoring switch all += with .append() for quicker times
    query1 = "INSERT INTO Event_Table(CreationDate, "
    query2 = "VALUES(NOW(),"

    for x in event.keys():
        query1 += x + ", "
        query2 += "'" + str(event[x]) + "', "

    query1=query1[0:len(query1)-2]
    query2=query2[0:len(query2)-2]

    query1 += ") "
    query2 += ");"
    query1 += query2

    cur.execute(query1)
    cur.execute("SELECT LAST_INSERT_ID();")
    #---------------------------
    #Section is for adding notification
    
    #Creating dictionary to convert to JSON
    item = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    




    query = "INSERT INTO Notification_Table VALUES ('"
    query += str(event['UserID']) 
    query += "','" 
    query +=  str(item[0]['LAST_INSERT_ID()']) 
    query += "', 0 ,'" 
    query += str(event['EventDate']) 
    query += "');"
    cur.execute(query)

    #---------------------------------

    con.commit()
    #Success return 201
    return make_response(jsonify({'event': event}), 201)

#------------------------------------------------
#Get Event by EventID
@app.route('/singlemind/events/<int:event_id>' , methods = ['GET'])
def get_event_by_eventid(event_id):
    
    #Queries by EventID
    query = "SELECT * FROM Event_Table WHERE EventID=" + str(event_id)
    cur.execute(query)

    #Check if no Event is found
    if(cur.rowcount == 0):
        abort(404)

    #Creating dictionary to convert to JSON
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'event':r})

#------------------------------------------------
#Get Events by UserID
@app.route('/singlemind/events/user/<int:user_id>' , methods = ['GET'])
def get_event_by_userid(user_id):
    
    #Queries by UserID
    query = "SELECT * FROM Event_Table WHERE UserID=" + str(user_id) + " ORDER BY EventDate DESC;"
    cur.execute(query)

    #Checks if no UserID is found
    if(cur.rowcount == 0):
        abort(404)

    #Creating dictionary to convert to JSON
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'events':r})

#------------------------------------------------
#Update Event
@app.route('/singlemind/events/<int:event_id>' , methods = ['PUT'])
def update_event(event_id):
    
    #Queries by EventID
    query = "SELECT * FROM Event_Table WHERE EventID=" + str(event_id)

    #Checks if no EventID is found
    if(cur.rowcount == 0):
        abort(404)

    #our info
    #EventDesc can be None which gets replaced with "No Description"
    event = {
    'EventName':request.json.get('EventName'),
    'EventDesc':request.json.get('EventDesc'),
    'EventDate':request.json.get('EventDate')
    }

    if event['EventDesc'] is None:
        event['EventDesc'] = "No description"

    query1 = "UPDATE Event_Table SET "
    query2 = " WHERE EventID = " + str(event_id) + ";"

    for x in event.keys():
        if event[x] is not None:
            query1 += x + "='" + event[x] + "', "
    query1 = query1[0:len(query1)-2]
    query1 += query2
    cur.execute(query1)
    con.commit()
    return make_response(jsonify({'event':event}),200)


#-----------------------------------------------
#Delete Event by EventID
@app.route('/singlemind/events/<int:event_id>' , methods = ['DELETE'])
def delete_event_by_id(event_id):
    
    #Queries by EventID
    query = "SELECT * FROM Event_Table WHERE EventID =" +str(event_id)
    cur.execute(query)

    #Checks if no EventID is found
    if(cur.rowcount == 0):
        abort(404)

    #Query to delete EventID
    query1 = "DELETE FROM Event_Table WHERE EventID=" + str(event_id)
    cur.execute(query1)
    con.commit()

    return make_response(jsonify({'status':'deleted'}), 200)













#-----------------------------------------------------
#Handler for 404 abort error
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)





if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80)

