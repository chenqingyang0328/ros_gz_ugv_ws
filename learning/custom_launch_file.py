#Python launch files provide more low-level customization and logic compared to XML launch files. For example, you can set environment variables and include Python specific functions and logic. In the following example, the user can replace the example package, world, and bridged topic with their own. This is intended as a scaffolding more than something that can be run on its own.
#Python 启动文件相较于 XML 启动文件提供了更多底层定制和逻辑。例如，您可以设置环境变量并包含 Python 特定的函数和逻辑。在以下示例中，用户可以将示例包、world 和桥接主题替换为自己的。这主要是作为一个脚手架，而不是可以独立运行的东西。

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import SetEnvironmentVariable, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

# 定义生成启动描述的函数
def generate_launch_description():
    # 获取ros_gz_sim包的共享目录路径
    ros_gz_sim_pkg_path = get_package_share_directory('ros_gz_sim')
    # 查找example_package包的共享目录路径，替换为你的包名
    example_pkg_path = FindPackageShare('example_package')
    # 构建gz_sim启动文件的路径
    gz_launch_path = PathJoinSubstitution([pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py'])

    # 返回一个LaunchDescription对象，包含了一系列启动动作
    return LaunchDescription([
        # 设置环境变量GZ_SIM_RESOURCE_PATH，指向example_package包中的models目录
        SetEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            PathJoinSubstitution([example_pkg_path, 'models'])
        ),
        # 设置环境变量GZ_SIM_PLUGIN_PATH，指向example_package包中的plugins目录
        SetEnvironmentVariable(
            'GZ_SIM_PLUGIN_PATH',
            PathJoinSubstitution([example_pkg_path, 'plugins'])
        ),
        # 包含另一个Python启动文件，并传递启动参数
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gz_launch_path),
            launch_arguments={
                # 指定Gazebo的启动参数，包括世界文件路径，替换为你的世界文件
                'gz_args': [PathJoinSubstitution([example_pkg_path, 'worlds/example_world.sdf'])],
                # 指定退出时是否关闭仿真
                'on_exit_shutdown': 'True'
            }.items(),
        ),

        # 创建一个节点，用于桥接和重映射Gazebo话题到ROS 2，替换为你的话题
        Node(
            package='ros_gz_bridge',  # 指定节点所在的包
            executable='parameter_bridge',  # 指定可执行文件
            arguments=['/example_imu_topic@sensor_msgs/msg/Imu@gz.msgs.IMU',],  # 指定桥接的话题和消息类型
            remappings=[('/example_imu_topic', '/remapped_imu_topic'),],  # 指定话题重映射
            output='screen'  # 指定节点输出到屏幕
        ),
    ])
