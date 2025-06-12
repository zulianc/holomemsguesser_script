import datetime
import collections

def load_answers_from_file(filename):
    file = open(filename)

    answers = []
    next_unknown_number = 0
    while True:
        line = file.readline()
        if (line == "END"):
            return answers
        
        member = line.split("=")[1]
        if (member == "\n"):
            member = next_unknown_number
            next_unknown_number += 1

        answers.append(member)

def write_answer_to_file(answer, filename):
    today_date = datetime.date.today()
    date_string_format = "%d/%m/%Y"

    file = open(filename, 'r')
    data = file.readlines()

    current_date = ""
    file = open(filename, 'w')
    for line in data:
        if line != "END":
            date = line.split("=")[0].split("/")
            current_date = datetime.date(day=int(date[0]), month=int(date[1]), year=int(date[2]))

            if current_date == today_date:
                print("Can't write answer to file: already an answer for today!")
                file.write(line)
                file.write("END")
                return

        if line == "END":
            if current_date != "":
                current_date += datetime.timedelta(days=1)
                while current_date != today_date:
                    file.write(current_date.strftime(date_string_format) + "=\n")
                    current_date += datetime.timedelta(days=1)
            
            file.write(today_date.strftime(date_string_format) + "=" + answer + "\n")
            file.write("END")
        else:
            file.write(line)

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

def count(answers):
    count = collections.Counter(answers)
    print("Members appearing most:")
    for member in sorted(count, key=count.get, reverse=True)[:5]:
        print(member.split("\n")[0], ": ", count[member], sep="")
