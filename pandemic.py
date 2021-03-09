from random import randrange
import time
import curses

################################
class Person:
    def __init__(self, pid):
        self.pid = pid
        self.virus = False
        self.pos = [randrange(0,cityWidth+1),randrange(0,cityHeight+1)]
        self.symbol = "O"

    def infect(self):
        self.virus = True
        self.symbol = "#"
    def cure(self):
        self.virus = False
        self.symbol = "O"

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
    
    def transmitVirus(self, people):
        if not self.virus: # if not sick dont do anything
            return
        for person in people:
            if(person.pid == self.pid): # skip myself
                continue 
            if(person.virus): # if already infected, also skip
                continue
            if(person.pos == self.pos):
                print("[VIRUS] I ("+ str(self.pid) + ") found a person ("+ str(person.pid)+") with me at " + str(self.pos) + " on step " + str(step))
                person.infect()

    def position(self):
        print("I am "+str(self.id)+" at position " + str(self.pos[0]) + " " + str(self.pos[1]))


### MAIN ###
## Globals
cityWidth = 130
cityHeight = 20
population = 25
infected = 5
duration = 1000

## Simulation Init
people = []
for pid in range(population): ## Generate population
    people.append(Person(pid))
for infected in range(infected): ## Patient zeros
    people[infected].infect()

# Curses GUI init
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

# Simulation
print("Simulation begins...")
step = 0
for step in range(duration): # People do move once per step
    #print("Day " + str(day))
    stdscr.erase()
    for person in people:
        person.move()
        stdscr.addstr(person.pos[1],person.pos[0], person.symbol)
    for person in people:
        person.transmitVirus(people)
    stdscr.refresh()
    time.sleep(0.05)

# Curses GUI cleanup (wait for keypress)
stdscr.getkey()
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

## Recap
print("Simulation ended")
print("Total people in the simulation: " + str(population))
print("People infected at the beginning: " + str(infected))
infected = 0
for person in people:
        if(person.virus):
            infected += 1
print("People infected at the end: " + str(infected) )