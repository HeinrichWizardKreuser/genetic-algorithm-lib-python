'''
Here we showcase the use of GeneticAlgorithmLib by creating a population to
guess any word of choice. To guess your word, simply run:
$ java Example1Unicorn <your word>
for example:
$ java Example1Unicorn Unicorn
and see what happens!
'''


import random

MUTATION_RATE = 0.8
POP_SIZE = 100

TRY_AGAIN = "Invalid word, please try again"
REQUEST_WORD = \
    "Please enter a word (only lower and uppercase letters are allowed"

def complain(word: str):
    print(f"Invalid word '{word}', must all be lower or uppercase letters!")

def random_letter():
    c = chr(ord('a') + random.randint(0, 25))
    if random.random() < 0.5:
        return c.upper()
    return c

def random_word():
    s = ""
    for _ in word:
        s += random_letter()
    return str(s)

import sys
if len(sys.argv) > 1:
    word = sys.argv[1]
    if not word.isalpha():
        complain(word)
        exit()
else:
    print(REQUEST_WORD)
    word = input("> ")
    while not word.isalpha():
        complain(word)
        print(TRY_AGAIN)
        word = input("> ")

ln = len(word)
population = [ random_word() for _ in range(POP_SIZE) ]

def cost(s):
    ''' cost function is how many letters are wrong '''
    c = 0
    for s_c, w_c in zip(s, word):
        if s_c != w_c:
            c += 1
    return c

def mutate(s):
    ''' changes a random index to a random letter '''
    mutant = list(s)
    # print(f"mutate({s})")
    mutant[random.randint(0, ln-1)] = random_letter()
    return "".join(mutant)

def reproduce(mother, father):
    ''' combines two words to make one '''
    child = ""
    for m_c, f_c in zip(mother, father):
        if bool(random.getrandbits(1)):
            child += m_c
        else:
            child += f_c
    return str(child)

import geneticalgorithmlib

generation = 0
while True:
    word2cost = geneticalgorithmlib.evolve(
        population,
        cost,
        mutate,
        reproduce,
        mutation_rate=MUTATION_RATE,
        reverse=False,
        pop_size=POP_SIZE,
        top_k=4,
        generations=1)

    # report on findings
    generation += 1;
    print(f"---- GENERATION {generation} ----")
    iteration = 0
    top_performers = 5
    print(f"top {top_performers} performers:")
    # display the outcome of this population
    lowest_cost = ln
    best_word = None
    for s, word_cost in word2cost.items():
        if iteration == 0:
            lowest_cost = word_cost
            best_word = s
        iteration += 1
        if iteration > top_performers:
            break
        print(f"{s}: {word_cost}")
    if lowest_cost <= 0:
        print("---- SUCCESS ----")
        print(f"> {best_word}")
        break
    population = list(word2cost.keys())
