import pygame
import os
from pygame.locals import *
from SrcLoad import agentinit,initset,imageinit,fontinit,setbutton
from Painting import repainting
from Agents import Pacman,Ghost,pacmanmap_valid,ghostmap_valid,if_dead
from Util import Map,Directions,Buttons
from Parameter import *
import Control

def restart(type=0,scarce=False,onedot=False):
    global pygame_event_text,ifwin
    agentinit(type)
    tempMap=Map.mapobject
    if scarce==True:
        tempMap.fillsomefood(8)
    if onedot==True:
        tempMap.fillonefood()
    tempPac=Pacman.pacmanobject
    tempPacDir=tempPac.getposition()
    tempMap.eat(tempPacDir[0],tempPacDir[1])
    repainting()
    pygame_event_text=[]
    Control.clear_manhanttan()
    Control.clearDFS()
    Control.cleardp()
    ifwin=False
    # pygame.event.set_blocked(MOUSEMOTION)


def reset():
    tempPac=Pacman.pacmanobject
    initpos=tempPac.getinit()
    tempMap=Map.mapobject
    newPac=Pacman(initpos[0],initpos[1],initpos[2])
    tempPacDir=newPac.getposition()
    tempMap.resetscore()
    tempMap.refillfood()
    tempMap.eat(tempPacDir[0],tempPacDir[1])
    repainting()
    pygame_event_text=[]
    Control.clear_manhanttan()
    Control.clearDFS()
    Control.cleardp()
    ifwin=False
    
if __name__=="__main__":
    #pacman_flash_x,pacman_flash_y
    
    '''These are first-only functions'''
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    pygame.init()
    initset()
    imageinit()
    fontinit()
    setbutton()
    ifwin=False
    '''End'''
    
    agentinit(0)
    repainting()
    pygame_event_text=[]
    # pygame.event.set_blocked(MOUSEMOTION)


    while True:
        now_event=pygame.event.get()
        if len(now_event)>0:
            # print(len(now_event))
            for every_event in now_event:
                # print(str(every_event))
                temp_pacman=Pacman.pacmanobject
                temp_predic=temp_pacman.getpreviousposition()
                temp_dic=temp_pacman.getposition()
                temp_ori=temp_pacman.getorient()
                temp_map=Map.mapobject
                if every_event.type==QUIT:
                    exit()
                if every_event.type==25:
                    Pacman.pacmanobject.changemouthopen()
                    if_pacmanmouse_open=Pacman.pacmanobject.getmouthopen()
                    # print(str(every_event))
                    
                if every_event.type==27:
                    if movingtick%2==0 and temp_map.if_win()==False:
                        temp_map.updatetime()
                    temp_pacman.pacman_flash_x=temp_predic[0]+movingtick/10*(temp_dic[0]-temp_predic[0])
                    temp_pacman.pacman_flash_y=temp_predic[1]+movingtick/10*(temp_dic[1]-temp_predic[1])
                    if movingtick>=10:
                        
                        if temp_map.if_win()==False:
                            temp_map.updatestep()
                        # print("pacmanx:"+str(temp_dic[0]))
                        # print("pacmany:"+str(temp_dic[1]))
                        movingtick-=10
                        
                        ''''''
                        Pacman.pacmanobject.updatepreviousposition()
                        Pacman.pacmanobject.updatepreviousorient()
                        if temp_ori!=None:
                            pacman_move_vector=Directions.getmove(temp_ori)
                        if temp_ori in Pacman.pacmanobject.validPosition():
                            # print("move:")
                            Pacman.pacmanobject.move(temp_ori)
                    if movingtick==5:
                        # print(Map.mapobject.get_ifeaten(temp_dic[0],temp_dic[1]))
                        if Map.mapobject.get_ifeaten(temp_dic[0],temp_dic[1])==1:
                            temp_map.eat(temp_dic[0],temp_dic[1])
                            temp_map.if_win()
                            scores+=1
                        if navigating_method==1:
                            temp_moveaction=Control.greedy_search_bfs()
                            if temp_moveaction!=-1:
                                temp_pacman.changeorient(temp_moveaction)
                            # temp_ori=temp_moveaction
                        elif navigating_method==2:
                            temp_moveaction=Control.greedy_search_massive_manhattan()
                            if temp_moveaction!=-1:
                                temp_pacman.changeorient(temp_moveaction)
                            # temp_ori=temp_moveaction
                        elif navigating_method==3:
                            # print("3333")
                            temp_moveaction=Control.greedy_search_dfs()
                            # print("tempmove:"+str(temp_moveaction))
                            if temp_moveaction!=-1:
                                temp_pacman.changeorient(temp_moveaction)
                            # temp_ori=temp_moveaction
                        elif navigating_method==4:
                            # print("3333")
                            temp_moveaction=Control.dp()
                            # print("tempmove:"+str(temp_moveaction))
                            if temp_moveaction!=-1:
                                temp_pacman.changeorient(temp_moveaction)
                            # temp_ori=temp_moveaction
                    movingtick+=1
                    repainting()  
                if every_event.type==29:
                    beclicked.changebackcolor((153,153,255))
                    beclicked.changelinecolor((255,255,255))
                if every_event.type==KEYDOWN and navigating_method==0:
                    if every_event.key==K_w:
                        movevec=Directions.getmove(2)
                        if pacmanmap_valid(temp_dic[0]+movevec[0],temp_dic[1]+movevec[1])==True:
                            temp_pacman.changeorient(2)
                    elif every_event.key==K_s:
                        movevec=Directions.getmove(0)
                        if pacmanmap_valid(temp_dic[0]+movevec[0],temp_dic[1]+movevec[1])==True:
                            temp_pacman.changeorient(0)
                    elif every_event.key==K_a:
                        movevec=Directions.getmove(3)
                        if pacmanmap_valid(temp_dic[0]+movevec[0],temp_dic[1]+movevec[1])==True:
                            temp_pacman.changeorient(3)
                    elif every_event.key==K_d:
                        movevec=Directions.getmove(1)
                        if pacmanmap_valid(temp_dic[0]+movevec[0],temp_dic[1]+movevec[1])==True:
                            temp_pacman.changeorient(1)
                    
                    # ghostpanel()
                    
                    if if_dead()==True:
                        print("You died!")
                        # restart()
                         
                        # print(score)
                if every_event.type==MOUSEMOTION:
                    # print("True")
                    temp_mousepos=pygame.mouse.get_pos()
                    for everybutton in Buttons.buttonobject:
                        if everybutton.be_clicked(temp_mousepos)==True:
                            everybutton.changebackcolor((177,145,217))
                            everybutton.changelinecolor((240,218,119))
                            # pygame.time.set_timer(29,200,1)
                        else:
                            everybutton.changebackcolor((153,153,255))
                            everybutton.changelinecolor((255,255,255))
                if every_event.type==MOUSEBUTTONDOWN:
                    temp_mousepos=pygame.mouse.get_pos()
                    #restart button
                    for everybutton in Buttons.buttonobject:
                        if everybutton.be_clicked(temp_mousepos)==True:
                            everybutton.changebackcolor((67,11,133))
                            everybutton.changelinecolor((194,162,18))
                            pygame.time.set_timer(29,200,1)
                            beclicked=everybutton
                            # table
                            if everybutton.tag==1:
                                restart(0,False,False)
                            if everybutton.tag==2:
                                restart(1,False,False)
                            if everybutton.tag==3:
                                restart(1,False,True)
                            if everybutton.tag==4:
                                navigating_method=0
                            if everybutton.tag==5:
                                navigating_method=1
                            if everybutton.tag==6:
                                navigating_method=2
                                Control.clear_manhanttan()
                            if everybutton.tag==7:
                                navigating_method=3
                                Control.clearDFS()
                            if everybutton.tag==8:
                                restart(1,True,False)
                            if everybutton.tag==9:
                                reset()
                            if everybutton.tag==10:
                                restart(0,True,False)
                            if everybutton.tag==11:
                                navigating_method=4
                                Control.cleardp()
                                # print(len(Control.how_to_go(0,0,15,15)))
                                # print(temp_map.getmap())
                                # print(bin(10))
                                # print(Control.dp())
                repainting()
        pygame.display.update()

