import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import numpy as np
from matplotlib import font_manager

class Visualizer:
    """
    迷宫可视化类
    开发日志：
    2025.04.15 22:13 - 初始构想
    - 确定使用matplotlib作为可视化工具
    - 设计迷宫和文本显示区域布局
    - 规划按钮和交互功能

    2025.04.15 22:45 - 基础框架
    - 创建Visualizer类基本结构
    - 实现迷宫矩阵显示
    - 设置中文字体支持

    2025.04.15 23:28 - 界面布局
    - 划分迷宫和信息显示区域
    - 创建按钮控制区域
    - 设置文本框样式

    2025.04.16 09:35 - 路径显示
    - 实现起点终点标记
    - 添加路径绘制功能
    - 优化显示比例

    2025.04.16 09:57 - 动画控制
    - 实现动画更新逻辑
    - 添加暂停继续功能
    - 优化帧率控制

    2025.04.16 10:19 - 信息展示
    - 实现代价信息显示
    - 添加节点状态显示
    - 优化文本布局

    2025.04.16 10:42 - 交互优化
    - 完善按钮响应逻辑
    - 优化动画流畅度
    - 添加进度显示
    """
    
    def __init__(self, maze):
        """
        初始化可视化器
        设置说明：
        - 设置中文字体，不然显示不了中文
        - 创建一个足够大的画布
        - 添加一个开始按钮
        """
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        
        self.maze = maze
        maze_height, maze_width = maze.shape
        # 调整画布大小，为文本显示区域留出空间
        fig_width = max(15, maze_width / 3)
        fig_height = max(10, maze_height / 4)
        self.fig = plt.figure(figsize=(fig_width, fig_height))
        
        # 创建迷宫显示区域
        self.maze_ax = plt.axes([0.1, 0.1, 0.5, 0.8])
        self.maze_ax.set_xticks([])
        self.maze_ax.set_yticks([])
        
        # 创建文本显示区域
        self.text_ax = plt.axes([0.65, 0.1, 0.3, 0.8])
        self.text_ax.set_xticks([])
        self.text_ax.set_yticks([])
        self.text_ax.set_title('A*算法信息', fontsize=14, pad=15)
        
        # 设置文本框背景色和边框
        self.text_ax.set_facecolor('#f0f0f0')
        for spine in self.text_ax.spines.values():
            spine.set_color('#cccccc')
            spine.set_linewidth(2)
        
        self.path_points = []
        self.current_path = []
        self.animation = None
        self.is_animating = False
        self.is_paused = False
        self.cost_history = []
        
        # 创建按钮区域
        self.button_ax = plt.axes([0.1, 0.92, 0.15, 0.05])
        self.start_button = Button(self.button_ax, '开始寻路')
        self.start_button.on_clicked(self.start_animation)
        
        self.pause_ax = plt.axes([0.3, 0.92, 0.15, 0.05])
        self.pause_button = Button(self.pause_ax, '暂停/继续')
        self.pause_button.on_clicked(self.toggle_pause)
        
    def draw_maze(self):
        """
        绘制迷宫
        怎么画？
        - 用黑白二值图显示迷宫（1是黑，0是白）
        - 隐藏坐标轴，让画面更干净
        - 用绿色圆点标记起点，红色圆点标记终点
        """
        self.maze_ax.clear()
        self.maze_ax.imshow(self.maze, cmap='binary')
        self.maze_ax.set_xticks([])
        self.maze_ax.set_yticks([])
        
        # 标记起点和终点
        if self.path_points:
            start = self.path_points[0]
            end = self.path_points[-1]
            marker_size = max(10, min(20, self.maze.shape[0] / 4))
            self.maze_ax.plot(start[1], start[0], 'go', markersize=marker_size)
            self.maze_ax.plot(end[1], end[0], 'ro', markersize=marker_size)
        
    def draw_path(self, path, costs=None):
        """
        绘制路径
        准备工作：
        - 保存完整的路径信息
        - 清空当前显示的路径
        - 重新绘制迷宫
        """
        self.path_points = path
        self.current_path = []
        self.cost_history = costs if costs else []
        self.draw_maze()
        
    def update(self, frame):
        """
        更新动画帧
        动画效果：
        - 一帧一帧地添加路径点
        - 实时更新显示
        - 保持起点和终点的标记
        """
        if frame < len(self.path_points):
            self.current_path.append(self.path_points[frame])
            self.draw_maze()
            
            # 绘制已探索的路径
            if self.current_path:
                path_x = [p[1] for p in self.current_path]
                path_y = [p[0] for p in self.current_path]
                line_width = max(1, min(3, self.maze.shape[0] / 20))
                self.maze_ax.plot(path_x, path_y, 'r-', linewidth=line_width)
                
                # 更新代价信息
                if self.cost_history and frame < len(self.cost_history):
                    self.text_ax.clear()
                    self.text_ax.set_xticks([])
                    self.text_ax.set_yticks([])
                    self.text_ax.set_title('A*算法信息', fontsize=14, pad=15)
                    
                    current_cost = self.cost_history[frame]
                    current_node = self.path_points[frame]
                    
                    # 创建信息文本
                    info_text = []
                    info_text.append('当前节点信息:')
                    info_text.append(f'坐标: ({current_node[0]}, {current_node[1]})')
                    
                    # 根据状态显示不同的状态文本
                    status_text = {
                        "evaluating": "评估中",
                        "reached": "已到达终点",
                        "on_path": "在最短路径上"
                    }.get(current_cost["status"], "未知状态")
                    info_text.append(f'状态: {status_text}')
                    
                    info_text.append('')
                    info_text.append('代价评估:')
                    info_text.append(f'g(n) = {current_cost["g"]:.2f} (实际代价)')
                    info_text.append(f'h(n) = {current_cost["h"]:.2f} (估计代价)')
                    info_text.append(f'f(n) = {current_cost["f"]:.2f} (总评估值)')
                    
                    info_text.append('')
                    info_text.append('搜索进度:')
                    info_text.append(f'已探索节点: {frame + 1}')
                    info_text.append(f'剩余节点: {len(self.path_points) - frame - 1}')
                    
                    # 设置文本样式
                    text_props = dict(
                        fontsize=11,
                        verticalalignment='center',
                        horizontalalignment='left',
                        transform=self.text_ax.transAxes
                    )
                    
                    # 绘制文本
                    y_pos = 0.95
                    for line in info_text:
                        if ':' in line:
                            # 标题行加粗
                            self.text_ax.text(0.1, y_pos, line, 
                                            fontweight='bold', **text_props)
                        else:
                            self.text_ax.text(0.1, y_pos, line, **text_props)
                        y_pos -= 0.07  # 减小行间距
    
    def start_animation(self, event):
        """
        开始动画
        点击按钮后：
        - 检查是否已经有路径
        - 防止重复点击
        - 创建动画对象开始播放
        """
        if not self.is_animating and self.path_points:
            self.is_animating = True
            self.is_paused = False
            interval = max(50, min(200, self.maze.shape[0] * 2))
            self.animation = animation.FuncAnimation(
                self.fig, self.update, frames=len(self.path_points),
                interval=interval, repeat=False
            )
            plt.draw()
    
    def toggle_pause(self, event):
        if self.is_animating:
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.animation.event_source.stop()
            else:
                self.animation.event_source.start()
    
    def show(self):
        """
        显示迷宫
        显示流程：
        - 先画好迷宫
        - 显示整个界面
        - 等待用户点击按钮
        """
        self.draw_maze()
        plt.show() 