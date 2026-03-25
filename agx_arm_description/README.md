# agx_arm_description

AgileX 系列机械臂的 ROS 2 Description 功能包。

通过统一的 Xacro 入口文件 `urdf/agx_arm_description.urdf.xacro`，以参数化方式支持多种机械臂型号、末端执行器、相机支架和 RealSense D435 相机的灵活组合，在 RViz2 中可视化 URDF 模型。

---

## 目录

- [支持的机械臂型号](#支持的机械臂型号)
- [功能包结构](#功能包结构)
- [依赖](#依赖)
- [安装](#安装)
- [使用方法](#使用方法)
  - [Launch 参数说明](#launch-参数说明)
  - [常用启动命令](#常用启动命令)
  - [相机支架挂载逻辑](#相机支架挂载逻辑)
- [在其他 Launch 文件中引用](#在其他-launch-文件中引用)
- [直接调用 xacro 解析](#直接调用-xacro-解析)

---

## 支持的机械臂型号

| `arm_type` | 型号 | 可选末端执行器 |
|---|---|---|
| `piper` | Piper | `none` / `gripper` / `revo2_left` / `revo2_right` |
| `piper_h` | Piper H | `none` / `gripper` / `revo2_left` / `revo2_right` |
| `piper_l` | Piper L | `none` / `gripper` / `revo2_left` / `revo2_right` |
| `piper_x` | Piper X | `none` / `gripper` / `revo2_left` / `revo2_right` |
| `nero` | Nero | `none` / `gripper` / `revo2_left` / `revo2_right` |
| `revo2` | Revo2 灵巧手 | 通过 `revo2_side` 参数选择 `left` / `right` |

---

## 功能包结构

```
agx_arm_description/
├── agx_arm_urdf/                        # git submodule（来自 agilexrobotics/agx_arm_urdf）
│   ├── piper/
│   │   ├── meshes/dae/
│   │   └── urdf/
│   ├── piper_h/
│   ├── piper_l/
│   ├── piper_x/
│   ├── nero/
│   └── revo2/
├── meshes/
│   └── realsense_mid_stand.dae          # 相机支架 3D 模型
├── urdf/
│   └── agx_arm_description.urdf.xacro  # 统一入口 Xacro 文件
├── launch/
│   ├── display.launch.py               # 主 launch：带 RViz2 可视化
├── config/
│   └── arm_config.yaml
├── rviz/
│   └── default.rviz
├── CMakeLists.txt
└── package.xml
```

---

## 依赖

**ROS 2 包：**

```bash
sudo apt install \
  ros-$ROS_DISTRO-robot-state-publisher \
  ros-$ROS_DISTRO-joint-state-publisher \
  ros-$ROS_DISTRO-joint-state-publisher-gui \
  ros-$ROS_DISTRO-rviz2 \
  ros-$ROS_DISTRO-xacro
```

## 安装

### 1. 克隆并初始化子模块

```bash
cd ~/ros2_ws/src

# 克隆本功能包
git clone https://github.com/smalleha/agx_arm_sim.git

# 初始化 agx_arm_urdf 子模块
cd agx_arm_description
git submodule update --init --recursive
```

2. 安装依赖并编译

```bash
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build 
source install/setup.bash
```

---

## 使用方法

### Launch 参数说明

| 参数 | 默认值 | 可选值 | 说明 |
|---|---|---|---|
| `arm_type` | `piper` | `piper` `piper_h` `piper_l` `piper_x` `nero` `revo2` | 机械臂型号 |
| `end_effector` | `none` | `none` `gripper` `revo2_left` `revo2_right` | 末端执行器（`revo2` 型号无效） |
| `revo2_side` | `right` | `left` `right` | 仅当 `arm_type:=revo2` 时生效 |
| `with_camera_stand` | `false` | `true` `false` | 是否加载相机支架 |
| `with_camera` | `false` | `true` `false` | 是否加载 RealSense D435（需同时设 `with_camera_stand:=true`） |
| `use_gui` | `true` | `true` `false` | 是否启动关节滑条 GUI |
| `rviz_config` | 内置配置 | 任意 `.rviz` 路径 | 自定义 RViz2 配置文件 |

### 常用启动命令

```bash
# 默认（piper 基础型，无末端，无相机）
ros2 launch agx_arm_description display.launch.py

# 指定型号
ros2 launch agx_arm_description display.launch.py arm_type:=piper_h

# 带夹爪
ros2 launch agx_arm_description display.launch.py arm_type:=piper end_effector:=gripper

# 带右手灵巧手
ros2 launch agx_arm_description display.launch.py arm_type:=nero end_effector:=revo2_right

# revo2 左手
ros2 launch agx_arm_description display.launch.py arm_type:=revo2 revo2_side:=left

# 带相机支架（不含相机）
ros2 launch agx_arm_description display.launch.py \
  arm_type:=piper end_effector:=gripper \
  with_camera_stand:=true

# 带相机支架 + RealSense D435
ros2 launch agx_arm_description display.launch.py \
  arm_type:=piper end_effector:=gripper \
  with_camera_stand:=true with_camera:=true

# nero + 夹爪 + 相机（自动使用 nero 专属挂载偏移）
ros2 launch agx_arm_description display.launch.py \
  arm_type:=nero end_effector:=gripper \
  with_camera_stand:=true with_camera:=true
```

---

##  xacro 解析

无需 ROS 2 launch，可直接在命令行解析 xacro 文件进行调试：

```bash
# piper 基础型
xacro urdf/agx_arm_description.urdf.xacro arm_type:=piper

# nero + 夹爪 + 相机
xacro urdf/agx_arm_description.urdf.xacro \
  arm_type:=nero \
  end_effector:=gripper \
  with_camera_stand:=true \
  with_camera:=true

# 输出到文件
xacro urdf/agx_arm_description.urdf.xacro arm_type:=piper > piper.urdf
```

---

## License

MIT License
