import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

from .draw_utils import COLOR, LINE_STYLE

def draw_success_precision(success_ret, name, videos, attr, precision_ret=None,
        norm_precision_ret=None, bold_name=None, axis=[0, 1]):
    # success plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.grid(visible=True, linestyle='-', linewidth=0.5, alpha=0.7)
    ax.set_aspect(1)
    plt.xlabel('Overlap threshold',fontsize=14)
    plt.ylabel('Success rate',fontsize=14)
    if attr == 'ALL':
        plt.title("Success plots of OPE on %s" % (name),fontsize=14)
    else:
        plt.title("Success plots of OPE - %s" % (attr),fontsize=14)
    plt.axis([0, 1]+axis)
    success = {}
    thresholds = np.arange(0, 1.05, 0.05)
    for tracker_name in success_ret.keys():
        value = [v for k, v in success_ret[tracker_name].items() if k in videos]
        success[tracker_name] = np.mean(value)
    for idx, (tracker_name, auc) in  \
            enumerate(sorted(success.items(), key=lambda x:x[1], reverse=True)):
        if tracker_name == bold_name:
            label = r"\textbf{[%.3f] %s}" % (auc, tracker_name)
        else:
            label = "[%.3f] " % (auc) + tracker_name
        value = [v for k, v in success_ret[tracker_name].items() if k in videos]
        plt.plot(thresholds, np.mean(value, axis=0),
                color=COLOR[idx], linestyle=LINE_STYLE[idx],label=label, linewidth=2)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}' if x.is_integer() else f'{x:.1f}'))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{int(y)}' if y.is_integer() else f'{y:.1f}'))
    ax.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), fontsize=11, labelspacing=0.5)
    ax.autoscale(enable=True, axis='both', tight=True)
    xmin, xmax, ymin, ymax = plt.axis()
    ax.autoscale(enable=False)
    ax.tick_params(direction='in')
    ymax += 0.03
    plt.axis([xmin, xmax, ymin, ymax])
    plt.xticks(np.arange(xmin, xmax+0.01, 0.1))
    plt.yticks(np.arange(ymin, ymax, 0.1))
    ax.set_aspect((xmax - xmin)/(ymax-ymin))
    plt.tight_layout()
    path = f'./succ_prec/{attr}'
    if not os.path.exists(path):
        os.makedirs(path)
    plt.savefig(f'{path}/success.png')
    matplotlib.pyplot.close()


    if precision_ret:
        # norm precision plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.grid(visible=True, linestyle='-', linewidth=0.5, alpha=0.7)
        ax.set_aspect(50)
        plt.xlabel('Location error threshold',fontsize=14)
        plt.ylabel('Precision',fontsize=14)
        if attr == 'ALL':
            plt.title("Precision plots of OPE on %s" % (name))
        else:
            plt.title("Precision plots of OPE - %s" % (attr))
        plt.axis([0, 50]+axis)
        precision = {}
        thresholds = np.arange(0, 51, 1)
        for tracker_name in precision_ret.keys():
            value = [v for k, v in precision_ret[tracker_name].items() if k in videos]
            precision[tracker_name] = np.mean(value, axis=0)[20]
        for idx, (tracker_name, pre) in \
                enumerate(sorted(precision.items(), key=lambda x:x[1], reverse=True)):
            if tracker_name == bold_name:
                label = r"\textbf{[%.3f] %s}" % (pre, tracker_name)
            else:
                label = "[%.3f] " % (pre) + tracker_name
            value = [v for k, v in precision_ret[tracker_name].items() if k in videos]
            plt.plot(thresholds, np.mean(value, axis=0),
                    color=COLOR[idx], linestyle=LINE_STYLE[idx],label=label, linewidth=2)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}' if x.is_integer() else f'{x:.1f}'))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{int(y)}' if y.is_integer() else f'{y:.1f}'))
        ax.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), fontsize=11, labelspacing=0.5)
        ax.autoscale(enable=True, axis='both', tight=True)
        ax.tick_params(direction='in')
        xmin, xmax, ymin, ymax = plt.axis()
        ax.autoscale(enable=False)
        ymax += 0.03
        plt.axis([xmin, xmax, ymin, ymax])
        plt.xticks(np.arange(xmin, xmax+0.01, 5))
        plt.yticks(np.arange(ymin, ymax, 0.1))
        ax.set_aspect((xmax - xmin)/(ymax-ymin))
        plt.tight_layout()
        path = f'./succ_prec/{attr}'
        if not os.path.exists(path):
            os.makedirs(path)
        plt.savefig(f'{path}/pre.png')
        matplotlib.pyplot.close()

    # print(attr, " success:%.3f" % (auc), " precision:%.3f" % (pre))
    # norm precision plot
    if norm_precision_ret:
        fig, ax = plt.subplots()
        ax.grid(b=True)
        plt.xlabel('Location error threshold')
        plt.ylabel('Precision')
        if attr == 'ALL':
            plt.title(r'\textbf{Normalized Precision plots of OPE on %s}' % (name))
        else:
            plt.title(r'\textbf{Normalized Precision plots of OPE - %s}' % (attr))
        norm_precision = {}
        thresholds = np.arange(0, 51, 1) / 100
        for tracker_name in precision_ret.keys():
            value = [v for k, v in norm_precision_ret[tracker_name].items() if k in videos]
            norm_precision[tracker_name] = np.mean(value, axis=0)[20]
        for idx, (tracker_name, pre) in \
                enumerate(sorted(norm_precision.items(), key=lambda x:x[1], reverse=True)):
            if tracker_name == bold_name:
                label = r"\textbf{[%.3f] %s}" % (pre, tracker_name)
            else:
                label = "[%.3f] " % (pre) + tracker_name
            value = [v for k, v in norm_precision_ret[tracker_name].items() if k in videos]
            plt.plot(thresholds, np.mean(value, axis=0),
                    color=COLOR[idx], linestyle=LINE_STYLE[idx],label=label, linewidth=2)
        ax.legend(loc='lower right', labelspacing=0.2)
        ax.autoscale(enable=True, axis='both', tight=True)
        xmin, xmax, ymin, ymax = plt.axis()
        ax.autoscale(enable=False)
        ymax += 0.03
        plt.axis([xmin, xmax, ymin, ymax])
        plt.xticks(np.arange(xmin, xmax+0.01, 0.05))
        plt.yticks(np.arange(ymin, ymax, 0.1))
        ax.set_aspect((xmax - xmin)/(ymax-ymin))

