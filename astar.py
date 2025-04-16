"""
A*寻路算法实现类
开发日志：
2025.04.15 19:23 - 初始设计
- 设计Node类数据结构
- 规划A*算法框架
- 确定启发式函数方案

2025.04.15 20:05 - 基础实现
- 实现Node类基本属性
- 添加节点比较逻辑
- 创建AStar类框架

2025.04.15 21:17 - 核心功能
- 实现启发式函数
- 添加邻居节点获取
- 设计代价记录结构

2025.04.15 22:46 - 路径搜索
- 实现open/closed列表
- 添加节点扩展逻辑
- 完善代价计算

2025.04.16 09:28 - 优化结构
- 优化节点状态管理
- 完善路径记录
- 改进数据存储

2025.04.16 09:52 - 路径生成
- 实现路径重建
- 生成路径代价信息
- 优化状态记录

2025.04.16 10:08 - 边界处理
- 添加边界检查
- 完善异常处理
- 优化搜索性能
"""

import heapq
from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple, Any

@dataclass
class Node:
    """节点类，存储节点信息和代价"""
    pos: Tuple[int, int]  # 位置坐标
    g: float = float('inf')  # 从起点到当前节点的实际代价
    h: float = float('inf')  # 从当前节点到终点的估计代价
    f: float = float('inf')  # 总代价 f = g + h
    parent: Any = None  # 父节点
    status: str = "evaluating"  # 节点状态：evaluating（评估中）, reached（已到达）

    def __lt__(self, other):
        return self.f < other.f

class AStar:
    """
    A*寻路算法实现类
    开发日志：
    2025.04.16 - 初始版本
    - 实现基本的A*算法
    - 使用曼哈顿距离作为启发式函数
    - 优化数据结构提高效率
    
    2025.04.17 - 更新版本
    - 优化数据结构
    - 添加代价记录功能
    - 改进路径重建逻辑
    
    2025.04.23 - 更新版本 1
    - 添加节点状态标记
    - 优化代价计算
    - 修复终点判断逻辑
    
    2025.04.23 - 更新版本 2
    - 修复路径信息与代价历史不同步问题
    - 为最终路径生成正确的代价信息
    - 优化状态显示逻辑
    """
    
    def __init__(self, maze):
        """
        初始化A*算法
        参数说明：
        - maze: 迷宫矩阵，0表示能走的路，1表示墙
        - 自动获取迷宫大小，方便后面判断边界
        """
        self.maze = maze
        self.height, self.width = maze.shape
        self.cost_history = []  # 记录每一步的代价信息
        
    def heuristic(self, pos: Tuple[int, int], end: Tuple[int, int]) -> float:
        """
        计算启发式函数值（曼哈顿距离）
        pos: 当前位置
        end: 目标位置
        """
        return abs(pos[0] - end[0]) + abs(pos[1] - end[1])
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """获取相邻可行节点"""
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # 右、下、左、上
            nx, ny = pos[0] + dx, pos[1] + dy
            if (0 <= nx < self.height and 0 <= ny < self.width and 
                self.maze[nx, ny] == 0):
                neighbors.append((nx, ny))
        return neighbors
    
    def record_step(self, node: Node):
        """记录每一步的代价信息"""
        self.cost_history.append({
            "g": node.g,
            "h": node.h,
            "f": node.f,
            "status": node.status
        })
    
    def generate_path_costs(self, path: List[Tuple[int, int]], end: Tuple[int, int]) -> List[Dict]:
        """为最终路径生成正确的代价信息"""
        path_costs = []
        for i, pos in enumerate(path):
            # 计算实际代价（从起点到当前点的距离）
            g = i  # 每一步代价为1
            # 计算估计代价（从当前点到终点的曼哈顿距离）
            h = self.heuristic(pos, end)
            # 计算总代价
            f = g + h
            # 设置状态
            status = "reached" if pos == end else "on_path"
            
            path_costs.append({
                "g": float(g),
                "h": float(h),
                "f": float(f),
                "status": status
            })
        return path_costs
    
    def find_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], List[Dict]]:
        """
        A*寻路算法主函数
        start: 起点坐标
        end: 终点坐标
        返回：(路径, 代价历史)
        """
        # 初始化数据结构
        open_list: List[Node] = []
        closed_set: Set[Tuple[int, int]] = set()
        nodes: Dict[Tuple[int, int], Node] = {}
        
        # 创建起始节点
        start_node = Node(pos=start)
        start_node.g = 0
        start_node.h = self.heuristic(start, end)
        start_node.f = start_node.g + start_node.h
        
        # 将起始节点加入开放列表
        nodes[start] = start_node
        heapq.heappush(open_list, start_node)
        
        while open_list:
            current = heapq.heappop(open_list)
            current_pos = current.pos
            
            if current_pos == end:
                # 重建路径
                path = []
                while current:
                    path.append(current.pos)
                    current = current.parent
                path = path[::-1]
                
                # 为最终路径生成正确的代价信息
                path_costs = self.generate_path_costs(path, end)
                return path, path_costs
            
            closed_set.add(current_pos)
            
            # 记录当前节点的评估信息
            self.record_step(current)
            
            # 处理相邻节点
            for neighbor_pos in self.get_neighbors(current_pos):
                if neighbor_pos in closed_set:
                    continue
                
                tentative_g = current.g + 1
                
                if neighbor_pos not in nodes:
                    neighbor = Node(pos=neighbor_pos)
                    nodes[neighbor_pos] = neighbor
                else:
                    neighbor = nodes[neighbor_pos]
                    if tentative_g >= neighbor.g:
                        continue
                
                neighbor.parent = current
                neighbor.g = tentative_g
                neighbor.h = self.heuristic(neighbor_pos, end)
                neighbor.f = neighbor.g + neighbor.h
                
                if neighbor_pos not in [n.pos for n in open_list]:
                    heapq.heappush(open_list, neighbor)
        
        return [], []  # 没有找到路径 