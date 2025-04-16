from maze import Maze
from astar import AStar
from visualizer import Visualizer

def main():
    # 创建迷宫
    maze = Maze()
    maze.generate()
    
    # 创建A*算法实例
    astar = AStar(maze.get_maze())
    
    # 获取起点和终点
    start = maze.get_start()
    end = maze.get_end()
    
    # 寻找路径
    path, costs = astar.find_path(start, end)
    
    # 创建可视化器
    visualizer = Visualizer(maze.get_maze())
    
    # 绘制路径
    visualizer.draw_path(path, costs)
    
    # 显示迷宫
    visualizer.show()

if __name__ == "__main__":
    main() 