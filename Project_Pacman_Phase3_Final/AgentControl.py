from glob import glob
from logging import exception
from pathlib import Path
from Parameter import *
from Qtable import Qtable
from Util import Directions,Map
from Agents import Pacman,Ghost, if_touch
import random,PathControl
import copy

def getposindex(x,y):
    tempsize=Map.mapobject.get_size()
    return x*tempsize[0]+y

def ghost_random(ghostobj:Ghost):
    tempghostpos=ghostobj.getposition()
    tempchoice=ghostobj.validposition()
    if tempchoice==[]:
        return -1
    else:
        return tempchoice[random.randint(0,len(tempchoice)-1)]

def ghost_best(ghostobj:Ghost):
    global navigating_method
    if navigating_method==999:
        return -1
    temppacman=Pacman.pacmanobject
    temppacmanpos=temppacman.getposition()
    tempghostpos=ghostobj.getposition()
    way=PathControl.how_to_go(tempghostpos[0],tempghostpos[1],temppacmanpos[0],temppacmanpos[1])
    if len(way)<=1:
        return -1
    return way[1][2]

def ghost_predict(lambda_pos,ghostobj:Ghost):
    global navigating_method
    if navigating_method==999:
        return -1
    temppacman=Pacman.pacmanobject
    temppacmanpos=temppacman.getposition()
    tempghostpos=ghostobj.getposition()
    temppacori=temppacman.getorient()
    tempmovevec=Directions.movevector[temppacori]
    temprandom=random.random()
    if temprandom<lambda_pos:
        return ghost_random(ghostobj)
    predictpos=[temppacmanpos[0]+3*tempmovevec[0],temppacmanpos[1]+3*tempmovevec[1]]
    if Pacman.pacmanmap_valid(predictpos[0],predictpos[1])==True:
        way=PathControl.how_to_go(tempghostpos[0],tempghostpos[1],predictpos[0],predictpos[1])
    else:
        way=PathControl.how_to_go(tempghostpos[0],tempghostpos[1],temppacmanpos[0],temppacmanpos[1])
    if len(way)<=1:
        return -1
    return way[1][2]

def lambda_random(lambda_pos,ghostobj:Ghost):
    temprandom=random.random()
    if temprandom<lambda_pos:
        return ghost_random(ghostobj)
    else:
        return ghost_best(ghostobj)
        
def ghost_frightened(ghostobj:Ghost):
    global navigating_method
    if navigating_method==999:
        return -1
    temppacman=Pacman.pacmanobject
    temppacmanpos=temppacman.getposition()
    tempghostpos=ghostobj.getposition()
    way=PathControl.how_to_go(tempghostpos[0],tempghostpos[1],temppacmanpos[0],temppacmanpos[1])
    if len(way)<=1:
        return -1
    vaguedis=abs(tempghostpos[0]-temppacmanpos[0])+abs(tempghostpos[1]-temppacmanpos[1])
    togoway=-1
    for i in range(4):
        newx=tempghostpos[0]+Directions.movevector[i][0]
        newy=tempghostpos[1]+Directions.movevector[i][1]
        if Ghost.ghostmap_valid(newx,newy)==True:
            if abs(newx-temppacmanpos[0])+abs(newy-temppacmanpos[1])>vaguedis:
                vaguedis=abs(newx-temppacmanpos[0])+abs(newy-temppacmanpos[1])
                togoway=i
    return togoway
            
def lambda_frightened(lambda_pos,ghostobj:Ghost):
    temprandom=random.random()
    if temprandom<lambda_pos:
        return ghost_random(ghostobj)
    else:
        return ghost_frightened(ghostobj)

#Basic Rule-Based Pacman

def avoidance_pacman():
    temppacman=Pacman.pacmanobject
    temppacmanpos=temppacman.getposition()
    toghostdis=[0 for i in range(len(Ghost.ghostvector))]
    toway=[None for i in range(len(Ghost.ghostvector))]
    cnt=-1
    mindis=const_inf
    ghostpos=[]
    for ghostobj in Ghost.ghostvector:
        cnt+=1
        ghostpos.append(ghostobj.getposition())
        toway[cnt]=PathControl.how_to_go(temppacmanpos[0],temppacmanpos[1],ghostpos[cnt][0],ghostpos[cnt][1])
        toghostdis[cnt]=len(toway[cnt])-1
        mindis=min(mindis,toghostdis[cnt])
    if mindis>=6:
        scatter_food=PathControl.find_nearest(temppacmanpos[0],temppacmanpos[1])
        way=PathControl.how_to_go(temppacmanpos[0],temppacmanpos[1],scatter_food[0][0],scatter_food[0][1])
        return way[1][2]
    else:
        maxdis=0
        choice=-1
        for i in range(4):
            newpos=[temppacmanpos[0]+Directions.movevector[i][0],temppacmanpos[1]+Directions.movevector[i][1]]
            if Ghost.ghostmap_valid(newpos[0],newpos[1])==True:
                tempmindis=const_inf
                for j in range(len(Ghost.ghostvector)):
                    tempmindis=min(tempmindis,abs(ghostpos[j][0]-newpos[0])+abs(ghostpos[j][1]-newpos[1]))
                if tempmindis>maxdis:
                    choice=i
                    maxdis=tempmindis
        return choice

#Rule-Based Pacman with higher Intelligence and smarter consideration

def attack_pacman():
    temppacman=Pacman.pacmanobject
    temppacmanpos=temppacman.getposition()
    toghostdis=[0 for i in range(len(Ghost.ghostvector))]
    toway=[None for i in range(len(Ghost.ghostvector))]
    cnt=-1
    mindis=const_inf
    ghostpos=[]
    for ghostobj in Ghost.ghostvector:
        cnt+=1
        ghostpos.append(ghostobj.getposition())
        toway[cnt]=PathControl.how_to_go(temppacmanpos[0],temppacmanpos[1],ghostpos[cnt][0],ghostpos[cnt][1])
        toghostdis[cnt]=len(toway[cnt])-1
        mindis=min(mindis,toghostdis[cnt])
    # print(mindis)
    maxdis=0
    choice=-1
    if temppacman.invtime==0:
        if mindis<=4:
            for i in range(4):
                # if i==toway[0][1][2] or i==toway[1][1][2]:
                    # continue
                newpos=[temppacmanpos[0]+Directions.movevector[i][0],temppacmanpos[1]+Directions.movevector[i][1]]
                if Ghost.ghostmap_valid(newpos[0],newpos[1])==True:
                    tempmindis=const_inf
                    for j in range(len(Ghost.ghostvector)):
                        tempmindis=min(tempmindis,abs(ghostpos[j][0]-newpos[0])+abs(ghostpos[j][1]-newpos[1]))
                    if tempmindis>maxdis:
                        choice=i
                        maxdis=tempmindis
            # print("choice"+str(choice))
            return choice
        elif mindis<=8 and (system_default_ghost_num<=1 or toway[0][1][2]!=toway[1][1][2]):
            for i in range(4):
                # if i==toway[0][1][2] or i==toway[1][1][2]:
                    # continue
                newpos=[temppacmanpos[0]+Directions.movevector[i][0],temppacmanpos[1]+Directions.movevector[i][1]]
                if Ghost.ghostmap_valid(newpos[0],newpos[1])==True:
                    tempmindis=const_inf
                    for j in range(len(Ghost.ghostvector)):
                        tempmindis=min(tempmindis,abs(ghostpos[j][0]-newpos[0])+abs(ghostpos[j][1]-newpos[1]))
                    if tempmindis>maxdis:
                        choice=i
                        maxdis=tempmindis
            # print("choice"+str(choice))
            return choice
        else:
            scatter_food=PathControl.find_nearest(temppacmanpos[0],temppacmanpos[1])
            for tempfood in scatter_food:    
                way=PathControl.how_to_go(temppacmanpos[0],temppacmanpos[1],tempfood[0],tempfood[1])
                tempgoal=way[1][2]
                newpos=[temppacmanpos[0]+Directions.movevector[tempgoal][0],temppacmanpos[1]+Directions.movevector[tempgoal][1]]
                tempmindis=const_inf
                for j in range(len(Ghost.ghostvector)):
                    tempmindis=min(tempmindis,abs(ghostpos[j][0]-newpos[0])+abs(ghostpos[j][1]-newpos[1]))
                if tempmindis>maxdis:
                    choice=tempgoal
                    maxdis=tempmindis
            return choice
    else:                
        scatter_food=PathControl.find_nearest(temppacmanpos[0],temppacmanpos[1])
        for tempfood in scatter_food:    
            way=PathControl.how_to_go(temppacmanpos[0],temppacmanpos[1],tempfood[0],tempfood[1])
            tempgoal=way[1][2]
            newpos=[temppacmanpos[0]+Directions.movevector[tempgoal][0],temppacmanpos[1]+Directions.movevector[tempgoal][1]]
            tempmindis=const_inf
            for j in range(len(Ghost.ghostvector)):
                tempmindis=min(tempmindis,abs(ghostpos[j][0]-newpos[0])+abs(ghostpos[j][1]-newpos[1]))
            if tempmindis>maxdis:
                choice=tempgoal
                maxdis=tempmindis
        return choice
    
    
def reward(pacmanx:int,pacmany:int,ghostx:list,ghosty:list,ghostnum:int):
    mindis=const_inf
    fooddis=const_inf
    capsuledis=const_inf
    ghostdist=[0,0]
    factnum=0
    
    ghostvalue=0
    foodvalue=0
    
    for i in range(ghostnum):
        if Ghost.ghostvector[i].if_scared==0:
            factnum+=1
            
        if pacmanx==ghostx[i] and pacmany==ghosty[i]:
            ghostdist[i]=0
            continue
        tempway=PathControl.how_to_go(ghostx[i],ghosty[i],pacmanx,pacmany)
        if tempway==None:
            # print("Problem:"+str(pacmanx)+" "+str(pacmany)+" "+str(ghostx[i])+" "+str(ghosty[i]))
            # print(tempway)
            pass
        ghostdist[i]=len(tempway)-1
        
    if Map.mapobject.get_ifeaten(pacmanx,pacmany)==1:
        if Map.mapobject.get_ifcapsule(pacmanx,pacmany)==True:
            capsuledis=0
            fooddis=0
        else:
            fooddis=0
    else:
        scafood=PathControl.find_nearest(pacmanx,pacmany)
        for ele in scafood:
            if Map.mapobject.get_ifcapsule(ele[0],ele[1])==True:
                capsuledis=min(capsuledis,len(PathControl.how_to_go(pacmanx,pacmany,ele[0],ele[1]))-1)
                fooddis=capsuledis
            else:
                fooddis=min(fooddis,len(PathControl.how_to_go(pacmanx,pacmany,ele[0],ele[1]))-1)

    # if mindis!=0 and fooddis==0 and Map.mapobject.getfoodnum()==1:
    #     return const_inf
    
    #Calculate 
    if ghostdist[0]>=len(ghost_distance_value[0]):
        ghostdist[0]=len(ghost_distance_value)-1
    if ghostnum==2:
        if ghostdist[1]>=len(ghost_distance_value[0]):
            ghostdist[1]=len(ghost_distance_value)-1
        
    if factnum==2:
        ghostvalue=ghost_distance_value[ghostdist[0]][ghostdist[1]]
    else:
        for i in range(ghostnum):
            if Ghost.ghostvector[i].if_scared==1:
                ghostvalue+=scared_value[ghostdist[i]]
            else:
                ghostvalue+=ghost_one_value[ghostdist[i]]
        
    if fooddis>=len(food_distance_value):
        fooddis=len(food_distance_value)-1
    
    if fooddis==const_inf and capsuledis==const_inf:
        foodvalue=0
    elif Pacman.pacmanobject.invtime>0:
        if capsuledis<=fooddis:
            foodvalue=-1*capsule_distance_value[capsuledis]
        else:
            foodvalue=food_distance_value[fooddis]
    elif Pacman.pacmanobject.invtime==0:
        if capsuledis<=fooddis:
            foodvalue=capsule_distance_value[capsuledis]
        else:
            foodvalue=food_distance_value[fooddis]
    
        
    return foodvalue+ghostvalue
        
        
        
    
#minimax search

#Pacman's turn
def max_search(depth,pacmanx:int,pacmany:int,ghostx:list,ghosty:list,ghostnum:int):
    maxvalue=-const_inf
    maxchoice=-1
    if depth>=2:
        return (None,reward(pacmanx,pacmany,ghostx,ghosty,ghostnum))
    elif Map.mapobject.get_ifeaten(pacmanx,pacmany)==1:
        return (None,reward(pacmanx,pacmany,ghostx,ghosty,ghostnum))
    for i in range(4):
        newx=pacmanx+Directions.movevector[i][0]
        newy=pacmany+Directions.movevector[i][1]
        if Pacman.pacmanmap_valid(newx,newy)==False:
            continue
        tempans=min_search(depth,newx,newy,ghostx,ghosty,ghostnum,0)
        if tempans[1]>maxvalue:
            maxvalue=tempans[1]
            maxchoice=i
    return (maxchoice,maxvalue)

#Ghost's turn 
def min_search(depth,pacmanx:int,pacmany:int,ghostx:list,ghosty:list,ghostnum:int,nowghost:int):
    minvalue=const_inf
    minchoice=-1
    for i in range(ghostnum):
        if pacmanx==ghostx[i] and pacmany==ghosty[i]:
            return (None,-const_inf)
    for i in range(4):
        newghostx=ghostx[nowghost]+Directions.movevector[i][0]
        newghosty=ghosty[nowghost]+Directions.movevector[i][1]
        
        newghostxlist=copy.copy(ghostx)
        newghostylist=copy.copy(ghosty)
        newghostxlist[nowghost]=newghostx
        newghostylist[nowghost]=newghosty
        
        if Ghost.ghostmap_valid(newghostx[0],newghosty[0])==False:
            continue
        if nowghost==ghostnum-1:
            tempans=max_search(depth+1,pacmanx,pacmany,newghostxlist,newghostylist,ghostnum)
        else:
            tempans=min_search(depth,pacmanx,pacmany,newghostxlist,newghostylist,ghostnum,nowghost+1)
        if tempans[1]<minvalue:
            minvalue=tempans[1]
            minchoice=i
    return (minchoice,minvalue)
    
def minimax_search():
    global system_default_ghost_num
    if Map.mapobject.if_win()==True:
        return -1
    temppacman=Pacman.pacmanobject
    temppacmanpos=temppacman.getposition()
    tempghostx=[]
    tempghosty=[]
    for i in range(system_default_ghost_num):
        tempghost=Ghost.ghostvector[i]
        tempghostpos=tempghost.getposition()
        tempghostx.append(tempghostpos[0])
        tempghosty.append(tempghostpos[1])
    ans=max_search(0,temppacmanpos[0],temppacmanpos[1],tempghostx,tempghosty,system_default_ghost_num)
    return ans[0]


#minimax search with alpha-beta prune

def max_search_upgraded(depth,mina,maxb,pacmanx:int,pacmany:int,ghostx:list,ghosty:list,ghostnum:int):
    # print("maxsearch:"+str(depth)+" "+str(mina)+" "+str(maxb))
    maxvalue=-const_inf
    maxchoice=-1
    if depth>=2:
        return (-1,reward(pacmanx,pacmany,ghostx,ghosty,ghostnum))
    elif Map.mapobject.get_ifeaten(pacmanx,pacmany)==1:
        return (-1,reward(pacmanx,pacmany,ghostx,ghosty,ghostnum))
    for i in range(ghostnum):
        if pacmanx==ghostx[i] and pacmany==ghosty[i]:
            return (-1,-const_inf)
        
    for i in range(4):
        newx=pacmanx+Directions.movevector[i][0]
        newy=pacmany+Directions.movevector[i][1]
        if Pacman.pacmanmap_valid(newx,newy)==False:
            continue
        
        if system_default_ghost_num>0:
            tempans=min_search_upgraded(depth,mina,maxb,newx,newy,ghostx,ghosty,ghostnum)
        else:
            tempans=max_search_upgraded(depth+1,mina,maxb,pacmanx,pacmany,ghostx,ghosty,ghostnum)
            
        if tempans[1]>=maxb:
            return (-1,-const_inf)
        mina=max(mina,maxvalue)
        if tempans[1]>maxvalue:
            maxvalue=tempans[1]
            maxchoice=i
        elif tempans[1]==maxvalue:
            temprand=random.random()
            if temprand<0.5:
                maxvalue=tempans[1]
                maxchoice=i    
    return (maxchoice,maxvalue)

#Ghost's turn 
def min_search_upgraded(depth,mina,maxb,pacmanx:int,pacmany:int,ghostx:list,ghosty:list,ghostnum:int):
    # print("minsearch:"+str(depth)+" "+str(mina)+" "+str(maxb))
    minvalue=const_inf
    minchoice=-1
    for i in range(ghostnum):
        if pacmanx==ghostx[i] and pacmany==ghosty[i]:
            return (-1,-const_inf)
    for i in range(5):
        for j in range(5):
            newghostx=copy.copy(ghostx)
            newghosty=copy.copy(ghosty)
            if ghostnum<=0:
                newghostx[0]=0
                newghostx[0]=0
            if i!=4:
                newghostx[0]=newghostx[0]+Directions.movevector[i][0]
                newghosty[0]=newghosty[0]+Directions.movevector[i][1]
                
            if ghostnum<=1:
                if j>0:
                    continue
            elif j!=4:
                newghostx[1]=newghostx[1]+Directions.movevector[j][0]
                newghosty[1]=newghosty[1]+Directions.movevector[j][1]
            
            if ghostnum>1:
                if Ghost.ghostmap_valid(newghostx[0],newghosty[0])==False or Ghost.ghostmap_valid(newghostx[1],newghosty[1])==False:
                    continue
            elif ghostnum>0:
                if Ghost.ghostmap_valid(newghostx[0],newghosty[0])==False:
                    continue
            tempans=max_search_upgraded(depth+1,mina,maxb,pacmanx,pacmany,newghostx,newghosty,ghostnum)
            
            if tempans[1]<=mina:
                return (-1,-const_inf)
            maxb=max(maxb,minvalue)
            
            if tempans[1]<minvalue:
                minvalue=tempans[1]
                minchoice=i
    return (minchoice,minvalue)

def minimax_search_with_alphabeta(ghostnum):
    temppacman=Pacman.pacmanobject
    temppacmanpos=temppacman.getposition()
    tempghostx=[]
    tempghosty=[]
    for i in range(ghostnum):
        tempghost=Ghost.ghostvector[i]
        tempghostpos=tempghost.getposition()
        tempghostx.append(tempghostpos[0])
        tempghosty.append(tempghostpos[1])
    ans=max_search_upgraded(0,-const_inf,const_inf,temppacmanpos[0],temppacmanpos[1],tempghostx,tempghosty,ghostnum)
    # print("--Search Ended--")
    return ans[0]

def Qlearningmethod(ghostnum):
    if Map.mapobject.if_win()==True:
        return -1
    temppacmapos=Pacman.pacmanobject.getposition()
    pacposidx=getposindex(temppacmapos[0],temppacmapos[1])
    if ghostnum>0:
        ghost0pos=Ghost.ghostvector[0].getposition()
        gho0posidx=getposindex(ghost0pos[0],ghost0pos[1])
    else:
        gho0posidx=0
    if ghostnum>1:
        ghost1pos=Ghost.ghostvector[1].getposition()
        gho1posidx=getposindex(ghost1pos[0],ghost1pos[1])
    else:
        gho1posidx=0
    beststra=Qtable.qtableobj.find_beststra([pacposidx,gho0posidx,gho1posidx])
    if beststra==None:
        if if_qlearning_help==1:
            return minimax_search_with_alphabeta(ghostnum)
        else:
            return -1
    else:
        return beststra[0]
    