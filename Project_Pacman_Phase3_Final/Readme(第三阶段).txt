执行MainLoad.py即可运行WSAD控制上下左右（但当选择了智能算法时无法操作），游戏仅需pygame库即可运行，采用了相对路径所以无需担心

上面六个按钮是不同的地图（和重置地图按钮）
下面六个按钮是不同的自动寻路算法（和手动游戏按钮Manual）

先点击地图按钮，再点击算法按钮即可运行对应的智能（或是手动游戏）
Reset Map按钮重新开始游戏，但不改变游戏地图和智能算法

智能程度：Q-Learning+Minimax ≈ Sarsa+Minimax > Minimax > Attack Pacman > Avoidance Pacman ? Manual (Manual的智能程度取决于玩家)
单纯的Q-Learning和Sarsa存在局限性，故不在排序之中

关于智能算法的具体原理、性能的详细测试和结果写在了程序设计报告（阶段三）中

程序设计中，/pic文件夹中是图片文件，/qtable和/pkl文件夹是快速存储Q-table的文件夹（具体见报告），/map是存储地图的文件夹，/QL-C++是Q-Learning和Sarsa算法的C++实现版本和备份
QL-C++中的QLearning-Pacman-Basis.cpp和Sarsa-Pacman-Basis.cpp是c++的参考文件。