from common.database import Database

Database.initialize()
Database.insert('users', {"Name": "Jack_Huang", "Account": "j84077200345@gmail.com", "Password": "jack6114"})
user = Database.find_one('users', {"Account": "j84077200345@gmail.com"})
print(user)