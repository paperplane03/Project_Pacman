from numpy import size
from Parameter import *
import pygame,random

class Map():
    mapobject=None
    def __init__(self,width,length,maplist:list) -> None:
        self.__width=width
        self.__length=length
        self.__maplist=maplist
        self.__ifonedot=False
        self.__somedot=False
        self.__somedotlist=[]
        self.__ifonedotx=-1
        self.__ifonedoty=-1
        self.validmap=1
        self.__scores=0
        self.__gametick=0
        self.__gamestep=0
        self.ifwin=False
        # print("maplist:")
        # print(maplist)
        Map.mapobject=self
        if len(self.__maplist)!=self.__length:
            self.validmap=0
        else:
            for i in self.__maplist:
                if len(i)!=self.__width:
                    self.validmap=0
                    break
        self.refillfood()
    
    def getmap(self):
        return self.__maplist
    
    def updatetime(self):
        self.__gametick+=1
    
    def updatestep(self):
        self.__gamestep+=1
    
    def resetscore(self):
        self.__scores=0
        self.__gametick=0
        self.__gamestep=0
    
    def get_ticks(self):
        return self.__gametick
    
    def get_steps(self):
        return self.__gamestep
    
    def clearfood(self):
        self.__ifeaten=[]
        for i in range(self.__length):
            self.__ifeaten.append([])
            for j in range(self.__width):
                self.__ifeaten[i].append(0)
                    
    def refillfood(self):
        if self.__ifonedot==False and self.__somedot==False:
            self.__ifeaten=[]
            for i in range(self.__length):
                self.__ifeaten.append([])
                for j in range(self.__width):
                    if self.__maplist[i][j]!=0:
                        self.__ifeaten[i].append(0)
                    else:
                        self.__ifeaten[i].append(1)
        elif self.__ifonedot==True:
            self.clearfood()
            self.__ifeaten[self.__ifonedotx][self.__ifonedoty]=1
        elif self.__somedot==True:
            self.clearfood()
            for i in self.__somedotlist:
                self.__ifeaten[i[0]][i[1]]=1
                
    
    def fillonefood(self):
        self.__ifonedot=True
        self.__ifeaten=[]
        for i in range(self.__length):
            self.__ifeaten.append([])
            for j in range(self.__width):
                self.__ifeaten[i].append(0)
        while True:
            i=random.randint(0,self.__length-1)
            j=random.randint(0,self.__width-1)
            if self.__maplist[i][j]==0:
                self.__ifeaten[i][j]=1
                self.__ifonedotx=i
                self.__ifonedoty=j
                break
    
    def fillsomefood(self,num):
        # print("yes")
        self.__somedot=True
        self.__somedotlist=[]
        self.__ifeaten=[]
        haveeaten=0
        for i in range(self.__length):
            self.__ifeaten.append([])
            for j in range(self.__width):
                self.__ifeaten[i].append(0)
        while haveeaten<num:
            i=random.randint(0,self.__length-1)
            j=random.randint(0,self.__width-1)
            if self.__maplist[i][j]==0 and self.__ifeaten[i][j]==0:
                self.__somedotlist.append((i,j))
                self.__ifeaten[i][j]=1
                haveeaten+=1
    
    def get_size(self):
        return [self.__length,self.__width]
    
    def get_score(self):
        return self.__scores
              
    def if_win(self):
        temp_size=self.get_size()
        for i in range(temp_size[0]):
            for j in range(temp_size[1]):
                if self.__maplist[i][j]==0 and self.__ifeaten[i][j]!=0:
                    self.ifwin=False
                    return False
        self.ifwin=True
        return True
      
    def eat(self,x,y):
        if self.__maplist[x][y]!=0:
            return False
        elif self.__ifeaten[x][y]==0:
            return False
        self.__ifeaten[x][y]=0
        self.__scores+=1
        # if self.if_win()==True:
            # print("WINWINIWNIWNIWNIWNIWNIWNINWI")
            # ifwin=True
        return True
            
    def get_value(self,x,y):
        return self.__maplist[x][y]
    
    def get_ifeaten(self,x,y):
        return self.__ifeaten[x][y]
    

# class SystemParameter():
#     def __init__(self,blockgeneratePossibly,) -> None:
#         self.blockge=blockgeneratePossibly
#         pass

def generatevalid(x,y,templist:list):
    # tempmap=Map.mapobject
    # tempsize=tempmap.get_size()
    tempsize=[map_height,map_width]
    if x<0 or x>=tempsize[0]:
        return False
    if y<0 or y>=tempsize[1]:
        return False
    if templist[x][y]>=1:
        return False
    return True

class Directions():
    movemethod=4
    movevector=[[1,0],[0,1],[-1,0],[0,-1]]
    # __movevector.append([1,0]) #South
    # __movevector.append([0,1]) #East
    # __movevector.append([-1,0]) #North
    # __movevector.append([0,-1]) #West
    def __init__(self) -> None:
        pass
    
    @classmethod
    def getmove(cls,x):
        return Directions.movevector[x]
    
def checkconnecting(templist:list):
    # if iffirst==True:
        # print(templist)
    tempsize=[map_height,map_width]
    tempqueue=[]
    nowfrontnum=0
    check=[[0 for i in range(tempsize[0])] for j in range(tempsize[1])]
    # print(check)
    for i in range(tempsize[0]):
        for j in range(tempsize[1]):
            if check[i][j]==0 and templist[i][j]==0:
                # print("i:"+str(i)+" j:"+str(j))
                nowfrontnum+=1
                tempqueue.append((i,j))
                while len(tempqueue)>0:
                    tempx,tempy=tempqueue[0]
                    tempqueue.pop(0)
                    if check[tempx][tempy]!=0:
                        continue
                    check[tempx][tempy]=nowfrontnum
                    for k in range(4):
                        tempvector=Directions.getmove(k)
                        if generatevalid(tempx+tempvector[0],tempy+tempvector[1],templist)==True and\
                        check[tempx+tempvector[0]][tempy+tempvector[1]]==0:
                            tempqueue.append((tempx+tempvector[0],tempy+tempvector[1]))
    # print(nowfrontnum)
    return nowfrontnum

    
class Buttons():
    buttonobject=[]
    def __init__(self,name:str,butfont:'pygame.font.SysFont',position:tuple,size:tuple,\
        linergb:tuple,wordrgb:tuple,bgrgb:tuple,if_border,tag) -> None:
        Buttons.buttonobject.append(self)
        self.__name=name
        self.__font=butfont
        self.__position=position
        self.__size=size
        self.__wordrgb=wordrgb
        self.__linergb=linergb
        self.__bgrgb=bgrgb
        self.__if_border=if_border
        self.tag=tag
        self.buttonobj=butfont.render(self.__name,True,wordrgb,bgrgb)
        self.buttonrect=self.buttonobj.get_rect()
        self.buttonrect.center=(position[0]+size[0]/2,position[1]+size[1]/2)
        
    def be_clicked(self,tmpposition):
        tmpx=tmpposition[0]
        tmpy=tmpposition[1]
        if self.__position[0]<=tmpx<=self.__position[0]+self.__size[0] and\
        self.__position[1]<=tmpy<=self.__position[1]+self.__size[1]:
            return True
        return False    
    
    def changebackcolor(self,changed_color):
        self.__bgrgb=changed_color
        self.buttonobj=(self.__font).render(self.__name,True,self.__wordrgb,changed_color)
        self.buttonrect=self.buttonobj.get_rect()
        self.buttonrect.center=(self.__position[0]+self.__size[0]/2,self.__position[1]+self.__size[1]/2)
    
    def changelinecolor(self,changed_color):
        self.__linergb=changed_color
    
    def getifborder(self):
        return self.__if_border
    
    def getposition(self):
        return self.__position
    
    def getsize(self):
        return self.__size
    
    def getbg(self):
        return self.__bgrgb
    
    def getline(self):
        return self.__linergb
    
    def paintingbutton():
        
    # def 
        pass