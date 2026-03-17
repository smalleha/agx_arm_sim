"""
agx_arm_description — load_urdf.launch.py
==========================================
仅加载 robot_description，不启动 RViz2。
适合被其他 launch 文件 IncludeLaunchDescription 复用。

include 示例:
  IncludeLaunchDescription(
      PythonLaunchDescriptionSource([
          get_package_share_directory('agx_arm_description'),
          '/launch/load_urdf.launch.py'
      ]),
      launch_arguments={
          'arm_type': 'piper',
          'end_effector': 'gripper',
      }.items(),
  )
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro


def launch_setup(context, *args, **kwargs):
    arm_type     = LaunchConfiguration("arm_type").perform(context)
    end_effector = LaunchConfiguration("end_effector").perform(context)
    revo2_side   = LaunchConfiguration("revo2_side").perform(context)

    pkg_share  = get_package_share_directory("agx_arm_description")
    xacro_file = os.path.join(pkg_share, "urdf", "agx_arm_description.urdf.xacro")

    if not os.path.exists(xacro_file):
        raise FileNotFoundError(
            f"[agx_arm_description] 找不到入口 xacro 文件:\n  {xacro_file}"
        )

    robot_description_content = xacro.process_file(
        xacro_file,
        mappings={
            "arm_type":     arm_type,
            "end_effector": end_effector,
            "revo2_side":   revo2_side,
        },
    ).toxml()

    ef_label = revo2_side if arm_type == "revo2" else end_effector

    return [
        LogInfo(msg=f"[agx_arm_description] arm_type={arm_type}, end_effector={ef_label}"),
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            output="screen",
            parameters=[{"robot_description": robot_description_content}],
        ),
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            "arm_type", default_value="piper",
            choices=["piper", "piper_h", "piper_l", "piper_x", "nero", "revo2"],
            description="机械臂型号",
        ),
        DeclareLaunchArgument(
            "end_effector", default_value="none",
            choices=["none", "gripper", "revo2_left", "revo2_right"],
            description="末端执行器",
        ),
        DeclareLaunchArgument(
            "revo2_side", default_value="right",
            choices=["left", "right"],
            description="revo2 左/右手",
        ),
        OpaqueFunction(function=launch_setup),
    ])
