from glob import glob
import pygame,random,copy
from Parameter import *
from Agents import Pacman,Ghost
from Util import Map,Directions,checkconnecting,Buttons



def input_file():
    map_input=open("./map/map.txt",'r')
    tempmap=[]
    for lines in map_input.readlines():
        mapline=lines.split(" ")
        tempmap.append(list(map(int,mapline)))
    map_input.close()
    return tempmap

def input_mazefile():
    map_input=open("./map/map-full.txt",'r')
    tempmap=[]
    for lines in map_input.readlines():
        mapline=lines.split(" ")
        tempmap.append(list(map(int,mapline)))
    map_input.close()
    return tempmap

def input_smallfile():
    map_input=open("./map/map-small.txt",'r')
    tempmap=[]
    for lines in map_input.readlines():
        mapline=lines.split(" ")
        tempmap.append(list(map(int,mapline)))
    map_input.close()
    return tempmap

def dust2_file():
    map_input=open("./map/map-dust2.txt",'r')
    tempmap=[]
    for lines in map_input.readlines():
        mapline=lines.split(" ")
        tempmap.append(list(map(int,mapline)))
    map_input.close()
    return tempmap

def imageinit():
    global apple_image,block_image,ghost_image,capsule_image
    global pacman_image_left,pacman_image_north,pacman_image_right,pacman_image_south
    global pacman_image_left_inv,pacman_image_north_inv,pacman_image_right_inv,pacman_image_south_inv
    global pacman_image_leftsmaller,pacman_image_northsmaller,pacman_image_rightsmaller,pacman_image_southsmaller
    global pacman_image_leftsmaller_inv,pacman_image_northsmaller_inv,pacman_image_rightsmaller_inv,pacman_image_southsmaller_inv
    global pacman_image_none,pacman_image_none_inv
    global ghost_left,ghost_north,ghost_right,ghost_south,ghost_scared
    
    apple_image=pygame.image.load('./pic/apple.jpg')
    block_image=pygame.image.load('./pic/block.jpg')
    capsule_image=pygame.image.load('./pic/capsule.jpg')
    
    pacman_image_right=pygame.image.load('./pic/pacman_right.png')
    pacman_image_left=pygame.image.load('./pic/pacman_left.png')
    pacman_image_north=pygame.image.load('./pic/pacman_north.png')
    pacman_image_south=pygame.image.load('./pic/pacman_south.png')
    pacman_image_none=pygame.image.load('./pic/pacman_none.png')
    
    pacman_image_right_inv=pygame.image.load('./pic/pacman_right_inv.png')
    pacman_image_left_inv=pygame.image.load('./pic/pacman_left_inv.png')
    pacman_image_north_inv=pygame.image.load('./pic/pacman_north_inv.png')
    pacman_image_south_inv=pygame.image.load('./pic/pacman_south_inv.png')
    pacman_image_none_inv=pygame.image.load('./pic/pacman_none_inv.png')

    pacman_image_rightsmaller=pygame.image.load('./pic/pacman_right_smaller.png')
    pacman_image_leftsmaller=pygame.image.load('./pic/pacman_left_smaller.png')
    pacman_image_northsmaller=pygame.image.load('./pic/pacman_north_smaller.png')
    pacman_image_southsmaller=pygame.image.load('./pic/pacman_south_smaller.png')
    
    pacman_image_rightsmaller_inv=pygame.image.load('./pic/pacman_right_smaller_inv.png')
    pacman_image_leftsmaller_inv=pygame.image.load('./pic/pacman_left_smaller_inv.png')
    pacman_image_northsmaller_inv=pygame.image.load('./pic/pacman_north_smaller_inv.png')
    pacman_image_southsmaller_inv=pygame.image.load('./pic/pacman_south_smaller_inv.png')
    
    ghost_right=pygame.image.load('./pic/ghost_right.jpg')
    ghost_left=pygame.image.load('./pic/ghost_left.jpg')
    ghost_north=pygame.image.load('./pic/ghost_north.jpg')
    ghost_south=pygame.image.load('./pic/ghost_south.jpg')
    ghost_scared=pygame.image.load('./pic/scared_ghost.png')
    
def fontinit():
    global font16,font32,font24,font28,font16_height
    font16=pygame.font.SysFont("arial",16)
    font24=pygame.font.SysFont("arial",24)
    font32=pygame.font.SysFont("arial",32)
    font28=pygame.font.SysFont("arial",28)
    font16_height=font16.get_linesize()
    
def initset():
    global main_screen
    global windows_width,windows_height
    global autospeed
    # navigating method : 0 for play, 1 for greedy, 2 for DFS
    
    pygame.init()
    pygame.display.set_caption("pacman")
    windows_width=block_size*map_width
    windows_height=block_size*map_height
    main_screen=pygame.display.set_mode((2*mapboarder_buffer+windows_width+480,windows_height+2*mapboarder_buffer))
    
    #signal 25, for flush 
    pygame.time.set_timer(25,100)
    
    #signal 26, for automating frequency
    # pygame.time.set_timer(26,autospeed)
    
    #signal 27, for moving (automatic)
    pygame.time.set_timer(27,autospeed)
    
    #signal 29,for clicking
    
    
def agentinit(temptype=0):
    global system_default_ghost_num
    tempsize=[map_height,map_width]
    if temptype==1:
        pacman_obj=Pacman(initx=random.randint(0,15),inity=random.randint(0,15),initorient=random.randint(0,3))
        temp_mapinput=[[0 for i in range(tempsize[0])] for j in range(tempsize[1])]
        if_eaten=[[0 for i in range(tempsize[0])] for j in range(tempsize[1])]
        temppacmanposition=Pacman.pacmanobject.getposition()
        # print("Final")
        # print(temp_mapinput)
        # print(checkconnecting(temp_mapinput))
        for i in range(tempsize[0]):
            for j in range(tempsize[1]):
                if i==temppacmanposition[0] and j==temppacmanposition[1]:
                    continue
                temp_mapinput[i][j]=1
                connectnum=checkconnecting(temp_mapinput)
                temp_mapinput[i][j]=0
                if connectnum==1:
                    temp_randomint=random.random()
                    if temp_randomint<blockgeneratePossibly:
                        temp_mapinput[i][j]=1
        map_obj=Map(map_height,map_width,temp_mapinput)
    elif temptype==0:
        system_default_ghost_num=2
        pacman_obj=Pacman(0,0,1)
        map_obj=Map(map_height,map_width,input_file())
        for i in range(system_default_ghost_num):
            ghost_obj=Ghost(system_default_ghost_vector[i][0],system_default_ghost_vector[i][1],0,system_default_ghost_vector[i][2])
    elif temptype==10:
        system_default_ghost_num=1
        pacman_obj=Pacman(0,0,1)
        map_obj=Map(map_height,map_width,input_file())
        ghost_obj=Ghost(0,15,2)
    elif temptype==2:
        system_default_ghost_num=2
        pacman_obj=Pacman(0,0,1)
        map_obj=Map(map_height,map_width,input_mazefile())
        for i in range(system_default_ghost_num):
            ghost_obj=Ghost(system_default_ghost_vector[i][0],system_default_ghost_vector[i][1],0,system_default_ghost_vector[i][2])
    elif temptype==12:
        system_default_ghost_num=1
        pacman_obj=Pacman(0,0,1)
        map_obj=Map(map_height,map_width,input_mazefile())
        ghost_obj=Ghost(0,15,2)       
    elif temptype==3:
        system_default_ghost_num=1
        # print(system_default_ghost_num)
        pacman_obj=Pacman(2,0,1)
        map_obj=Map(map_height,map_width,input_smallfile())
        ghost_obj=Ghost(2,4,3)
    scores=0    
    
    
    
    
def setbutton():
    global score_text,textRect,win_text,winRect,ticks_text,tickRect,step_text,stepRect,invtime_text,invtimeRect
    global manualbutton,resetbutton,mazebutton,smallbutton,mazetwobutton
    global minimaxbutton,defaultbutton,rulebutton1,rulebutton2,defaulttwobutton
    global Q_LearningButton,SarsaButton
    
    
    #Text Scores:
    score_text=font32.render("Scores:"+str(scores),True,(255,255,255),(0,0,0))
    ticks_text=font32.render("Time:"+str(game_ticks)+"s",True,(255,255,255),(0,0,0))
    win_text=font32.render("You Win!",True,(255,255,255),(0,0,0))
    step_text=font32.render("Steps:0",True,(255,255,255),(0,0,0))
    invtime_text=font32.render("Invtime:",True,(255,255,255),(0,0,0))
    
    textRect=score_text.get_rect()
    textRect.center=(800,50)
    winRect=win_text.get_rect()
    winRect.center=(800,100)
    tickRect=ticks_text.get_rect()
    tickRect.center=(1000,50)
    stepRect=step_text.get_rect()
    stepRect.center=(1000,100)
    invtimeRect=invtime_text.get_rect()
    invtimeRect.center=(1000,150)
    
    #default
    defaultbutton=Buttons("Default(One Ghost)",font24,(740,220),(200,50),(255,255,255),(255,255,255),(153, 153, 255),True,1)
    #default-ghost2
    defaulttwobutton=Buttons("Default(Two Ghost)",font24,(960,220),(200,50),(255,255,255),(255,255,255),(153, 153, 255),True,2)
    #mazemap
    mazebutton=Buttons("MazeMap(One Ghost)",font24,(740,290),(200,50),(255,255,255),(255,255,255),(153, 153, 255),True,3)
    #mazemap2
    mazetwobutton=Buttons("MazeMap(Two Ghost)",font24,(960,290),(200,50),(255,255,255),(255,255,255),(153, 153, 255),True,4)
    #small-map
    smallbutton=Buttons("Small Map",font24,(740,360),(200,50),(255,255,255),(255,255,255),(153, 153, 255),True,5)
    #ResetRandom
    resetbutton=Buttons("Reset Map",font24,(960,360),(200,50),(255,255,255),(255,255,255),(153, 153, 255),True,6)
    # avoidancebutton=Buttons("Minimax",font32,(740,380),(200,60),(255,255,255),(255,255,255),(153, 153, 255),True,3)
    
    #Manual Button
    manualbutton=Buttons("Manual",font24,(740,470),(200,50),(255,255,255),(255,255,255),(153, 153, 255),True,7)
    #MinimaxSearch
    minimaxbutton=Buttons("Minimax Search",font24,(960,470),(200,50),(255,255,255),(255,255,255),(153, 153, 255),True,8)
    
    rulebutton1=Buttons("Avoidance Search",font24,(960,540),(200,50),(255,255,255),(255,255,255),(153, 153, 255),True,9)
    rulebutton2=Buttons("Attack Search",font24,(740,540),(200,50),(255,255,255),(255,255,255),(153, 153, 255),True,10)
    
    #QL
    Q_LearningButton=Buttons("Q-Learning",font24,(740,610),(200,50),(255,255,255),(255,255,255),(153, 153, 255),True,11)
    #Sarsa
    SarsaButton=Buttons("Sarsa",font24,(960,610),(200,50),(255,255,255),(255,255,255),(153, 153, 255),True,12)
    
    
    #add Ghost
    # ghostone_button=font32