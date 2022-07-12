from Util import Directions
from Util import Map

class Pacman():
    pacmanobject=None
    def __init__(self,initx,inity,initorient):
        self.__x=initx
        self.__y=inity
        self.__previous_x=initx
        self.__previous_y=inity
        self.pacman_flash_x=initx
        self.pacman_flash_y=inity
        self.__orient=initorient
        self.__previous_orient=initorient
        self.__initx=initx
        self.__inity=inity
        self.__initorient=initorient
        self.__mouth_open=0
        Pacman.pacmanobject=self
    
    def getmouthopen(self):
        if self.__mouth_open%2!=0:
            return 1
        else:
            return self.__mouth_open%4
        return self.__mouth_open
    
    def changemouthopen(self):
        self.__mouth_open=(self.__mouth_open+1)%4
        return True
    
    def getorient(self):
        return self.__orient
    
    def getpreviousorient(self):
        return self.__previous_orient
        
    def getposition(self):
        return [self.__x,self.__y]
    
    def getpreviousposition(self):
        return [self.__previous_x,self.__previous_y]
    
    def validPosition(self):
        ansMove=[]
        for i in range(Directions.movemethod):
            movevec=Directions.getmove(i)
            tempx=self.__x+movevec[0]
            tempy=self.__y+movevec[1]
            if pacmanmap_valid(tempx,tempy)==True:
                ansMove.append(i)
        return ansMove
    
    def updatepreviousorient(self):
        self.__previous_orient=self.__orient
    
    def changeorient(self,moveorient):
        self.__orient=moveorient
    
    def updatepreviousposition(self):
        self.__previous_x=self.__x
        self.__previous_y=self.__y
    
    def move(self,movedirection):
        movevec=Directions.getmove(movedirection)
        tempx=self.__x+movevec[0]
        tempy=self.__y+movevec[1]
        if pacmanmap_valid(tempx,tempy)==True:
            self.__x=tempx
            self.__y=tempy
            return True
        return False
    
    def getinit(self):
        return (self.__initx,self.__inity,self.__initorient)

def pacmanmap_valid(mapx,mapy):
    # print("pacmanvalid:"+str(mapx)+","+str(mapy))
    tempmap=Map.mapobject
    tempsize=Map.mapobject.get_size()
    if mapx>=0 and mapx<tempsize[0] and mapy>=0 and mapy<tempsize[1]:
        if tempmap.get_value(mapx,mapy)==0:
            return True
        else:
            return False
    else:
        return False

class Ghost():
    ghostnum=0
    ghostvector=[]
    def __init__(self,initx,inity):
        self.__x=initx
        self.__y=inity
        self.__previous_x=initx
        self.__previous_y=inity
        self.__orient=0
        self.__previous_orient=0
        self.__ifscared=0
        self.__id=Ghost.ghostnum
        Ghost.ghostnum+=1
        Ghost.ghostvector.append(self)
        
    def validposition(self):
        ansMove=[]
        for i in range(Directions.movemethod):
            movevec=Directions.getmove(i)
            tempx=self.__x+movevec[0]
            tempy=self.__y+movevec[1]
            if ghostmap_valid(tempx,tempy)==True:
                ansMove.append(i)
        return ansMove
    
    def getposition(self):
        return [self.__x,self.__y]
    
    def move(self,movedirection):
        movevec=Directions.getmove(movedirection)
        tempx=self.__x+movevec[0]
        tempy=self.__y+movevec[1]
        if ghostmap_valid(tempx,tempy)==True:
            self.__x=tempx
            self.__y=tempy
            return True
        return False
    
    @classmethod
    def getallghostposition(cls):
        ans=[]
        for obj in cls.ghostvector:
            ans.append(obj.getposition())
    
def if_dead(pacman_object=Pacman.pacmanobject):
    for j in range(Ghost.ghostnum):
        if Ghost.ghostvector[j]==[pacman_object.__x,pacman_object.__y]:
            return True
    return False


def ghostmap_valid(mapx,mapy,ghostid):
    tempsize=Map.mapobject.get_size()
    for i in range(Ghost.ghostnum):
        if i!=ghostid and Ghost.ghostvector[i].getposition()==[mapx,mapy]:
            return False
    if mapx>=0 and mapx<tempsize[0] and mapy>=0 and mapy<tempsize[1]:
        if map[mapx][mapy]==0:
            return True
        else:
            return False
    else:
        return False