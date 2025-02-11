import MySQLdb
db = MySQLdb.connect(host="localhost", user="root", passwd="password")
db.cursor().execute("CREATE DATABASE contactDB")
print("Success")
