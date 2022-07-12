import pygame
def imageinit():
    global apple_image
    global block_image_E,block_image_W,block_image_N,block_image_S
    global block_image_SE,block_image_SW,block_image_NE,block_image_NW
    global pacman_image_left,pacman_image_north,pacman_image_right,pacman_image_south
    global pacman_orient,ghost_image
    
    apple_image=pygame.image.load('./pic/apple.jpg')
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
    pacman_orient=0
    ghost_image=pygame.image.load('./pic/ghost.png')