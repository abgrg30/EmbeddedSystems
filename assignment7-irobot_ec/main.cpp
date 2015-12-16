/*
This Code is for RADAR SYSTEM integration using FCFS on mbed 1768 which detects an object and displays on OLED.
Course: CSE291E ( Robotics/Embedded Systems)
Assignment: 5
Last Modified: 21-Nov-2015
Team: CodeIT
Developers: Abhinav Garg; Abhijit Tripathi; Pulkit Bhatnagar
University of California, San Diego
*/

#include "mbed.h"
#include "motor.h"
#include "ultra.h"
#include "magnetometer.h"
#include "radar.h"
#include "queue.h"

#define motor 0
#define ultra 1
#define magneto 3
#define lcd 2

Serial uart(p13, p14);          //(tx,rx)


void schedule_event();

Ticker random_event;            //Ticker to add events to queue
event e;        //Create an event for pushing tasks in queue.
    
int main()
{
uart.baud(57600);
    e.pr = low;     //Default priority for FCFS

random_event.attach(schedule_event, 0.4);

//Peripheral Initialization    
   motor_init(0.02);
   ultra_init();
   //mag_init(0.01);
   //radar_init();
    
//Push first event Motor in queue
   e.type = motor;
   queue_push(e);
    
//Object distance and Heading
    float dis = 0.0;
    //int angle = 13; //256;
    int angle=13;

//Push events in queue and service FIFO
    while(1)
    {        
        e = queue_front();
        
        switch(e.type)
        {
            case motor:
            {
                //printf("\nMotor....");
                angle=motor_rotate();              

            }
            break;
            
            case ultra:
            {
                //printf("\nUltra....");
                dis=ultra_start();
                wait_us(1);
                if (dis <= 15) {
                    uart.putc('1');
                    }
                else {
                    uart.putc('0');
                }
                printf("\nDistance=%f",dis);
            }
            break;
            
            case magneto:
            {
               //printf("\nMagneto....");
                mag_start();          

            }
            break;
            
            case lcd:
            {                
            //printf("\nLCD....");
            display_radar(dis, angle);       //Display the object position and heading        

            }
            break;
            
            default:
            {
               //printf("\nDefault....");
               angle=motor_rotate();

            }
            break;  
        }
    }
}

static int evnt_count=0;
void schedule_event()
{

evnt_count = evnt_count % 2;            //generate sequential events
evnt_count++;                     //Generate interrupts and add to queue
//printf("\nEvent:%d", evnt_count);
e.type = evnt_count;  

queue_push(e);
}
