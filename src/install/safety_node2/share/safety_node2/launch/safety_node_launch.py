from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    # Path to the simulator launch file
    gym_launch = os.path.join(
        get_package_share_directory('f1tenth_gym_ros'),
        'launch',
        'gym_bridge_launch.py'
    )

    return LaunchDescription([

        # Launch simulator
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gym_launch)
        ),

        # Launch safety node
        Node(
            package='safety_node2',
            executable='safety_node',
            name='safety_node',
            output='screen',

            # Remapping topics
            remappings=[
                ('/scan', '/scan'),
                ('/odom', '/odom'),
                ('/drive_in', '/drive'),
                ('/drive_out', '/drive')
            ]
        )
    ])