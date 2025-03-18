# cle_plotter.py

import numpy as np
import matplotlib.pyplot as plt
from typing import List
from matplotlib import rcParams
from matplotlib import font_manager
import os

class CLEPlotter:
    """
    一个用于计算和绘制中心位置误差（CLE, Center Location Error）曲线图的类。
    """
    
    def __init__(self, gt_center: List[np.ndarray], tracker_center: List[np.ndarray]):
        """
        初始化 CLEPlotter 类。
        
        参数:
            gt_center (List[np.ndarray]): 地面真实中心轨迹，格式为 [np.array([x1, y1]), np.array([x2, y2]), ...]
            tracker_center (List[np.ndarray]): 跟踪器预测中心轨迹，格式为 [np.array([x1, y1]), np.array([x2, y2]), ...]
        """
        if len(gt_center) != len(tracker_center):
            raise ValueError("gt_center 和 tracker_center 的长度不一致。")
        
        self.gt_center = np.vstack(gt_center)  # 转换为二维数组，形状为 (num_frames, 2)
        self.tracker_center = np.vstack(tracker_center)  # 转换为二维数组，形状为 (num_frames, 2)
        self.cle = self._calculate_cle()
    
    def _calculate_cle(self) -> np.ndarray:
        """
        计算每一帧的中心位置误差（CLE）。
        
        返回:
            np.ndarray: 每一帧的 CLE 值。
        """
        cle = np.linalg.norm(self.gt_center - self.tracker_center, axis=1)
        return cle
    
    
    def save_plot(self, dataset:str,filename: str):
        """
        将 CLE 曲线图保存为图片文件。
        
        参数:
            filename (str): 保存的文件名
            title (str): 图表标题。
            xlabel (str): X 轴标签。
            ylabel (str): Y 轴标签。
        """
        plt.rc('text', usetex=True)  # 启用 LaTeX 渲染
        font_path = "../../../../../usr/share/fonts/times.ttf"  # 正常字体路径
        font_prop = font_manager.FontProperties(fname=font_path)
        rcParams['font.family'] = font_prop.get_name()

        frames = np.arange(1, len(self.cle) + 1)
        
        # 使用 fig 和 ax 绘图
        # fig, ax = plt.subplots(figsize=(14, 2.5))#uav123,uavdt
        fig, ax = plt.subplots(figsize=(12, 2.5))
        ax.plot(frames, self.cle, label=r"$\textbf{CLE}$", color='red', linewidth=2)
        # 添加水平虚线
        threshold = 20  # 设定水平虚线的位置
        ax.hlines(y=threshold, xmin=frames[0], xmax=frames[-1], colors='blue', linestyles='--', linewidth=2, label='Threshold')
        ax.set_xlabel(r"$\textbf{Frame(\#)}$", fontsize=14)
        ax.set_ylabel(r"$\textbf{CLE}$", fontsize=14)
        # 设置坐标轴范围
        ax.set_xlim([min(frames), max(frames)])  # 设置 X 轴范围
        ax.set_ylim([0, 25])  # 设置 Y 轴范围
        
        ax.grid(visible=True, linestyle='-', linewidth=0.5, alpha=0.7)
        ax.tick_params(direction='in',labelsize=14)
        

        # 调整布局
        fig.tight_layout()

        save_path = f'./CLE/{dataset}/' + filename
        
        plt.savefig(save_path,dpi=300,bbox_inches='tight')
        plt.close()
        print(f"CLE 曲线图已保存为 {filename}")

# 如果需要，可以添加一个示例用法
if __name__ == "__main__":
    # 示例数据
    gt_center = [
        np.array([716.5, 443.0]),
        np.array([701.0, 436.5]),
        np.array([692.0, 424.5]),
        np.array([680.0, 420.0]),
        np.array([670.0, 415.0]),
        np.array([660.0, 410.0]),
        np.array([650.0, 405.0]),
        np.array([640.0, 400.0]),
        np.array([630.0, 395.0]),
        np.array([620.0, 390.0])
    ]

    tracker_center = [
        np.array([718.0, 445.0]),
        np.array([700.5, 434.0]),
        np.array([691.0, 423.0]),
        np.array([679.5, 419.0]),
        np.array([669.5, 414.5]),
        np.array([659.5, 409.5]),
        np.array([649.5, 404.5]),
        np.array([639.5, 399.5]),
        np.array([629.5, 394.5]),
        np.array([619.5, 389.5])
    ]

    # 创建 CLEPlotter 实例
    cle_plotter = CLEPlotter(gt_center=gt_center, tracker_center=tracker_center)
    
    # 保存 CLE 曲线图为图片
    cle_plotter.save_plot('cle_plot.png')
