import pygame,random,copy
from Parameter import *
from Agents import Pacman,Ghost
from Util import Map,Directions,checkconnecting,Buttons



def input_file():
    # print("input file:")
    map_input=open("./map/map.txt",'r')
    i=0
    tempmap=[]
    for lines in map_input.readlines():
        # print(lines)
        mapline=lines.split(" ")
        # print(mapline)
        tempmap.append(list(map(int,mapline)))
    # print(map)
    map_input.close()
    # print(tempmap)
    return tempmap

def dust2_file():
    # print("input file:")
    map_input=open("./map/map-dust2.txt",'r')
    i=0
    tempmap=[]
    for lines in map_input.readlines():
        # print(lines)
        mapline=lines.split(" ")
        # print(mapline)
        tempmap.append(list(map(int,mapline)))
    # print(map)
    map_input.close()
    # print(tempmap)
    return tempmap

def imageinit():
    global apple_image,block_image,ghost_image
    global pacman_image_left,pacman_image_north,pacman_image_right,pacman_image_south
    global pacman_image_leftsmaller,pacman_image_northsmaller,pacman_image_rightsmaller,pacman_image_southsmaller
    global pacman_image_none
    
    apple_image=pygame.image.load('./pic/apple.jpg')
    block_image=pygame.image.load('./pic/block.jpg')
    
    pacman_image_right=pygame.image.load('./pic/pacman_right.png')
    pacman_image_left=pygame.image.load('./pic/pacman_left.png')
    pacman_image_north=pygame.image.load('./pic/pacman_north.png')
    pacman_image_south=pygame.image.load('./pic/pacman_south.png')
    pacman_image_none=pygame.image.load('./pic/pacman_none.png')

    pacman_image_rightsmaller=pygame.image.load('./pic/pacman_right_smaller.png')
    pacman_image_leftsmaller=pygame.image.load('./pic/pacman_left_smaller.png')
    pacman_image_northsmaller=pygame.image.load('./pic/pacman_north_smaller.png')
    pacman_image_southsmaller=pygame.image.load('./pic/pacman_south_smaller.png')
    
    
def fontinit():
    global font16,font32,font24,font16_height
    font16=pygame.font.SysFont("arial",16)
    font24=pygame.font.SysFont("arial",24)
    font32=pygame.font.SysFont("arial",32)
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
    
    
def agentinit(temptype):
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
        pacman_obj=Pacman(0,0,1)
        map_obj=Map(map_height,map_width,input_file())
    elif temptype==2:
        pacman_obj=Pacman(15,5,2)
        map_obj=Map(map_height,map_width,dust2_file())
    scores=0    
    
    
    
    
def setbutton():
    global score_text,textRect,win_text,winRect,ticks_text,tickRect,step_text,stepRect
    global restartbutton,autobutton,manualbutton,randombutton,dpbutton
    global autobutton2,autobuttonfail
    #Text Scores:
    score_text=font32.render("Scores:"+str(scores),True,(255,255,255),(0,0,0))
    ticks_text=font32.render("Time:"+str(game_ticks)+"s",True,(255,255,255),(0,0,0))
    win_text=font32.render("You Win!",True,(255,255,255),(0,0,0))
    step_text=font32.render("Steps:0",True,(255,255,255),(0,0,0))
    
    textRect=score_text.get_rect()
    textRect.center=(800,50)
    winRect=win_text.get_rect()
    winRect.center=(800,100)
    tickRect=ticks_text.get_rect()
    tickRect.center=(1000,50)
    stepRect=step_text.get_rect()
    stepRect.center=(1000,100)
    
    restartbutton=Buttons("Default Map",font32,(740,140),(200,60),(255,255,255),(255,255,255),(153, 153, 255),True,1)
    
    #autofind_greedy
    autobutton=Buttons("Random Map",font32,(740,220),(200,60),(255,255,255),(255,255,255),(153, 153, 255),True,2)
    
    #Manual Button
    manualbutton=Buttons("OneFood Map",font32,(740,300),(200,60),(255,255,255),(255,255,255),(153, 153, 255),True,3)
    
    #Random Map Button
    randombutton=Buttons("Manual",font32,(740,380),(200,60),(255,255,255),(255,255,255),(153, 153, 255),True,4)
    
    #autofind_manhattan
    autobutton2=Buttons("BFS auto",font32,(740,460),(200,60),(255,255,255),(255,255,255),(153, 153, 255),True,5)
    
    #Randommap_onlyonedotmatters
    randombutton=Buttons("Heuristic",font32,(740,540),(200,60),(255,255,255),(255,255,255),(153, 153, 255),True,6)
    
    #Randommap_dfs
    autobuttonfail=Buttons("DFS auto",font32,(740,620),(200,60),(255,255,255),(255,255,255),(153, 153, 255),True,7)
    
    #default-scarce
    scarcebutton=Buttons("Default Scarce",font32,(960,140),(200,60),(255,255,255),(255,255,255),(153, 153, 255),True,10)
    
    #dust2-Map
    autobuttonfail=Buttons("Random Scarce",font32,(960,220),(200,60),(255,255,255),(255,255,255),(153, 153, 255),True,8)
    
    #fixedRandom
    autobuttonfail=Buttons("Reset Map",font32,(960,300),(200,60),(255,255,255),(255,255,255),(153, 153, 255),True,9)
    
    #DP
    dpbutton=Buttons("DP auto",font32,(960,460),(200,60),(255,255,255),(255,255,255),(153, 153, 255),True,11)
    
    
    #add Ghost
    # ghostone_button=font32