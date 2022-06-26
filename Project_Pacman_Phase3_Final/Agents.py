from Util import Directions
from Util import Map
from Parameter import *

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
        self.invtime=0
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
    
    def getflashposition(self):
        return [self.pacman_flash_x,self.pacman_flash_y]
    
    def validPosition(self):
        ansMove=[]
        for i in range(Directions.movemethod):
            movevec=Directions.getmove(i)
            tempx=self.__x+movevec[0]
            tempy=self.__y+movevec[1]
            if Pacman.pacmanmap_valid(tempx,tempy)==True:
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
        if Pacman.pacmanmap_valid(tempx,tempy)==True:
            self.__x=tempx
            self.__y=tempy
            return True
        return False
    
    def getinit(self):
        return (self.__initx,self.__inity,self.__initorient)

    def becomeinv(self):
        self.invtime=200
        print("become invinsible")
    
    def decreaseinvtime(self):
        if self.invtime>0:
            if self.invtime==1:
                for ghostobj in Ghost.ghostvector:
                    ghostobj.if_scared=0
            self.invtime-=1
        
        return self.invtime>0
    
    @classmethod
    def pacmanmap_valid(cls,mapx,mapy):
        # print("pacmanvalid:"+str(mapx)+","+str(mapy))
        tempmap=Map.mapobject
        tempsize=Map.mapobject.get_size()
        if mapx>=0 and mapx<tempsize[0] and mapy>=0 and mapy<tempsize[1]:
            if tempmap.get_value(mapx,mapy)==0 or tempmap.get_value(mapx,mapy)==2:
                return True
            else:
                return False
        else:
            return False

class Ghost():
    ghostnum=0
    ghostvector=[]
    def __init__(self,initx,inity,initorient=0,initsearchmethod=1):

        self.__x=initx
        self.__y=inity
        self.__previous_x=initx
        self.__previous_y=inity
        self.ghost_flash_x=initx
        self.ghost_flash_y=inity
        self.__orient=initorient
        self.__previous_orient=initorient
        self.if_scared=0
        self.__id=Ghost.ghostnum
        self.__initx=initx
        self.__inity=inity
        self.__initorient=initorient
        
        self.chasemethod=initsearchmethod
        Ghost.ghostnum+=1
        Ghost.ghostvector.append(self)
    
    @classmethod
    def clearghost(cls):
        Ghost.ghostvector.clear()
        Ghost.ghostnum=0
    
    def getorient(self):
        return self.__orient
    
    def getflashposition(self):
        return [self.ghost_flash_x,self.ghost_flash_y]
    
    def getpreviousposition(self):
        return [self.__previous_x,self.__previous_y]
    
    def getpreviousorient(self):
        return self.__previous_orient
        
    def getposition(self):
        return [self.__x,self.__y]
    
    def changescared(self):
        # pass
        self.if_scared=1-self.if_scared
    
    def updatepreviousorient(self):
        self.__previous_orient=self.__orient
    
    def changeorient(self,moveorient):
        self.__orient=moveorient
    
    def updatepreviousposition(self):
        self.__previous_x=self.__x
        self.__previous_y=self.__y
    
    def validposition(self):
        ansMove=[]
        for i in range(Directions.movemethod):
            movevec=Directions.getmove(i)
            tempx=self.__x+movevec[0]
            tempy=self.__y+movevec[1]
            if Ghost.ghostmap_valid(tempx,tempy)==True:
                ansMove.append(i)
        return ansMove
    
    def getposition(self):
        return [self.__x,self.__y]
    
    def move(self,movedirection):
        movevec=Directions.getmove(movedirection)
        tempx=self.__x+movevec[0]
        tempy=self.__y+movevec[1]
        if Ghost.ghostmap_valid(tempx,tempy)==True:
            self.__x=tempx
            self.__y=tempy
            return True
        return False
    
    @classmethod
    def getallghostposition(cls):
        ans=[]
        for obj in cls.ghostvector:
            ans.append(obj.getposition())
    
    @classmethod
    def ghostmap_valid(cls,mapx,mapy):
        tempsize=Map.mapobject.get_size()
        for tempghost in Ghost.ghostvector:
            if tempghost.getposition()==[mapx,mapy]:
                return False
        if mapx>=0 and mapx<tempsize[0] and mapy>=0 and mapy<tempsize[1]:
            if Map.mapobject.get_value(mapx,mapy)==0 or Map.mapobject.get_value(mapx,mapy)==2:
                return True
            else:
                return False
        else:
            return False
        
    def respawn(self):
        newobj=Ghost(self.__initx,self.__inity,self.__initorient,self.chasemethod)
        Ghost.ghostvector.remove(self)
        del self
        
        
def if_touch():
    temppacman=Pacman.pacmanobject
    pacman_flashpos=temppacman.getflashposition()
    pacman_pos=temppacman.getposition()
    minans=const_inf
    # for ghostobj in Ghost.ghostvector:
    #     tempghostpos=ghostobj.getflashposition()
    #     # if Ghost.ghostvector[j]==[pacman_object.__x,pacman_object.__y]:
    #     minans=min(minans,(tempghostpos[0]-pacman_flashpos[0])**2+(tempghostpos[1]-pacman_flashpos[1])**2)
    # print(minans)
    for ghostobj in Ghost.ghostvector:
        ghost_flashpos=ghostobj.getflashposition()
        ghost_pos=ghostobj.getposition()
        # if Ghost.ghostvector[j]==[pacman_object.__x,pacman_object.__y]:
        if (ghost_flashpos[0]-pacman_flashpos[0])**2+(ghost_flashpos[1]-pacman_flashpos[1])**2<=1:
            return (True,ghostobj)
    return (False,None)

