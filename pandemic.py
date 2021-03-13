### IMPORT
from random import randrange
import curses
import time

### GLOBALS
population = 400 # Initial population
patientZero = 1 # amount
duration = 5000 # Duration in frames
fps = 10 # Frames per second (default 10)
lifespan = 80 # Virus lifespan in steps
deadlyhood = 0.1 # Deadlyhood of the virus in percentage

version = "0.2a" 
deaths = 0 
cured = 0 
initialPopulation = population
infected = 0

### Main ##########################
def main(stdscr):
    # Define Sizes
    global topWinHeight
    global bottomWinHeight
    global footerHeight
    global simPlaneHeight
    global simPlaneWidth 
    topWinHeight = 1
    bottomWinHeight = 4
    footerHeight = 1
    simPlaneWidth = (stdscr.getmaxyx()[1] - 1)
    simPlaneHeight = stdscr.getmaxyx()[0] - (topWinHeight + bottomWinHeight + footerHeight)

    # Init GUI
    GUI = WindowMgr(stdscr)

    # Initialize objects
    global people
    people = []
    for pid in range(population): ## Generate population
        people.append(Person(pid))
    for i in range(patientZero): ## Patient zeros
        people[i].infect()

    # Begin simulation
    GUI.setTopText("Simulation running")
    
    global frame
    frame = 0
    ### Simulation Loop ###
    for frame in range(duration): # People do move once per frame
        for person in people:
            if not person.alive: continue # Skip dead people
            person.move()
            GUI.addToSimPlane(person.pos[1],person.pos[0], person.symbol)
        for person in people:
            if not person.alive: continue # Skip dead people
            person.transmitVirus(people)
        GUI.refreshSimPlane()
        GUI.updateStats()
        time.sleep(1/fps)
    ###

    GUI.setTopText("Simulation ended. Press any key to quit")
    stdscr.getkey()


### Classes ##########################
# Handles the curses calls and controls
class WindowMgr:
    def __init__(self, stdscr):
        ## Init curses, clear Screen, defines colours
        stdscr.clear()
        stdscr.refresh()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.topText = "Press any key to start the simulation"
        self.footerText = "Press 'q' to exit | Version " + version
        ## Init windows    
        # Top bar
        self.topWin = curses.newwin(topWinHeight,simPlaneWidth, 0, 0)
        self.topWin.attron(curses.color_pair(1))  
        self.topWin.addstr(0,0,self.topText)
        self.topWin.refresh()
        # Center space
        self.centerWin = curses.newwin(simPlaneHeight,simPlaneWidth, topWinHeight, 0)
        self.centerWin.refresh()
        # Bottom space
        self.bottomWin = curses.newwin(bottomWinHeight,simPlaneWidth, topWinHeight+simPlaneHeight, 0)
        self.bottomWin.addstr(0,0,"STATS:")
        self.bottomWin.refresh()
        # Footer
        self.footerWin = curses.newwin(footerHeight,simPlaneWidth, topWinHeight+simPlaneHeight+bottomWinHeight, 0)
        self.footerWin.attron(curses.color_pair(3))    
        self.footerWin.addstr(0,0," " + self.footerText + " " * (simPlaneWidth - len(self.footerText) - 2)) 
        self.footerWin.refresh()

    # Changes and refreshes the text of the top bar
    def setTopText(self, message):
        self.topWin.clear()
        self.topWin.addstr(0,0,message)
        self.topWin.refresh()

    # Edit the simulation plane
    def addToSimPlane(self,y,x,symbol):
        if(symbol == "#"):
            self.centerWin.addch(y,x,symbol, curses.color_pair(2))
        else:
            self.centerWin.addch(y,x,symbol)
        
    def refreshSimPlane(self):
        self.centerWin.refresh()
        self.centerWin.clear() # Prep for the next frame

    def updateStats(self):
        self.bottomWin.nodelay(1)
        if(self.bottomWin.getch() == ord("q")):
            quit() 
        
        self.bottomWin.clear()
        self.bottomWin.addstr(0,0,"STATS:")
        self.bottomWin.addstr(1,0,"Infected population: " + str(infected) + "/" + str(population) + " (" + str(round(infected / population * 100,2)) + "%)")
        self.bottomWin.addstr(2,0,"Vaccinated population: 0.0%")
        
        self.bottomWin.addstr(1,40,"Initial population: " + str(initialPopulation))
        self.bottomWin.addstr(2,40,"Deaths: " + str(deaths) + " (" + str(round(deaths/initialPopulation*100,2)) + "%)")
        self.bottomWin.addstr(3,40,"Cured: " + str(cured))


        self.bottomWin.refresh()

# Its the main moving entity
class Person:
    def __init__(self, pid):
        self.pid = pid
        self.virus = None
        self.pos = [randrange(2,simPlaneWidth-2),randrange(2,simPlaneHeight-2)]
        self.symbol = "O"
        self.vaccinated = False
        self.alive = True

    def infect(self):
        global infected
        infected = infected + 1
        self.virus = Virus()
        self.symbol = "#"

    def cure(self):
        global infected
        global cured
        infected = infected - 1
        cured = cured + 1
        self.virus = None
        self.symbol = "O"

    def die(self):
        global deaths
        global population
        global infected
        population = population - 1
        deaths = deaths + 1
        infected = infected - 1
        self.alive = False # u dead next refresh dude

    def move(self):
        # Move Randomly, but keep inside city boundries
        # X (width)
        if(self.pos[0] == 0):
            self.pos[0] += randrange(0,2)
        elif(self.pos[0] == simPlaneWidth-2):
            self.pos[0] += randrange(-1,1)
        else:
            self.pos[0] += randrange(-1,2)
        # Y (height)
        if(self.pos[1] == 0):
            self.pos[1] += randrange(0,2)
        elif(self.pos[1] == simPlaneHeight-2):
            self.pos[1] += randrange(-1,1)
        else:
            self.pos[1] += randrange(-1,2)
        # Virus ttl
        self.updateViralStatus()
    
    def updateViralStatus(self):
        if(self.virus == None):
            return
        if(self.virus.ttl == 0):
            self.rnd = randrange(0,100)
            if((deadlyhood * 100) > self.rnd):
                self.die()
            else:
                self.cure()
        else:
            self.virus.ttl = self.virus.ttl - 1

    def transmitVirus(self, people):
        if not self.virus: # if not sick dont do anything
            return
        for person in people:
            if(person.pid == self.pid): # skip myself
                continue 
            if(person.virus): # if already infected, also skip
                continue
            if(person.pos == self.pos):
                person.infect()
                
class Virus:
    def __init__(self):
        self.ttl = lifespan ## life left


### INIT
curses.wrapper(main)