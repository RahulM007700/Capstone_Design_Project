import datetime as dt
import pymongo
import urllib
from pymongo import MongoClient

connurl = "mongodb+srv://Rahul_Muthyala:" + urllib.parse.quote("P@$$word") + "@captstone-cluster.njozi.mongodb.net/Rotation_Data?retryWrites=true&w=majority"
client = pymongo.MongoClient(connurl)
mydb = client["Rotation_Data"]
Users = mydb["Users"]
Students = mydb["Students"]
Stations = mydb["Stations"]


class Student:
    def __init__(self, id, email, first_name, last_name, station_list, visited_list):
        self.id = id
        self.email = email
        self.name = first_name + " " + last_name
        self.first_name = first_name
        self.last_name = last_name
        self.station_list = station_list
        self.visited_list = visited_list

    def add_vendor(self, Station):
        find = {"_id": self.id}
        update = {"$push": {"Station_List": {
            "Station_id": Station.id,
            "Start_Time": Station.starttime,
            "End_Time": Station.endtime,
            "Company": Station.company,
            "Lab_Name": Station.lab_name,
            "Station_Name": Station.station_name
        }}}
        Students.update_one(find, update)
        self.station_list.append(Station)
        for item in self.visited_list:
            if item["Company"] is Station.company:
                item["Times_Visited"] += 1
                c = "Visited_List.$.Times_Visited"
                find = {"_id": self.id, "Visited_List.Company": Station.company}
                update = {"$inc": {c: 1}}
                Students.update_one(find, update)

    def add_new_company(self, name):
        not_exist = True
        for item in self.visited_list:
            if item["Company"] == name:
                not_exist = False

        if not_exist:
            self.visited_list.append({"Company": name, "Times_Visited": 0})

    def print_schedule(self):
        print("Date\t\tStart Time\tEnd Time\tVendor")
        for item in self.station_list:
            temp1 = str(item.starttime).split()
            temp2 = str(item.endtime).split()
            print(temp1[0] + "\t" + temp1[1] + "\t" + temp2[1] + "\t" + item.company)

    def get_station_list(self):
        return self.station_list


class Station:
    def __init__(self, id, starttime, endtime, company, max_students, lab_name, station_name, list):
        self.id = id
        self.starttime = starttime
        self.endtime = endtime
        self.company = company
        self.max_students = max_students
        self.lab_name = lab_name
        self.station_name = station_name
        self.student_list = list

    def add_student(self, new_student):
        self.student_list.append(new_student)


def determine_students(Station):
    tempList = students
    available_students = []

    if len(Station_Master_List) == 0:
        for i in range(Station.max_students):
            available_students.append(tempList[i])
        return available_students

    limit = Station.max_students
    for i in range(1, len(tempList)):
        key = tempList[i]
        keyvistedlist = key.visited_list
        tempvisitedlist = tempList[i].visited_list
        x = 0
        for l in range(0, len(keyvistedlist) - 1):
            if keyvistedlist[l]["Company"] is Station.company:
                x = l
                break
        j = i - 1
        while j >= 0 and key.visited_list[x]["Times_Visited"] < tempList[j].visited_list[x]["Times_Visited"]:
            tempList[j + 1] = tempList[j]
            j -= 1
        tempList[j + 1] = key

    for i in range(len(tempList)):
        available_students.append(tempList[i])

    print("before")
    for x in available_students:
        print(x.name)
    i = 0
    last_student = available_students[len(available_students)-1]
    while i < len(available_students):
        print(i)
        Free = True
        if available_students[i] == last_student:
            break
        print(available_students[i].name)
        print(available_students[i].station_list)
        for s in available_students[i].station_list:
            print("Station starttime: " + str(Station.starttime))
            print("Station endtime: " + str(Station.endtime))
            print("s starttime: " + str(s.starttime))
            print("s endtime: " + str(s.endtime))
            if Station.starttime >= s.starttime and Station.endtime <= s.endtime:
                print("false")
                Free = False
        if not Free:
            available_students.append(available_students.pop(i))
            i = i - 1
            print("i here is " + str(i))
        i += 1

    print("after")
    for x in available_students:
        print(x.name)
    '''
    booleanList = []
    for student in available_students:
        for station in student.station_list:
            if Station.starttime >= station.starttime and Station.endtime <= station.endtime:
                booleanList.append(False)
            else:
                booleanList.append(True)

    for i in range(limit):
        if not booleanList:
            available_students.append(available_students.pop(i))
    '''
    return available_students

Station_Master_List = []
students = []
for user in Students.find():
        students.append(Student(id=user["_id"], email=user["Email"], first_name=user["First_Name"], last_name=user["Last_Name"], station_list=user["Station_List"], visited_list=user["Visited_List"]))
        #Students.insert_one({"_id": user["_id"], "Email": user["Email"], "First_Name": user["First_Name"],"Last_Name": user["Last_Name"], "Station_List": []})

for station in Stations.find():
    try:
        Station_Master_List.append(Station(id=station["_id"], starttime=station["Start_Time"], endtime=station["End_Time"], company=station["Company_Name"], lab_name=station["Lab_Name"], max_students=station["Group_Size"], list=station["Student_List"]))
    except:
        print()

def new_station(lab_name, station_name, company_name, date, start_time, end_time, group_size):
    d = date.split("-")
    st = start_time.split(":")
    et = end_time.split(":")
    for student in students:
        student.add_new_company(company_name)
        find = {"_id": student.id}
        update = {"$push": {"Visited_List": {
            "Company": company_name,
            "Times_Visited": 0
        }}}
        Students.update_one(find, update)
    stat = Station(id=len(Station_Master_List), starttime=dt.datetime(int(d[0]), int(d[1]), int(d[2]), int(st[0]), int(st[1]), 0),
                   endtime=dt.datetime(int(d[0]), int(d[1]), int(d[2]), int(et[0]), int(et[1]), 0), company=company_name,
                   max_students=int(group_size), lab_name=lab_name, station_name=station_name, list=[])

    available_students = determine_students(stat)
    Station_Master_List.append(stat)
    print(len(Station_Master_List))
    Stations.insert_one({
        "_id": Stations.count(),
        "Start_Time": stat.starttime,
        "End_Time": stat.endtime,
        "Company_Name": stat.company,
        "Group_Size": stat.max_students,
        "Lab_Name": stat.lab_name,
        "Station_Name": stat.station_name,
        "Student_List": []
    })
    count = 0
    for student in available_students:
        if count < stat.max_students:
            Station_Master_List[len(Station_Master_List) - 1].student_list.append(student.name)
            find = {"_id": len(Station_Master_List)-1}
            update = {"$push": {"Student_List": student.name}}
            Stations.update_one(find, update)
            student.add_vendor(stat)
            count = count + 1


'''
for student in students:
    print(student.name)
    print(student.visited_list)
    student.print_schedule()
'''

def get_student(name_needed):
    print("here")
    stationlist = []
    for item in Students.find():
        if item["Email"].lower() == name_needed.lower():
            for station in item["Station_List"]:
                #print(station)
                start = str(station["Start_Time"]).split()
                #print(start)
                end = str(station["End_Time"]).split()
                company_name = str(station["Company"])
                lab_name = str(station["Lab_Name"])
                station_name = str(station["Station_Name"])
                stationlist.append({"Date": start[0], "Lab Name": lab_name, "Station Name": station_name, "Start Time": start[1], "End Time": end[1], "Company": company_name})
    return stationlist


def get_master_list():
    station_list = []
    for item in Stations.find():
        print(item)
        start = str(item["Start_Time"]).split()
        end = str(item["End_Time"]).split()
        company_name = str(item["Company_Name"])
        lab_name = str(item["Lab_Name"])
        station_name = str(item["Station_Name"])
        student_list = item["Student_List"]
        print(student_list)
        station_list.append({"Date": start[0], "Lab Name":lab_name, "Station Name": station_name, "Start Time": start[1], "End Time": end[1], "Student List": student_list,
             "Company": company_name})
    return station_list

