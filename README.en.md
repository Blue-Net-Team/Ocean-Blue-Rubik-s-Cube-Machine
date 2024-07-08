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

- Operating System: Ubuntu
- Programming Language: Python

## References

1. [SVM Recognition Solution](https://blog.csdn.net/lemonbit/article/details/117004167)
2. [Rubik's Cube Solving Algorithm](https://github.com/hkociemba/RubiksCube-TwophaseSolver)
3. [Robotic Arm Planning Algorithm](https://gitee.com/harry-fan/rubiks-cube-robot/tree/master)

## Introduction

This Rubik's Cube machine adopts a dual-claw eight-shaped layout, 4 cameras, 2 stepper motors, an air slip ring, and a gripper cylinder. By inflating the air tank with an air compressor, removing the air compressor, placing the Rubik's Cube on the rack, pressing the start button, and closing the gripper, the machine begins solving the Rubik's Cube.

### Equipment List

- NVIDIA Jetson Nano
- [ESP32-S3R8N8](https://item.szlcsc.com/22034693.html?fromZone=s)
- 4 cameras
- [42 stepper motor-L40](https://item.taobao.com/item.htm?abbucket=5&id=682797640293&ns=1&spm=a21n57.1.0.0.6903523cZRZY1D&skuId=5057239338765) + [Closed-loop controller Emm42 Industrial Edition](https://item.taobao.com/item.htm?abbucket=5&id=673302946671&ns=1&spm=a21n57.1.0.0.6903523cZRZY1D&skuId=5032954871240) *2
- [MHL2-16D gripper cylinder](https://item.taobao.com/item.htm?id=537049565191&spm=a1z0d.6639537/tb.1997196601.34.257c7484ZwafTI&skuId=3206052770907) *2
- [Pneumatic slip ring, 2-way air, side air outlet M5 thread](https://detail.tmall.com/item.htm?_u=d2qf50kdb8b2&id=555594152568&skuId=3431370232744)*2
- [Two-way five-way solenoid valve](https://item.taobao.com/item.htm?spm=a1z09.2.0.0.2e4a2e8dQz8SzG&id=631999517519&_u=42qf50kd72cc)*2
- [200M 2F busbar](https://item.taobao.com/item.htm?spm=a1z09.2.0.0.2e4a2e8dQz8SzG&id=682537654244&_u=42qf50kd02df)
- [200M plug 3 and muffler 2](https://item.taobao.com/item.htm?spm=a1z09.2.0.0.2e4a2e8dQz8SzG&id=682537654244&_u=42qf50kd02df)
- [12V lithium battery](https://item.taobao.com/item.htm?spm=a1z09.2.0.0.2e4a2e8dQz8SzG&id=632184698346&_u=42qf50kd578b)
- Several 6mm pneumatic tube connectors

## Introduction

The Jetson Nano, as the upper computer, will use SVM to recognize the colors of the Rubik's Cube's blocks, determine the current state of the Rubik's Cube, and then use the Rubik's Cube solving algorithm to obtain the restoration steps. However, the restoration steps cannot be directly transmitted to the lower computer to control the two robotic arms. The restoration steps need to undergo shortest path calculation to obtain the shortest mechanical steps. These mechanical steps will be sent to the ESP32 of the lower computer, which will control the stepper motors and cylinders to complete the restoration of the Rubik's Cube.
This machine frame uses 30 aluminum profiles and a full metal frame. **Attention should be paid to prevent short circuits in the circuit board**.

### Instructions

The main difficulty of this project lies in the visual aspect. The following will mainly introduce the connection, program startup, and debugging of Jetson Nano.

#### Connection

First, power on the Jetson Nano and use the remote connection feature of VS Code to connect to the Jetson Nano. For the first use of Jetson Nano, an external display is required to connect to WiFi and perform operations such as confirming the IP address. After that, the connection method is the same as Raspberry Pi.

#### Rubik's Cube Placement

In this visual recognition solution, there are specific requirements for the placement of the Rubik's Cube because the recognized colors need to be mapped to each face of the Rubik's Cube in order to solve it. Therefore, the color of the center block of the Rubik's Cube corresponds to that face. For example, Blue->U is already bound in the dictionary.

The sample images of the cameras are located in the path **./Vision/pic**, and the corresponding recognition files of the cameras are located in **./Vision/cam**.
In the images, the left side of the upper camera is the side where the left robotic arm is located. Based on this:

- The **blue face** is above the right robotic arm.
- The **orange face** is in front of the machine (in the position where the right camera is facing), which corresponds to the position of the person's left hand when facing the machine with the left hand corresponding to the left robotic arm.
- And so on.

#### ROI Area Debugging

This project uses VS Code for debugging and does not rely on an external display. Therefore, OpenCV functions related to Qt windows cannot be used in the code. To solve the need for fast debugging, we use remote image transmission for debugging the ROI area.

- We have written the file *ROIlocater.py* in the *Vision* folder for quickly adjusting the ROI area of each color block of the camera.
- We have also written the remote image transmission file *Captest.py* that runs on Jetson Nano in the *Vision* folder. The file needs to be run with command-line arguments. When using the *Python Debugger* for debugging, select the **Python file with arguments** option and negotiate the corresponding parameter name and parameter in the interactive box.
  `--cap 1` This parameter means using the camera with ID `1` for remote image transmission.
  Alternatively, you can directly run the Python file using the Python command in the command line.

  ```bash
  python Captest.py --cap 1
  ```

  Before starting the *ROIlocater.py* file, you need to modify the `serface_name` parameter on line 222 to the corresponding position of the camera that needs to be modified, for example:
  
  - Upper camera: U
  - Lower camera: D
  - Left camera: L
  - Right camera: R

  **Start the remote image transmission server program on Jetson Nano first, and then start the *ROIlocater.py* file on the other end.**

  After both files are started, a slider window will pop up for adjusting the position, size, and ID of the sliders. Before adjustment, you need to check the order of the IDs on the example image. The order of the ROIs must not be wrong. The ID of the ROI corresponds to the value of the slider *ID*, and **ID 0 is an invalid ROI**.

  The example images are located in the folder **./Vision/pic**.

  For each example image, click on the corresponding recognition area according to the order of the ROIs. This operation should be done when the stepper motor is powered on, so that the angle of the motor remains basically unchanged. After setting the ROIs by clicking, you can directly end the program. The slider with the *OK* label serves as the save button. If you use the click mode, you can ignore this slider. However, if you use the slider to adjust the ROI position, you need to slide the *OK* label to 1 to save and then back to 0 to reset.

  After setting the ROIs, copy the corresponding JSON file from the working directory to the working directory of Jetson Nano, replacing the original JSON file to complete the ROI settings.

#### Recognition Debugging

In this project, most of the errors after adjusting the ROI area are caused by color recognition errors. Running the *main.py* file allows you to directly view the recognition results of each camera. The recognized images will be saved in the **./Vision/pic** folder with the camera position as the name. By comparing the images and the results, you can identify the cameras with recognition errors. Modify the brightness in the corresponding camera file (located in the **./Vision/cam** folder) to solve most of the recognition issues.

```python
# Auto exposure
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)

cap.set(10,0) # Brightness 0
```

After testing, the automatic exposure parameter '3' has the best effect

## Development Instructions

- The **Vision** folder is used to store the code for visual recognition and Rubik's cube solving.
- The **Control** folder is used to store the electrical control code. It is a microPython project folder. After installing the *RT-Thread MicroPython* plugin in *vscode*, you can create a microPython project in this folder, which can be connected to ESP32 for code writing. However, please make sure that the firmware of esp32 has been burned.
  - Download the firmware of esp32 from the[microPython offical website](https://micropython.org/)
  - Use esptool or [Thonny](https://micropython.org/) to burn the firmware
- The **Structure** folder is used to store related models of mechanical structure, which can be opened with *SolidWorks2023*.
- The **PCB** folder is used to store the circuit board design files, which can be opened with *JLCPCB EDA Professional Edition*.

# Final Note

The Raspberry Pi branch in this repository is the original version that was developed using only Raspberry Pi. It is now deprecated and no longer maintained. If you have related needs or ideas, you can join us.