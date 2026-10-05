import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'my_ugv_description'

    # URDF file ka path
    urdf_file = os.path.join(get_package_share_directory(pkg_name), 'urdf', 'my_robot.urdf')
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    # 1. Gazebo Launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    )

    # 2. Robot State Publisher Node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    # 3. Spawn Entity Node
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'ASHWINI', '-z', '0.2'],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        node_robot_state_publisher,
        spawn_entity,
    ])
