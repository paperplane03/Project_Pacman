from curses import window
import os,sys
from black import main
import pygame
from pygame.locals import *
import random
import copy
###
windows_length=0
windows_height=0
map=[]
if_eaten=[]
direction_x=[1,0,-1,0]
direction_y=[0,1,0,-1]
blockgeneratePossibly=0.4

###
# block:40*40
# map: 10*10
# screen:960*640
os.chdir("D:\zhongyunhua\Project_Pacman")
score=1
block_size=40
mapboarder_buffer=40
map_size=16
clock=pygame.time.Clock()
if_bfssh=0
const_inf=10000000
autospeed=200

def imageinit():
    global apple_image,block_image
    global block_image_E,block_image_W,block_image_N,block_image_S
    global block_image_SE,block_image_SW,block_image_NE,block_image_NW
    global pacman_image_left,pacman_image_north,pacman_image_right,pacman_image_south
    global pacman_image_none
    global pacman_orient,ghost_image
    
    apple_image=pygame.image.load('./pic/apple.jpg')
    block_image=pygame.image.load('./pic/block.jpg')
    block_image_E=pygame.image.load('./pic/E.jpg')
    block_image_W=pygame.image.load('./pic/W.jpg')
    block_image_N=pygame.image.load('./pic/N.jpg')
    block_image_S=pygame.image.load('./pic/S.jpg')

    block_image_SE=pygame.image.load('./pic/SE.jpg')
    block_image_SW=pygame.image.load('./pic/SW.jpg')
    block_image_NE=pygame.image.load('./pic/NE.jpg')
    block_image_NW=pygame.image.load('./pic/NW.jpg')
    
    pacman_image_right=pygame.image.load('./pic/pacman_right.png')
    pacman_image_left=pygame.image.load('./pic/pacman_left.png')
    pacman_image_north=pygame.image.load('./pic/pacman_north.png')
    pacman_image_south=pygame.image.load('./pic/pacman_south.png')
    pacman_image_none=pygame.image.load('./pic/pacman_none.png')
    pacman_orient=0
    ghost_image=pygame.image.load('./pic/ghost.png')

def initsize():
    global main_screen
    global windows_length,windows_height
    global font16,font32,font_height
    global pacman_x,pacman_y,scores
    global ghost_x,ghost_y,ghost_num
    global if_pacmanmouse_open
    global autospeed
    global navigating_method  #0 for play, 1 for greedy, 2 for DFS
    pygame.init()
    pygame.display.set_caption("pacman")
    windows_length=block_size*map_size
    windows_height=block_size*map_size
    if_pacmanmouse_open=1
    main_screen=pygame.display.set_mode((2*mapboarder_buffer+windows_length+320,windows_height+2*mapboarder_buffer))
    
    font16=pygame.font.SysFont("arial",16)
    font32=pygame.font.SysFont("arial",32)
    font_height=font16.get_linesize()
    
    #signal 25, for flush 
    pygame.time.set_timer(25,300)
    #signal 26, for automating frequency
    pygame.time.set_timer(26,autospeed)
    
    navigating_method=0
    scores=0
    pacman_x=pacman_y=0
    ghost_num=0
    ghost_x=[15,0,15]
    ghost_y=[0,15,15]
    
def setbutton():
    global score_text,textRect
    global restart_button,restartRect
    global autofind_greedy_button,autofindRect
    global manual_button,manualRect
    global randommapRect,randommap_button
    #Text Scores:
    score_text=font32.render("Scores:"+str(scores),True,(255,255,255),(0,0,0))
    textRect=score_text.get_rect()
    textRect.center=(800,80)
    
    #Restart Button
    restart_button=font32.render("Restart",True,(255,255,255),(255,0,0))
    restartRect=restart_button.get_rect()
    restartRect.center=(800,320)
    
    #autofind_greedy
    autofind_greedy_button=font32.render("Auto(Greedy Algo)",True,(255,255,255),(255,0,0))
    autofindRect=autofind_greedy_button.get_rect()
    autofindRect.center=(870,400)
    
    #Manual Button
    manual_button=font32.render("Manual",True,(255,255,255),(255,0,0))
    manualRect=manual_button.get_rect()
    manualRect.center=(800,480)
    
    #Random Map Button
    randommap_button=font32.render("Random Map",True,(255,255,255),(255,0,0))
    randommapRect=randommap_button.get_rect()
    randommapRect.center=(840,560)
    
    #add Ghost
    # ghostone_button=font32
   
        
 
def input_file():
    global map_input,map,if_eaten
    map_input=open("./map.txt",'r')
    i=0
    map=[]
    if_eaten=[]
    for lines in map_input.readlines():
        i+=1
        map.append([])
        if_eaten.append([])
        mapline=lines.split(" ")
        for words in mapline:  
            map[i-1].append(int(words))
            if_eaten[i-1].append(0)
    print(i)
    # print(map)
    map_input.close()

def generatevalid(x,y):
    global temp_mapinput
    if x<0 or x>=map_size:
        return False
    if y<0 or y>=map_size:
        return False
    if temp_mapinput[x][y]>=1:
        return False
    return True

def checkconnecting(iflast=False):
    global temp_mapinput
    tempqueue=[]
    nowfrontnum=0
    check=[[0 for i in range(map_size)] for j in range(map_size)]
    # print(check)
    for i in range(map_size):
        for j in range(map_size):
            if check[i][j]==0 and temp_mapinput[i][j]==0:
                if iflast==True:
                    print("pair:",end="")
                    print(i,j)
                nowfrontnum+=1
                tempqueue.append((i,j))
                while len(tempqueue)>0:
                    tempx,tempy=tempqueue[0]
                    tempqueue.pop(0)
                    if check[tempx][tempy]!=0:
                        continue
                    check[tempx][tempy]=nowfrontnum
                    for k in range(4):
                        if generatevalid(tempx+direction_x[k],tempy+direction_y[k])==True and\
                        check[tempx+direction_x[k]][tempy+direction_y[k]]==0:
                            tempqueue.append((tempx+direction_x[k],tempy+direction_y[k]))
    # print(nowfrontnum)
    return nowfrontnum 
                
                
def randomized_start():
    global map,if_eaten,temp_mapinput
    global pacman_x,pacman_y
    global blockgeneratePossibly
    pacman_x=random.randint(0,15)
    pacman_y=random.randint(0,15)
    temp_mapinput=[[0 for i in range(map_size)] for j in range(map_size)]
    if_eaten=[[0 for i in range(map_size)] for j in range(map_size)]
    for i in range(map_size):
        for j in range(map_size):
            if i==pacman_x and j==pacman_y:
                continue
            temp_mapinput[i][j]=1
            connectnum=checkconnecting()
            temp_mapinput[i][j]=0
            if connectnum==1:
                temp_randomint=random.random()
                if temp_randomint<blockgeneratePossibly:
                    temp_mapinput[i][j]=1
    # for i in range(map_size):
    #     map_input.append([])
    #     for j in range(map_size):
    #         map_input[i].append(temp_mapinput[i][j])
            # print(str(temp_mapinput[i][j])+" ",end="")
        # print("")
    print(checkconnecting(iflast=True))
    map=copy.deepcopy(temp_mapinput)
    return None
                
        
def pacmanmap_valid(mapx,mapy):
    if mapx>=0 and mapx<map_size and mapy>=0 and mapy<map_size:
        if map[mapx][mapy]==0:
            return True
        else:
            return False
    else:
        return False

def ghostmap_valid(mapx,mapy):
    for i in range(ghost_num):
        if ghost_x[i]==mapx and ghost_y[i]==mapy:
            return False
    if mapx>=0 and mapx<map_size and mapy>=0 and mapy<map_size:
        if map[mapx][mapy]==0:
            return True
        else:
            return False
    else:
        return False

def if_dead(mapx,mapy):
    for j in range(ghost_num):
        if mapx==ghost_x[j] and mapy==ghost_y[j]:
            return True
    return False    

def if_win():
    for i in range(map_input):
        for j in range(map_input):
            if map[i][j]==0 and if_eaten[i][j]==0:
                return False
    return True
            
def ghostpanel():
    for i in range(ghost_num):
        temp_flag=1
        for j in range(4):
            if ghostmap_valid(ghost_x[i]+direction_x[j],ghost_y[i]+direction_y[j])==True:
                temp_flag=0
        if temp_flag==1:
            return None
        while True:
            temp_randint=random.randint(0,3)
            if ghostmap_valid(ghost_x[i]+direction_x[temp_randint],ghost_y[i]+direction_y[temp_randint])==True:
                ghost_x[i]+=direction_x[temp_randint]
                ghost_y[i]+=direction_y[temp_randint]
                break
    return None
            
            
def repainting(pacman_direction,if_first=0):
    
    main_screen.fill((0,0,0))
    
    #painting map
    if True:
        for i in range(map_size):
            for j in range(map_size):
                if map[i][j]>=1:
                    main_screen.blit(block_image,(i*40+mapboarder_buffer,j*40+mapboarder_buffer,40,40))
                elif if_eaten[i][j]==0:
                    main_screen.blit(apple_image,(i*40+mapboarder_buffer,j*40+mapboarder_buffer,40,40))
    
    #painting pacman
    if if_pacmanmouse_open==1:
        if pacman_direction==3:
            main_screen.blit(pacman_image_north,(pacman_x*block_size+mapboarder_buffer,pacman_y*block_size+mapboarder_buffer))
        if pacman_direction==1:
            main_screen.blit(pacman_image_south,(pacman_x*block_size+mapboarder_buffer,pacman_y*block_size+mapboarder_buffer))
        if pacman_direction==2:
            main_screen.blit(pacman_image_left,(pacman_x*block_size+mapboarder_buffer,pacman_y*block_size+mapboarder_buffer))
        if pacman_direction==0:
            main_screen.blit(pacman_image_right,(pacman_x*block_size+mapboarder_buffer,pacman_y*block_size+mapboarder_buffer))
    else:
        main_screen.blit(pacman_image_none,(pacman_x*block_size+mapboarder_buffer,pacman_y*block_size+mapboarder_buffer))
    #painting ghost
    for i in range(ghost_num):
        main_screen.blit(ghost_image,(ghost_x[i]*block_size+mapboarder_buffer,ghost_y[i]*block_size+mapboarder_buffer))
    
    #painting lines
    for i in range(map_size+1):
        pygame.draw.line(main_screen,(255,255,255),(40*(i+1),mapboarder_buffer),(40*(i+1),windows_height+mapboarder_buffer),width=1)
        pygame.draw.line(main_screen,(255,255,255),(mapboarder_buffer,40*(i+1)),(windows_length+mapboarder_buffer,40*(i+1)),width=1)
    
    #painting border lines
    pygame.draw.line(main_screen,(0,255,255),(mapboarder_buffer/2,mapboarder_buffer/2),(mapboarder_buffer/2,map_size*block_size+3/2*mapboarder_buffer),width=3)
    pygame.draw.line(main_screen,(0,255,255),(mapboarder_buffer/2,mapboarder_buffer/2),(map_size*block_size+3/2*mapboarder_buffer,mapboarder_buffer/2),width=3)
    pygame.draw.line(main_screen,(0,255,255),(map_size*block_size+3/2*mapboarder_buffer,mapboarder_buffer/2),(map_size*block_size+3/2*mapboarder_buffer,map_size*block_size+3/2*mapboarder_buffer),width=3)
    pygame.draw.line(main_screen,(0,255,255),(mapboarder_buffer/2,map_size*block_size+3/2*mapboarder_buffer),(map_size*block_size+3/2*mapboarder_buffer,map_size*block_size+3/2*mapboarder_buffer),width=3)
    
    #painting parting lines
    pygame.draw.line(main_screen,(0,255,255),(mapboarder_buffer*2+map_size*block_size,0),(mapboarder_buffer*2+map_size*block_size,windows_height+2*mapboarder_buffer),width=3)
    
    #painting scores
    score_text=font32.render("Scores:"+str(scores),True,(255,255,255),(0,0,0))
    
    #painting scores and restart button
    main_screen.blit(score_text, textRect)
    main_screen.blit(restart_button,restartRect)
    
    pygame.draw.line(main_screen,(255,255,255),(750,290),(850,290))
    pygame.draw.line(main_screen,(255,255,255),(750,350),(850,350))
    pygame.draw.line(main_screen,(255,255,255),(750,290),(750,350))
    pygame.draw.line(main_screen,(255,255,255),(850,290),(850,350))
    
    #painting greedy button
    main_screen.blit(autofind_greedy_button,autofindRect)
    pygame.draw.line(main_screen,(255,255,255),(750,370),(990,370))
    pygame.draw.line(main_screen,(255,255,255),(750,430),(990,430))
    pygame.draw.line(main_screen,(255,255,255),(750,370),(750,430))
    pygame.draw.line(main_screen,(255,255,255),(990,370),(990,430))
    
    #painting manual button
    main_screen.blit(manual_button,manualRect)
    pygame.draw.line(main_screen,(255,255,255),(750,450),(850,450))
    pygame.draw.line(main_screen,(255,255,255),(750,510),(850,510))
    pygame.draw.line(main_screen,(255,255,255),(750,450),(750,510))
    pygame.draw.line(main_screen,(255,255,255),(850,450),(850,510))
    
    #painting random-map button
    main_screen.blit(randommap_button,randommapRect)
    pygame.draw.line(main_screen,(255,255,255),(750,530),(930,530))
    pygame.draw.line(main_screen,(255,255,255),(750,590),(930,590))
    pygame.draw.line(main_screen,(255,255,255),(750,530),(750,590))
    pygame.draw.line(main_screen,(255,255,255),(930,530),(930,590))

def DFS_shortest(nowx,nowy):
    # print("BFSsearch:"+str(nowx)+" "+str(nowy))
    shortest=const_inf
    shortest_dir=0
    if if_eaten[nowx][nowy]==0:
        return 0,0
    else:
        bfs_visitmap[nowx][nowy]=1
        for i in range(4):
            if pacmanmap_valid(nowx+direction_x[i],nowy+direction_y[i])==True and \
            bfs_visitmap[nowx+direction_x[i]][nowy+direction_y[i]]==0:
                temp_dis,temp_dir= DFS_shortest(nowx+direction_x[i],nowy+direction_y[i])
                if temp_dis+1<shortest:
                    shortest=temp_dis+1
                    shortest_dir=i
        bfs_visitmap[nowx][nowy]=0
        return shortest_dir

def BFS_shortest(nowx,nowy):
    global if_bfssh,bfs_visitmap,bfs_dire
    # print("len:"+str(len(bfs_dire)))
    temp_BFSqueue=[]
    temp_BFSqueue.append((nowx,nowy,0,0))
    while len(temp_BFSqueue)>0:
        temp_front=temp_BFSqueue[0] 
        temp_BFSqueue=temp_BFSqueue[1:]
        temp_x=temp_front[0]
        temp_y=temp_front[1]
        if temp_front[2]>=bfs_visitmap[temp_x][temp_y]:
            continue
        # print(temp_front)
        bfs_visitmap[temp_front[0]][temp_front[1]]=temp_front[2]
        bfs_dire[temp_x][temp_y]=temp_front[3]
        if if_eaten[temp_x][temp_y]==0:
            while True:
                # print(str(temp_x)+" "+str(temp_y))
                temp_direction=bfs_dire[temp_x][temp_y]
                # print(temp_direction)
                if temp_x+direction_x[temp_direction]==nowx and temp_y+direction_y[temp_direction]==nowy:
                    return (temp_direction+2)%4
                else:
                    temp_x+=direction_x[temp_direction]
                    temp_y+=direction_y[temp_direction]
        for i in range(4):
            if pacmanmap_valid(temp_x+direction_x[i],temp_y+direction_y[i])==True:
                temp_BFSqueue.append((temp_x+direction_x[i],temp_y+direction_y[i],bfs_visitmap[temp_x][temp_y]+1,(i+2)%4 ))
    return -1
            
    
#greedy search based on BFS
def greedy_search():
    if score==155:
        return -1
    global if_bfssh,bfs_visitmap,bfs_dire
    bfs_visitmap=[]
    bfs_dire=[]
    for i in range(map_size):
        bfs_visitmap.append([])
        bfs_dire.append([])
        for j in range(map_size):
            bfs_visitmap[i].append(const_inf)
            bfs_dire[i].append(-1)
    #find the shortest way
    temp_direction=BFS_shortest(pacman_x,pacman_y)
    # print("BFS:"+str(temp_direction))
    return temp_direction
    
def restart(randomized=False):
    global if_eaten
    global pygame_event_text
    initsize()
    if randomized==False:
        input_file()
    else:
        randomized_start()
    if_eaten[pacman_x][pacman_y]=1
    repainting(3,1)
    pygame_event_text=[]
    pygame.event.set_blocked(MOUSEMOTION)
    
# restart()
if __name__=="__main__":
    imageinit()
    initsize()
    setbutton()
    input_file()
    if_eaten[pacman_x][pacman_y]=1
    repainting(3,1)
    pygame_event_text=[]
    pygame.event.set_blocked(MOUSEMOTION)


    while True:
        now_event=pygame.event.get()
        if len(now_event)>0:
            # print(len(now_event))
            for every_event in now_event:
                # print(str(every_event))
                if every_event.type==QUIT:
                    exit()
                if every_event.type==25:
                    if_pacmanmouse_open=1-if_pacmanmouse_open
                    # print(str(every_event))
                if every_event.type==26:
                    if navigating_method==1:
                        temp_moveaction=greedy_search()
                        if temp_moveaction!=-1:
                            pacman_x+=direction_x[temp_moveaction]
                            pacman_y+=direction_y[temp_moveaction]
                            pacman_orient=temp_moveaction
                            ghostpanel()
                            if if_eaten[pacman_x][pacman_y]==0:
                                if_eaten[pacman_x][pacman_y]=1
                                scores+=1
                if every_event.type==KEYDOWN and navigating_method==0:
                    if every_event.key==K_w:
                        if pacmanmap_valid(pacman_x,pacman_y-1)==True:
                            pacman_y=max(0,pacman_y-1)
                        pacman_orient=3
                    elif every_event.key==K_s:
                        if pacmanmap_valid(pacman_x,pacman_y+1)==True:
                            pacman_y=min(map_size-1,pacman_y+1)
                        pacman_orient=1
                    elif every_event.key==K_a:
                        if pacmanmap_valid(pacman_x-1,pacman_y)==True:
                            pacman_x=max(0,pacman_x-1)
                        pacman_orient=2
                    elif every_event.key==K_d:
                        if pacmanmap_valid(pacman_x+1,pacman_y)==True:
                            pacman_x=min(map_size-1,pacman_x+1)
                        pacman_orient=0
                    if if_dead(pacman_x,pacman_y)==True:
                        print("You died!")
                        restart()
                    
                    ghostpanel()
                    
                    if if_dead(pacman_x,pacman_y)==True:
                        print("You died!")
                        restart()
                    if if_eaten[pacman_x][pacman_y]==0:
                        if_eaten[pacman_x][pacman_y]=1
                        scores+=1       
                        # print(score)             
                if every_event.type==MOUSEBUTTONDOWN:
                    temp_mousepos=pygame.mouse.get_pos()
                    #restart button
                    if 750<=temp_mousepos[0]<=850 and 290<=temp_mousepos[1]<=350:
                        restart()
                    
                    #automating search algo(greedy)    
                    if 750<=temp_mousepos[0]<=990 and 370<=temp_mousepos[1]<=430:
                        navigating_method=1
                        pygame.event.set_allowed(26)
                        # pygame.time.set_timer(26,800) # Automating moving frequency
                        
                    if 750<=temp_mousepos[0]<=850 and 450<=temp_mousepos[1]<=510:
                        navigating_method=0
                        pygame.event.set_blocked(26)
                    
                    if 750<=temp_mousepos[0]<=930 and 530<=temp_mousepos[1]<=590:
                        restart(randomized=True)
                        # initsize()
                        # setbutton()
                        # input_file()
                        # if_eaten[pacman_x][pacman_y]=1
                        # repainting(3,1)
                        # pygame_event_text=[]
                        # pygame.event.set_blocked(MOUSEMOTION)
                        # pass
            
            repainting(pacman_orient,0)
        pygame.display.update()