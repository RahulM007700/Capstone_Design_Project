import pymongo
import urllib
import pandas as pd
import random, string

connurl = "mongodb+srv://Rahul_Muthyala:" + urllib.parse.quote(
    "P@$$word") + "@captstone-cluster.njozi.mongodb.net/Rotation_Data?retryWrites=true&w=majority"
client = pymongo.MongoClient(connurl)
mydb = client["Rotation_Data"]
Users = mydb["Users"]
Students = mydb["Students"]
Stations = mydb["Stations"]
Users = mydb["Users"]

Users.drop()
Students.drop()
Stations.drop()

# print(db.Company.find_one({"_id": 1}))

data = pd.read_excel("students.xlsx")
dict = data.to_dict('records')
userlist = []
for i in range(len(dict)):
    userlist.append({"_id": i, "First_Name": dict[i]["FirstName"], "Last_Name": dict[i]["LastName"],
                     "Email": dict[i]["FirstName"] + "@gmail.com", "Password": "password", "Role": dict[i]["Role"]})

print(userlist)
Users.insert_many(userlist)

for user in Users.find():
    if user["Role"] == "student":
        Students.insert_one({"_id": user["_id"], "Email": user["Email"], "First_Name": user["First_Name"],
                             "Last_Name": user["Last_Name"], "Station_List": [], "Visited_List": []})

'''
company = "Company 1"
c = "Visited_List.$.Times_Visited"
find = {"_id": 0}
find = {"_id": 0, "Visited_List.Company": company}
update = {"$inc": {c: 1}}
Students.update_one(find, update)
print(Students.find_one(find))
'''


def generate_random_password():
    x = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return x
