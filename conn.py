import pyodbc
from Utils import *

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'quasar'
database = 'ChocolateBiscuitFactoryIMS'
username = 'sa'
password = 'Cse-3055'
cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

cursor = cnxn.cursor()

cursor.execute('select * from ChocolateBiscuitFactoryIMS.dbo.Worker')
worker = create_copy(cursor)
cursor.execute("select * from ChocolateBiscuitFactoryIMS.dbo.Person")
person = create_copy(cursor)
set_workers(workers=worker, person=person)
