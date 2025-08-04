from cmu_graphics import *
import random
import math
from PIL import Image

class Bee:
    
    def __init__(self,x,y,pollen,intendedMovement,rotation,flipped):
        self.x=x
        self.y=y
        self.pollen=pollen
        self.intendedMovement=intendedMovement
        self.rotation=rotation
        self.flipped=flipped

    def flapWings(self,app):
        dist=distance(self.x,app.posX,self.y,app.posY)
        if self.x<app.posX:
            self.rotation+=45+dist//90
        else:
            self.rotation+=45+dist//90
        if self.y<app.posY:
            self.rotation+=45+dist//90
        else:
            self.rotation+=45+dist//90
    
    def drawPlayer(self,app):
        #https://pngtree.com/freepng/cute-honey-bee-cartoon-png_5446521.html
        #https://www.remove.bg/
        if not self.flipped:
            drawImage(app.beeimage,self.x,self.y,height=80,width=80,align='center')
            drawOval(self.x-8,self.y-10,20,10,fill='black',rotateAngle=-self.rotation)
            drawOval(self.x+8,self.y-8,20,10,fill='black',rotateAngle=-self.rotation)
        else:
            drawImage(app.flippedBeeImage,self.x,self.y,height=80,width=80,align='center')
            drawOval(self.x-8,self.y-10,20,10,fill='black',rotateAngle=-self.rotation)
            drawOval(self.x+8,self.y-8,20,10,fill='black',rotateAngle=-self.rotation)

        for i in range(len(self.pollen)):
            drawCircle(self.x-10+i*10,self.y+20,5,fill=self.pollen[i],
            border='black')
        
    #main function for the movement of the helper bees
    def helperBeeTargets(self,app):
        #best template is used to keep track of which flower the bee 
        #should intend to move towards
        bestFlowerDistance=None
        if self.intendedMovement!=None:
            if (self.intendedMovement.gathered==True or 
                self.intendedMovement.y<15):
                self.intendedMovement=None
        for flower in app.flowers:
            if ((not flower.gathered and flower.pollinator==True) or 
                (not flower.gathered and flower.color in self.pollen)):
                bestTargetDistance=distance(self.x,flower.x,self.y,flower.y)
                if (bestFlowerDistance==None or 
                    bestTargetDistance<bestFlowerDistance):
                    bestFlowerDistance=bestTargetDistance
                    self.intendedMovement=flower

    def playerOnStep(self,app):
        self.helperBeeTargets(app)
        if self.intendedMovement!=None:
            distX=abs(self.x-self.intendedMovement.x)
            distY=abs(self.y-self.intendedMovement.y)
            if self.x<self.intendedMovement.x:
                self.x+=.5+distX//30
                self.flipped=True
            else:
                self.x-=.5+distX//30
                self.flipped=False
            if self.y<self.intendedMovement.y:
                self.y+=.5+distY//30
            else:
                self.y-=.5+distY//30
        
class Player(Bee):
    
    def __init__(self,x,y,pollen,intendedMovement,rotation,flipped):
        #uses inheritance from the bee class to give the player bee attributes
        super().__init__(x,y,pollen,intendedMovement,rotation,flipped)

    def flapWings(self,app):
        #flaps wings based off distance of bee from cursor,changes angle rotation in ovals
        dist=distance(self.x,app.posX,self.y,app.posY)
        if self.x<app.posX:
            self.rotation+=45+dist//90
        else:
            self.rotation+=45+dist//90
        if self.y<app.posY:
            self.rotation+=45+dist//90
        else:
            self.rotation+=45+dist//90

    def drawPlayer(self,app):
        #https://pngtree.com/freepng/cute-honey-bee-cartoon-png_5446521.html
        #https://www.remove.bg/
        if not self.flipped:
            drawImage(app.beeimage,self.x,self.y,height=90,width=90,align='center')
            drawOval(self.x-8,self.y-10,20,10,fill='black',rotateAngle=-self.rotation)
            drawOval(self.x+8,self.y-8,20,10,fill='black',rotateAngle=-self.rotation)
        else:
            drawImage(app.flippedBeeImage,self.x,self.y,height=90,width=90,align='center')
            drawOval(self.x-8,self.y-10,20,10,fill='black',rotateAngle=-self.rotation)
            drawOval(self.x+8,self.y-8,20,10,fill='black',rotateAngle=-self.rotation)
        #draws bee and the wings as ovals 
        drawOval(self.x-8,self.y-10,20,10,fill='black',rotateAngle=-self.rotation)
        drawOval(self.x+8,self.y-8,20,10,fill='black',rotateAngle=-self.rotation)
        #draws inventory pollen and pollen in top left thats collected
        for i in range(len(self.pollen)):
            drawCircle(self.x-10+i*10,self.y+20,5,fill=self.pollen[i],
            border='black')
            drawCircle(10+i*10,10,5,fill=self.pollen[i],border='black')
        
    def playerOnStep(self,app):
        #moves bee faster or slower based off of the distance it is from the cursor
        distToX=abs(self.x-app.posX)
        distToY=abs(self.y-app.posY)
        if self.x<=app.posX:
            self.x+=2+distToX//30
            self.flipped=True
        elif self.x>app.posX:
            self.x-=2+distToX//30
            if distToX>5:
                self.flipped=False
        if self.y<app.posY:
            self.y+=2+distToY//30
        else:
            self.y-=2+distToY//30

class Flower:
    
    def __init__(self,x,y,radius,color,pollinator,gathered):
        self.x=x
        self.y=y
        self.color=color
        self.pollinator=pollinator
        self.gathered=gathered
        self.radius=radius
        
    def drawFlower(self):
        drawCircle(self.x,self.y, self.radius, fill=self.color)
        #draws 4 petals with a simple for loop
        petals=4
        for petal in range(petals):
            if petal==0:
                drawCircle(self.x,self.y-15,self.radius/1.5,fill=self.color)
            elif petal==1:
                drawCircle(self.x+15,self.y+2.5,self.radius/1.5,fill=self.color)
            elif petal==2:
                drawCircle(self.x,self.y+15,self.radius/1.5,fill=self.color)
            elif petal==3:
                drawCircle(self.x-15,self.y+2.5,self.radius/1.5,fill=self.color)

        if self.pollinator==True:
            drawCircle(self.x,self.y,10, fill='yellow',border='black')
        if self.gathered==True and self.pollinator==True:
            drawCircle(self.x,self.y,10,fill='white')
    
    def growFlower(self,app):
        #grows the flowers radius if pollen is gathered and if flower isn't a pollinator
        if not self.pollinator and self.gathered:
            if self.radius<30:
                self.radius+=5
    
    def flowerOnStepEasy(self,app):
        #gives the flower movement from left to right
        self.y-=1
        sinMovement=math.sin(self.y//30)
        self.x+=sinMovement*1.5 
    
    def flowerOnStepMedium(self,app):
        #gives the flower movement from left to right
        self.y-=2
        sinMovement=math.sin(self.y//30)
        self.x+=sinMovement*2
    
    def flowerOnStepHard(self,app):
        #gives the flower movement from left to right
        self.y-=3
        sinMovement=math.sin(self.y//30)
        self.x+=sinMovement*2.5

def onAppStart(app):
    #https://pngtree.com/freepng/cute-honey-bee-cartoon-png_5446521.html
    #https://www.remove.bg/
    app.beeimage=Image.open('bee-removebg-preview.png')
    app.flippedBeeImage = app.beeimage.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    app.beeimage=CMUImage(app.beeimage)
    app.flippedBeeImage = CMUImage(app.flippedBeeImage)
    app.posX=0
    app.posY=0
    app.flowers=[Flower(app.width/2,app.height/2,20,'pink',False,False), 
    Flower(app.width//3,app.height//3,20,'mediumSlateBlue',True,False)]
    app.players=[Bee(20,20,[],None,45,False), Bee(app.width//2,app.height//2,[],None,45,False), Player(40,40,[],None,45,False)]
    app.flowercount=0
    app.startScreen=True
    app.instructions=False
    app.easybutton=False
    app.mediumbutton=False
    app.hardbutton=False

def redrawAll(app):
    #different conditionals for when different buttons are pressed for different gamemodes
    
    if app.easybutton==True:
        drawRect(0,0,400,400,fill='lightGreen')
        for flower in app.flowers:
            flower.drawFlower()
        for player in app.players:
            player.drawPlayer(app)
        drawRect(400,0,75,30,fill='black', align='center')
        drawLabel('Quit',382,6,fill='white',size=10,bold=True,align='center')
    elif app.mediumbutton==True:
        drawRect(0,0,400,400,fill='orange')
        for flower in app.flowers:
            flower.drawFlower()
        for player in app.players:
            player.drawPlayer(app)
        drawRect(400,0,75,30,fill='black', align='center')
        drawLabel('Quit',382,6,fill='white',size=10,bold=True,align='center')
    elif app.hardbutton==True:
        drawRect(0,0,400,400,fill='red')
        for flower in app.flowers:
            flower.drawFlower()
        for player in app.players:
            player.drawPlayer(app)
        drawRect(400,0,75,30,fill='black', align='center')
        drawLabel('Quit',382,6,fill='white',size=10,bold=True,align='center')
    
    if app.startScreen==True:
        drawRect(0,0,400,400,fill='white')
        for flower in app.flowers:
            flower.drawFlower()
        drawLabel('Welcome to the Bee Game!',200,50,fill='pink',bold=True,size=20)
        drawLabel('Press i for instructions',200,80,bold=True,size=15,fill='lightGreen')
        drawLabel('Choose your game level:',200,110,bold=True,size=15,fill='lightGreen')
        drawRect(200,170,75,25,fill='pink',align='center',border='black')
        drawLabel('Easy',200,170,fill='black',size=10,bold=True)
        drawRect(200,210,75,25,fill='pink',align='center',border='black')
        drawLabel('Medium',200,210,fill='black',size=10,bold=True)
        drawRect(200,250,75,25,fill='pink',align='center',border='black')
        drawLabel('Hard',200,250,fill='black',size=10,bold=True)
    
    if app.instructions==True:
        drawRect(200,200,350,350,fill='black',align='center')
        drawLabel('Instructions:',200,50,align='center',fill='white',bold=True,size=16)
        drawLabel('Main Bee follows the mouse cursor',200,70,align='center',fill='white',bold=True,size=12)
        drawLabel('Move your bee to collect pollen and pollinate the flowers',200,90,align='center',fill='white',bold=True,size=12)
        drawLabel('Choose between level modes',200,110,align='center',bold=True,fill='white',size=12)
        drawLabel(' Two AI Helper Bees will help collect pollen',200,130,align='center',bold=True,fill='white',size=12)
        drawLabel('Have Fun!',200,150,align='center',bold=True,fill='white',size=12)
        drawLabel('Press i to go back to home screen',200,180,align='center',bold=True,fill='white',size=16)

def onKeyPress(app,key):
    #toggle for changing screens
    if key=='i': app.instructions=not app.instructions

def createFlowers(app):
    #generates flowers in the flower list by using random for position,color,pollinator
    newX=random.randint(10,app.width-10)
    newCol=random.randint(0,3)
    poll=random.randint(0,1)
    colors=['purple','pink','mediumSlateBlue','blue']
    app.flowers.append(Flower(newX,app.height+15,20,colors[newCol],
    bool(poll), False))

def onMouseMove(app,mouseX,mouseY):
    app.posX=mouseX
    app.posY=mouseY
def onMousePress(app,mouseX,mouseY):
    #sets variables if quit button is clicked
    if 362<=mouseX<=400 and 0<=mouseY<=15:
            for player in app.players:
                player.pollen=[]
            app.startScreen=True
            app.hardbutton=False
            app.mediumbutton=False
            app.easybutton=False
    #sets variables if different button modes are clicked
    if app.startScreen==True:
        if 162<=mouseX<=238 and 158<=mouseY<=182:
            for player in app.players:
                player.pollen=[]
            app.easybutton=True
            app.startScreen=False
        if 162<=mouseX<=238 and 198<=mouseY<=222:
            for player in app.players:
                player.pollen=[]
            app.mediumbutton=True
            app.startScreen=False
        if 162<=mouseX<=238 and 238<=mouseY<=262:
            for player in app.players:
                player.pollen=[]
            app.hardbutton=True
            app.startScreen=False

def onStep(app):
    #onstep flowers on main screen for decoration
    if app.startScreen==True:
        for flower in app.flowers:
            flower.flowerOnStepEasy(app)
        app.flowercount+=1
        if app.flowercount==120:
            app.flowercount=0
        if app.flowercount%40==0:
            createFlowers(app)
    
    if app.easybutton==True:
        app.flowercount+=1
        if app.flowercount==120:
            app.flowercount=0
        if app.flowercount%80==0:
            createFlowers(app)
    
        for player in app.players:
            player.playerOnStep(app)
            player.flapWings(app)
        
        for flower in app.flowers:
            if app.flowercount%5==0:
                flower.growFlower(app)
            if flower.y<20:
                app.flowers.remove(flower)
            flower.flowerOnStepEasy(app)
        
        for player in app.players:
            for flower in app.flowers:
                dist=distance(flower.x,player.x,flower.y,player.y)
                #checks if bee is close enough to the flower for some action
                if dist<30:
                    if flower.pollinator==True and not flower.gathered:
                        player.pollen.append(flower.color)
                        flower.gathered=True
                    if (flower.pollinator==False and flower.gathered==False 
                    and flower.color in player.pollen):
                        flower.gathered=True
                        player.pollen.remove(flower.color)
    
    if app.mediumbutton==True:
        app.flowercount+=1
        if app.flowercount==120:
            app.flowercount=0
        if app.flowercount%30==0:
            createFlowers(app)
        
        for player in app.players:
            player.playerOnStep(app)
            player.flapWings(app)
        
        for flower in app.flowers:
            if app.flowercount%5==0:
                flower.growFlower(app)
            if flower.y<20:
                app.flowers.remove(flower)
            flower.flowerOnStepMedium(app)
        
        for player in app.players:
            for flower in app.flowers:
                dist=distance(flower.x,player.x,flower.y,player.y)
                #checks if bee is close enough to the flower for some action
                if dist<30:
                    if flower.pollinator==True and not flower.gathered:
                        player.pollen.append(flower.color)
                        flower.gathered=True
                    if (flower.pollinator==False and flower.gathered==False 
                    and flower.color in player.pollen):
                        flower.gathered=True
                        player.pollen.remove(flower.color)
    
    if app.hardbutton==True:
        app.flowercount+=1
        if app.flowercount==120:
            app.flowercount=0
        if app.flowercount%15==0:
            createFlowers(app)
        
        for player in app.players:
            player.playerOnStep(app)
            player.flapWings(app)
        
        for flower in app.flowers:
            if app.flowercount%5==0:
                flower.growFlower(app)
            if flower.y<20:
                app.flowers.remove(flower)
            flower.flowerOnStepHard(app)
        
        for player in app.players:
            for flower in app.flowers:
                dist=distance(flower.x,player.x,flower.y,player.y)
                #checks if bee is close enough to the flower for some action
                if dist<30:
                    if flower.pollinator==True and not flower.gathered:
                        player.pollen.append(flower.color)
                        flower.gathered=True
                    if (flower.pollinator==False and flower.gathered==False 
                    and flower.color in player.pollen):
                        flower.gathered=True
                        player.pollen.remove(flower.color)
    
def distance(x1,x2,y1,y2):
    return ((x1-x2)**2+(y1-y2)**2)**.5
        
        
runApp()