import pyodbc
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'quasar'
database = 'ChocolateBiscuitFactoryIMS'
username = 'sa'
password = 'Cse-3055'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

cursor = cnxn.cursor()


cursor.execute("SELECT TOP (1000) [Salary] ,[Department] ,[Date_Employed] ,[Worker_ID] ,[Working_Machine] FROM [ChocolateBiscuitFactoryIMS].[dbo].[Worker]")

row = cursor.fetchone()
while row:
    print(row[0])
    row = cursor.fetchone()