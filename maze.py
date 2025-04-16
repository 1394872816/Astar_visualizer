import numpy as np
import random

class Maze:
    """
    迷宫生成类
    开发日志：
    2025.04.15 - 初始版本
    - 实现基本的DFS迷宫生成算法
    - 添加入口和出口缺口
    - 使用numpy数组存储迷宫数据
    
    2025.04.16 - 更新版本
    - 增加迷宫默认尺寸到41x41
    - 实现随机起点和终点生成
    - 确保起点和终点在迷宫边界上
    - 优化路径生成算法，保证起点和终点连通
    """
    
    def __init__(self, width=41, height=41):
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        self.maze = np.ones((self.height, self.width), dtype=int)
        self.start = None
        self.end = None
        
    def generate_start_end(self):
        # 生成起点（在左边界）
        start_y = random.randint(1, self.height-2)
        while self.maze[start_y, 1] == 1:  # 确保起点附近有通路
            start_y = random.randint(1, self.height-2)
        self.start = (start_y, 0)
        
        # 生成终点（在右边界）
        end_y = random.randint(1, self.height-2)
        while self.maze[end_y, self.width-2] == 1:  # 确保终点附近有通路
            end_y = random.randint(1, self.height-2)
        self.end = (end_y, self.width-1)
        
        # 打通起点和终点的通道
        self.maze[start_y, 0] = 0
        self.maze[end_y, self.width-1] = 0
        
    def generate(self):
        # 初始化起点
        self.maze[1, 1] = 0
        
        # 定义四个方向：上、右、下、左
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        
        # 使用栈来记住走过的路
        stack = [(1, 1)]
        
        while stack:
            current = stack[-1]
            x, y = current
            
            # 看看周围哪些地方还没去过
            unvisited = []
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 < nx < self.height-1 and 0 < ny < self.width-1 and 
                    self.maze[nx, ny] == 1):
                    unvisited.append((nx, ny))
            
            if unvisited:
                # 随机选一个没去过的地方
                next_cell = random.choice(unvisited)
                nx, ny = next_cell
                
                # 打通中间的墙
                self.maze[(x + nx) // 2, (y + ny) // 2] = 0
                self.maze[nx, ny] = 0
                
                stack.append(next_cell)
            else:
                # 走到死路了，回退一步
                stack.pop()
        
        # 生成随机起点和终点
        self.generate_start_end()
    
    def get_maze(self):
        return self.maze
    
    def get_start(self):
        return self.start
    
    def get_end(self):
        return self.end 