'''System-Related Parameter(Do not edit)'''
map_height=16 
map_width=16  
map_size=16
movingtick=1
mapboarder_buffer=40
block_size=40
'''System-Unrelated Parameter(Do not edit unless I mark)'''
blockgeneratePossibly=0.25
if_bfssh=0
const_inf=10000000
autospeed=50    #Recommend edit it,which will influence the speed of Game
if_qlearning_help=1  #If this is 1, Q-Learning+Minimax will place the Q-Learning
navigating_method=0
ghost_navigating_method=1
nowmaptype=0
nownavigating=0
scores=0
game_ticks=0
system_default_ghost_num=2 
system_default_ghost_vector=[[0,15,1],[15,0,2]]
qtable_name=["./qtable/DefGh1-QL.txt","./qtable/DefGh2-QL.txt","./qtable/MazeGh1-QL.txt","./qtable/MazeGh2-QL.txt","./qtable/Small-QL.txt"]
qpkl_name=["./pkl/DefGh1-QL.pkl","./pkl/DefGh2-QL.pkl","./pkl/MazeGh1-QL.pkl","./pkl/MazeGh2-QL.pkl","./pkl/Small-QL.pkl"]
sstable_name=["./qtable/DefGh1-SS.txt","./qtable/DefGh2-SS.txt","./qtable/MazeGh1-SS.txt","./qtable/MazeGh2-SS.txt","./qtable/Small-SS.txt"]
sspkl_name=["./pkl/DefGh1-SS.pkl","./pkl/DefGh2-SS.pkl","./pkl/MazeGh1-SS.pkl","./pkl/MazeGh2-SS.pkl","./pkl/Small-SS.pkl"]
ghost_lambda=0.4
ifwin=False
# ghost_distance_value=[-const_inf,-200,-80,0,10,25,27,29,30]
ghost_distance_value=[[-999,-999,-999,-999,-999,-999,-999,-999,-999],
                    [-999,-200,-190,-190,-180,-180,-180,-170,-170],
                    [-999,-190,-130,-100,-70 ,-55 ,-45 ,-40 ,-35],
                    [-999,-190,-100,-50 ,-35 ,-10 ,5   ,15   ,25],
                    [-999,-180,-70 ,-35 ,0   ,20  ,25  ,27   ,29.4],
                    [-999,-180,-55 ,-10 ,20  ,30  ,31  ,32.6 ,33.8],
                    [-999,-180,-45 ,5   ,25  ,31  ,33.5,34.8 ,35.6],
                    [-999,-170,-40 ,15  ,27  ,32.6,34.8,35.7 ,36.2],
                    [-999,-170,-35 ,25  ,29.4,33.8,35.6,36.2 ,36.4]]
ghost_one_value=[-999,-180,-50,0,20,25,28,30,31,32]
scared_value=[18,10,8,6,5,3,2,1,0]

food_distance_value=[35,25,15,11,8,6,4,3]
#if having invincible,this will be negative
capsule_distance_value=[50,40,30,15,10,8,6,5]

'''Moving-Related(Do not edit it)'''
pacman_flash_x=0
pacman_flash_y=0
''' End '''