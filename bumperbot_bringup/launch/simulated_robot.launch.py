import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    use_slam = LaunchConfiguration("use_slam")

    # Launch argument to decide whether to use SLAM
    use_slam_arg = DeclareLaunchArgument(
        "use_slam",
        default_value="false",
        description="Whether to run SLAM"
    )

    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("bumperbot_description"),
                "launch",
                "gazebo.launch.py"
            )
        )
    )

    # Controller launch
    controller = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("bumperbot_controller"),
                "launch",
                "controller.launch.py"
            )
        ),
        launch_arguments={"use_simple_controller": "False"}.items()
    )

    # Joystick launch
    joystick = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("bumperbot_controller"),
                "launch",
                "joystick_teleop.launch.py"
            )
        ),
        launch_arguments={"use_sim_time": "True"}.items()
    )

    # Localization launch (only if not using SLAM)
    localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("bumperbot_localization"),
                "launch",
                "global_localization.launch.py"
            )
        ),
        condition=UnlessCondition(use_slam)
    )

    # SLAM launch (only if using SLAM)
    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("bumperbot_mapping"),
                "launch",
                "slam.launch.py"
            )
        ),
        condition=IfCondition(use_slam)
    )

    # RViz node for normal navigation (no SLAM)
    rviz_nav = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", os.path.join(
            get_package_share_directory("nav2_bringup"),
            "rviz",
            "nav2_default_view.rviz"
        )],
        output="screen",
        parameters=[{"use_sim_time": True}],
        condition=UnlessCondition(use_slam)
    )

    # RViz node for SLAM
    rviz_slam = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", os.path.join(
            get_package_share_directory("bumperbot_mapping"),
            "rviz",
            "slam.rviz"
        )],
        output="screen",
        parameters=[{"use_sim_time": True}],
        condition=IfCondition(use_slam)
    )

    return LaunchDescription([
        use_slam_arg,
        gazebo,
        controller,
        joystick,
        localization,
        slam,
        rviz_nav,
        rviz_slam,
    ])
