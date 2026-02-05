# 🤖 BumperBot — ROS 2 Reference Platform & Extensions

![OS](https://img.shields.io/badge/Ubuntu-22.04-orange)
![ROS_2](https://img.shields.io/badge/ROS_2-Humble-blue)

This repository is based on **BumperBot**, an open-source ROS 2 mobile robot originally developed by **Antonio Brandi**:
👉 https://github.com/AntoBrandi/Bumper-Bot

The original BumperBot is a low-cost, 3D-printed, self-driving robot designed as a learning platform and featured in the courses:

- *Self Driving and ROS 2 – Learn by Doing! Odometry & Control*
- *Self Driving and ROS 2 – Learn by Doing! Map & Localization*

This repository follows the **same core architecture and philosophy**, and is intended as a **personal extension workspace** built on top of the original project.

---

## 🎯 Purpose of This Repository
The goal of this repository is **not to reimplement BumperBot from scratch**, but to use the original project as a **stable reference platform** for:

- Adding small, well-scoped extensions
- Exploring configuration and parameter choices
- Testing navigation and simulation behavior
- Documenting observations and design decisions

All changes are kept **incremental and traceable**, with the intention of remaining close to the upstream implementation.

---

## 🚀 Demo: BumperBot in Simulation

The following demonstrations illustrate the main simulation modes supported by BumperBot, covering both mapping and localization workflows.

### 🗺️ Mapping Mode (SLAM)

![BumperBot SLAM Mapping Demo](docs/images/bumperbot_slam_mapping.gif)
*Figure: BumperBot performing online SLAM and building a 2D occupancy grid map in simulation.*

### 📍 Localization Mode (AMCL)

![BumperBot AMCL Localization Demo](docs/images/bumperbot_amcl_localization.gif)
*Figure: BumperBot localizing itself using AMCL on a prebuilt map, visualized in RViz.*