import json
import enum
import datetime

import test_repetitions

file = open("members.json", "r")
data = json.load(file)

members_name = list(data.keys())

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
    alives = alive_members.copy()

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

        group_pick = set([x.strip() for x in data[pick][GROUP].split(",")])
        group_member = set([x.strip() for x in data[member][GROUP].split(",")])
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
            if (data[member][GENERATION] != data[pick][GENERATION]):
                alives.remove(member)
                continue
        elif (generation == Answers.RED):
            if (data[member][GENERATION] == data[pick][GENERATION]):
                alives.remove(member)
                continue

        if (branch == Answers.GREEN):
            if (data[member][BRANCH] != data[pick][BRANCH]):
                alives.remove(member)
                continue
        elif (branch == Answers.RED):
            if (data[member][BRANCH] == data[pick][BRANCH]):
                alives.remove(member)
                continue

        date_pick = data[pick][BIRTHDAY].split("/")
        date_pick = datetime.date(2004, int(date_pick[0]), int(date_pick[1]))
        date_member = data[member][BIRTHDAY].split("/")
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
            if (data[member][STATUS] != data[pick][STATUS]):
                alives.remove(member)
                continue
        elif (status == Answers.RED):
            if (data[member][STATUS] == data[pick][STATUS]):
                alives.remove(member)
                continue

        height_pick = int(data[pick][HEIGHT].split("cm")[0])
        height_member = int(data[member][HEIGHT].split("cm")[0])
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
    if (data[solution][DEBUT_DATE] == data[pick][DEBUT_DATE]):
        debut_date = Answers.GREEN
    elif (data[solution][DEBUT_DATE] < data[pick][DEBUT_DATE]):
        debut_date = Answers.RED_MINUS
    else:
        debut_date = Answers.RED_PLUS

    group_pick = set([x.strip() for x in data[pick][GROUP].split(",")])
    group_solution = set([x.strip() for x in data[solution][GROUP].split(",")])
    if (group_pick == group_solution):
        group = Answers.GREEN
    elif (len(group_pick & group_solution) > 0):
        group = Answers.ORANGE
    else:
        group = Answers.RED

    if (data[solution][GENERATION] == data[pick][GENERATION]):
        generation = Answers.GREEN
    else:
        generation = Answers.RED

    if (data[solution][BRANCH] == data[pick][BRANCH]):
        branch = Answers.GREEN
    else:
        branch = Answers.RED

    date_pick = data[pick][BIRTHDAY].split("/")
    date_pick = datetime.date(2004, int(date_pick[0]), int(date_pick[1]))
    date_solution = data[solution][BIRTHDAY].split("/")
    date_solution = datetime.date(2004, int(date_solution[0]), int(date_solution[1]))
    difference = abs((date_pick - date_solution).days)
    if (difference == 0):
        birthday = Answers.GREEN
    elif (difference <= 30):
        birthday = Answers.ORANGE
    else:
        birthday = Answers.RED

    if (data[solution][STATUS] == data[pick][STATUS]):
        status = Answers.GREEN
    else:
        status = Answers.RED

    height_pick = int(data[pick][HEIGHT].split("cm")[0])
    height_solution = int(data[solution][HEIGHT].split("cm")[0])
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

def find_best_by_average_left(alive_members):
    average_left_by_member = dict.fromkeys(alive_members, 0)

    for pick in alive_members:
        for solution in alive_members:
            sanity_check = compute_possible_answers(alive_members, pick, solution)
            if not solution in sanity_check:
                print("failed", solution, pick, sanity_check)

            average_left_by_member[pick] += len(sanity_check)
        average_left_by_member[pick] /= len(alive_members)

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

def find_best_by_average_guesses(alive_members):
    average_guesses_by_member = compute_best_average(alive_members)

    print("[Guess: Average guesses to win]")
    for member in sorted(average_guesses_by_member, key=average_guesses_by_member.get)[:5]:
        print(member, ": ", average_guesses_by_member[member], sep="")

    return average_guesses_by_member

def ask_color(category_name, allow_orange, allow_plusminus):
    while True:
        answer = input("What color did you get for " + category_name + "? Answer with g/o/o-/o+/r-/r+ : ")
        if (answer == "g"):
            return Answers.GREEN
        if (answer == "o" and allow_orange and not allow_plusminus):
            return Answers.ORANGE
        if (answer == "o-" and allow_orange and allow_plusminus):
            return Answers.ORANGE_MINUS
        if (answer == "o+" and allow_orange and allow_plusminus):
            return Answers.ORANGE_PLUS
        if (answer == "r" and not allow_plusminus):
            return Answers.RED
        if (answer == "r-" and allow_plusminus):
            return Answers.RED_MINUS
        if (answer == "r+" and allow_plusminus):
            return Answers.RED_PLUS

def UI(members_name, skip_first):
    alive_members = members_name.copy()

    skip = skip_first
    while (len(alive_members) > 1):
        if (not skip):
            print("--------------------")
            find_best_by_average_left(alive_members)
            print("--------------------")
            find_best_by_average_guesses(alive_members)
        skip = False
        print("--------------------")

        pick = ""
        while (pick == ""):
            answer = input("What member did you guessed? ")
            for member in alive_members:
                names = member.lower().split(" ")
                if (answer.lower() in names):
                    pick = member
        print("You guessed:", pick)

        answer = input("Correst guess? Answer with y/n : ")
        if (answer == "y"):
            alive_members = [pick]
        else:
            debut_date = ask_color("debut date", False, True)
            group = ask_color("group", True, False)
            generation = ask_color("generation", False, False)
            branch = ask_color("branch", False, False)
            birthday = ask_color("birthday", True, False)
            status = ask_color("status", False, False)
            height = ask_color("height", True, True)

            alive_members = eliminate_impossible_answers(alive_members, pick, debut_date, group, generation, branch, birthday, status, height)

        print("--------------------")
        print("Possible members left:", alive_members)

    if (len(alive_members) != 1):
        print("Error: no members left!")
        return

    last_member = alive_members[0]
    filename = "answers.txt"
    
    test_repetitions.write_answer_to_file(last_member, filename)
    answers = test_repetitions.load_answers_from_file(filename)

    print("--------------------")
    test_repetitions.check(answers, 7)
    print("--------------------")
    test_repetitions.count(answers)
    print("--------------------")

UI(members_name, True)

def testo(members_name, pick):
    guess_number_per_member = dict.fromkeys(members_name, 0)

    for solution in members_name:
        alive_members = members_name.copy()
        next_pick = pick
        while True:
            guess_number_per_member[solution] += 1
            alive_members = compute_possible_answers(alive_members, next_pick, solution)

            print("----------------", solution, next_pick, alive_members)

            if len(alive_members) == 1 and next_pick == alive_members[0]:
                break
            else:
                algo_results = find_best_by_average_guesses(alive_members)
                next_pick = sorted(algo_results, key=algo_results.get)[0]

            print("/////////////////", algo_results)

    print([(str(x) + ": " + str(guess_number_per_member[x])) for x in sorted(guess_number_per_member, key=guess_number_per_member.get)])

# testo(members_name, "Kazama Iroha")

# website: https://holomemsguesser.com/classic.html
# members.json: https://holomemsguesser.com/members
