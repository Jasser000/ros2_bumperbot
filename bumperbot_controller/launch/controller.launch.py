from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, OpaqueFunction, GroupAction, RegisterEventHandler
from launch.substitutions import LaunchConfiguration
from launch.conditions import UnlessCondition, IfCondition
from launch.event_handlers import OnProcessExit

def noisy_controller(context, *args, **kwargs):
    wheel_radius = float(LaunchConfiguration("wheel_radius").perform(context))
    wheel_separation = float(LaunchConfiguration("wheel_separation").perform(context))
    wheel_radius_error = float(LaunchConfiguration("wheel_radius_error").perform(context))
    wheel_separation_error = float(LaunchConfiguration("wheel_separation_error").perform(context))

    noisy_controller_cpp = Node(
        package="bumperbot_controller",
        executable="noisy_controller",
        parameters=[
            {"wheel_radius" :wheel_radius + wheel_radius_error,
             "wheel_separation": wheel_separation + wheel_radius_error}
        ]
    )
    return [noisy_controller_cpp]

def generate_launch_description():

    wheel_radius_arg = DeclareLaunchArgument(
        "wheel_radius",
        default_value="0.033" 
    )

    wheel_separation_arg = DeclareLaunchArgument(
        "wheel_separation",
        default_value="0.17"
    )

    use_simple_controller_arg = DeclareLaunchArgument(
        "use_simple_controller",
        default_value="True"
    )

    wheel_radius_error_arg = DeclareLaunchArgument(
        "wheel_radius_error",
        default_value="0.005"
    )

    wheel_separation_error_arg = DeclareLaunchArgument(
        "wheel_separation_error",
        default_value="0.02"
    )

    wheel_radius = LaunchConfiguration("wheel_radius")
    wheel_separation = LaunchConfiguration("wheel_separation")
    use_simple_controller = LaunchConfiguration("use_simple_controller")

    # Node to spawn joint_state_broadcaster
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager"
        ]
    )

    # Node to spawn wheel controller
    wheel_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "bumperbot_controller",
            "--controller-manager",
            "/controller_manager"
        ],
        condition=UnlessCondition(use_simple_controller)
    )

    # Simple controller setup
    simple_controller = GroupAction(
        condition=IfCondition(use_simple_controller),
        actions=[
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=[
                    "simple_velocity_controller",
                    "--controller-manager",
                    "/controller_manager"
                ]
            ),
            Node(
                package="bumperbot_controller",
                executable="simple_controller",
                parameters=[{"wheel_radius": wheel_radius,
                             "wheel_separation": wheel_separation}]
            )
        ]
    )

    # Register event handlers to launch controllers sequentially after dependencies
    wheel_controller_event_handler = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_spawner, on_exit=[wheel_controller_spawner]
        )
    )

    simple_controller_event_handler = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_spawner, on_exit=[simple_controller]
        )
    )

    # Launch the noisy controller using OpaqueFunction
    noisy_controller_launch = OpaqueFunction(function=noisy_controller)

    return LaunchDescription([
        wheel_radius_arg,
        wheel_separation_arg,
        use_simple_controller_arg,
        wheel_radius_error_arg,
        wheel_separation_error_arg,
        joint_state_broadcaster_spawner,
        wheel_controller_event_handler,
        simple_controller_event_handler,
        noisy_controller_launch
    ])
