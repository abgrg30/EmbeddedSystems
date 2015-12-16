/*
This Code is for RADAR SYSTEM: ULTASONIC SENSOR API.
Course: CSE291E ( Robotics/Embedded Systems)
Assignment: 5
Last Modified: 05-Nov-2015
Team: CodeIT
Developers: Abhinav Garg; Abhijit Tripathi; Pulkit Bhatnagar
University of California, San Diego
*/

#include "ultra.h"
#include "mbed.h"

 
DigitalIn echo(p6);
DigitalOut  trigger(p25);
Serial term(USBTX, USBRX);
Timer pulse_width;

float cal_distance(int duration)
{
        float range;
        range = (float(duration)/58);
        return(range);
}
    

float ultra_start()
{
 int duration;
 float dist;
    while(1) {
        trigger = 0;
        wait_us(1);
        trigger = 1;
        wait_us(10);
        trigger = 0;
        while(!echo);
        pulse_width.start();
        while(echo);
        pulse_width.stop();
        duration=pulse_width.read_us();
 //       term.printf("\nTimer Reading cm:%d",duration );
        dist = cal_distance(duration);
        term.printf("\nObject Distance cm:%f",dist );
        pulse_width.reset();
        wait_us(10);
        return dist;
    }

}
