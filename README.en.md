# Ocean Blue Rubik's Cube Machine

For Theme 2 of the [China University Intelligent Robot Creative Contest 2024](https://www.robotcontest.cn/datacenter/news/detail?id=6292), which focuses on building a robot that can solve Rubik's Cube, our team aims to achieve faster solving speeds.

## Development Team

- University: Guangdong Ocean University
- College: College of Mechanical Engineering
- Team Name: [Blue Net Technology Innovation Team](https://gitee.com/blue-net-vision)
- Team Members:
  - Vision: [许凯杰](https://gitee.com/d-vision), [何云峰](https://gitee.com/iven_he)
  - Algorithm: [许凯杰](https://gitee.com/d-vision)
  - Electronics: [何云峰](https://gitee.com/iven_he)
  - Structure: 吉泧均, 何云峰

## Development Platform

NVIDIA jetson nano
ESP32-S3R8N8

## Development Environment

- Operating System: Raspbian
- Programming Language: Python

## References

1. [SVM Recognition Solution](https://blog.csdn.net/lemonbit/article/details/117004167)
2. [Rubik's Cube Solving Algorithm](https://github.com/hkociemba/RubiksCube-TwophaseSolver)
3. [Robotic Arm Planning Algorithm](https://gitee.com/harry-fan/rubiks-cube-robot/tree/master)

## Introduction

This Rubik's Cube machine adopts a dual-claw eight-shaped layout, 4 cameras, 2 stepper motors, an air slip ring, and a gripper cylinder. By inflating the air tank with an air compressor, removing the air compressor, placing the Rubik's Cube on the rack, pressing the start button, and closing the gripper, the machine begins solving the Rubik's Cube.

### Equipment List

- Raspberry Pi 4B
- 4 cameras
- [42 Stepper Motor-L40](https://item.taobao.com/item.htm?abbucket=5&id=682797640293&ns=1&spm=a21n57.1.0.0.6903523cZRZY1D&skuId=5057239338765) + [Closed-loop Controller Emm42 Industrial Version](https://item.taobao.com/item.htm?abbucket=5&id=673302946671&ns=1&spm=a21n57.1.0.0.6903523cZRZY1D&skuId=5032954871240) *2
- [MHL2-16D Gripper Cylinder](https://item.taobao.com/item.htm?id=537049565191&spm=a1z0d.6639537/tb.1997196601.34.257c7484ZwafTI&skuId=3206052770907) *2
- [Air Slip Ring 2-way Air Side Outlet M5 Thread](https://detail.tmall.com/item.htm?_u=d2qf50kdb8b2&id=555594152568&skuId=3431370232744) *2
- Several air pipe connectors
