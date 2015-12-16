# Embedded Robotic Systems
CSE291 - University of California, San Diego

## Team Name ##
CodeIT

## Team Members ##
1. Abhinav Garg
2. Abhijit Tripathy
3. Pulkit Bhatnagar

hardware - MBED 1768, Beaglebone, iRobot Create
skills - C/C++, python, Java, I2C

* assignment1 - rotated stepper motor clockwise/anticlockwise using half step PWM
## [Video](https://youtu.be/B-4KtUcY1ow)
* assignment2 - used ultrasonic to detect objects and measure distance.
## [Video](https://youtu.be/vaDhymuwKxo)
* assignment3 - used 3 axis accelerometer to get x,y,z surface inclination and magnetometer to get N,S,E,W direction.
## [Video](https://youtu.be/gX-dk2MojDM)
* assignment4 - used oled to display characters, words & paragraphs. Scrolled if reached end of screen.
## [Video](https://youtu.be/D8ZZfRR-DTo)
* assignment5 - built a radar system. Used FCFS scheduling.
## [Video](https://www.youtube.com/watch?v=We3mmS9L6GY)
* assignment6(iRadar) - used socket to establish wifi connection between laptop(client) and beaglebone(server). Used UART communication to send commands to radar system from beaglebone.  Youtube Link: https://youtu.be/LQLI4sQDyJw
## [Video](https://www.youtube.com/watch?v=TVXw8hi9qRY)
* assignment7 - used socket to establish wifi connection between laptop(client), iRobot and beaglebone(server). Used UART communication to send commands to radar system & iRobot from beaglebone.  
## [Video](https://youtu.be/LQLI4sQDyJw)

* Final project(iRover) - 
Interfaced iRobot Create(slave) and ARM Mbed LPC 1768 microcontroller(slave) with Beaglebone(server) to create iRover. Mbed controls the movement of motor that has a camera fixed over it. Camera provides the real time buffered Video stream for obstacle detection and object recognition. OpenCV and Gstreamer give us 30fps buffered video. Beaglebone sends commands to iRobot and Mbed over UART1 and UART2. 2 Laptop clients are connected to beaglebone through socket communication over WIFI.1 Laptop manages video stream and other controls iRover's movement through GUI. GUI also displays the obstacle distance and direction reading sent by Mbed. Overall, we have a iRover controlled over a WIFI network.
## [Video](https://youtu.be/LQLI4sQDyJw)
