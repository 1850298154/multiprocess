import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
import matplotlib.dates as mdates

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from entity import MAP_SIZE


def plot_comm_topoloty(workers, comm_alive_dict):
    # 创建一个新的图像
    fig, ax = plt.subplots()

    # 绘制网络图的节点
    for worker in workers:
        circle = Circle(worker.pose, radius=2, edgecolor='black', facecolor='skyblue')  # 创建一个圆形
        ax.add_patch(circle)  # 将圆形添加到图像中
        ax.text(worker.pose[0], worker.pose[1], worker.name, fontsize=6, ha='center', va='center', color='black')  # 绘制标签

    # 绘制网络图的边
    for (worker_name, other_name), alive in comm_alive_dict.items():
        if alive:
            worker_pose = next(worker.pose for worker in workers if worker.name == worker_name)
            other_pose = next(worker.pose for worker in workers if worker.name == other_name)
            ax.plot([worker_pose[0], other_pose[0]], [worker_pose[1], other_pose[1]], color='grey', linewidth=1.5)  # 绘制边

    # 设置坐标轴的范围
    ax.set_xlim(0, MAP_SIZE)
    ax.set_ylim(0, MAP_SIZE)

    # 移除坐标轴
    ax.axis('off')

    # 显示图像
    plt.pause(3)
    

def plot_agent_value(final_workers):
    
    colors = iter([plt.cm.tab20(i) for i in range(20)])
    fig, ax = plt.subplots()

    for worker in final_workers:
        ax.plot(worker.time_list, worker.comm_iter_list, 
                linewidth = 3,
                color = next(colors),
                label=worker.name
                )


    # 获取最后一个数据的横坐标值
    # 获取最后一个数据的横坐标值
    max_times = [max(worker.time_list) for worker in final_workers]
    last_x = max(max_times)
    # 在最后一个数据上画一条红色虚线
    ax.axvline(x=last_x, color='red', linestyle='--')

    # 在图上添加横坐标值
    ax.text(last_x, 0, str(last_x), color='red', ha='right')


    # 设置标题和坐标轴标签
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .22), loc='lower left',
            ncol=10, mode="expand", borderaxespad=0.,
            frameon=True,
            fancybox=True,
            fontsize=6,
            edgecolor='black')

    # 显示图像
    plt.show()
