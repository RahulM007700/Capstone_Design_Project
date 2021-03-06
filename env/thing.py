import datetime as dt


class Student:
    def __init__(self, name):
        self.name = name
        self.station_list = []
        self.visited_list = []

    def add_vendor(self, Station):
        self.station_list.append(Station)
        for item in self.visited_list:
            if item["Company"] is Station.company:
                item["Times_Visited"] += 1

    def add_new_company(self, name):
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
    def __init__(self, starttime, endtime, company, max_students):
        self.starttime = starttime
        self.endtime = endtime
        self.company = company
        self.max_students = max_students
        self.student_list = []

    def add_student(self, new_student):
        self.student_list.append(new_student)


def determine_students(Station):
    tempList = students
    available_students = []

    if len(Station_Master_List) is 0:
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

    for i in range(Station.max_students):
        available_students.append(tempList[i])
    return available_students


Station_Master_List = []
students = [Student("Rahul@gmail.com"), Student("Student 2"), Student("Student 3"), Student("Student 4")]
for student in students:
    student.add_new_company("Company 1")
    student.add_new_company("Company 2")

new_station_1 = Station(dt.datetime(2021, 6, 15, 15, 0, 0), dt.datetime(2021, 6, 15, 15, 30, 0), "Company 1", 2)
new_station_2 = Station(dt.datetime(2021, 6, 15, 15, 0, 0), dt.datetime(2021, 6, 15, 15, 30, 0), "Company 1", 2)

available_students = determine_students(new_station_1)
# print("length of list is " + str(len(available_students)))
for student in available_students:
    Station_Master_List.append(new_station_1)
    student.add_vendor(new_station_1)

available_students = determine_students(new_station_2)
# print("length of list is " + str(len(available_students)))
# for student in available_students:
#    print(student.name)
# print("length of list is " + str(len(available_students)))
for student in available_students:
    Station_Master_List.append(new_station_2)
    student.add_vendor(new_station_2)

new_station_3 = Station(dt.datetime(2021, 6, 15, 15, 0, 0), dt.datetime(2021, 6, 15, 15, 30, 0), "Company 1", 2)

available_students = determine_students(new_station_3)
# print("length of list is " + str(len(available_students)))
for student in available_students:
    Station_Master_List.append(new_station_3)
    student.add_vendor(new_station_3)

new_station_4 = Station(dt.datetime(2021, 6, 15, 15, 0, 0), dt.datetime(2021, 6, 15, 15, 30, 0), "Company 1", 2)

available_students = determine_students(new_station_4)
# print("length of list is " + str(len(available_students)))
for student in available_students:
    Station_Master_List.append(new_station_4)
    student.add_vendor(new_station_4)

new_station_5 = Station(dt.datetime(2021, 6, 15, 15, 0, 0), dt.datetime(2021, 6, 15, 15, 30, 0), "Company 1", 2)

available_students = determine_students(new_station_5)
# print("length of list is " + str(len(available_students)))
for student in available_students:
    Station_Master_List.append(new_station_5)
    student.add_vendor(new_station_5)

new_station_6 = Station(dt.datetime(2021, 6, 15, 15, 0, 0), dt.datetime(2021, 6, 15, 15, 30, 0), "Company 1", 2)

available_students = determine_students(new_station_6)
# print("length of list is " + str(len(available_students)))
for student in available_students:
    Station_Master_List.append(new_station_6)
    student.add_vendor(new_station_6)

for student in students:
    print(student.name)
    print(student.visited_list)
    student.print_schedule()


def get_student(name_needed):
    stationlist = []
    for item in students:
        if item.name == name_needed:
            for station in item.station_list:
                start = str(station.starttime).split()
                end = str(station.endtime).split()
                stationlist.append({"Date": start[0], "Start Time": start[1], "End Time": end[1], "Company": station.company})
    return stationlist
