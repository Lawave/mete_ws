from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    battery_node = Node(
        package='battery_odev',
        executable='battery_node',
        output='screen',
    )

    monitor_node = Node(
        package='battery_odev',
        executable='monitor_node',
        output='screen',
    )

    return LaunchDescription([
        battery_node,
        monitor_node,
    ])