import random
import time
import string
from collections import Counter, defaultdict

# color console output
black_bold = "\033[1;30m"
red_col = "\033[91m"
red_bold = "\033[1;31m"
endc = "\033[0m"


class Pokemon:
    MAX_HIT_POINTS = 100
    MIN_HIT_POINTS = 1
    MAX_NUM_ROUNDS = 10
    # a nested dictionary to determine the multiplier of attack points
    attackingDict = {'fire': {'fire': 0.5, 'electric': 2.0, 'water': 0.5},
                     'electric': {'fire': 0.5, 'electric': 0.5, 'water': 2.0},
                     'water': {'fire': 2.0, 'electric': 0.5, 'water': 0.5}}

    def __init__(self, adaptive_ai=False):
        # set the name of the Pokemon
        while True:
            pokemanName = input("Please name your Pokemon (no punctuation): ")
            count = 0
            for i in pokemanName:
                if i not in string.punctuation:
                   count += 1
            if count == len(pokemanName):
                break
            else:
                print(red_col + "Sorry, name cannot include punctuation. " + endc)
                time.sleep(0.5)
        self.name = pokemanName

        # The Hit Points of pokemon instance
        while True:
            hitPoints = input("How many hit points will it have? (1-100) \n")
            if self.MIN_HIT_POINTS <= int(hitPoints) <= self.MAX_HIT_POINTS:
                break
            else:
                print(red_col + "Sorry. Hit points must be between 1 and 100. " + endc)
                time.sleep(0.5)
        self.HP = int(hitPoints)

        # Determine the type of the pokmeon
        while True:
            pokemanType = input("Select from the following Pokemon types: \n 1 - Electric Pokemon "
                                "\n 2 - Fire Pokemon \n 3 - Water Pokemon \n")
            if pokemanType == "1":
                pokemanType = "electric"
                break
            elif pokemanType == "2":
                pokemanType = "fire"
                break
            elif pokemanType == "3":
                pokemanType = "water"
                break
            else:
                print(red_col + "Sorry, you must pick either 1, 2, or 3." + endc)
                time.sleep(0.5)
        self.type = pokemanType

        self.adaptive_ai = adaptive_ai
        if adaptive_ai:
            # This player will keep track of how many times the opponent
            # chooses its Pokemon type, to make a theoretically better choice
            # against them next time:
            self.opponent_choices = defaultdict(Counter)

    # print method
    def __str__(self):
        if self.type == "electric":
            return self.name + " is an " + self.type + " Pokemon. "
        else:
            return self.name + " is a " + self.type + " Pokemon. "

    # getter of Pokemon name
    def getName(self):
        return self.name

    # getter of Pokemon type
    def getType(self):
        return self.type

    # getter of Pokemon HP
    def getHP(self):
        return self.HP

    # swap instance of Pokemon class in the case of which player goes first
    def swap(self, opponent):
        assert(isinstance(opponent, self.__class__))
        self.__dict__, opponent.__dict__ = opponent.__dict__, self.__dict__

    # roll a dice to determine which player goes first
    def dice(self, opponent):
        turn = random.randint(1, 2)
        print(self.name + " will roll a dice, to decide who goes first.")
        print(self.name + " rolls a " + str(turn) + " and will go", end="")
        if turn == 1:
            print(" first.")
        else:
            print(" second.")
            self.swap(opponent)

    # determine which player is ahead currently
    def printWhoIsAhead(self, opponent):
        if self.HP > opponent.HP:
            print(black_bold + self.name + endc + " is currently ahead!")
        elif self.HP < opponent.HP:
            print(black_bold + opponent.name + endc + " is currently ahead!")
        else:
            print(black_bold + "It's currently a tie!" + endc)

    # determine the winner of the game
    def determineWinner(self, opponent):
        if self.getHP() <= 0:
            print(red_bold + opponent.name + " is the winner!" + endc)
        else:
            print(red_bold + self.name + " is the winner!" + endc)

    # attack method. two Pokemon attack each other until one of them has less than 0 points
    def Attack(self, opponent):
        attack = random.randint(2, 50)
        attackDamage = attack * self.attackingDict[self.type][opponent.type]

        print(self.name + " is attacking " + opponent.name)
        if opponent.HP - attackDamage > 0:
            print("%s did %d Damage to %s" % (self.name, attackDamage, opponent.name))
            print("%s has %d HP left" % (opponent.name, opponent.HP - attackDamage))
        else:
            print("%s did %d Damage to %s" % (self.name, attackDamage, opponent.name))
            print("%s has been defeated!" % opponent.name)
        opponent.HP -= attackDamage
        return opponent.getHP() < 1

    # in the maximum of 10 rounds, determine the winner of the game
    def Battle(self, opponent):
        self.dice(opponent)
        ifWinner = False
        print()
        for i in range(self.MAX_NUM_ROUNDS):
            if not ifWinner:
                print("-----------------")
                print("Round " + str(i + 1) + "!")

                ifWinner = self.Attack(opponent)
                if not ifWinner:
                    ifWinner = opponent.Attack(self)
                    if not ifWinner:
                        self.printWhoIsAhead(opponent)

        if not ifWinner:
            print(red_bold + "It's a tie!" + endc)
        else:
            self.determineWinner(opponent)
        return self, opponent


if __name__ == "__main__":
    # 1. peopple vs people  check
    # 2. people vs computer
    # 3. computer vs computer

    print("\nHey there, let's start the Pokemon game! ")
    time.sleep(1)
    print("Player 1, build your Pokemon!")
    print("=================")
    time.sleep(0.5)
    Player1 = Pokemon()
    print()
    time.sleep(1)
    print("Player 2, build your Pokemon!")
    print("=================")
    time.sleep(0.5)
    Player2 = Pokemon()
    print()
    print(Player1)
    print(Player2)
    print()
    Player1.Battle(Player2)
