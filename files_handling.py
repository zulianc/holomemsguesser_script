import datetime

def load_answers_from_file(filename):
    filepath = "files/" + filename + ".txt"
    file = open(filepath)

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

    filepath = "files/" + filename + ".txt"

    file = open(filepath, 'r')
    data = file.readlines()

    current_date = ""
    file = open(filepath, 'w')
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
