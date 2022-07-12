import pygame
import os
from pygame.locals import *
from SrcLoad import agentinit,initset,imageinit,fontinit,setbutton
from Painting import repainting
from Agents import Pacman,Ghost,pacmanmap_valid,ghostmap_valid,if_dead
from Util import Map,Directions,Buttons
from Parameter import *
import Control
