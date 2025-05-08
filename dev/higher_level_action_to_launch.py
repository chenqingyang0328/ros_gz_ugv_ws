# Here’s another example using a higher level action from Python to launch gzserver:
# 这是一个使用 Python 中更高层次动作的另一个示例来启动 gzserver ：
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ros_gz_sim.actions import GzServer

# 定义生成启动描述的函数
def generate_launch_description():

    # 声明一个启动参数，用于指定SDF世界文件的路径，默认值为空
    declare_world_sdf_file_cmd = DeclareLaunchArgument(
        'world_sdf_file', default_value='',
        description='Path to the SDF world file')

    # 创建一个LaunchDescription对象，并添加GzServer动作
    # GzServer动作使用前面声明的world_sdf_file参数作为其世界文件路径
    ld = LaunchDescription([
        GzServer(
            world_sdf_file=LaunchConfiguration('world_sdf_file')
        ),
    ])

    # 将声明启动参数的动作添加到启动描述中
    ld.add_action(declare_world_sdf_file_cmd)

    # 返回启动描述
    return ld
