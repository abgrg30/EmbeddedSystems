# Embedded Systems
CSE291 - University of California, San Diego

board used - MBED 1768, Beaglebone

* assignment1 - rotated stepper motor clockwise/anticlockwise using half step PWM
* assignment2 - used ultrasonic to detect objects and measure distance.
* assignment3 - used 3 axis accelerometer to get x,y,z surface inclination and magnetometer to get N,S,E,W direction.
* assignment4 - used oled to display characters, words & paragraphs. Scrolled if reached end of screen.
* assignment5 - built a radar system. Used FCFS scheduling.
* assignment6(iRadar) - used socket to establish wifi connection between laptop(client) and beaglebone(server). Used UART communication to send commands to radar system from beaglebone. 
* assignment7 - used socket to establish wifi connection between laptop(client), iRobot and beaglebone(server). Used UART communication to send commands to radar system & iRobot from beaglebone. 
* final project(iRover) - Interfaced iRobot Create(slave) and ARM Mbed LPC 1768 microcontroller(slave) with Beaglebone(server) to create iRover. Mbed controls the movement of motor that has a camera fixed over it. Camera provides the real time buffered Video stream for obstacle detection and object recognition. OpenCV and Gstreamer give us 30fps buffered video. Beaglebone sends commands to iRobot and Mbed over UART1 and UART2. 2 Laptop clients are connected to beaglebone through socket communication over WIFI.1 Laptop manages video stream and other controls iRover's movement through GUI. GUI also displays the obstacle distance and direction reading sent by Mbed. Overall, we have a iRover controlled over a WIFI network. Youtube Link: https://youtu.be/LQLI4sQDyJw
