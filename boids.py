import pygame, random, math, sys
from pygame import mixer
pygame.init()

WIDTH, HEIGHT=1366, 768


white=(255, 255, 255)
black=(0, 0, 0)


NUMBEROFBOIDS=15
H2=00
H=00
M=00
S=00

FPS=60

boidList=[]

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BOIDS")

boidimage=pygame.image.load('boidimage.png')
boidimage=pygame.transform.scale(boidimage, (17, 17))

mixer.music.load('backgroundm.mp3')
mixer.music.play(-1)


win.fill((242, 170, 76))
pygame.display.update()

##############################################################

font = pygame.font.SysFont("comicsans", 25)
font2 = pygame.font.SysFont("comicsans", 25)
font3 = pygame.font.SysFont("comicsans", 25)
font4 = pygame.font.SysFont("comicsans", 25)
font5 = pygame.font.SysFont("comicsans", 25)

##############################################################

clicked=False

#Buton
class button():
    button_col=(16, 24, 32)
    hover_col=(242, 170, 76)
    click_col=(242, 170, 76)
    text_col=(255, 255, 255)
    wB=20
    hB=20
    
    def __init__(self, x, y, text):
        self.x=x
        self.y=y
        self.text=text
        
    def draw_button(self):
        global clicked
        action = False

		#get mouse position
        pos = pygame.mouse.get_pos()

		#create pygame Rect object for the button
        button_rect = pygame.Rect(self.x, self.y, self.wB, self.hB)
		
		#check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(win, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                    clicked = False
                    action = True
            else:
                pygame.draw.rect(win, self.hover_col, button_rect)
        else:
            pygame.draw.rect(win, self.button_col, button_rect)
		
		#add shading to button
        pygame.draw.line(win, white, (self.x, self.y), (self.x + self.wB, self.y), 2)
        pygame.draw.line(win, white, (self.x, self.y), (self.x, self.y + self.hB), 2)
        pygame.draw.line(win, black, (self.x, self.y + self.hB), (self.x + self.wB, self.y + self.hB), 2)
        pygame.draw.line(win, black, (self.x + self.wB, self.y), (self.x + self.wB, self.y + self.hB), 2)

		#add text to button
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        win.blit(text_img, (self.x + int(self.wB / 2) - int(text_len / 2), self.y))
        return action

plusbutt= button(220, 733, '+')
minusbutt= button(240, 733, '-')

##############################################################

# CLASA BOID (pos, size) si CLASA OBSTACOL 

class Obstacol:
    def __init__(self, position):
        self.x , self.y =position
    def draw(self):
        pygame.draw.circle(win, (16, 24, 32), (self.x, self.y), 20)
        

class Boid:
    def __init__(self, position, size):
        self.x, self.y = position
        self.velocityX=random.randint(1, 4)
        self.velocityY=random.randint(1, 4)
        self.radius=size/2
        self.speed=2
        self.force=0.2
        self.angle=1
        
    def update(self, surface):
       # pygame.draw.circle(win, (16, 24, 32), (int(self.x), int(self.y)), self.radius, 0)
       boidimg=pygame.transform.rotate(boidimage, pygame.math.Vector2(self.velocityX, self.velocityY).angle_to((1,0))-90)
       win.blit(boidimg, (self.x, self.y))
       
    def move(self):
        if abs(self.velocityX) > 4 or abs(self.velocityY) > 4:
            Scalare = 4 / max(abs(self.velocityX), abs(self.velocityY))
            self.velocityX *= Scalare
            self.velocityY *= Scalare
        self.x += self.velocityX
        self.y += self.velocityY
    
    def bounce(self):
        if self.x>WIDTH:
            self.x=0
        elif self.x<0:
            self.x=WIDTH
        if self.y>HEIGHT:
            self.y=0
        elif self.y<0:
            self.y=HEIGHT
    
    def separare(self, neighbors, size):
        
        OtherX=0
        OtherY=0
        
        for neighbor in neighbors:
            X=self.x-neighbor.x
            Y=self.y-neighbor.y
            distN=math.sqrt(X*X + Y*Y)
            if distN < 10:
                OtherX += X
                OtherY += Y
        self.velocityX += OtherX
        self.velocityY += OtherY
        
    def aliniere(self, neighbors):
        
        if len(neighbors)<1:
            return
        
        OtherX=0
        OtherY=0
        
        for neighbor in neighbors:
            OtherX+=neighbor.velocityX
            OtherY+=neighbor.velocityY
        
        
        OtherX=OtherX/len(neighbors)
        OtherY=OtherY/len(neighbors)
        
        
        self.velocityX += OtherX/30
        self.velocityY += OtherY/30
        
    def coliziune(self, neighbors):
        
        if len(neighbors)<1:
            return
        
        OtherX=0
        OtherY=0
        
        for neighbor in neighbors:
            OtherX+=(self.x-neighbor.x)
            OtherY+=(self.y-neighbor.y)
        
        
        OtherX=OtherX/len(neighbors)
        OtherY=OtherY/len(neighbors)
        
        
        self.velocityX -= OtherX/90
        self.velocityY -= OtherY/90

        
        
##############################################################
        
#Create BOIDS
        
def create_Boids():
    for i in range(NUMBEROFBOIDS):
        posX=random.randint(WIDTH/2 -550, WIDTH/2 + 550)
        posY=random.randint(HEIGHT/2 -200, HEIGHT/2 + 200)
        pos=(posX, posY)
        size=8
        
        b=Boid(pos, size)
        Boid.speed=random.random()
        Boid.angle=random.uniform(0, math.pi*2)
        
        boidList.append(b)
        b.update(win)
        pygame.display.update()
    return size

##############################################################





sizeofBoid=create_Boids()
clock = pygame.time.Clock()
run = True

Obstacole=[]

a=0
s=0
c=0
while run:
    
    
    
    win.fill((242, 170, 76))
   # pygame.draw.rect(win, (16, 24, 32), (0,0,1366, 25))
    pygame.draw.rect(win, (16, 24, 32), (0,718,1366, 50))
    
    keys=pygame.key.get_pressed()
    
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type==pygame.MOUSEBUTTONUP:
            pos=pygame.mouse.get_pos()
            Obstacole.append(Obstacol(pos))
        
        if keys[pygame.K_a]:
            if a==0:
                a=1
            else:
                a=0
            print("a apasat", a)
    
        if keys[pygame.K_s]:
            if s==0:
                s=1
            else:
                s=0
            print("s apasat", s)
    
        if keys[pygame.K_c]:
            if c==0:
                c=1
            else:
                c=0
            print("c apasat", c)
            
            
            
            
            
            
        
    for boid in boidList:
        Neighbors=[]
        for otherBoid in boidList:
            if boid.x==otherBoid.x and boid.y==otherBoid.y:
                continue
            Xf=boid.x-otherBoid.x
            Yf=boid.y-otherBoid.y
            distf=math.sqrt(Xf*Xf + Yf*Yf)
            
            if distf<150:
                Neighbors.append(otherBoid)
                

        
        
        if s==1:
            boid.separare(Neighbors, 20)
        if a==1:
            boid.aliniere(Neighbors)
        if c==1:
            boid.coliziune(Neighbors)
        boid.separare(Obstacole, 30)
        boid.bounce()
        boid.update(win)
        boid.move()
        
        for o in Obstacole:
            o.draw()
    
    if s==1:
        pygame.draw.rect(win, (16, 24, 32), (400,736,50, 50))
        text_on=font3.render("ON", 10, (255, 255, 255))
        win.blit(text_on, (400, 736))
    else:
        pygame.draw.rect(win, (16, 24, 32), (400,736,50, 50))
        text_off=font3.render("OFF", 10, (255, 255, 255))
        win.blit(text_off, (400, 736))   
    
    if a==1:
        pygame.draw.rect(win, (16, 24, 32), (500,736,50, 50))
        text_on2=font4.render("ON", 10, (255, 255, 255))
        win.blit(text_on2, (538, 736))
    else:
        pygame.draw.rect(win, (16, 24, 32), (500,736,50, 50))
        text_off2=font4.render("OFF", 10, (255, 255, 255))
        win.blit(text_off2, (538, 736))
    
    if c==1:
        pygame.draw.rect(win, (16, 24, 32), (685,736,50, 50))
        text_on3=font4.render("ON", 10, (255, 255, 255))
        win.blit(text_on3, (685, 736))
    else:
        pygame.draw.rect(win, (16, 24, 32), (685,736,50, 50))
        text_off3=font4.render("OFF", 10, (255, 255, 255))
        win.blit(text_off3, (685, 736))
    
    textS=font3.render("SEPARARE:", 10, (255, 255, 255))
    textA=font4.render("ALINIERE:", 10, (255, 255, 255))
    textC=font5.render("COLIZIUNE:", 10, (255, 255, 255))
    textNOB=font.render("NUMBER OF BOIDS:" + str(NUMBEROFBOIDS), 10, (255, 255, 255))
    textClock=font2.render(str(H2)+":"+str(H)+":"+str(M), 10, (255, 255, 255))
    
    S+=1
    if S==60:
        S=0
        M+=1
    if M==60:
        M=0
        H+=1
    if H==60:
        H=0
        H2+=1
    
    
    
            
    if plusbutt.draw_button() or keys[pygame.K_UP]:
        NUMBEROFBOIDS+=1
        posX=random.randint(WIDTH/2 -600, WIDTH/2 + 600)
        posY=random.randint(HEIGHT/2 -200, HEIGHT/2 + 200)
        pos=(posX, posY)
        size=8
        b=Boid(pos, size)
        boidList.append(b)
    
    if minusbutt.draw_button() or keys[pygame.K_DOWN]:
        if NUMBEROFBOIDS >=1:
            NUMBEROFBOIDS-=1
            del boidList[0]
            
    win.blit(textS, (300, 736))
    win.blit(textA, (450, 736))
    win.blit(textC, (585, 736))
    win.blit(textNOB, (15, 736))
    win.blit(textClock, (1300, 736))
   
    pygame.display.update()
    
    
		
    #pygame.display.update()
    
##############################################################
        
pygame.quit()
sys.exit()
