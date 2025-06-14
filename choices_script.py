import json
import enum
import datetime

MEMBERS_DATA = json.load(open("files/members.json", "r"))

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

def get_all_members_name():
    return list(MEMBERS_DATA.keys())

def eliminate_impossible_answers(alive_members, pick, debut_date, group, generation, branch, birthday, status, height):
    alives = alive_members.copy()

    for member in alive_members:
        if (debut_date == Answers.GREEN):
            if (MEMBERS_DATA[member][DEBUT_DATE] != MEMBERS_DATA[pick][DEBUT_DATE]):
                alives.remove(member)
                continue
        elif (debut_date == Answers.RED_MINUS):
            if (MEMBERS_DATA[member][DEBUT_DATE] >= MEMBERS_DATA[pick][DEBUT_DATE]):
                alives.remove(member)
                continue
        elif (debut_date == Answers.RED_PLUS):
            if (MEMBERS_DATA[member][DEBUT_DATE] <= MEMBERS_DATA[pick][DEBUT_DATE]):
                alives.remove(member)
                continue

        group_pick = set([x.strip() for x in MEMBERS_DATA[pick][GROUP].split(",")])
        group_member = set([x.strip() for x in MEMBERS_DATA[member][GROUP].split(",")])
        if (group == Answers.GREEN):
            if (group_pick != group_member):
                alives.remove(member)
                continue
        elif (group == Answers.ORANGE):
            if (len(group_pick & group_member) == 0 or group_pick == group_member):
                alives.remove(member)
                continue
        elif (group == Answers.RED):
            if (len(group_pick & group_member) > 0):
                alives.remove(member)
                continue

        if (generation == Answers.GREEN):
            if (MEMBERS_DATA[member][GENERATION] != MEMBERS_DATA[pick][GENERATION]):
                alives.remove(member)
                continue
        elif (generation == Answers.RED):
            if (MEMBERS_DATA[member][GENERATION] == MEMBERS_DATA[pick][GENERATION]):
                alives.remove(member)
                continue

        if (branch == Answers.GREEN):
            if (MEMBERS_DATA[member][BRANCH] != MEMBERS_DATA[pick][BRANCH]):
                alives.remove(member)
                continue
        elif (branch == Answers.RED):
            if (MEMBERS_DATA[member][BRANCH] == MEMBERS_DATA[pick][BRANCH]):
                alives.remove(member)
                continue

        date_pick = MEMBERS_DATA[pick][BIRTHDAY].split("/")
        date_pick = datetime.date(2004, int(date_pick[0]), int(date_pick[1]))
        date_member = MEMBERS_DATA[member][BIRTHDAY].split("/")
        date_member = datetime.date(2004, int(date_member[0]), int(date_member[1]))
        difference = abs((date_pick - date_member).days)
        if (birthday == Answers.GREEN):
            if (difference > 0):
                alives.remove(member)
                continue
        elif (birthday == Answers.ORANGE):
            if (difference == 0 or difference > 30):
                alives.remove(member)
                continue
        elif (birthday == Answers.RED):
            if (difference <= 30):
                alives.remove(member)
                continue

        if (status == Answers.GREEN):
            if (MEMBERS_DATA[member][STATUS] != MEMBERS_DATA[pick][STATUS]):
                alives.remove(member)
                continue
        elif (status == Answers.RED):
            if (MEMBERS_DATA[member][STATUS] == MEMBERS_DATA[pick][STATUS]):
                alives.remove(member)
                continue

        height_pick = int(MEMBERS_DATA[pick][HEIGHT].split("cm")[0])
        height_member = int(MEMBERS_DATA[member][HEIGHT].split("cm")[0])
        difference = abs(height_pick - height_member)
        if (height == Answers.GREEN):
            if (difference > 0):
                alives.remove(member)
                continue
        elif (height == Answers.ORANGE_MINUS):
            if (difference == 0 or difference > 3 or height_member > height_pick):
                alives.remove(member)
                continue
        elif (height == Answers.ORANGE_PLUS):
            if (difference == 0 or difference > 3 or height_member < height_pick):
                alives.remove(member)
                continue
        elif (height == Answers.RED_MINUS):
            if (difference <= 3 or height_member > height_pick):
                alives.remove(member)
                continue
        elif (height == Answers.RED_PLUS):
            if (difference <= 3 or height_member < height_pick):
                alives.remove(member)
                continue

    return alives

def compute_possible_answers(alive_members, pick, solution):
    if (MEMBERS_DATA[solution][DEBUT_DATE] == MEMBERS_DATA[pick][DEBUT_DATE]):
        debut_date = Answers.GREEN
    elif (MEMBERS_DATA[solution][DEBUT_DATE] < MEMBERS_DATA[pick][DEBUT_DATE]):
        debut_date = Answers.RED_MINUS
    else:
        debut_date = Answers.RED_PLUS

    group_pick = set([x.strip() for x in MEMBERS_DATA[pick][GROUP].split(",")])
    group_solution = set([x.strip() for x in MEMBERS_DATA[solution][GROUP].split(",")])
    if (group_pick == group_solution):
        group = Answers.GREEN
    elif (len(group_pick & group_solution) > 0):
        group = Answers.ORANGE
    else:
        group = Answers.RED

    if (MEMBERS_DATA[solution][GENERATION] == MEMBERS_DATA[pick][GENERATION]):
        generation = Answers.GREEN
    else:
        generation = Answers.RED

    if (MEMBERS_DATA[solution][BRANCH] == MEMBERS_DATA[pick][BRANCH]):
        branch = Answers.GREEN
    else:
        branch = Answers.RED

    date_pick = MEMBERS_DATA[pick][BIRTHDAY].split("/")
    date_pick = datetime.date(2004, int(date_pick[0]), int(date_pick[1]))
    date_solution = MEMBERS_DATA[solution][BIRTHDAY].split("/")
    date_solution = datetime.date(2004, int(date_solution[0]), int(date_solution[1]))
    difference = abs((date_pick - date_solution).days)
    if (difference == 0):
        birthday = Answers.GREEN
    elif (difference <= 30):
        birthday = Answers.ORANGE
    else:
        birthday = Answers.RED

    if (MEMBERS_DATA[solution][STATUS] == MEMBERS_DATA[pick][STATUS]):
        status = Answers.GREEN
    else:
        status = Answers.RED

    height_pick = int(MEMBERS_DATA[pick][HEIGHT].split("cm")[0])
    height_solution = int(MEMBERS_DATA[solution][HEIGHT].split("cm")[0])
    difference = abs(height_pick - height_solution)
    if (difference == 0):
        height = Answers.GREEN
    elif (difference <= 3):
        if (height_solution < height_pick):
            height = Answers.ORANGE_MINUS
        else:
            height = Answers.ORANGE_PLUS
    else:
        if (height_solution < height_pick):
            height = Answers.RED_MINUS
        else:
            height = Answers.RED_PLUS

    return eliminate_impossible_answers(alive_members, pick, debut_date, group, generation, branch, birthday, status, height)

def find_best_by_average_left(alive_members, print_answers):
    average_left_by_member = dict.fromkeys(alive_members, 0)

    for pick in alive_members:
        for solution in alive_members:
            sanity_check = compute_possible_answers(alive_members, pick, solution)
            if not solution in sanity_check:
                print("failed", solution, pick, sanity_check)

            average_left_by_member[pick] += len(sanity_check)
        average_left_by_member[pick] /= len(alive_members)

    if print_answers:
        print("[Guess: Average members left after guess]")
        for member in sorted(average_left_by_member, key=average_left_by_member.get)[:5]:
            print(member, ": ", average_left_by_member[member], sep="")

    return average_left_by_member

def compute_best_average(alive_members):
    average_guesses_by_member = dict.fromkeys(alive_members, 0)

    for guess in alive_members:
        for solution in alive_members:
            average_guesses_by_member[guess] += 1
            if (guess == solution):
                continue

            left_alive = compute_possible_answers(alive_members, guess, solution)

            if len(left_alive) == 0:
                print("failed", guess, solution, alive_members)

            best_average = min(compute_best_average(left_alive).values())
            average_guesses_by_member[guess] += best_average
        average_guesses_by_member[guess] /= len(alive_members)
    
    return average_guesses_by_member

def find_best_by_average_guesses(alive_members, print_answers):
    average_guesses_by_member = compute_best_average(alive_members)

    if print_answers:
        print("[Guess: Average guesses to win]")
        for member in sorted(average_guesses_by_member, key=average_guesses_by_member.get)[:5]:
            print(member, ": ", average_guesses_by_member[member], sep="")

    return average_guesses_by_member
