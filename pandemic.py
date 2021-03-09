from os import system
from random import randrange
system("cls")

################################
class Person:
    def __init__(self, id, virus):
        self.id = id
        self.virus = virus
        self.pos = [randrange(0,51),randrange(0,51)]

    def move(self):
        # Move Randomly, but keep inside city boundries
        # X
        if(self.pos[0] == 0):
            self.pos[0] += randrange(0,2)
        elif(self.pos[0] == cityWidth):
            self.pos[0] += randrange(-1,1)
        else:
            self.pos[0] += randrange(-1,2)
        # Y
        if(self.pos[1] == 0):
            self.pos[1] += randrange(0,2)
        elif(self.pos[1] == cityHeight):
            self.pos[1] += randrange(-1,1)
        else:
            self.pos[1] += randrange(-1,2)
        return self.pos
    
    def transmitVirus(self, people):
        if not self.virus:
            return
        for person in people:
            if(person.id == self.id):
                continue # skip myself
            if(person.pos == self.pos):
                print("[VIRUS] I ("+ str(self.id) + ") found a person ("+ str(person.id)+") with me at " + str(self.pos) + " on day " + str(day))

    def position(self):
        print("I am "+str(self.id)+" at position " + str(self.pos[0]) + " " + str(self.pos[1]))


### MAIN ###
## Globals
cityWidth = 50
cityHeight = 50
population = 200
duration = 60

## Init
people = []
for pID in range(population):
    people.append(Person(pID, False))
people[0].virus = True

"""
print("Staring positions: ")
for person in people:
        person.position()
"""
print("Simulation begins...")
day = 0
for day in range(duration): # People do move once per day
    #print("Day " + str(day))
    for person in people:
        person.move()
    for person in people:
        person.transmitVirus(people)
print("Simulation ended")

"""
print("Final  positions:")
for person in people:
        person.position()
"""