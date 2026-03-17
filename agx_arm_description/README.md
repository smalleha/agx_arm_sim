# agx_arm_description

AgileX 系列机械臂的 ROS2 `description` 功能包，支持通过参数选择机械臂型号与末端执行器，在 RViz2 中可视化 URDF/Xacro 模型。

## 支持的机械臂型号

| `arm_type` 参数 | 型号名称 | 末端执行器选项 |
|---|---|---|
| `piper` | Piper | none / gripper / revo2_left / revo2_right |
| `piper_h` | Piper H | none / gripper / revo2_left / revo2_right |
| `piper_l` | Piper L | none / gripper / revo2_left / revo2_right |
| `piper_x` | Piper X | none / gripper / revo2_left / revo2_right |
| `nero` | Nero | none / gripper / revo2_left / revo2_right |
| `revo2` | Revo2 灵巧手 | left / right（通过 `revo2_side` 参数区分） |

---

## 目录结构

```
agx_arm_description/
├── agx_arm_urdf/           # git submodule（来自 agilexrobotics/agx_arm_urdf）
│   ├── piper/
│   │   ├── meshes/dae/
│   │   └── urdf/
│   ├── piper_h/  ...
│   └── ...
├── launch/
│   ├── display.launch.py   # 主 launch：带 RViz2 可视化
│   └── load_urdf.launch.py # 仅加载 robot_description，供其他 launch include
├── config/
│   └── arm_config.yaml     # 参数默认值与型号信息
├── rviz/
│   └── default.rviz        # 内置 RViz2 配置
├── scripts/
│   └── get_urdf_path.py    # CLI 工具：查询 URDF 路径
├── CMakeLists.txt
└── package.xml
```

---

## 安装与编译

### 1. 克隆仓库（含子模块）

```bash
cd ~/ros2_ws/src

# 克隆本功能包
git clone <your_repo_url> agx_arm_description

# 初始化 agx_arm_urdf 子模块
cd agx_arm_description
git submodule add https://github.com/agilexrobotics/agx_arm_urdf.git agx_arm_urdf
git submodule update --init --recursive
```

> 如果已有 `agx_arm_urdf` 目录（已手动克隆），也可直接放入功能包根目录。

### 2. 安装依赖

```bash
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
```

### 3. 编译

```bash
cd ~/ros2_ws
colcon build --packages-select agx_arm_description
source install/setup.bash
```

---

## 使用方法

### 查看机械臂模型（带 RViz2）

```bash
# 基础 piper（无末端）
ros2 launch agx_arm_description display.launch.py arm_type:=piper

# piper 带夹爪
ros2 launch agx_arm_description display.launch.py arm_type:=piper end_effector:=gripper

# piper 带右手灵巧手
ros2 launch agx_arm_description display.launch.py arm_type:=piper end_effector:=revo2_right

# nero 带夹爪，不显示关节滑条
ros2 launch agx_arm_description display.launch.py arm_type:=nero end_effector:=gripper use_gui:=false

# revo2 左手
ros2 launch agx_arm_description display.launch.py arm_type:=revo2 revo2_side:=left

# 使用自定义 RViz 配置
ros2 launch agx_arm_description display.launch.py arm_type:=piper_h \
    rviz_config:=/path/to/my.rviz
```

### launch 参数说明

| 参数 | 默认值 | 说明 |
|---|---|---|
| `arm_type` | `piper` | 机械臂型号 |
| `end_effector` | `none` | 末端执行器（`none`/`gripper`/`revo2_left`/`revo2_right`） |
| `revo2_side` | `right` | 仅当 `arm_type=revo2` 时生效（`left`/`right`） |
| `use_gui` | `true` | 是否启动 `joint_state_publisher_gui` 滑条 |
| `rviz_config` | 内置配置 | 自定义 RViz2 `.rviz` 配置文件路径 |

### 仅加载 robot_description（被其他 launch 引用）

```python
# 在其他 launch.py 中 include
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

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
```

### CLI 工具：查询 URDF 路径

```bash
# 查看 nero 带夹爪的文件路径
ros2 run agx_arm_description get_urdf_path.py --arm_type nero --end_effector gripper

# 打印解析后的 URDF XML
ros2 run agx_arm_description get_urdf_path.py --arm_type piper --print_xml

# 列出所有支持的型号
ros2 run agx_arm_description get_urdf_path.py --list
```

---

## 依赖

- `robot_state_publisher`
- `joint_state_publisher`
- `joint_state_publisher_gui`
- `rviz2`
- `xacro`

---

## License

MIT License — 与上游 [agx_arm_urdf](https://github.com/agilexrobotics/agx_arm_urdf) 保持一致。
