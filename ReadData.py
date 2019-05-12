
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

def setupData():

    global main_data
    global locations
    global person_types
    global people
    global hours_req
    global hours_wrk
    global hours_rem
    global shift_len
    locations = []
    person_types = []
    people = []
    hours_req = []
    hours_wrk = []
    hours_rem = []
    shift_len = []

    with open('scheduler_settings.json') as json_file:
        data = json.load(json_file)


    main_data = data
    locations = main_data['locations']

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


    print("\n--------------------")
    print("ALL DATA")
    print("--------------------\n")

    print("\nlocations = " + str(locations))
    print("person_types = " + str(person_types))
    print("people = " + str(people))

    print("\nhours_req = " + str(hours_req))
    print("hours_wrk = " + str(hours_wrk))
    print("hours_rem = " + str(hours_rem))

    print("\nshift_len = " + str(shift_len) + "\n")


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

    local_locations = locationName
    local_person_types = []
    local_people = []
    local_hours_req = []
    local_hours_wrk = []
    local_hours_rem = []
    local_shift_len = []

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

    return local_people, local_shift_len, local_hours_rem
    # nurse_names = copy.deepcopy(local_people)
    # nurses = copy.deepcopy(local_shift_len)
    # nurse_req_hours = copy.deepcopy(local_hours_rem)


def Diff(li1, li2):

    tmp = []
    for i in range(len(li1)):
        tmp = tmp + [li1[i] - li2[i]]
    return tmp
