# jeudi 05/06 Sakura Miko
# vendredi 06/06 AZKi
# samedi 07/06 Kureiji Ollie
# dimanche 08/06 Otonose Kanade

answers = ['Sakura Miko', 'AZKi', 'Kureiji Ollie', 'Otonose Kanade']

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

def check(answers):
    print("Can be 7 bag?  ", check_can_be_n_bag(answers, 7))
    print("Can be 7 queue?", check_can_be_n_queue(answers, 7))

check(answers)
