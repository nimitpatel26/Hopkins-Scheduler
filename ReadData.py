
import json
import copy

global main_data
global locations
global person_types
global people
global hours_req
global hours_wrk
global hours_rem
global shift_len
global req_on
global req_off

'''
Printing locations
------------------
Main Hospital
Nursery
Branch 2

locations = ['Main Hospital', 'Nursery', 'Branch 2']


Printing personTypes
--------------------
['Nurse', '200', 'Main Hospital']
['Nurse2', '300', 'Nursery']
['Nurse3', '400', 'Branch 2']

PersonType = ['Nurse', 'Nurse2', 'Nurse3']

Printing people
---------------
['John', 'Nurse', '50']
['Alex', 'Nurse2', '100']
['Cynthia', 'Nurse3', '200']
['Luke', 'Nurse', '100']
['Samuel', 'Nurse', '30']
['Jack', 'Nurse2', '70']



[['John', 'Luke', 'Samuel'] , ['Alex', 'Jack'], ['Cynthia']]

Printing shiftTypes
--------------------
['10', ['Nurse2'], ['Weekdays']]
['5', ['Nurse3'], ['Weekends']]
['8', ['Nurse2'], ['Weekdays']]
['2', ['Nurse'], ['Weekdays']]
['6', ['Nurse2'], ['Weekends']]
['3', ['Nurse3'], ['Weekends']]

[[2], [10, 8, 6], [5, 3]]


'''
#def main():
def setupData():

    global main_data
    global locations
    global person_types
    global people
    global hours_req
    global hours_wrk
    global hours_rem
    global shift_len
    global must_off
    global req_on
    global req_off
    global num_days

    locations = []
    person_types = []
    people = []
    hours_req = []
    hours_wrk = []
    hours_rem = []
    shift_len = []
    must_off = []
    req_on = []
    req_off = []

    with open('scheduler_settings.json') as json_file:
        data = json.load(json_file)


    main_data = data
    locations = main_data['locations']
    num_days = int(main_data['numDays'])
    
    for i in main_data['personTypes']:
        person_types = person_types + [i[0]]

    people = [[]] * len(person_types)
    hours_req = [[]] * len(person_types)
    hours_wrk = [[]] * len(person_types)

    for i in main_data['people']:
        personTypeIndex = person_types.index(i[1])
        people[personTypeIndex] = people[personTypeIndex] + [i[0]]
        hours_req[personTypeIndex] = hours_req[personTypeIndex] + [int(main_data['personTypes'][personTypeIndex][1])]
        hours_wrk[personTypeIndex] = hours_wrk[personTypeIndex] + [int(i[2])]


    hours_rem = [[]] * len(person_types)
    for i in range(len(hours_req)):
        hours_rem[i] = Diff(hours_req[i], hours_wrk[i])


    shift_len = [[]] * len(person_types)
    for i in main_data['shiftTypes']:
        personTypeIndex = person_types.index(i[1][0])
        shift_len[personTypeIndex] = shift_len[personTypeIndex] + [int(i[0])]





    req_off = [[]] * len(person_types)
    for i in range(len(req_off)):
        req_off[i] = [[]] * len(people[i])

    #print("\nreq_off = " + str(req_off))
    #print("\nPrinting resquest off:")
    for i in main_data['requestOff']:
        #print(str(i) + ": " + str(main_data['requestOff'][i]))
        personTypeIndex, personIndex = findIndexes(i)
        #print(str(i) + " is at index " + str(personTypeIndex) + " and " + str(personIndex))
        for j in main_data['requestOff'][i]:
            daysoff = getDays(j)
            req_off[personTypeIndex][personIndex] = req_off[personTypeIndex][personIndex] + daysoff


    req_on = [[]] * len(person_types)
    for i in range(len(req_on)):
        req_on[i] = [[]] * len(people[i])

    # print("\nreq_on = " + str(req_on))
    # print("\nPrinting resquest on:")
    for i in main_data['requestOn']:
        # print(str(i) + ": " + str(main_data['requestOn'][i]))
        personTypeIndex, personIndex = findIndexes(i)
        # print(str(i) + " is at index " + str(personTypeIndex) + " and " + str(personIndex))
        for j in main_data['requestOn'][i]:
            dayson = getDays(j)
            req_on[personTypeIndex][personIndex] = req_on[personTypeIndex][personIndex] + dayson
            
            
    must_off = [[]] * len(person_types)
    for i in range(len(must_off)):
        must_off[i] = [[]] * len(people[i])

    # print("\nmust_off = " + str(must_off))
    # print("\nPrinting must off:")
    for i in main_data['mustOff']:
        # print(str(i) + ": " + str(main_data['requestOn'][i]))
        personTypeIndex, personIndex = findIndexes(i)
        # print(str(i) + " is at index " + str(personTypeIndex) + " and " + str(personIndex))
        for j in main_data['mustOff'][i]:
            daysmustoff = getDays(j)
            must_off[personTypeIndex][personIndex] = must_off[personTypeIndex][personIndex] + daysmustoff


    # print("\nprinting req_on:")
    # req_on = [[]] * len(person_types)
    # for i in main_data['requestOn']:
    #     personTypeIndex = person_types.index(i[1][0])


    print("\n--------------------")
    print("ALL DATA")
    print("--------------------\n")

    print("\nlocations = " + str(locations))
    print("person_types = " + str(person_types))
    print("people = " + str(people))

    print("\nhours_req = " + str(hours_req))
    print("hours_wrk = " + str(hours_wrk))
    print("hours_rem = " + str(hours_rem))

    print("\nshift_len = " + str(shift_len))
    print("\nmust_off = " + str(must_off))
    print("\nreq_off = " + str(req_off))
    print("req_on = " + str(req_on) + "\n")

    # getData(locations[0])

    return locations


def getData(locationName):
    global main_data
    global locations
    global person_types
    global people
    global hours_req
    global hours_wrk
    global hours_rem
    global shift_len
    global must_off
    global req_on
    global req_off
    global num_days
    
    local_locations = locationName
    local_person_types = []
    local_people = []
    local_hours_req = []
    local_hours_wrk = []
    local_hours_rem = []
    local_shift_len = []
    local_must_off = []
    local_req_on = []
    local_req_off = []

    peopleWrkAtLocation = []

    for i in range(len(main_data['personTypes'])):
        if (main_data['personTypes'][i][2] == locationName):
            peopleWrkAtLocation = peopleWrkAtLocation + [i]


    for i in peopleWrkAtLocation:

        local_person_types = local_person_types + [person_types[i]]
        local_people = local_people + people[i]

        for j in range(len(people[i])):

            local_hours_req = local_hours_req + [[hours_req[i][j]]]
            local_hours_wrk = local_hours_wrk + [[hours_wrk[i][j]]]
            local_hours_rem = local_hours_rem + [[hours_rem[i][j], hours_rem[i][j]]]
            local_shift_len = local_shift_len + [shift_len[i]]

            local_must_off = local_must_off + [must_off[i][j]]
            local_req_on = local_req_on + [req_on[i][j]]
            local_req_off = local_req_off + [req_off[i][j]]


    tmp_req_on = []
    for i in range(len(local_req_on)):
        for j in range(len(local_req_on[i])):
            data = local_req_on[i][j]
            if (data != []):
                tmp_req_on = tmp_req_on + [[i, local_req_on[i][j]]]

    local_req_on = tmp_req_on

    # print("\nreq_on = " + str(local_req_on))
    tmp_req_off = []
    for i in range(len(local_req_off)):
        for j in range(len(local_req_off[i])):
            data = local_req_off[i][j]
            if (data != []):
                tmp_req_off = tmp_req_off + [[i, local_req_off[i][j]]]

    local_req_off = tmp_req_off
    
    tmp_must_off = []
    for i in range(len(local_must_off)):
        for j in range(len(local_must_off[i])):
            data = local_must_off[i][j]
            if (data != []):
                tmp_must_off = tmp_must_off + [[i, local_must_off[i][j]]]

    local_must_off = tmp_must_off

    ######################################
    days_must_off = local_must_off
    days_req_off = local_req_off
    days_req_on = local_req_on
    ######################################

    tmp_req_on = []
    for i in local_req_on:
        base = i
        tmp_list = []
        #print (i)
        for j in range(0, 24):
            tmp_list = tmp_list + [base + [j]]
        tmp_req_on = tmp_req_on + tmp_list
    #print("\ntmp_req_on = " + str(tmp_req_on))
    local_req_on = tmp_req_on

    tmp_req_off = []
    for i in local_req_off:
        base = i
        tmp_list = []
        #print (i)
        for j in range(0, 24):
            tmp_list = tmp_list + [base + [j]]
        tmp_req_off = tmp_req_off + tmp_list
    #print("\ntmp_req_on = " + str(tmp_req_on))
    local_req_off = tmp_req_off
    
    tmp_must_off = []
    for i in local_must_off:
        base = i
        tmp_list = []
        #print (i)
        for j in range(0, 24):
            tmp_list = tmp_list + [base + [j]]
        tmp_must_off = tmp_must_off + tmp_list
    #print("\ntmp_req_on = " + str(tmp_req_on))
    local_must_off = tmp_must_off

    ######################################
    hourly_must_off = local_must_off
    hourly_req_off = local_req_off
    hourly_req_on = local_req_on
    ######################################


    # print("\nreq_on: = " + str(local_req_on))
    # print("\nreq_off: = " + str(local_req_off))
    # print("\n\n---------------------------")
    # print("locations = " + str(local_locations))
    # print("---------------------------\n")
    # print("person_types = " + str(local_person_types))
    # print("people = " + str(local_people))
    #
    # print("\nhours_req = " + str(local_hours_req))
    # print("hours_wrk = " + str(local_hours_wrk))
    # print("hours_rem = " + str(local_hours_rem))
    #
    # print("\nshift_len = " + str(local_shift_len) + "\n")

    return local_people, local_shift_len, local_hours_rem, num_days, local_req_on, local_req_off, local_must_off, days_req_on, days_req_off, days_must_off

def Diff(li1, li2):

    tmp = []
    for i in range(len(li1)):
        tmp = tmp + [li1[i] - li2[i]]
    return tmp

def findIndexes(name):

    global people

    mainIndex = 0
    innerIndex = 0

    for i in people:
        innerIndex = 0
        for j in i:
            if (name == j):
                return mainIndex, innerIndex

            innerIndex = innerIndex + 1
        mainIndex = mainIndex + 1

def getDays(days):
    stripString = lambda x: int(x.strip())


    if (days.find("-") != -1):
        tmp = days.split("-")
        tmpList = list(range(int(tmp[0]), int(tmp[1])))
        return tmpList

    if (days.find(",") != -1):
        tmp = days.split(",")
        tmpList = list(map(stripString, tmp))
        return tmpList

    return [int(days)]

#main()
