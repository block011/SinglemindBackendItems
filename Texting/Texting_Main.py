import mysql.connector


con = mysql.connector.connect (
        host= "localhost",
        user="root",
        passwd = "root",
        database = "SingleMind",
        auth_plugin = 'mysql_native_password'
        )

test(var)
test(var)





def test(var):
    print("This is test")
