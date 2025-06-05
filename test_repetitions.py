# jeudi 05/06 Sakura Miko

answers = ['Sakura Miko']

def check_can_be_7bag(answers):
    if len(answers) < 7:
        return True

    for i in range(0, 7):
        i_possible = True

        start_bag = answers[0:i]
        if len(set(start_bag)) < i:
            i_possible = False
        
        for j in range(0 + i, len(answers) - 7 + 1, 7):
            bag = answers[j:j+7]
            if len(set(bag)) < 7:
                i_possible = False

        end_bag = answers[j+7:len(answers)]
        if (len(set(end_bag))) < (len(answers) - (j + 7)):
            i_possible = False

        if i_possible:
            return True

    return False

def check_can_be_7queue(answers):
    for i in range(0, len(answers) - 7 + 1):
        bag = answers[i:i+7]
        if len(set(bag)) < 7:
            return False
        
    return True

def check(answers):
    print("Can be 7 bag?  ", check_can_be_7bag(answers))
    print("Can be 7 queue?", check_can_be_7queue(answers))

check(answers)
