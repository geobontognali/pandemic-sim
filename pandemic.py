### IMPORT
from random import randrange
import curses
import time

### GLOBALS
version = "0.1a"
population = 20
initiallyInfected = 1
duration = 50


### Main ##########################
def main(stdscr):
    # Text
    topText = "Simulation running"
    footerText = "Press 'q' to exit | Version " + version

    # Init Screens and colors
    stdscr.clear()
    stdscr.refresh()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Simulation Plane
    global simPlaneWidth 
    global simPlaneHeight
    simPlaneWidth = stdscr.getmaxyx()[0] - 11
    simPlaneHeight = stdscr.getmaxyx()[1] - 1

    # Top bar
    topWin = curses.newwin(1,simPlaneHeight, 0, 0)
    topWin.attron(curses.color_pair(1))  
    topWin.addstr(0,0,topText)
    topWin.refresh()
    # Center space
    centerWin = curses.newwin(simPlaneWidth,simPlaneHeight, 1, 0)
    centerWin.addstr(0,0,"center")
    centerWin.refresh()
    # Bottom space
    bottomWin = curses.newwin(9,simPlaneHeight, simPlaneWidth+1, 0)
    bottomWin.addstr(0,0,"bottom")
    bottomWin.refresh()
    # Footer
    footerWin = curses.newwin(1,simPlaneHeight, simPlaneWidth+10, 0)
    footerWin.attron(curses.color_pair(3))    
    footerWin.addstr(0,0," " + footerText + " " * (simPlaneHeight - len(footerText) - 2))   
    footerWin.refresh()


    stdscr.getkey()


    # Initialize objects
    global people
    people = []
    for pid in range(population): ## Generate population
        people.append(Person(pid))
    for i in range(initiallyInfected): ## Patient zeros
        people[i].infect()

    # Begin simulation
    print("Simulation begins...")
    global frame
    frame = 0
    for frame in range(duration): # People do move once per frame
        stdscr.erase()
        for person in people:
            person.move()
            stdscr.addch(person.pos[1],person.pos[0], person.symbol)
        for person in people:
            person.transmitVirus(people)
        stdscr.refresh()
        time.sleep(0.1)

    ## Terminate simulation by keypress
    stdscr.getkey()

    ## Recap
    print("Simulation ended")
    print("Total people in the simulation: " + str(population))
    print("People infected at the beginning: " + str(initiallyInfected))
    infected = 0
    for person in people:
            if(person.virus):
                infected += 1
    print("People infected at the end: " + str(infected) )


### Classes ##########################
class Person:
    def __init__(self, pid):
        self.pid = pid
        self.virus = False
        self.pos = [randrange(0,simPlaneHeight+1),randrange(0,simPlaneWidth+1)]
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
        elif(self.pos[0] == simPlaneHeight):
            self.pos[0] += randrange(-1,1)
        else:
            self.pos[0] += randrange(-1,2)
        # Y
        if(self.pos[1] == 0):
            self.pos[1] += randrange(0,2)
        elif(self.pos[1] == simPlaneWidth):
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
                print("[VIRUS] I ("+ str(self.pid) + ") found a person ("+ str(person.pid)+") with me at " + str(self.pos) + " on frame " + str(frame))
                person.infect()

    def position(self):
        print("I am "+str(self.id)+" at position " + str(self.pos[0]) + " " + str(self.pos[1]))


### INIT
curses.wrapper(main)