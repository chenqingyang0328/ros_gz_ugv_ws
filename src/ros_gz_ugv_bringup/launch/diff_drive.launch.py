# 版权声明：2022年开源机器人基金会
#
# 根据Apache许可证2.0版（“许可证”）获得授权；
# 除非遵守许可证，否则您不得使用此文件。
# 您可以在以下地址获取许可证的副本：
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# 除非适用法律要求或书面同意，否则根据许可证分发的软件
# 将以“原样”基础分发，不附带任何明示或暗示的保证或条件。
# 请参阅许可证以了解管理权限和限制的具体语言。

import os  # 导入操作系统模块

# 从ament_index_python.packages导入获取包共享目录的函数
from ament_index_python.packages import get_package_share_directory

# 导入launch相关模块
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

# 导入launch_ros.actions中的Node类
from launch_ros.actions import Node

# 定义生成启动描述的函数
def generate_launch_description():
    # 配置启动的ROS节点

    # 设置项目路径
    pkg_project_bringup = get_package_share_directory('ros_gz_ugv_bringup')
    pkg_project_gazebo = get_package_share_directory('ros_gz_ugv_gazebo')
    pkg_project_description = get_package_share_directory('ros_gz_ugv_description')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # 从"description"包中加载SDF文件
    sdf_file  =  os.path.join(pkg_project_description, 'models', 'diff_drive', 'model.sdf')
    with open(sdf_file, 'r') as infp:
        robot_desc = infp.read()

    # 设置启动模拟器和Gazebo世界的配置
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': PathJoinSubstitution([
            pkg_project_gazebo,
            'worlds',
            'diff_drive.sdf'
        ])}.items(),
    )

    # 节点：接收机器人描述和关节角度作为输入，发布机器人链接的3D姿态
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[
            {'use_sim_time': True},
            {'robot_description': robot_desc},
        ]
    )

    # 节点：在RViz中可视化
    rviz = Node(
       package='rviz2',
       executable='rviz2',
       arguments=['-d', os.path.join(pkg_project_bringup, 'config', 'diff_drive.rviz')],
       condition=IfCondition(LaunchConfiguration('rviz'))
    )

    # 节点：桥接ROS话题和Gazebo消息以建立通信
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': os.path.join(pkg_project_bringup, 'config', 'ros_gz_ugv_bridge.yaml'),
            'qos_overrides./tf_static.publisher.durability': 'transient_local',
        }],
        output='screen'
    )

    # 返回启动描述，包含模拟器、RViz、桥接节点和机器人状态发布节点
    return LaunchDescription([
        gz_sim,
        DeclareLaunchArgument('rviz', default_value='true',
                              description='是否打开RViz。'),
        bridge,
        robot_state_publisher,
        rviz
    ])
