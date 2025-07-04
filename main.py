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
        
def show_script_results(alive_members, number_showed):
    average_left_by_member = choices_script.find_best_by_average_left(alive_members)
    print("--------------------")
    print("[Guess: Average members left after guess]")
    for member in sorted(average_left_by_member, key=average_left_by_member.get)[:number_showed]:
        print(str(member) + ": " + str(average_left_by_member[member]))

    average_guesses_by_member = choices_script.find_best_by_average_guesses(alive_members)
    print("--------------------")
    print("[Guess: Average guesses to win]")
    for member in sorted(average_guesses_by_member, key=average_guesses_by_member.get)[:number_showed]:
        print(str(member) + ": " + str(average_guesses_by_member[member]))

def check_results(filename):
    answers = files_handling.load_answers_from_file(filename)

    print("--------------------")
    test_repetitions.check(answers, 7)
    print("--------------------")
    test_repetitions.count(answers)

def register_results(solution, filename):
    files_handling.write_answer_to_file(solution, filename)
    check_results(filename)

def find_member(alive_members, message):
    while True:
        answer = input(message)
        for member in alive_members:
            names = member.lower().split(" ") + [member.lower()]
            if (answer.lower() in names):
                print("You typed:", member)
                return member

def UI_base(members_name, skip_first):
    alive_members = members_name.copy()

    skip = skip_first
    while (len(alive_members) > 1):
        if (not skip):
            show_script_results(alive_members, 5)
        skip = False
        print("--------------------")

        pick = find_member(alive_members, "What member did you guessed? ")

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
    
    register_results(alive_members[0], "answers_base")

def UI_music(members_name):
    alive_members = members_name.copy()
    print("--------------------")
    solution = find_member(alive_members, "What is the solution for music? ")
    register_results(solution, "answers_music")

def UI_fanbase(members_name):
    alive_members = members_name.copy()
    print("--------------------")
    solution = find_member(alive_members, "What is the solution for fanbase? ")
    register_results(solution, "answers_fanbase")

def UI_stream(members_name):
    alive_members = members_name.copy()
    print("--------------------")
    solution = find_member(alive_members, "What is the solution for stream? ")
    register_results(solution, "answers_stream")

def skip_option(mode_name):
    print("--------------------")
    answer = input("Will you skip answering for " + mode_name + " mode? Answer with 'y' or nothing: ")
    return (answer == 'y')

def UI(members_name, skip_first):
    if skip_option("every"):
        check_results("answers_base")
        check_results("answers_music")
        check_results("answers_fanbase")
        check_results("answers_stream")
    else:
        if not skip_option("base"):
            UI_base(members_name, skip_first)
        if not skip_option("music"):
            UI_music(members_name)
        if not skip_option("fanbase"):
            UI_fanbase(members_name)
        if not skip_option("stream"):
            UI_stream(members_name)

    print("--------------------")

def compute_needed_guesses(members_name, pick):
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
                algo_results = choices_script.find_best_by_average_guesses(alive_members)
                next_pick = sorted(algo_results, key=algo_results.get)[0]

    print([(str(x) + ": " + str(guess_number_per_member[x])) for x in sorted(guess_number_per_member, key=guess_number_per_member.get)])

members_name = choices_script.get_all_members_name()

UI(members_name, True)

#compute_needed_guesses(members_name, "Kazama Iroha")
#compute_needed_guesses(members_name, "Koseki Bijou")

# website: https://holomemsguesser.com/classic.html
# members.json: https://holomemsguesser.com/members
# song files: https://hololive-assets.sfo3.digitaloceanspaces.com/hololive-songs/{name123}.mp3
