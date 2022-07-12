from Parameter import *
from Util import Directions,Map
from Agents import Pacman,Ghost,pacmanmap_valid

DFSgoal=None
def DFS_shortest_origin(nowx,nowy):
    global dfs_visitmap
    tempmap=Map.mapobject
    tempsize=tempmap.get_size()
    print("DFSsearch11:"+str(nowx)+" "+str(nowy))
    shortest=const_inf
    shortest_dir=0
    if tempmap.get_ifeaten(nowx,nowy)==1:
        return 0,0
    else:
        dfs_visitmap[nowx][nowy]=1
        for i in range(4):
            tempvector=Directions.getmove(i)
            if pacmanmap_valid(nowx+tempvector[0],nowy+tempvector[1])==True and \
            dfs_visitmap[nowx+tempvector[0]][nowy+tempvector[1]]==0:
                temp_dis,temp_dir= DFS_shortest_origin(nowx+tempvector[0],nowy+tempvector[1])
                if temp_dis+1<shortest:
                    shortest=temp_dis+1
                    shortest_dir=i
        dfs_visitmap[nowx][nowy]=0
        return shortest,shortest_dir


def DFS_shortest_altered(nowx,nowy):
    global dfs_visitmap
    tempmap=Map.mapobject
    tempsize=tempmap.get_size()
    # print("DFSsearch:"+str(nowx)+" "+str(nowy))
    shortest=const_inf
    shortest_dir=0
    # if dfs_visitmap[nowx][nowy]==1:
    #     return -1,0
    dfs_visitmap[nowx][nowy]=1
    if tempmap.get_ifeaten(nowx,nowy)==1:
        return nowx,nowy
    else:
        for i in range(4):
            tempvector=Directions.getmove(i)
            if pacmanmap_valid(nowx+tempvector[0],nowy+tempvector[1])==True and \
            dfs_visitmap[nowx+tempvector[0]][nowy+tempvector[1]]==0:
                if_able=True
                temp_x,temp_y= DFS_shortest_altered(nowx+tempvector[0],nowy+tempvector[1])
                if temp_x>=0 and temp_y>=0:
                    return temp_x,temp_y
        return -1,-1

def clearDFS():
    global DFSgoal
    DFSgoal=None

###-------------------------###

def BFS_shortest(nowx,nowy):
    global if_bfssh,bfs_visitmap,bfs_dire
    # print("len:"+str(len(bfs_dire)))
    tempmap=Map.mapobject
    temp_BFSqueue=[]
    temp_BFSqueue.append((nowx,nowy,0,0))
    while len(temp_BFSqueue)>0:
        temp_front=temp_BFSqueue[0] 
        temp_BFSqueue=temp_BFSqueue[1:]
        temp_x=temp_front[0]
        temp_y=temp_front[1]
        if temp_front[2]>=bfs_visitmap[temp_x][temp_y]:
            continue
        if pacmanmap_valid(temp_x,temp_y)==False:
            continue
        # print(temp_front)
        bfs_visitmap[temp_front[0]][temp_front[1]]=temp_front[2]
        bfs_dire[temp_x][temp_y]=temp_front[3]
        if tempmap.get_ifeaten(temp_x,temp_y)==1:
            while True:
                # print("temp:"+str(temp_x)+" "+str(temp_y))
                temp_direction=bfs_dire[temp_x][temp_y]
                tempvector=Directions.getmove(temp_direction)
                # print(temp_direction)
                if temp_x+tempvector[0]==nowx and temp_y+tempvector[1]==nowy:
                    return (temp_direction+2)%4
                else:
                    temp_x+=tempvector[0]
                    temp_y+=tempvector[1]
        for i in range(4):
            tempvector=Directions.getmove(i)
            if pacmanmap_valid(temp_x+tempvector[0],temp_y+tempvector[1])==True:
                temp_BFSqueue.append((temp_x+tempvector[0],temp_y+tempvector[1],bfs_visitmap[temp_x][temp_y]+1,(i+2)%4 ))
    return -1
            


#greedy search based on BFS
def greedy_search_bfs():
    global if_bfssh,bfs_visitmap,bfs_dire
    if Map.mapobject.if_win()==True:
        return -1
    bfs_visitmap=[]
    bfs_dire=[]
    for i in range(map_size):
        bfs_visitmap.append([])
        bfs_dire.append([])
        for j in range(map_size):
            bfs_visitmap[i].append(const_inf)
            bfs_dire[i].append(-1)
    #find the shortest way
    tempdic=Pacman.pacmanobject.getposition()
    temp_direction=BFS_shortest(tempdic[0],tempdic[1])
    # print("BFS:"+str(temp_direction))
    # print("ans:"+str(temp_direction))
    return temp_direction

#greedy search based on DFS
def greedy_search_dfs():
    global dfs_visitmap,DFSgoal
    tempsize=Map.mapobject.get_size()
    tempdic=Pacman.pacmanobject.getposition()
    if Map.mapobject.if_win()==True:
        return -1
    if DFSgoal==None or (tempdic[0]==DFSgoal[0] and tempdic[1]==DFSgoal[1]):
        dfs_visitmap=[[0 for i in range(tempsize[1]) ]for j in range(tempsize[0])]
        temp_ans=DFS_shortest_altered(tempdic[0],tempdic[1])
        temp_way=how_to_go(tempdic[0],tempdic[1],temp_ans[0],temp_ans[1])
        DFSgoal=temp_ans
        #find the shortest way
        # print("DFS:"+str(temp_ans))
        # print("ans:"+str(temp_direction))
        return temp_way[1][2]
    else:
        temp_way=how_to_go(tempdic[0],tempdic[1],DFSgoal[0],DFSgoal[1])
        return temp_way[1][2]


#find nearest
def find_nearest(nowx,nowy):
    tempmap=Map.mapobject
    tempsize=tempmap.get_size()
    temp_BFSqueue=[]
    nearestdis=None
    ifvisitmap=[[0 for i in range(tempsize[1])] for j in range(tempsize[0])]
    tempans=[]
    temp_BFSqueue.append((nowx,nowy,0))
    while len(temp_BFSqueue)>0:
        temp_front=temp_BFSqueue[0] 
        temp_BFSqueue=temp_BFSqueue[1:]
        temp_x=temp_front[0]
        temp_y=temp_front[1]
        if pacmanmap_valid(temp_x,temp_y)==False:
            continue
        if ifvisitmap[temp_x][temp_y]==1:
            continue
        if nearestdis!=None and temp_front[2]>nearestdis:
            continue
        ifvisitmap[temp_x][temp_y]=1
        if tempmap.get_ifeaten(temp_x,temp_y)==1:
            nearestdis=temp_front[2]
            tempans.append((temp_x,temp_y))
        for i in range(4):
            tempvector=Directions.getmove(i)
            if pacmanmap_valid(temp_x+tempvector[0],temp_y+tempvector[1])==True:
                temp_BFSqueue.append((temp_x+tempvector[0],temp_y+tempvector[1],temp_front[2]+1))
    return tempans


#using BFS, return a list showing how to go from (x,y) to (u,v)
def how_to_go(beginx,beginy,endx,endy):
    tempmap=Map.mapobject
    tempsize=tempmap.get_size()
    temp_BFSqueue=[]
    vectormap=[[None for i in range(tempsize[1])] for j in range(tempsize[0])]
    temp_BFSqueue.append((beginx,beginy,-1))
    while len(temp_BFSqueue)>0:
        temp_front=temp_BFSqueue[0] 
        temp_BFSqueue=temp_BFSqueue[1:]
        temp_x=temp_front[0]
        temp_y=temp_front[1]
        if pacmanmap_valid(temp_x,temp_y)==False:
            continue
        if vectormap[temp_x][temp_y]!=None:
            continue
        vectormap[temp_front[0]][temp_front[1]]=temp_front[2]
        if temp_x==endx and temp_y==endy:
            tempans=[]
            while True:
                # print("temp:"+str(temp_x)+" "+str(temp_y))
                if temp_x==beginx and temp_y==beginy:
                    tempans.append((beginx,beginy,-1))
                    tempans.reverse()
                    return tempans
                temp_direction=vectormap[temp_x][temp_y]
                tempans.append((temp_x,temp_y,temp_direction))
                tempvector=Directions.getmove(temp_direction)
                temp_x-=tempvector[0]
                temp_y-=tempvector[1]
        for i in range(4):
            tempvector=Directions.getmove(i)
            if pacmanmap_valid(temp_x+tempvector[0],temp_y+tempvector[1])==True:
                temp_BFSqueue.append((temp_x+tempvector[0],temp_y+tempvector[1],i))


def floyd_algo():
    global mapdis
    tempmap=Map.mapobject
    mapdis=[]
    for i in range(map_height):
        mapdis.append([])
        for j in range(map_height):
            mapdis[i].append([])
    print(mapdis)
    

#greedy search based on massive Analysis
def all_manhattan(nowx,nowy):
    tempmap=Map.mapobject
    tempsize=tempmap.get_size()
    tempans=0
    for i in range(tempsize[0]):
        for j in range(tempsize[1]):
            if tempmap.get_ifeaten(i,j)==1:
                tempans+=abs(i-nowx)+abs(i-nowy)
    return tempans
            

manhanttangoal=None
to_manhanttan=[]
def greedy_search_massive_manhattan():
    global manhanttangoal,to_manhanttan
    tempmap=Map.mapobject
    if tempmap.if_win()==True:
        manhanttangoal=None
        to_manhanttan=[]
        return -1
    temppacman=Pacman.pacmanobject
    nowdic=temppacman.getposition()
    if manhanttangoal==None or manhanttangoal==tuple(nowdic):
        temp_possiblegoal=find_nearest(nowdic[0],nowdic[1])
        if temp_possiblegoal==[]:
            return -1
        tempmindis=const_inf
        for i in temp_possiblegoal:
            choicedis=all_manhattan(i[0],i[1])
            if choicedis<tempmindis:
                tempmindis=choicedis
                manhanttangoal=i
                to_manhanttan=how_to_go(nowdic[0],nowdic[1],i[0],i[1])
        # print(to_manhanttan)
        return to_manhanttan[1][2]
    else:
        # print("nowdic:"+str(nowdic))
        for i in range(len(to_manhanttan)):
            if to_manhanttan[i][0]==nowdic[0] and to_manhanttan[i][1]==nowdic[1]:
                # print(i)
                return to_manhanttan[i+1][2]
            
    
    
    # print(find_nearest(nowdic[0],nowdic[1]))
    # print(how_to_go(nowdic[0],nowdic[1],15,15))
    # if if_manhattangoal==None or 1:
        
def clear_manhanttan():
    global manhanttangoal,to_manhanttan
    manhanttangoal=None
    to_manhanttan=[]


DPway=None
# DPmethod=[]
def cleardp():
    global DPway
    DPway=None
    
def dp():
    global DPway
    tempobj=[]
    dparr=[]
    tempmap=Map.mapobject
    tempsize=tempmap.get_size()
    tempdic=Pacman.pacmanobject.getposition()
    if tempmap.if_win()==True:
        return -1
    if DPway==None:
        for i in range(tempsize[0]):
            for j in range(tempsize[1]):
                if tempmap.get_ifeaten(i,j)==1:
                    tempobj.append((i,j))
        # print(tempobj)
        if len(tempobj)>15:
            return -1
        templen=len(tempobj)
        dparr=[[const_inf,0] for j in range(2**templen+1)]
        dparr[0][0]=0
        # print(dparr)
        for i in range(2**templen):
            tempbinarr=[0 for i in range(templen)]
            ibin=bin(i)
            lenibin=len(ibin)
            if i!=0:
                fromwhere=dparr[i][1]
                for j in range(lenibin-1,1,-1):
                    tempbinarr[lenibin-1-j]=int(ibin[j])
                for j in range(templen):
                    if tempbinarr[j]==0:
                        dis=len(how_to_go(tempobj[fromwhere][0],tempobj[fromwhere][1],tempobj[j][0],tempobj[j][1]))-1
                        if dparr[i][0]+dis<dparr[i+2**j][0]:
                            dparr[i+2**j][0]=dparr[i][0]+dis
                            dparr[i+2**j][1]=j
            else:
                for i in range(templen):
                    dis=len(how_to_go(tempdic[0],tempdic[1],tempobj[i][0],tempobj[i][1]))-1
                    if dis<dparr[2**i][0]:
                        dparr[2**i][0]=dis
                        dparr[2**i][1]=i
        DPway=[]
        j=2**templen-1
        while j>0:
            k=dparr[j][1]
            DPway.append([tempobj[k][0],tempobj[k][1],k])
            j-=2**k
        # print(DPway)
    for i in range(len(DPway)):
        if tempmap.get_ifeaten(DPway[i][0],DPway[i][1])==0:
            continue
        templist=how_to_go(tempdic[0],tempdic[1],DPway[i][0],DPway[i][1])
        return templist[1][2]
    return -1
    # print(dparr)