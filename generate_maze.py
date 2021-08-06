#!/usr/bin/env python3
# coding  : utf-8
# @author : Francis.zz
# @date   : 2021-08-05 14:57
# @desc   : 使用并查集随机生成迷宫

"""
  0 1 2 3 4 5 6 7 8
0 # # # # # # # # #
1 #   #   #   #   #
2 # # # # # # # # #
3 #   #   #   #   #
4 # # # # # # # # #
5 #   #   #   #   #
6 # # # # # # # # #

设计思路：

1. 先构建地图
先创建一个N × M大小的地图，N和M均为奇数，设为高宽，height,width
把地图使用墙分隔成小房间，房间数量为 (height-1)/2 * (width-1)/2，
由上图可知空白房间位置(X, Y)，如(1, 1)，(3, 1)都是基数单元（x当前高，y当前宽）
墙分外墙和内墙，外墙为四周四面墙，内墙用来分隔房间，由图可知内墙节点都是1奇1偶
地图节点位置(x, y)可用索引表示 index = x * width + y

2. 利用并查集打通节点，制造迷宫
将所有内墙节点保存到集合，随机取出一个内墙节点，利用并查集查找根节点来判断其分隔的左右或者上下两个房间是否连通，
如果两个房间根节点不相同，则打通该墙，并把两个房间节点集合并到并查集，
从集合中删除该墙，循环直到集合中没有墙节点。

3. 利用控制台打印迷宫
使用二维数据表示迷宫地图，墙节点输出" #"，房间节点或者已经打通的墙节点使用"  "输出，
即可用值1或0表示，1:联通，0:墙

"""
from random import choice


class DisjointSet(object):
    """
    并查集实现，使用不交集森林实现。数组中的每个元素即为一个节点，存放其父节点的引用，根节点存放空引用或者自身
    使用map替代数组
    并查集有union和find两个方法，union合并两个树节点，find查找元素根节点
    """

    def __init__(self, ele):
        if isinstance(ele, int):
            self.parent = []
            self.rank = []
            # 初始化时每个节点的父节点都指向自身
            for i in range(ele):
                self.parent[i] = i
                self.rank[i] = 1
        elif isinstance(ele, list):
            self.parent = {}
            self.rank = {}
            for i in ele:
                self.parent[i] = i
                self.rank[i] = 1
        else:
            raise TypeError("并查集初始化失败，类型错误")

    # 按秩合并两个节点，即高度小的树合并到高度大的树上
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return
        # 按秩合并
        if self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_x] = root_y

        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_y] += 1

    # 查找元素根节点，路径压缩
    def find(self, x):
        if self.parent[x] == x:
            return x
        else:
            self.parent[x] = self.find(self.parent[x])
            return self.parent[x]


class Point(object):
    def __init__(self, h, w):
        self.x = h
        self.y = w

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


# 获取内墙分隔的两个房间的节点索引
def get_room_near_wall(wall, w):
    room_index = {}
    # 高
    x = wall.get_x()
    y = wall.get_y()
    if x % 2 != 0:
        # 左
        room_index[1] = x * w + y - 1
        # 右
        room_index[0] = x * w + y + 1
    elif y % 2 != 0:
        # 上
        room_index[0] = (x - 1) * w + y
        # 下
        room_index[1] = (x + 1) * w + y

    return room_index


if __name__ == "__main__":
    width = 31
    height = 21

    # 迷宫地图，二维数组
    maze_map = [[0 for i in range(width)] for j in range(height)]
    room_list = []
    wall_list = []

    # 构建地图
    for x in range(height):
        for y in range(width):
            if x % 2 == 1 and y % 2 == 1:
                # 房间节点
                maze_map[x][y] = 1
                room_list.append(x * width + y)
            else:
                # 墙
                maze_map[x][y] = 0
                # 内墙
                if 0 < x < height - 1 and 0 < y < width - 1 and (x + y) % 2 != 0:
                    wall_list.append(Point(x, y))

    # 初始化房间的并查集
    disjoint_set = DisjointSet(room_list)

    while len(wall_list) > 0:
        # 随机取出一面墙
        point = choice(wall_list)
        near_room_index = get_room_near_wall(point, width)
        if disjoint_set.find(near_room_index[0]) != disjoint_set.find(near_room_index[1]):
            # 拆除墙
            maze_map[point.get_x()][point.get_y()] = 1
            # 合并两个节点
            disjoint_set.union(near_room_index[0], near_room_index[1])

        wall_list.remove(point)

    # 打通入口和出口，(1, 0)和(height - 2, width - 1)
    maze_map[1][0] = 1
    maze_map[height - 2][width - 1] = 1

    for i in maze_map:
        for j in i:
            if j == 0:
                print(" #", end="")
            elif j == 1:
                print("  ", end="")
        print()
