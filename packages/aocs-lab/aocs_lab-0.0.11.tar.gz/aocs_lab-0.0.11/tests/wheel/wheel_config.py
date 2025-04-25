"""飞轮配置设计"""
import numpy as np
import matplotlib.pyplot as plt


def plot_wheel_config(n: np.ndarray):
    """绘制飞轮配置"""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(0, 0, 0, 1, 0, 0, color='b', label='x')
    ax.quiver(0, 0, 0, 0, 1, 0, color='b', label='y')
    ax.quiver(0, 0, 0, 0, 0, 1, color='b', label='z')
    ax.text(1, 0, 0, 'x', color='b')
    ax.text(0, 1, 0, 'y', color='b')
    ax.text(0, 0, 1, 'z', color='b')

    ax.quiver(0, 0, 0, n[0], n[1], n[2], color='r')
    ax.quiver(0, 0, 0, n[0], n[1], -n[2], color='g')
    ax.quiver(0, 0, 0, n[0], -n[1], n[2], color='k')
    ax.quiver(0, 0, 0, n[0], -n[1], -n[2], color='y')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-1.5, 1.5)
    ax.set_aspect('equal', adjustable='box')  # 使用 'box' 以保持轴标签的比例·
    plt.grid()
    plt.show()


def calc_wheel_config(inertial: np.ndarray, omega: np.ndarray):
    """计算飞轮配置"""
    # 主轴惯量
    # 角速度需求

    h = inertial * omega
    n = h / np.linalg.norm(h)

    ny = np.array([1, -1, 1])
    nz = np.array([1, 1, -1])

    wheel_n = []
    wheel_n.append(n)
    wheel_n.append(n*ny)
    wheel_n.append(n*nz)
    wheel_n.append(n*ny*nz)

    print(f"三轴动量需求: [{h[0]:.3f}, {h[1]:.3f}, {h[2]:.3f}] Nms")
    print(f"飞轮角动量需求: {np.linalg.norm(h):.3f} Nms")
    print("本体系下飞轮角动量方向单位矢量")
    for i, v in enumerate(wheel_n):
        print(f"飞轮 {i}: [{v[0]:6.3f}, {v[1]:6.3f}, {v[2]:6.3f}]", end=' ')
        print(f"或 [{-v[0]:6.3f}, {-v[1]:6.3f}, {-v[2]:6.3f}]")

    return n


if __name__ == "__main__":

    wheel_v = calc_wheel_config(
        inertial=np.array([100, 300, 300]),
        omega=np.array(np.deg2rad([1, 1, 1])))

    # plot_wheel_config(wheel_v)
