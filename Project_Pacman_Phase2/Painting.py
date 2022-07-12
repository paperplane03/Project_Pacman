from Parameter import *
import pygame
import SrcLoad
from Util import Map,Buttons
import math
from Agents import Ghost,Pacman

def paintingbuttonborder(tempbutton:Buttons):
    tempposition=tempbutton.getposition()
    tempsize=tempbutton.getsize()
    templine=tempbutton.getline()
    pygame.draw.line(SrcLoad.main_screen,templine,tempposition,(tempposition[0]+tempsize[0],tempposition[1]),width=2)
    pygame.draw.line(SrcLoad.main_screen,templine,tempposition,(tempposition[0],tempposition[1]+tempsize[1]),width=2)
    pygame.draw.line(SrcLoad.main_screen,templine,(tempposition[0],tempposition[1]+tempsize[1]),(tempposition[0]+tempsize[0],tempposition[1]+tempsize[1]),width=2)
    pygame.draw.line(SrcLoad.main_screen,templine,(tempposition[0]+tempsize[0],tempposition[1]),(tempposition[0]+tempsize[0],tempposition[1]+tempsize[1]),width=2)

def repainting():
    global ifwin
    SrcLoad.main_screen.fill((0,0,0))
    
    tempmap=Map.mapobject
    tempsize=tempmap.get_size()
    temppacman=Pacman.pacmanobject
    tempghostvec=Ghost.ghostvector
    #painting map
    if True:
        for i in range(map_height):
            for j in range(map_width):
                if tempmap.get_value(i,j)>=1:
                    SrcLoad.main_screen.blit(SrcLoad.block_image,(j*40+mapboarder_buffer,i*40+mapboarder_buffer,40,40))
                elif tempmap.get_ifeaten(i,j)==1:
                    SrcLoad.main_screen.blit(SrcLoad.apple_image,(j*40+mapboarder_buffer,i*40+mapboarder_buffer,40,40))
    
    #painting pacman
    # flushpacman()
    if temppacman.getmouthopen()==2:
        # print("flash"+str(pacman_flash_x)+" "+str(pacman_flash_y))
        if temppacman.getpreviousorient()==3:
            SrcLoad.main_screen.blit(SrcLoad.pacman_image_left,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
        if temppacman.getpreviousorient()==1:
            SrcLoad.main_screen.blit(SrcLoad.pacman_image_right,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
        if temppacman.getpreviousorient()==2:
            SrcLoad.main_screen.blit(SrcLoad.pacman_image_north,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
        if temppacman.getpreviousorient()==0:
            SrcLoad.main_screen.blit(SrcLoad.pacman_image_south,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
    elif temppacman.getmouthopen()==1:
        if temppacman.getpreviousorient()==3:
            SrcLoad.main_screen.blit(SrcLoad.pacman_image_leftsmaller,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
        if temppacman.getpreviousorient()==1:
            SrcLoad.main_screen.blit(SrcLoad.pacman_image_rightsmaller,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
        if temppacman.getpreviousorient()==2:
            SrcLoad.main_screen.blit(SrcLoad.pacman_image_northsmaller,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
        if temppacman.getpreviousorient()==0:
            SrcLoad.main_screen.blit(SrcLoad.pacman_image_southsmaller,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
    else:
        SrcLoad.main_screen.blit(SrcLoad.pacman_image_none,(temppacman.pacman_flash_y*block_size+mapboarder_buffer,temppacman.pacman_flash_x*block_size+mapboarder_buffer))
    #painting ghost
    # for i in range(Ghost.ghostnum):
    # SrcLoad.main_screen.blit(SrcLoad.ghost_image,(ghost_x[i]*block_size+mapboarder_buffer,ghost_y[i]*block_size+mapboarder_buffer))
    
    #painting border lines
    pygame.draw.line(SrcLoad.main_screen,(102,102,255),(mapboarder_buffer-10,mapboarder_buffer-10),(mapboarder_buffer-10,map_size*block_size+mapboarder_buffer+10),width=2)
    pygame.draw.line(SrcLoad.main_screen,(102,102,255),(mapboarder_buffer-10,mapboarder_buffer-10),(map_size*block_size+mapboarder_buffer+10,mapboarder_buffer-10),width=2)
    pygame.draw.line(SrcLoad.main_screen,(102,102,255),(map_size*block_size+mapboarder_buffer+10,mapboarder_buffer-10),(map_size*block_size+mapboarder_buffer+10,map_size*block_size+mapboarder_buffer+10),width=2)
    pygame.draw.line(SrcLoad.main_screen,(102,102,255),(mapboarder_buffer-10,map_size*block_size+mapboarder_buffer+10),(map_size*block_size+mapboarder_buffer+10,map_size*block_size+mapboarder_buffer+10),width=2)
    
    pygame.draw.line(SrcLoad.main_screen,(102,102,255),(mapboarder_buffer-15,mapboarder_buffer-15),(mapboarder_buffer-15,map_size*block_size+mapboarder_buffer+15),width=2)
    pygame.draw.line(SrcLoad.main_screen,(102,102,255),(mapboarder_buffer-15,mapboarder_buffer-15),(map_size*block_size+mapboarder_buffer+15,mapboarder_buffer-15),width=2)
    pygame.draw.line(SrcLoad.main_screen,(102,102,255),(map_size*block_size+mapboarder_buffer+15,mapboarder_buffer-15),(map_size*block_size+mapboarder_buffer+15,map_size*block_size+mapboarder_buffer+15),width=2)
    pygame.draw.line(SrcLoad.main_screen,(102,102,255),(mapboarder_buffer-15,map_size*block_size+mapboarder_buffer+15),(map_size*block_size+mapboarder_buffer+15,map_size*block_size+mapboarder_buffer+15),width=2)
    
    #painting scores
    score_text=SrcLoad.font32.render("Scores:"+str(tempmap.get_score()),True,(255,255,255),(0,0,0))
    tick_text=SrcLoad.font32.render("Time:"+'%.2f'%(tempmap.get_ticks()/20)+"s",True,(255,255,255),(0,0,0))
    win_text=SrcLoad.font32.render("You Win!",True,(255,255,255),(0,0,0))
    step_text=SrcLoad.font32.render("Steps:"+str(tempmap.get_steps()),True,(255,255,255),(0,0,0))
    #painting scores and restart button
    SrcLoad.main_screen.blit(score_text, SrcLoad.textRect)
    SrcLoad.main_screen.blit(tick_text,SrcLoad.tickRect)
    SrcLoad.main_screen.blit(step_text,SrcLoad.stepRect)
    if Map.mapobject.ifwin==True:
        SrcLoad.main_screen.blit(win_text,SrcLoad.winRect)
        
    for everybutton in Buttons.buttonobject:
        tempposition=everybutton.getposition()
        tempsize=everybutton.getsize()
        pygame.draw.rect(SrcLoad.main_screen,everybutton.getbg(),(tempposition[0],tempposition[1],tempsize[0],tempsize[1]))
        SrcLoad.main_screen.blit(everybutton.buttonobj,everybutton.buttonrect)
        paintingbuttonborder(everybutton)
    
    