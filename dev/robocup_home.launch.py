import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import OpaqueFunction
import time

# 定义生成启动描述的函数
def generate_launch_description():
    # 获取wpr_simulation2包的launch目录路径
    launch_file_dir = os.path.join(get_package_share_directory('wpr_simulation2'), 'launch')
    # 获取gazebo_ros包的共享目录路径
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    # 设置使用仿真时间的配置项，默认为true
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # 设置仿真世界文件的路径
    world = os.path.join(
        get_package_share_directory('wpr_simulation2'),
        'worlds',
        'robocup_home.world'
    )

    # 包含gzserver的启动文件，并传递世界文件路径作为参数
    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world}.items()
    )

    # 包含gzclient的启动文件
    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )

    # 包含spawn_wpb_lidar的启动文件，并设置机器人的初始位置
    spawn_robot_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, 'spawn_wpb_lidar.launch.py')
        ),
        launch_arguments={
        'pose_x': '-6.0',
        'pose_y': '-0.5',
        'pose_theta': '0.0'
    }.items()
    )

    # 包含spawn_objects的启动文件，用于在仿真中生成物体
    spawn_objects = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, 'spawn_objects.launch.py')
        )
    )

    # 创建一个LaunchDescription对象
    ld = LaunchDescription()

    # 将启动命令添加到启动描述中
    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)
    ld.add_action(spawn_robot_cmd)
    ld.add_action(spawn_objects)
    
    # 返回启动描述
    return ld
