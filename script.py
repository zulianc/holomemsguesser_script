import json
import enum

# website: https://holomemsguesser.com/classic.html
# members.json: https://holomemsguesser.com/members

file = open("members.json", "r")
data = json.load(file)

members_name = data.keys()

DEBUT_DATE = "Debut_Date"
GROUP = "Group"
GENERATION = "Generation"
BRANCH = "Branch"
BIRTHDAY = "Birthday"
STATUS = "Status"
HEIGHT = "Height"

class Answers(enum.Enum):
    GREEN = 1
    ORANGE = 2
    ORANGE_PLUS = 3
    ORANGE_MINUS = 4
    RED = 5
    RED_PLUS = 6
    RED_MINUS = 7

def eliminate_impossible_answers(alive_members, pick, debut_date, group, generation, branch, birthday, status, height):
    alives = list(alive_members)

    for member in alive_members:
        if (debut_date == Answers.GREEN):
            if (data[member][DEBUT_DATE] != data[pick][DEBUT_DATE]):
                alives.remove(member)
                continue
        elif (debut_date == Answers.RED_MINUS):
            if (data[member][DEBUT_DATE] >= data[pick][DEBUT_DATE]):
                alives.remove(member)
                continue
        elif (debut_date == Answers.RED_PLUS):
            if (data[member][DEBUT_DATE] <= data[pick][DEBUT_DATE]):
                alives.remove(member)
                continue

        group_pick = set(data[pick][GROUP].split(","))
        group_member = set(data[member][GROUP].split(","))
        if (group == Answers.GREEN):
            if (group_pick != group_member):
                alives.remove(member)
                continue
        elif (group == Answers.ORANGE):
            if (len(group_pick and group_member) == 0):
                alives.remove(member)
                continue
        elif (group == Answers.RED):
            if (len(group_pick and group_member) > 0):
                alives.remove(member)
                continue

        if (generation == Answers.GREEN):
            if (data[member][GENERATION] != data[pick][GENERATION]):
                alives.remove(member)
                continue
        elif (generation == Answers.RED):
            if (data[member][GENERATION] == data[pick][GENERATION]):
                alives.remove(member)
                continue

    return alives

def compute_number_possible_left(alive_members, pick, solution):
    if (data[solution][DEBUT_DATE] == data[pick][DEBUT_DATE]):
        debut_date = Answers.GREEN
    elif (data[solution][DEBUT_DATE] < data[pick][DEBUT_DATE]):
        debut_date = Answers.RED_MINUS
    else:
        debut_date = Answers.RED_PLUS

    group_pick = set(data[pick][GROUP].split(","))
    group_solution = set(data[solution][GROUP].split(","))
    if (group_pick == group_solution):
        group = Answers.GREEN
    elif (len(group_pick and group_solution) > 0):
        group = Answers.ORANGE
    else:
        group = Answers.RED

    if (data[solution][GENERATION] == data[pick][GENERATION]):
        generation = Answers.GREEN
    else:
        generation = Answers.RED

    return len(eliminate_impossible_answers(alive_members, pick, "", "", generation, "", "", "", ""))

def find_best_pick(alive_members):
    average_left_by_member = dict.fromkeys(alive_members, 0)

    for pick in alive_members:
        for solution in alive_members:
            average_left_by_member[pick] += compute_number_possible_left(alive_members, pick, solution)
        average_left_by_member[pick] /= len(alive_members)

    for member in sorted(average_left_by_member, key=average_left_by_member.get, reverse=True):
        print(member, average_left_by_member[member])

find_best_pick(members_name)
