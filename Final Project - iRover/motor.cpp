/*
This Code is for RADAR SYSTEM: MOTOR API.
Course: CSE291E ( Robotics/Embedded Systems)
Assignment: 5
Last Modified: 05-Nov-2015
Team: CodeIT
Developers: Abhinav Garg; Abhijit Tripathi; Pulkit Bhatnagar
University of California, San Diego
*/
#include "motor.h"
#include "mbed.h"

#define MIN 0.001
#define MAX 0.01
#define MID 0.005

#define ON 1
#define OFF 0

float delay = 0.01;


DigitalOut motorpin1(p21);
DigitalOut motorpin2(p22);
DigitalOut motorpin3(p23);
DigitalOut motorpin4(p24);

void motor_clockwise()
{
    motorpin1 = ON;
    wait(delay);
    motorpin4 = OFF;
    wait(delay);
    motorpin2 = ON;
    wait(delay);
    motorpin1 = OFF;
    wait(delay);        
    motorpin3 = ON;
    wait(delay);
    motorpin2 = OFF;
    wait(delay);
    motorpin4 = ON;
    wait(delay);
    motorpin3 = OFF;
    wait(delay);
}

void motor_anticlockwise()
{
    motorpin1 = ON;
    wait(delay);
    motorpin2 = OFF;
    wait(delay);
    motorpin4 = ON;
    wait(delay);
    motorpin1 = OFF;
    wait(delay);        
    motorpin3 = ON;
    wait(delay);
    motorpin4 = OFF;
    wait(delay);
    motorpin2 = ON;
    wait(delay);
    motorpin3 = OFF;
    wait(delay);
}
