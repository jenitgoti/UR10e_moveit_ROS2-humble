# UR10e_moveit_ROS2-humble
 A ROS 2 Humble package for controlling the UR10e robotic arm using MoveIt, including example nodes for motion planning and execution.

 ### Attribution

This project includes components from the [Universal Robots](https://github.com/UniversalRobots), [Universal Robots ROS2 Driver](https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver), [Universal_Robots_Client_Library](https://github.com/UniversalRobots/Universal_Robots_Client_Library.git), and [Universal_Robots_ROS2_Description](https://github.com/UniversalRobots/Universal_Robots_ROS2_Description.git) which is licensed under the Apache License 2.0 and BSD 3-Clause License.

# step-by-step detailed guide 

### Clone the main repos to your workspace (src)
```bash

git clone -b humble https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver.git
git clone -b humble https://github.com/UniversalRobots/Universal_Robots_ROS2_Description.git

```

### Clone the example_moveit_config if you're using MoveIt 2
```bash
git clone -b humble https://github.com/UniversalRobots/Universal_Robots_ROS2_MoveIt2_Config.git

```

### Install Dependencies
```bash
cd ~/ur_ws 
rosdep update
rosdep install --from-paths src --ignore-src -r -y

```
 ### Build the Workspace

 
```bash
colcon build --symlink-install
source install/setup.bash

```
## Control the Robot Using Python

- Create your Python node to publish to (/joint_trajectory_controller/joint_trajectory), (/scaled_joint_trajectory_controller/joint_trajectory) or use MoveIt 2.
- Save this as ur10e_commander.py, put it in a Python package, and make sure it's executable.
  
## Create and Use a Python ROS 2 Package

```bash
cd ~/ur_ws/src
# Creates a new Python package
ros2 pkg create --build-type ament_python ur10e_control --dependencies rclpy trajectory_msgs


```
### Place ur10e_commander.py inside the ur10e_control/ur10e_control/ folder:
 Make sure it's inside the package's main module directory, like this:
 ```bash
 ~/ur_ws/src/ur10e_control/
  ├── package.xml
  ├── setup.py
  └── ur10e_control/
     └── ur10e_commander.py
     └── hemisphere.py
     └── part_sphere.py
     └── plane.py
     


```
     
### Make the script executable:
 ```bash
chmod +x ~/ur_ws/src/ur10e_control/ur10e_control/ur10e_commander.py

```
### Rebuild your workspace:

 ```bash
cd ~/ur_ws
colcon build --symlink-install
source install/setup.bash

```

### Run your Python node

 ```bash
ros2 run ur10e_control ur10e_commander


```

## correct sequence to run your UR10e simulation with MoveIt and a Python control script
- After opening each terminal, you must source the environment


### Terminal 1 — Launch the robot simulation (with fake hardware)

```bash


ros2 launch ur_robot_driver ur_control.launch.py \
  ur_type:=ur10e \
  robot_ip:=127.0.0.1 \
  use_fake_hardware:=true \
  headless_mode:=false \
  launch_rviz:=true
```

#### Simulation vs Real Robot: When to Use `use_fake_hardware`

| Use Case             | `use_fake_hardware:=true` | Real Robot |
|----------------------|:-------------------------:|:----------:|
| Learning ROS 2       | ✅ Yes                     | ❌ No      |
| Writing/Test Scripts | ✅ Yes                     | ✅ Yes     |
| Safe Testing         | ✅ Yes                     | ❌ No      |
| Real Robot Motion    | ❌ No                      | ✅ Yes     |


### Terminal 2 — Launch MoveIt

```bash
ros2 launch ur_moveit_config ur_moveit.launch.py ur_type:=ur10e

```
 ### Terminal 3 — Run your custom Python node script
 
```bash
ros2 run ur10e_control ur10e_commander

```

## If you're Publishing to the Wrong Topic
   1. The Arm Doesn’t Move
   2. Feedback Loops Break
   3. Visualization Tools Show Nothing

### How to Check or Fix It
- Use rostopic list to see all active topics.
- Use rostopic echo /your_topic to verify that messages are being published.
- Use rosnode info <node_name> to see what topics a node publishes/subscribes to.
- Use rqt_graph to visually inspect connections.
