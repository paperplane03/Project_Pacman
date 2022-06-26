from ast import Pass
import pygame
import os
from pygame.locals import *
import Qtable
from SrcLoad import agentinit,initset,imageinit,fontinit,setbutton
from Painting import repainting
from Agents import Pacman,Ghost,if_touch
from Util import Map,Directions,Buttons
from Parameter import *
import PathControl
import AgentControl


def restart(type=0,scarce=False,onedot=False,navigate=nownavigating):
    global pygame_event_text,ifwin,navigating_method
    Ghost.clearghost()
    agentinit(type)
    tempMap=Map.mapobject
    navigating_method=nownavigating
    if scarce==True:
        tempMap.fillsomefood(8)
    if onedot==True:
        tempMap.fillonefood()
    tempPac=Pacman.pacmanobject
    tempPacDir=tempPac.getposition()
    eatresult=tempMap.eat(tempPacDir[0],tempPacDir[1])
    if eatresult==2:
        tempPac.becomeinv()
    repainting()
    pygame_event_text=[]
    PathControl.clear_manhanttan()
    PathControl.clearDFS()
    PathControl.cleardp()
    ifwin=False
    # pygame.event.set_blocked(MOUSEMOTION)

def restart_phase3(type=0,navigate=nownavigating):
    global pygame_event_text,ifwin,navigating_method
    Ghost.clearghost()
    agentinit(type)
    tempMap=Map.mapobject
    navigating_method=nownavigating
    tempPac=Pacman.pacmanobject
    tempPacDir=tempPac.getposition()
    eatresult=tempMap.eat(tempPacDir[0],tempPacDir[1])
    if eatresult==2:
        tempPac.becomeinv()
    repainting()
    pygame_event_text=[]
    PathControl.clear_manhanttan()
    PathControl.clearDFS()
    PathControl.cleardp()
    ifwin=False
    # pygame.event.set_blocked(MOUSEMOTION)
    
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
                temp_ghostvec=Ghost.ghostvector
                temp_pacmanpredic=temp_pacman.getpreviousposition()
                temp_pacmandic=temp_pacman.getposition()
                temp_ori=temp_pacman.getorient()
                temp_map=Map.mapobject
                if temp_map.if_win()==True or temp_map.getfoodnum()==0:
                    navigating_method=999
                if every_event.type==QUIT:
                    exit()
                if every_event.type==25:
                    Pacman.pacmanobject.changemouthopen()
                    if_pacmanmouse_open=Pacman.pacmanobject.getmouthopen()
                    # print(str(every_event))
                    
                if every_event.type==27:
                    if temp_map.if_win()==False and navigating_method!=999:
                        temp_map.updatetime()
                        temp_pacman.decreaseinvtime()
                    temp_pacman.pacman_flash_x=temp_pacmanpredic [0]+movingtick/5*(temp_pacmandic[0]-temp_pacmanpredic[0])
                    temp_pacman.pacman_flash_y=temp_pacmanpredic[1]+movingtick/5*(temp_pacmandic[1]-temp_pacmanpredic[1])
                    for ghostobj in Ghost.ghostvector:
                        temp_ghostdic=ghostobj.getposition()
                        temp_ghostpredic=ghostobj.getpreviousposition()
                        ghostobj.ghost_flash_x=temp_ghostpredic[0]+movingtick/5*(temp_ghostdic[0]-temp_ghostpredic[0])
                        ghostobj.ghost_flash_y=temp_ghostpredic[1]+movingtick/5*(temp_ghostdic[1]-temp_ghostpredic[1])
                    
                    touchtime=if_touch()
                    if touchtime[0]==True:
                        if temp_pacman.invtime==0:
                            # print("You died!")
                            navigating_method=999
                            diepacman=Pacman(0,0,-1)
                            for ghostobj in Ghost.ghostvector:
                                ghostobj.changeorient(-1)
                        else:
                            # Ghost.ghostvector.remove(touchtime[1])
                            touchtime[1].respawn()
                            temp_map.updatescore(10)
                        # restart(0,False,False)
                        # pass
                        # print(score)
                    if movingtick>=5:
                        
                        if temp_map.if_win()==False and navigating_method!=999:
                            temp_map.updatestep()
                        # print("pacmanx:"+str(temp_dic[0]))
                        # print("pacmany:"+str(temp_dic[1]))
                        movingtick-=5
                        
                        ''''''
                        Pacman.pacmanobject.updatepreviousposition()
                        Pacman.pacmanobject.updatepreviousorient()
                        for ghostobj in Ghost.ghostvector:
                            ghostobj.updatepreviousposition()
                            ghostobj.updatepreviousorient()
                            temp_ghostori=ghostobj.getorient()
                            
                            # if temp_ori!=None:
                                # pacman_move_vector=Directions.getmove(temp_ori)
                            if temp_ghostori in ghostobj.validposition():
                            # print("move:")
                                ghostobj.move(temp_ghostori)
                        # if temp_ori!=None:
                            # pacman_move_vector=Directions.getmove(temp_ori)
                        if temp_ori in Pacman.pacmanobject.validPosition():
                            # print("move:")
                            Pacman.pacmanobject.move(temp_ori)
                    if movingtick==3:
                        # print(Map.mapobject.get_ifeaten(temp_dic[0],temp_dic[1]))
                        if Map.mapobject.get_ifeaten(temp_pacmandic[0],temp_pacmandic[1])==1:
                            eatresult=temp_map.eat(temp_pacmandic[0],temp_pacmandic[1])
                            if eatresult==2:
                                Pacman.pacmanobject.becomeinv()
                                for ghost in Ghost.ghostvector:
                                    ghost.if_scared=1
                            temp_map.if_win()
                            scores+=1
                        if navigating_method==1:
                            temp_moveaction=AgentControl.minimax_search_with_alphabeta(system_default_ghost_num)
                            if temp_moveaction!=-1:
                                temp_pacman.changeorient(temp_moveaction)
                        elif navigating_method==2:
                            temp_moveaction=AgentControl.attack_pacman()
                            if temp_moveaction!=-1:
                                temp_pacman.changeorient(temp_moveaction)
                        elif navigating_method==3:
                            temp_moveaction=AgentControl.avoidance_pacman()
                            if temp_moveaction!=-1:
                                temp_pacman.changeorient(temp_moveaction)
                            # temp_ori=temp_moveaction
                        elif navigating_method==10:
                            #--------------------------------------------------------------------------------------#
                            temp_moveaction=AgentControl.Qlearningmethod(system_default_ghost_num)
                            #--------------------------------------------------------------------------------------#
                            if temp_moveaction!=-1:
                                temp_pacman.changeorient(temp_moveaction)
                        elif navigating_method==999:
                            pass
                        if ghost_navigating_method==1:
                            for ghostobj in Ghost.ghostvector:
                                # temp_move=AgentControl.ghost_random(ghostobj)
                                if navigating_method==999:
                                    continue
                                if ghostobj.if_scared>0:
                                    temp_move=AgentControl.lambda_frightened(ghost_lambda,ghostobj)
                                elif ghostobj.chasemethod==1:
                                    temp_move=AgentControl.lambda_random(ghost_lambda,ghostobj)
                                elif ghostobj.chasemethod==2:
                                    temp_move=AgentControl.ghost_predict(ghost_lambda,ghostobj)
                                if temp_move!=-1:
                                    ghostobj.changeorient(temp_move)
                    movingtick+=1
                    repainting()  
                if every_event.type==29:
                    beclicked.changebackcolor((153,153,255))
                    beclicked.changelinecolor((255,255,255))
                if every_event.type==KEYDOWN and navigating_method==0:
                    if every_event.key==K_w:
                        movevec=Directions.getmove(2)
                        if Pacman.pacmanmap_valid(temp_pacmandic[0]+movevec[0],temp_pacmandic[1]+movevec[1])==True:
                            temp_pacman.changeorient(2)
                    elif every_event.key==K_s:
                        movevec=Directions.getmove(0)
                        if Pacman.pacmanmap_valid(temp_pacmandic[0]+movevec[0],temp_pacmandic[1]+movevec[1])==True:
                            temp_pacman.changeorient(0)
                    elif every_event.key==K_a:
                        movevec=Directions.getmove(3)
                        if Pacman.pacmanmap_valid(temp_pacmandic[0]+movevec[0],temp_pacmandic[1]+movevec[1])==True:
                            temp_pacman.changeorient(3)
                    elif every_event.key==K_d:
                        movevec=Directions.getmove(1)
                        if Pacman.pacmanmap_valid(temp_pacmandic[0]+movevec[0],temp_pacmandic[1]+movevec[1])==True:
                            temp_pacman.changeorient(1)
                    
                    # ghostpanel()
                    
                    # if if_touch()==True:
                        # print("You died!")
                        # restart()
                        # pass
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
                                system_default_ghost_num=1
                                restart_phase3(10,nownavigating)
                                nowmaptype=10
                            if everybutton.tag==2:
                                system_default_ghost_num=2
                                restart_phase3(0,nownavigating)
                                nowmaptype=0
                            if everybutton.tag==3:
                                system_default_ghost_num=1
                                restart_phase3(12,nownavigating)
                                nowmaptype=12
                            if everybutton.tag==4:
                                system_default_ghost_num=2
                                restart_phase3(2,nownavigating)
                                nowmaptype=2
                            if everybutton.tag==5:
                                restart_phase3(3,nownavigating)
                                system_default_ghost_num=1
                                nowmaptype=3
                            if everybutton.tag==6:
                                restart_phase3(nowmaptype,nownavigating)
                            if everybutton.tag==7:
                                navigating_method=0
                                nownavigating=0
                            if everybutton.tag==8:
                                navigating_method=1
                                nownavigating=1
                            if everybutton.tag==9:
                                navigating_method=2
                                nownavigating=2
                            if everybutton.tag==10:
                                navigating_method=3
                                nownavigating=3
                            if everybutton.tag==11:
                                navigating_method=10
                                nownavigating=10
                                if nowmaptype==10:
                                    Qtable.open_Qtable(0)
                                elif nowmaptype==0:
                                    Qtable.open_Qtable(1)
                                elif nowmaptype==12:
                                    Qtable.open_Qtable(2)
                                elif nowmaptype==2:
                                    Qtable.open_Qtable(3)
                                elif nowmaptype==3:
                                    Qtable.open_Qtable(4)
                                
                            if everybutton.tag==12:
                                navigating_method=10
                                nownavigating=10
                                if nowmaptype==10:
                                    Qtable.open_Sarsa(0)
                                elif nowmaptype==0:
                                    Qtable.open_Sarsa(1)
                                elif nowmaptype==12:
                                    Qtable.open_Sarsa(2)
                                elif nowmaptype==2:
                                    Qtable.open_Sarsa(3)
                                elif nowmaptype==3:
                                    Qtable.open_Sarsa(4)
                repainting()
        pygame.display.update()

