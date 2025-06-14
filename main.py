import choices_script
import test_repetitions
import files_handling

def ask_color(category_name, allow_orange, allow_plusminus):
    while True:
        answer = input("What color did you get for " + category_name + "? Answer with g/o/o-/o+/r-/r+ : ")
        if (answer == "g"):
            return choices_script.Answers.GREEN
        if (answer == "o" and allow_orange and not allow_plusminus):
            return choices_script.Answers.ORANGE
        if (answer == "o-" and allow_orange and allow_plusminus):
            return choices_script.Answers.ORANGE_MINUS
        if (answer == "o+" and allow_orange and allow_plusminus):
            return choices_script.Answers.ORANGE_PLUS
        if (answer == "r" and not allow_plusminus):
            return choices_script.Answers.RED
        if (answer == "r-" and allow_plusminus):
            return choices_script.Answers.RED_MINUS
        if (answer == "r+" and allow_plusminus):
            return choices_script.Answers.RED_PLUS
        
def UI(members_name, skip_first):
    alive_members = members_name.copy()

    skip = skip_first
    while (len(alive_members) > 1):
        if (not skip):
            print("--------------------")
            choices_script.find_best_by_average_left(alive_members, print_answers=True)
            print("--------------------")
            choices_script.find_best_by_average_guesses(alive_members, print_answers=True)
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

        answer = input("Correst guess? Answer with 'y' or nothing: ")
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

            alive_members = choices_script.eliminate_impossible_answers(alive_members, pick, debut_date, group, generation, branch, birthday, status, height)

        print("--------------------")
        print("Possible members left:", alive_members)

    if (len(alive_members) != 1):
        print("Error: no members left!")
        return

    last_member = alive_members[0]
    filename = "answers"
    
    files_handling.write_answer_to_file(last_member, filename)
    answers = files_handling.load_answers_from_file(filename)

    print("--------------------")
    test_repetitions.check(answers, 7)
    print("--------------------")
    test_repetitions.count(answers)
    print("--------------------")

def testo(members_name, pick):
    guess_number_per_member = dict.fromkeys(members_name, 0)

    for solution in members_name:
        alive_members = members_name.copy()
        next_pick = pick
        while True:
            guess_number_per_member[solution] += 1
            alive_members = choices_script.compute_possible_answers(alive_members, next_pick, solution)

            if len(alive_members) == 1 and next_pick == alive_members[0]:
                break
            else:
                algo_results = choices_script.find_best_by_average_guesses(alive_members, print_answers=False)
                next_pick = sorted(algo_results, key=algo_results.get)[0]

    print([(str(x) + ": " + str(guess_number_per_member[x])) for x in sorted(guess_number_per_member, key=guess_number_per_member.get)])

members_name = choices_script.get_all_members_name()

UI(members_name, True)

# testo(members_name, "Kazama Iroha")
# testo(members_name, "Koseki Bijou")

# website: https://holomemsguesser.com/classic.html
# members.json: https://holomemsguesser.com/members
