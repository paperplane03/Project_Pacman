import pickle,os
from Parameter import *
#Default-twoghost
# Pacman(0,0) Ghost0(0,15) Ghost1(15,0)

def open_Qtable(maptype):
    if Qtable.qtableobj!=None:
        del Qtable.qtableobj
    qtable1=[]
    cnt=-1
    if os.path.exists(qpkl_name[maptype])==False:
        qtable_input=open(qtable_name[maptype],'r')
        for lines in qtable_input.readlines():
            mapline=lines.split(" ")
            cnt+=1
            qtable1.append([])
            for i in range(4):
                qtable1[cnt].append(int(mapline[i]))
            qtable1[cnt].append(float(mapline[4]))
        with open(qpkl_name[maptype],"wb") as qtable_file1:
            pickle.dump(qtable1,qtable_file1)
    else:
        with open(qpkl_name[maptype],"rb") as qtable_file1:
            qtable1=pickle.load(qtable_file1)
    Qtable1obj=Qtable(16,16,4,2,1)
    Qtable1obj.import_Qtable(qtable1)
    return Qtable1obj
    # print(qtable1[:100])
    

def open_Sarsa(maptype):
    qtable1=[]
    cnt=-1
    if os.path.exists(sspkl_name[maptype])==False:
        qtable_input=open(sstable_name[maptype],'r')
        for lines in qtable_input.readlines():
            mapline=lines.split(" ")
            cnt+=1
            qtable1.append([])
            for i in range(4):
                qtable1[cnt].append(int(mapline[i]))
            qtable1[cnt].append(float(mapline[4]))
        with open(sspkl_name[maptype],"wb") as qtable_file1:
            pickle.dump(qtable1,qtable_file1)
    else:
        with open(sspkl_name[maptype],"rb") as qtable_file1:
            qtable1=pickle.load(qtable_file1)
    Qtable1obj=Qtable(16,16,4,2,1)
    Qtable1obj.import_Qtable(qtable1)
    return Qtable1obj

class Qtable():
    qtableobj=None
    tagvector=[]
    def __init__(self,length,height,stra_tot,ghostnum,tag) -> None:
        self.length=length
        self.height=height
        self.stra_tot=stra_tot
        self.problem_ghostnum=ghostnum
        self.tag=tag
        self.data={}
        self.beststra={}
        Qtable.qtableobj=self
        Qtable.tagvector.append(tag)
        
    def import_Qtable(self,Qtable:list):
        for ele in Qtable:
            index1=ele[0]
            index2=ele[1]
            
            if index1 not in self.data:
                self.data[index1]={}
            if index1 not in self.beststra:
                self.beststra[index1]={}
            if index2 not in self.data[index1]:
                self.data[index1][index2]={}
            if index2 not in self.beststra[index1]:
                self.beststra[index1][index2]={}
                
            qobj=self.data[index1][index2]
            qstra=self.beststra[index1][index2]
            
            index3=ele[2]
            index3stra=hash(tuple(ele[2:4]))
            # # self.data[hashele]=ele[-1]
            if index3stra not in qobj:
                qobj[index3stra]=[]
            if index3 not in qstra:
                qstra[index3]=[-1,-const_inf]
                
            qobj[index3stra].append([ele[-2],ele[-1]])
            # print("test:"+str(qstra[index3]))
            if ele[-1]>qstra[index3][1]:
                qstra[index3][0]=ele[-2]
                qstra[index3][1]=ele[-1]
        return
    
    def find_Qtable(self,index):
        index1=index[0]
        index2=index[1]
        index3=hash(tuple(index[2:]))
        
        if index1 not in self.data:
            return None
        if index2 not in self.data[index1]:
            return None
        if index3 not in self.data[index1][index2]:
            return None
        return self.data[index1][index2][index3]
        
        
    def find_beststra(self,index):
        index1=index[0]
        index2=index[1]
        index3=index[2]
        
        if index1 not in self.beststra:
            return None
        if index2 not in self.beststra[index1]:
            return None
        if index3 not in self.beststra[index1][index2]:
            return None
        return self.beststra[index1][index2][index3]