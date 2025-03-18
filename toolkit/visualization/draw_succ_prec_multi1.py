import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib import font_manager
import os

from .draw_utils import COLOR, LINE_STYLE

def draw_success_precision(success_ret, name, videos, attr, precision_ret=None,
                          norm_precision_ret=None, bold_name=None, axis=[0, 1]):
    # 启用 LaTeX 渲染
    plt.rc('text', usetex=True)
    
    # 指定 Times New Roman 字体的绝对路径
    font_path = "../../../../usr/share/fonts/times.ttf"  # 正常字体路径
    
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"指定的字体文件未找到: {font_path}")
    
    font_prop = font_manager.FontProperties(fname=font_path)
    rcParams['font.family'] = font_prop.get_name()
    rcParams['font.size'] = 14  # 设置全局字体大小，可以根据需要调整
    
    # 设置 LaTeX 字体为 Times
    rcParams['text.latex.preamble'] = r'\usepackage{times}'
    
    # 创建图形和坐标轴
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.grid(visible=True, linestyle='-', linewidth=0.5, alpha=0.7)
    
    # 设置坐标轴标签
    ax.set_xlabel(r"\textbf{Overlap threshold}", fontsize=18)
    ax.set_ylabel(r"\textbf{Success rate}", fontsize=18)
    
    # 设置标题
    if attr == 'ALL':
        # ax.set_title(r"\textbf{Success plots}", fontsize=18)
        plt.title(r"$\textbf{Success plots of OPE on %s}$" % name, fontsize=18)
    else:
        ax.set_title(f"Success plots of OPE - {attr}", fontsize=18)
    
    # 设置坐标轴范围
    ax.set_xlim(0, 1)
    ax.set_ylim(axis[0], axis[1])
    
    success = {}
    thresholds = np.arange(0, 1.05, 0.05)

    # 计算成功率均值
    for tracker_name in success_ret.keys():
        values = [v for k, v in success_ret[tracker_name].items() if k in videos]
        success[tracker_name] = np.mean(values)
    
    # 按成功率排序并绘图
    for idx, (tracker_name, auc) in enumerate(
            # sorted(success.items(), key=lambda x: x[1], reverse=True)):
            sorted(success.items(), key=lambda x: (x[0] != "SiamFFLA", -x[1]))):
        if tracker_name == "SiamFFLA":
            label = r"\textbf{[%.3f] SiamFFLA (Ours)}" % auc
        else:
            label = "[%.3f] %s" % (auc, tracker_name)
        
        values = [v for k, v in success_ret[tracker_name].items() if k in videos]
        mean_values = np.mean(values, axis=0)
        
        ax.plot(thresholds, mean_values,
                color=COLOR[idx % len(COLOR)],
                linestyle=LINE_STYLE[idx % len(LINE_STYLE)],
                label=label, linewidth=3)
    
    # 格式化坐标轴刻度
    ax.xaxis.set_major_formatter(plt.FuncFormatter(
        lambda x, _: f'{int(x)}' if x.is_integer() else f'{x:.1f}'))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(
        lambda y, _: f'{int(y)}' if y.is_integer() else f'{y:.1f}'))
    
    # 设置图例
    ax.legend(loc='center left', bbox_to_anchor=(1.01, 0.5),
              fontsize=14, labelspacing=0.2, frameon=True,
              edgecolor='black', framealpha=1)
    
    # 调整坐标轴
    ax.autoscale(enable=True, axis='both', tight=True)
    ax.tick_params(direction='in', labelsize=12)
    xmin, xmax, ymin, ymax = ax.axis()
    ymax += 0.03
    ax.set_ylim(ymin, ymax)
    ax.set_xticks(np.arange(0, 1.01, 0.1))
    ax.set_yticks(np.arange(ymin, ymax, 0.1))
    ax.set_aspect((xmax - xmin)/(ymax - ymin))
    
    # 优化布局并保存图像
    plt.tight_layout()
    # plt.savefig('./succ_prec_multi/success.png', dpi=300, bbox_inches='tight')
    plt.savefig('./succ_prec_multi/success.pdf', dpi=300, bbox_inches='tight', format='pdf')

    if precision_ret:
        # 准确率图
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.grid(visible=True, linestyle='-', linewidth=0.5, alpha=0.7)
        
        plt.xlabel(r"\textbf{Location error threshold}", fontsize=18)
        plt.ylabel(r"\textbf{Precision}", fontsize=18)
        
        if attr == 'ALL':
            # plt.title(r"\textbf{Precision plots}", fontsize=18)
            plt.title(r"$\textbf{Precision plots of OPE on %s}$" % name, fontsize=18)
        else:
            plt.title(f"Precision plots of OPE - {attr}", fontsize=18)
        
        ax.set_xlim(0, 50)
        ax.set_ylim(axis[0], axis[1])
        
        precision = {}
        thresholds = np.arange(0, 51, 1)

        for tracker_name in precision_ret.keys():
            values = [v for k, v in precision_ret[tracker_name].items() if k in videos]
            # 假设取第20个阈值的均值，具体根据需求调整
            precision[tracker_name] = np.mean([v[20] for v in values])
        
        for idx, (tracker_name, pre) in enumerate(
                # sorted(precision.items(), key=lambda x: (x[0] != "SiamFFLA", -x[1]))):
                sorted(precision.items(), key=lambda x: x[1], reverse=True)):
            if tracker_name == "SiamFFLA":
                label = r"\textbf{[%.3f] SiamFFLA (Ours)}" % pre
            else:
                label = "[%.3f] %s" % (pre, tracker_name)
            
            values = [v for k, v in precision_ret[tracker_name].items() if k in videos]
            mean_values = np.mean(values, axis=0)
            
            ax.plot(thresholds, mean_values,
                    color=COLOR[idx % len(COLOR)],
                    linestyle=LINE_STYLE[idx % len(LINE_STYLE)],
                    label=label, linewidth=3)
        
        # 格式化坐标轴刻度
        ax.xaxis.set_major_formatter(plt.FuncFormatter(
            lambda x, _: f'{int(x)}' if x.is_integer() else f'{x:.1f}'))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(
            lambda y, _: f'{int(y)}' if y.is_integer() else f'{y:.1f}'))
        
        # 设置图例
        ax.legend(loc='center left', bbox_to_anchor=(1.01, 0.5),
                  fontsize=14, labelspacing=0.2, frameon=True,
                  edgecolor='black', framealpha=1)
        
        # 调整坐标轴
        ax.autoscale(enable=True, axis='both', tight=True)
        ax.tick_params(direction='in', labelsize=12)
        xmin, xmax, ymin, ymax = ax.axis()
        ymax += 0.03
        ax.set_ylim(ymin, ymax)
        ax.set_xticks(np.arange(0, 51, 5))
        ax.set_yticks(np.arange(ymin, ymax, 0.1))
        ax.set_aspect((xmax - xmin)/(ymax - ymin))
        
        # 优化布局并保存图像
        plt.tight_layout()
        # plt.savefig('./succ_prec_multi/precision.png', dpi=300, bbox_inches='tight')
        plt.savefig('./succ_prec_multi/precision.pdf', dpi=300, bbox_inches='tight', format='pdf')
