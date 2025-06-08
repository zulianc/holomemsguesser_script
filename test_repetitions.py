def load_answers_from_file(filename):
    file = open(filename)

    start_day = file.readline().split("=")[1]
    start_year = file.readline().split("=")[1]

    answers = []
    next_unknown_number = 0
    while True:
        line = file.readline()
        if (line == "END"):
            return answers
        
        member = line.split("=")[1]
        if (member == ""):
            member = next_unknown_number
            next_unknown_number += 1

        answers.append(member)

def check_can_be_n_bag(answers, n):
    i_possibles = []

    for i in range(0, n):
        i_possible = True

        start_bag = answers[0:i]
        if len(set(start_bag)) < len(start_bag):
            continue
        
        for j in range(0 + i, len(answers), n):
            bag = answers[j:j+n]
            if len(set(bag)) < len(bag):
                i_possible = False
        
        if i_possible:
            i_possibles.append(i)

    return [len(i_possibles) > 0, i_possibles]

def check_can_be_n_queue(answers, n):
    for i in range(0, len(answers)):
        bag = answers[i:i+n]
        if len(set(bag)) < len(bag):
            return False
        
    return True

def check(answers, n):
    print("Can be " + str(n) + " bag?  ", check_can_be_n_bag(answers, n))
    print("Can be " + str(n) + " queue?", check_can_be_n_queue(answers, n))

answers = load_answers_from_file("answers.txt")
check(answers, 7)
