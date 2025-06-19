import collections

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
    members = [x for x in answers.copy() if isinstance(x, str)]
    count = collections.Counter(members)
    print("Members appearing most:")
    for member in sorted(count, key=count.get, reverse=True)[:5]:
        print(member.split("\n")[0], ": ", count[member], sep="")
