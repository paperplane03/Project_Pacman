#include<iostream>
#include<cstdio>
#include<vector>
#include<queue>
#include<stdlib.h>
#include<cstring>
#include<ctime>
#include<algorithm>
using namespace std;

int map_N=16;
int ghostnum=1;
double Q[257][257][257][4];
int best_strategy[257][257][257];
int mapvalue[17][17];
int stra_tot=4;
int dx[4]={1,0,-1,0};
int dy[4]={0,1,0,-1};
int training_time=500000;
double epsilon_possibility=0.1;
double future_reward=0.8;
double studying_rate=0.1;
long long globalsum=0;
//SOUTH RIGHT NORTH LEFT

int pacman[3]={0,0,0};
int ghost[10][3];

struct way{
	int len;
	vector<int> way_x,way_y,way_orient;
};

void readin(){
	int ua,ub,uc,ud;
	double ue;
	int u,v,w;
	int cnt=0;
	freopen("Small-QL.txt","r",stdin);
	while(1){
		cnt++;
		u=scanf("%d%d%d%d%lf",&ua,&ub,&uc,&ud,&ue);
//		if(cnt<=5){
//			cout<<cnt<<":"<<ua<<" "<<ub<<" "<<uc<<" "<<ud<<" "<<ue<<endl;
//		}
		if(u!=5)break;
		Q[ua][ub][uc][ud]=ue;
		if(best_strategy[ua][ub][uc]==-1)best_strategy[ua][ub][uc]=ud;
		else{
			if(ue>Q[ua][ub][uc][best_strategy[ua][ub][uc]])best_strategy[ua][ub][uc]=ud; 
		}
	}fclose(stdin);
	freopen("CON","r",stdin);
}

int getnum(int x,int y){
	return x*map_N+y;
}

int if_dead(){
	for(int i=0;i<ghostnum;i++){
		if(abs(ghost[i][0]-pacman[0])+abs(ghost[i][1]-pacman[1])<=0.1)return true;
	}return false;
}

int pacmanmap_valid(int x,int y){
	if(x>=0 && x<map_N && y>=0 && y<map_N){
		if(mapvalue[x][y]==0||mapvalue[x][y]==2)return true;
	}return false;
}

int ghostmap_valid(int x,int y){
	for(int i=0;i<ghostnum;i++){
		if(x==ghost[i][0] && y==ghost[i][1])return false;
	}
	if(x>=0 && x<map_N && y>=0 && y<map_N){
		if(mapvalue[x][y]==0||mapvalue[x][y]==2)return true;
	}return false;
}

int pacman_move(int orient){
	if(orient==-1)return false;
	pacman[2]=orient;
	int tempx=pacman[0]+dx[orient];
	int tempy=pacman[1]+dy[orient];
	if(pacmanmap_valid(tempx,tempy)==true){
		pacman[0]=tempx;
		pacman[1]=tempy;
		return 1;
	}return 0;
}

int ghost_move(int ghostnum,int orient){
	if(orient==-1)return false;
	ghost[ghostnum][2]=orient;
	int tempx=ghost[ghostnum][0]+dx[orient];
	int tempy=ghost[ghostnum][1]+dy[orient];
	if(ghostmap_valid(tempx,tempy)==true){
		ghost[ghostnum][0]=tempx;
		ghost[ghostnum][1]=tempy;
		return 1;
	}return 0;
}

void showway(way x){
	printf("waylen:%d\n",x.len);
	for(int i=0;i<x.len;i++){
		printf("way[%d]:%d %d %d\n",i,x.way_x[i],x.way_y[i],x.way_orient[i]);
	}
}

way how_to_go(int beginx,int beginy,int endx,int endy){
	int vectormap[17][17];
	int frontx, fronty, frontori;
	memset(vectormap, -1, sizeof(vectormap));
	way* p=new way;
	way tempans=(*p);
	tempans.len=0;
	tempans.way_x.clear();
	tempans.way_y.clear();
	tempans.way_orient.clear();
	
//	memset(tempans,0,sizeof(tempans));
	queue<int> x, y, ori;
	x.push(beginx);
	y.push(beginy);
	ori.push(-1);
	while(x.size()>0){
		frontx = x.front();
		fronty = y.front();
		frontori = ori.front();
		x.pop();
		y.pop();
		ori.pop();
		if(pacmanmap_valid(frontx,fronty)==false)continue;
		if(vectormap[frontx][fronty]!=-1)continue;
		vectormap[frontx][fronty] = frontori;
		if(frontx==endx&&fronty==endy){
			while(1){
				if(frontx==beginx&&fronty==beginy){
					tempans.len++;
					tempans.way_x.push_back(beginx);
					tempans.way_y.push_back(beginy);
					tempans.way_orient.push_back(-1);
					for(int i=0;i<tempans.len/2;i++){
						swap(tempans.way_x[i],tempans.way_x[tempans.len-i-1]);
						swap(tempans.way_y[i],tempans.way_y[tempans.len-i-1]);
						swap(tempans.way_orient[i],tempans.way_orient[tempans.len-i-1]);
					}
					return tempans;
				}
				int temp_direction = vectormap[frontx][fronty];
				tempans.len++;
				tempans.way_x.push_back(frontx);
				tempans.way_y.push_back(fronty);
				tempans.way_orient.push_back(temp_direction);
				frontx -= dx[temp_direction];
				fronty -= dy[temp_direction];
			}
		}
		for (int i = 0; i < 4;i++){
			if(pacmanmap_valid(frontx+dx[i],fronty+dy[i])==true){
				x.push(frontx + dx[i]);
				y.push(fronty + dy[i]);
				ori.push(i);
			}
		}
	}
}

int ghost_best(int ghostobj){
	way tempway=how_to_go(ghost[ghostobj][0],ghost[ghostobj][1],pacman[0],pacman[1]);
	if(tempway.len<=1){
		return -1;
	}return tempway.way_orient[1];
}

int ghost_random(int ghostobj){
	int tempx,tempy;
	bool flag=false;
	vector<int>choice;
	choice.clear();
	for(int i=0;i<4;i++){
		tempx=ghost[ghostobj][0]+dx[i];
		tempy=ghost[ghostobj][1]+dy[i];
		if(ghostmap_valid(tempx,tempy)==true)choice.push_back(i);
	}
	int choicelen=choice.size();
	if(choicelen==0)return -1;
	return choice[rand()%choicelen];
}

int lambda_chase(double lambda_pos,int ghostobj){
	double this_pos=(double)rand()/RAND_MAX;
	if(this_pos<lambda_pos)return ghost_random(ghostobj);
	else return ghost_best(ghostobj);
}

// int lambda_predict(int lambda_pos,int ghostobj);

int pacman_random(){
	int tempx,tempy;
	bool flag=false;
	vector<int>choice;
	choice.clear();
	for(int i=0;i<4;i++){
		tempx=dx[i]+pacman[0];
		tempy=dy[i]+pacman[1];
//		cout<<tempx<<" "<<tempy<<endl;
		if(pacmanmap_valid(tempx,tempy)==true){
			choice.push_back(i);
//			cout<<i<<endl;
		}
	}
	int choicelen=choice.size();
//	cout<<"ChoiceList:";
//	for(int i=0;i<choicelen;i++){
//		cout<<choice[i]<<" ";
//	}cout<<endl;
	if(choicelen==0)return -1;
	return choice[rand()%choicelen];
}

void agentsetup(){
	pacman[0]=2;
	pacman[1]=0;
	pacman[2]=0;

	ghost[0][0]=2;
	ghost[0][1]=4;
	ghost[0][2]=0;
	
//	ghost[1][0]=15;
	ghost[1][0]=0;
	ghost[1][1]=0;
	ghost[1][2]=0;
}

void show(){
	cout<<"Pacman:"<<pacman[0]<<" "<<pacman[1]<<endl;
	cout<<"Ghost1:"<<ghost[0][0]<<" "<<ghost[0][1]<<endl;
	cout<<"Ghost0:"<<ghost[1][0]<<" "<<ghost[1][1]<<endl;
	cout<<"----------"<<endl;
}

int epsilon_greedy_method(int b_strategy,int p){
	int temp_pos=rand()%100000;
	int tempx,tempy,randint;
	if(temp_pos<=100000*epsilon_possibility){
		return pacman_random();
	}return b_strategy;
}

void Qlearning_simu(int turn,bool if_test=false){
//	printf("simu:%d\n",turn);
	int chosen_stra,new_beststra;
	int min_len,pacmanidx;
	int ghostidx[5];
	double ins_reward;
	way ghost0way,ghost1way;

	if(turn>1000){
		globalsum+=1000;
		if(if_test==true)cout<<"This turn:"<<turn<<endl;
		return;
	}if(if_dead()==true){
		if(if_test==true)cout<<"This turn:"<<turn<<endl;
		return;}

	pacmanidx=getnum(pacman[0],pacman[1]);
	for(int i=0;i<2;i++){
		ghostidx[i]=getnum(ghost[i][0],ghost[i][1]);
	}
		
	chosen_stra=epsilon_greedy_method(best_strategy[pacmanidx][ghostidx[0]][ghostidx[1]],turn);
	
	pacman_move(chosen_stra);
	ghost_move(0,lambda_chase(0.5,0));
	if(ghostnum==2)ghost_move(1,lambda_chase(0.5,1));
	
	new_beststra=best_strategy[getnum(pacman[0],pacman[1])][getnum(ghost[0][0],ghost[0][1])][getnum(ghost[1][0],ghost[1][1])];
	if(if_dead()==true){
		ins_reward=-10;
	}else{
		ghost0way=how_to_go(ghost[0][0],ghost[0][1],pacman[0],pacman[1]);
		if(ghostnum==2)ghost1way=how_to_go(ghost[1][0],ghost[1][1],pacman[0],pacman[1]);
		if(ghostnum==1)min_len=ghost0way.len-1;
		else min_len=min(ghost0way.len,ghost1way.len)-1;
		ins_reward=min_len*min_len;
	}

	Q[pacmanidx][ghostidx[0]][ghostidx[1]][chosen_stra]=(1-studying_rate)*Q[pacmanidx][ghostidx[0]][ghostidx[1]][chosen_stra]+\
							studying_rate*(ins_reward+future_reward*Q[getnum(pacman[0],pacman[1])][getnum(ghost[0][0],ghost[0][1])][getnum(ghost[1][0],ghost[1][1])][new_beststra]);

	for(int i=0;i<stra_tot;i++){
		if(Q[pacmanidx][ghostidx[0]][ghostidx[1]][i]>Q[pacmanidx][ghostidx[0]][ghostidx[1]][best_strategy[pacmanidx][ghostidx[0]][ghostidx[1]]]&&\
			pacmanmap_valid(pacmanidx/map_N+dx[i],pacmanidx%map_N+dy[i])==1)best_strategy[pacmanidx][ghostidx[0]][ghostidx[1]]=i;
	}
	
	if(if_dead()==false)Qlearning_simu(turn+1,if_test);
	else{
		globalsum+=turn;
		if(if_test==true)cout<<"This turn:"<<turn<<endl;
	}
	return;
}


void nowloading(){
	printf("---start printing---\n");
	freopen("Small-QL.txt","w",stdout);
	for(int i=0;i<map_N*map_N;i++){//pacman
		for(int j=0;j<map_N*map_N;j++){
			for(int k=0;k<map_N*map_N;k++){
				for(int l=0;l<4;l++){
					if(Q[i][j][k][l]>0.001||Q[i][j][k][l]<-0.001)printf("%d %d %d %d %.4f\n",i,j,k,l,Q[i][j][k][l]);	
				}
			}	
		}
	}
	fclose(stdout);
	freopen("CON","w",stdout);
	printf("-------end-------\n");
}

void Qlearning_algo(){
	int state_x,state_y;
	for(int i=1;i<=training_time;i++){
		if(i<=1000&&i%100==0){
			printf("%d:%f\n",i,(double)globalsum/i);
		}
		if(i%1000==0){
			printf("%d:%f\n",i,(double)globalsum/1000);
			globalsum=0;
		}if(i%10000==0){
			nowloading();
		}
		agentsetup();
		Qlearning_simu(1);
	}

}

int main(){
	int tempx,tempy;
	int u,v,w;
	bool flag;
	memset(Q,0,sizeof(Q));
	memset(best_strategy,-1,sizeof(best_strategy));
	freopen("map-small.txt","r",stdin);
	srand(time(NULL));
	for(int i=0;i<map_N;i++){
		for(int j=0;j<map_N;j++){
			scanf("%d",&mapvalue[i][j]);
		}
	}
	fclose(stdin);
	freopen("CON","r",stdin);
	readin();
//	cout<<"test";
//	printf("test:%d\n",Q[0][1][2][1]);
//	freopen("Q-table.txt","r",stdin);
	for(int i=0;i<map_N*map_N;i++){//pacman
		for(int j=0;j<map_N*map_N;j++){
			for(int k=0;k<map_N*map_N;k++){
				if(best_strategy[i][j][k]!=-1)continue;
				
				flag=false;
				tempx=i/map_N;
				tempy=i%map_N;
				for(int l=0;l<4;l++){
					if(pacmanmap_valid(tempx+dx[l],tempy+dy[l])==true){
						flag=true;
						break;
					}
				}if(flag==false)continue;
				
				while(true){
					best_strategy[i][j][k]=rand()%stra_tot;
					tempx=i/map_N;
					tempy=i%map_N;
					if(pacmanmap_valid(tempx+dx[best_strategy[i][j][k]],tempy+dy[best_strategy[i][j][k]])==true)break;
				}
			}
		}
	}
	printf("finished\n");
	// agentsetup();
//	showway(how_to_go(0,0,4,4));
//	showway(how_to_go(0,2,4,4));
//	showway(how_to_go(0,2,2,4));
	Qlearning_algo();
	int onecnt=0;
//	freopen("Q-table.txt","w",stdout);
	for(int i=0;i<map_N*map_N;i++){//pacman
		for(int j=0;j<map_N*map_N;j++){
				printf("(%d,%d\\%d,%d):",i/map_N,i%map_N,j/map_N,j%map_N);
				if(best_strategy[i][j][0]==0)cout<<"об  ";
				if(best_strategy[i][j][0]==1)cout<<"ср  ";
				if(best_strategy[i][j][0]==2)cout<<"ио  ";
				if(best_strategy[i][j][0]==3)cout<<"вС  ";
				printf("Q:%f  ",Q[i][j][0][best_strategy[i][j][0]]);
			if(j%map_N==map_N-1)cout<<endl;
		}
	}
	
	fclose(stdin);
	fclose(stdout);
	return 0;
} 
