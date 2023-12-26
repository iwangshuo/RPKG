# RPKG(ROS Package Knowledge Graph)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


implementation of the paper [Recommending ROS Packages for Robot Task by Knowledge Graph](https://arxiv.org/abs/2312.14781) presented in arxiv. 





## Installation


- Create component models:
  - (Prerequisite) [Add communication objects](docu/NewCommunicationObjects.md)
  - [Create manually a new ROS component description](docu/RosModelDescription.md)
  - [Generation of code from models](https://github.com/CoreSenseEU/rossdl#usage)
  - [Create a ROS model from a deployed robot using our introspection at runtime tool](docu/IntrospectionNode.md)
  - [Create a ROS model from your source code(static code analyzer)](docu/NewRosModel.md))

- Combine components to form a ROS System
  - [Create manually a new RosSystem description](docu/RosSystemModelDescription.md)
  
- Examples:
  - [Simple publisher-subscriber](docu/Example_PubSub.md)
  - [Turtlesim](docu/Example_Turtlesim.md)

- [Update Release versions (only for administrators)](docu/Release.md)

Our codes have been tested in Ubuntu 16.04 with Python 2.7. 
1. Install [ROS kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu).
2. Create and build a catkin workspace and download the codes into src/:
```
mkdir -p ~/sarl_ws/src
cd ~/sarl_ws/
catkin_make
source devel/setup.bash
cd src
git clone https://github.com/LeeKeyu/sarl_star.git
```
3. Install other dependencies:

```
sudo apt-get install libbullet-dev
sudo apt-get install libsdl-image1.2-dev
sudo apt-get install libsdl-dev
sudo apt-get install ros-kinetic-bfl
sudo apt-get install ros-kinetic-tf2-sensor-msgs
sudo apt-get install ros-kinetic-turtlebot ros-kinetic-turtlebot-apps ros-kinetic-turtlebot-interactions ros-kinetic-turtlebot-simulator ros-kinetic-kobuki-ftdi ros-kinetic-ar-track-alvar-msgs
pip install empy
pip install configparser
```
4. Install [Python-RVO2](https://github.com/sybrenstuvel/Python-RVO2):

```
cd sarl_star/Python-RVO2/
pip install -r requirements.txt
python setup.py build
python setup.py install
```
5. Install CrowdNav (Note that the CrowdNav in this repository are modified from [the original SARL implementation](https://github.com/vita-epfl/CrowdNav)):

```
cd sarl_star/sarl_star_ros/CrowdNav/
pip install -e .
```

6. Build the catkin workspace:

```
cd ~/sarl_ws/
catkin_make
source devel/setup.bash
```



## Citation
If you find our work useful in your research, please consider citing our paper:
```
@misc{wang2023ros,
      title={ROS package search for robot software development: a knowledge graph-based approach}, 
      author={Shuo Wang and Xinjun Mao and Shuo Yang and Menghan Wu and Zhang Zhang},
      year={2023},
      eprint={2312.14781},
      archivePrefix={arXiv},
      primaryClass={cs.SE}
}
```
## Questions

If you have any questions, please contact "iwangshuo@qq.com".


