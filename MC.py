import random

class Membrane(object):
    """ creates a membrane (width x height) of hexagons"""
    def __init__(self, width, height):
        self.width = width
        self.height = height #must be even for correct coordinates!!!!
        self.room = []
        for x in range(self.width):
            room_x=[]
            for y in range(self.height):
                room_x.append('-')
            self.room.append(room_x)

    def __str__(self):
        for y in range(self.height-1, -1, -1):
            if y%2 == 1:
                print '  ',
            for x in range(self.width):
                if self.room[x][y] == '-':
                    print ' ' ,self.room[x][y], ' ',
                else:
                    print ' ' ,self.room[x][y].a_or_d, ' ',
            print ' '
            print ' '
        return ''

    def getRandomPos(self):
        """returns a random position of the membrane"""
        x = random.choice(range(self.width))
        y = random.choice(range(self.height))
        return Position(x,y)

class Position(object):

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.getX()) + ' ' + str(self.getY())
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def convert_pos(self, membrane):
        """ applys the concept of periodic boundry condition:
        if the position is out of the membrane, creates a new position at the oposite side of membrane"""
        if self.x<0:
            self.x = self.x + membrane.width
        if self.x>membrane.width-1:
            self.x = self.x - membrane.width
        if self.y<0:
            self.y = self.y + membrane.height
        if self.y>membrane.height-1:
            self.y = self.y - membrane.height

    def get_neighbour_pos(self, membrane):
        """ returns the coordinates of the neighbourous positions as a list"""
        neighbour_pos = []
        if self.getY()%2 == 0:
            for i in [(0,1),(1,0),(0,-1),(-1,-1),(-1,0),(-1,1)]:
                x = self.getX() + i[0]
                y = self.getY() + i[1]
                new_pos = Position(x,y)
                new_pos.convert_pos(membrane)
                neighbour_pos.append(new_pos)
        else:
            for i in [(1,1),(1,0),(1,-1),(0,-1),(-1,0),(0,1)]:
                x = self.getX() + i[0]
                y = self.getY() + i[1]
                new_pos = Position(x,y)
                new_pos.convert_pos(membrane)
                neighbour_pos.append(new_pos)
        return neighbour_pos

    def are_neighbours(self, pos, membrane):
        """ returns True if the two positions are neighbours, else return False"""
        pos_list = self.get_neighbour_pos(membrane)
        for i in pos_list:
            if i.getX() == pos.getX() and i.getY() == pos.getY():
                return True
        else:
            return False

class Receptor(object):
    """ creates a receptor, in a membrane. The receptor can be 'D'(onor) or 'A'(cceptor)
    paon, pdon, paoff, pdoff represents the probability of dimerization (on) or
    monomeization (off) with an acceptor (a) or donor(d). Donor receptors have
    an rluc luminsecence (rluc) and yfp luminescence vaue. Receptor is positioned
    into a random, not occupied hexa of the membrane"""
    def __init__(self, membrane, a_or_d, paon, pdon, paoff, pdoff):
        self.membrane = membrane
        self.a_or_d = a_or_d
        self.paon = paon
        self.pdon = pdon
        self.paoff = paoff
        self.pdoff = pdoff
        self.dimer = '-'
        self.has_moved = False                  #hasn't moved in this iteration
        self.has_changed_dimer_status = False   #hasn't changed dimer status in this iteration
        if self.a_or_d == 'D':
            self.rluc = 1.0
            self.yfp = 0.0
            self.bret = self.yfp / self.rluc
        occupied = True
        while occupied:
            self.pos = self.membrane.getRandomPos()
            if self.membrane.room[self.pos.getX()][self.pos.getY()] == '-':
                occupied = False
        self.membrane.room[self.pos.getX()][self.pos.getY()] = self

    def get_free_neighbour_pos(self):
        """returns a free neighbour position in a list"""
        neighbour_pos = self.pos.get_neighbour_pos(self.membrane)
        free_neighbour_pos = []
        for i in neighbour_pos:
            if self.membrane.room[i.getX()][i.getY()] == '-':
                free_neighbour_pos.append(i)
        return free_neighbour_pos

    def get_neighbours(self):
        """return the neighbouring receptors in a list"""
        neighbour_pos = self.pos.get_neighbour_pos(self.membrane)
        neighbours = []
        for i in neighbour_pos:
            if self.membrane.room[i.getX()][i.getY()] != '-':
                neighbours.append(self.membrane.room[i.getX()][i.getY()])
        return neighbours
    
    def get_free_neighbour_pos_dimer(self):
        """return the free neighbouring positions of a dimer"""
        neighbour_pos_self = self.pos.get_neighbour_pos(self.membrane)
        neighbour_pos_pair = self.dimer.pos.get_neighbour_pos(self.dimer.membrane)
        free_neighbour_pos = []
        for i in neighbour_pos_self:
            if self.membrane.room[i.getX()][i.getY()] == '-' or self.membrane.room[i.getX()][i.getY()] == self.dimer:
                for j in neighbour_pos_pair:
                    if self.dimer.membrane.room[j.getX()][j.getY()] == '-' or self.dimer.membrane.room[j.getX()][j.getY()] == self:
                        if i.are_neighbours(j,self.membrane):
                            free_neighbour_pos.append([i,j])                  
        return free_neighbour_pos
                                                                         
    def move(self):
        if self.has_moved == False:
            if self.dimer == '-':
                free_neighbour_pos=self.get_free_neighbour_pos()
                self.membrane.room[self.pos.getX()][self.pos.getY()] = '-'
                if len(free_neighbour_pos)>0:
                    self.pos=random.choice(free_neighbour_pos)
                self.membrane.room[self.pos.getX()][self.pos.getY()] = self
                self.has_moved = True
            elif self.dimer.has_moved == False:
                free_neighbour_pos = self.get_free_neighbour_pos_dimer()
                self.membrane.room[self.pos.getX()][self.pos.getY()] = '-'
                self.dimer.membrane.room[self.dimer.pos.getX()][self.dimer.pos.getY()] = '-'
                if len(free_neighbour_pos)>0:
                    new_pos = random.choice(free_neighbour_pos)
                    self.pos = new_pos[0]
                    self.dimer.pos = new_pos[1]
                self.membrane.room[self.pos.getX()][self.pos.getY()] = self
                self.dimer.membrane.room[self.dimer.pos.getX()][self.dimer.pos.getY()] = self.dimer
                self.has_moved = True
                self.dimer.has_moved = True

    def change_dimer_status(self):
        if self.has_changed_dimer_status == False:
            if self.dimer == '-':
                neighbours = self.get_neighbours()
                for i in neighbours:
                    if i.has_changed_dimer_status == False:
                        x = random.random()
                        if i.a_or_d == 'A':
                            p=self.paon
                        if i.a_or_d == 'D':
                            p=self.pdon
                        if x<p:
                            self.dimer = i
                            self.dimer.dimer = self
                            self.has_changed_dimer_status = True
                            self.dimer.has_changed_dimer_status = True
                            break
            else:
                if self.dimer.has_changed_dimer_status == False:
                    x=random.random()
                    if self.dimer.a_or_d == 'A':
                        p=self.paoff
                    if self.dimer.a_or_d == 'D':
                        p=self.pdoff
                    if x<p:
                        self.has_changed_dimer_status = True
                        self.dimer.has_changed_dimer_status = True
                        self.dimer.dimer = '-'
                        self.dimer = '-'

    def get_bret(self):
        if self.a_or_d == 'D':
            self.rluc = 1.0
            self.yfp = 0.4
            neighbours = self.get_neighbours()
            for i in neighbours:
                if i.a_or_d == 'A':
                    self.yfp = self.yfp + 0.2
                    self.rluc = self.rluc - 0.05
            self.bret=self.yfp/self.rluc         

def calculate_bret(rlist):
    bret = 0
    d = 0
    for i in rlist:
        i.get_bret()
    for i in rlist:
        if i.a_or_d == 'D':
            bret+=i.bret
            d+=1
    return bret/d
    

def graphics_demo():
    """ graphical demo with one donor and one acceptor, with pdimerization=1.0
    ends with 's' key"""
    mem = Membrane(6,6)
    rlist = []
    print mem
    for i in range(1):
        rlist.append(Receptor(mem,'A',0.0,1.0,0.0,0.0))
        rlist.append(Receptor(mem,'D',1.0,0.0,0.0,0.0))
    print mem
    while raw_input()!='s':
        print mem
        for i in rlist:
            i.has_moved=False
            i.has_changed_dimer_status=False
        for i in rlist:
            i.move()
        for i in rlist:
            i.change_dimer_status()
    
def simulate(d,a,pddon,pddoff,pdaon,pdaoff,paaon,paaoff):
    """ d: number of donors
        a: number of acceptors
        pddon: donor-donor association probability
        pddoff: donor-donor dissociation probability
        pdaon: donor-acceptor association probability
        pdaoff: donor-acceptor dissociation probability
        paaon: acceptor-acceptor association probability
        paaoff: acceptor-acceptor dissociation probability
        
        performs simulation for 1000 iterations, returns bret"""
    
    mem = Membrane(100,100)
    rlist = []
    for j in range(d):
        rlist.append(Receptor(mem, 'D', pdaon, pddon, pdaoff, pddoff))
    for j in range(a):
        rlist.append(Receptor(mem, 'A', paaon, pdaon, paaoff, pdaoff))
    for j in range(1000):
        for k in rlist:
            k.has_moved = False
            k.has_changed_dimer_status = False
        for k in rlist:
            k.move()
        for k in rlist:
            k.change_dimer_status()
    return calculate_bret(rlist)            
            
            
            
        
                
        
    
