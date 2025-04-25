from math import sqrt, sin, cos, pi
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
import numpy as np
from . import constants

def latitude_to_angular_velocity(latitude):
    # 返回在当地东北天坐标系下的速度分量
    omega_north = constants.EARTH_ROTATION_RATE * cos(latitude)
    omega_up = constants.EARTH_ROTATION_RATE * sin(latitude)

    return [0, omega_north, omega_up]

def orbit_period(semimajor_axis):
    return sqrt( 4*pi**2 * semimajor_axis**3 / constants.GM_EARTH ) # Kepler's Third laws of planetary motion

def orbit_angular_rate(semimajor_axis):
    return 2*pi / orbit_period(semimajor_axis)

# https://en.wikipedia.org/wiki/Latitude#Latitude_on_the_ellipsoid



def orthogonality_error(A: np.array):
    """
    计算矩阵 A 的正交性误差，基于 Frobenius 范数的偏离度计算。
    """
    I = np.eye(A.shape[1])  # 单位矩阵
    error_matrix = A.T @ A - I  # 计算 A^T A 与 I 的差
    frobenius_norm = np.linalg.norm(error_matrix, 'fro')  # Frobenius 范数
    return frobenius_norm

def theta_deg_to_cos_matrix(theta_deg):
    theta_rad = np.deg2rad(theta_deg)
    A = np.cos(theta_rad)    
    return A

def vector_angle(v1, v2):
    dot_product = np.dot(v1, v2)

    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)

    # 防止除以零错误
    if norm_v1 == 0 or norm_v2 == 0:
        raise ValueError("One of the vectors is zero, cannot compute angle.")

    cos_theta = dot_product / (norm_v1 * norm_v2)
    angle = np.arccos(cos_theta)

    return angle

def unit_vector(vector: list) -> list:
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def sphere_unit_vector(latitude: float, longitude: float):
    """
    计算球坐标系下的单位矢量。
    """

    x = np.cos(latitude) * np.cos(longitude)
    y = np.cos(latitude) * np.sin(longitude)
    z = np.sin(latitude)

    return np.array([x, y, z])

def dcm2quat(A_FG: np.array):
    """
    方向余弦矩阵到四元数的转换。与 MATLAB dcm2quat 定义一致。
    """
    A_GF = A_FG.T
    q_FG = R.from_matrix(A_GF).as_quat(scalar_first=True)

    return q_FG

def quat2dcm(q_FG: list):
    """
    四元数到方向余弦矩阵的转换。与 MATLAB quat2dcm 定义一致。
    """
    A_GF = R.from_quat(q_FG, scalar_first=True).as_matrix()

    return A_GF.T

def rotate_z(rot):
    # 2.164 (Markley 2014)
    return np.array([[ cos(rot),  sin(rot),  0],
                     [-sin(rot),  cos(rot),  0],
                     [        0,         0,  1]])

def rotate_y(rot):
    # 2.164 (Markley 2014)
    return np.array([[ cos(rot),  0,  -sin(rot)],
                     [        0,  1,         0],
                     [ sin(rot),  0,   cos(rot)]])

def rotate_x(rot):
    # 2.164 (Markley 2014)
    return np.array([[ 1,         0,        0],
                     [ 0,  cos(rot),  sin(rot)],
                     [ 0, -sin(rot),  cos(rot)]])

def euler2dcm(seq: str, angles, degrees: bool = False):
    """
    将欧拉角转换为方向余弦矩阵。
    :param euler: 欧拉角列表 [phi, theta, psi]
    :param order: 欧拉角顺序
    :return: 方向余弦矩阵
    """
    r = R.from_euler(seq, angles, degrees).as_matrix().transpose()
    return r


def generate_spherical_points_golden_spiral_method(n):
    """黄金螺旋法，生成球面均匀分布的 n 个点。"""
    phi = (1 + np.sqrt(5)) / 2  # 黄金比例
    points = []
    for i in range(n):
        z = 1 - 2 * i / (n - 1)  # 均匀分布 z 值
        theta = np.arccos(z)  # Polar angle
        azimuth = 2 * np.pi * phi * i  # 经度角
        x = np.sin(theta) * np.cos(azimuth)
        y = np.sin(theta) * np.sin(azimuth)
        points.append((x, y, z))
    return np.array(points)


if __name__ == "__main__":
    q = [0.7071, 0.7071, 0, 0]

    A = quat2dcm(q)

    print(A)

    print(dcm2quat(A))

    # 生成100个点
    points = generate_spherical_points_golden_spiral_method(1000)

    # 绘制3D球面点
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=10)
    ax.set_box_aspect([1, 1, 1])
    # plt.show()

    print(rotate_x(0.1) @ rotate_y(0.2) @ rotate_z(0.3) - euler2dcm('ZYX', [0.3, 0.2, 0.1]))
    print(rotate_z(0.1) @ rotate_y(0.2) @ rotate_x(0.3) - euler2dcm('XYZ', [0.3, 0.2, 0.1]))

