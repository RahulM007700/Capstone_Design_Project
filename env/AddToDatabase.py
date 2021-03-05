import pymongo
import urllib
import pandas as pd
connurl = "mongodb+srv://Rahul_Muthyala:" + urllib.parse.quote("P@$$word")+"@captstone-cluster.njozi.mongodb.net/Rotation_Data?retryWrites=true&w=majority"
client = pymongo.MongoClient(connurl)
db = client.Rotation_Data

#print(db.Company.find_one({"_id": 1}))

data = pd.read_excel("students.xlsx")
dict = data.to_dict('records')
studentlist = []
for i in range(len(dict)):
    studentlist.append({"_id": i, "First_Name": dict[i]["FirstName"], "Last_Name": dict[i]["LastName"], "Email": "", "Password": "", "Role": ""})

db.User.insert_many(studentlist)