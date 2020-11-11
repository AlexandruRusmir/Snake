import random
import pygame
pygame.init()
pygame.display.set_caption("Snake")
import random




width = 500
height = 500
rows = 20


class cube():
    rows = 20
    wid = 500
    def __init__(self, start, dirx=1, diry=0, color=(255,0,0)):
        self.pos = start
        self.dirx = dirx
        self.diry = diry
        # "Left", "Right", "Up", "Down"
        self.color = color

    def move(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        self.pos  = (self.pos[0] + self.dirx, self.pos[1] + self.diry)
            

    def draw(self, surface):
        dis = self.wid // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1,dis-3,dis-3))




class snake():
    body = []
    turns = dict()
    
    def __init__(self, color, pos): #pos given as coordinates on the grid
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirx = 0
        self.diry = 1

    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
           
            for key in keys: #directions
                if keys[pygame.K_LEFT]:
                    self.dirx = -1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx,self.diry]
                elif keys[pygame.K_RIGHT]:
                    self.dirx = 1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx,self.diry]
                elif keys[pygame.K_UP]:
                    self.diry = -1
                    self.dirx = 0
                    self.turns[self.head.pos[:]] = [self.dirx,self.diry]
                elif keys[pygame.K_DOWN]:
                    self.diry = 1
                    self.dirx = 0
                    self.turns[self.head.pos[:]] = [self.dirx,self.diry]
        
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                c.move(c.dirx,c.diry)
        
        
    def reset(self,pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = dict()
        self.dirx = 0
        self.diry = 1


    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirx, tail.diry

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1]))) #moving right
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1]))) #moving left
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1))) #moving down
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1))) #moving up

        self.body[-1].dirx = dx
        self.body[-1].diry = dy

    
    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i == 0:
                c.draw(surface)
            else:
                c.draw(surface)





def redraw_Window():
    global window
    window.fill((0,0,0))
    drawGrid(width, rows, window)
    s.draw(window)
    apple.draw(window)
    pygame.display.update()
    pass




def drawGrid(w, rows, surface):
    sizeBetween = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBetween
        y = y + sizeBetween

        pygame.draw.line(surface, (255,255,255), (x, 0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0, y),(w,y))
    




def randomApple(rows, item):
    positions = item.body

    while True:
        x = random.randrange(1,rows-1)
        y = random.randrange(1,rows-1)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
               continue
        else:
               break

    return (x,y)




def main():
    global s, apple, window
    window = pygame.display.set_mode((width,height))
    s = snake((255,0,0), (10,10))
    s.addCube()
    apple = cube(randomApple(rows,s), color=(0,255,0))
    sw = True
    clck = pygame.time.Clock()
    
    while sw:
        pygame.time.delay(50)
        clck.tick(11) #game doesn't run at more than 11 fps
        s.move()
        headPos = s.head.pos
        if headPos[0] >= 20 or headPos[0] < 0 or headPos[1] >= 20 or headPos[1] < 0: #the snake hits the borders
            print("You lost! Your score was:", len(s.body))
            s.reset((10, 10))

        if s.body[0].pos == apple.pos:
            s.addCube()
            apple = cube(randomApple(rows,s), color=(0,255,0))
            
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])): #the snake hits itself
                print("You lost! Your score was:", len(s.body))
                s.reset((10,10))
                break
                    
        redraw_Window()

main()
