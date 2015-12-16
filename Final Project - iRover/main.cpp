#include "mbed.h"
#include "motor.h"
#include "ultra.h"
#include "magnetometer.h"


Serial pc(USBTX, USBRX);
Serial uart(p13, p14);


int main() 
{
    while(1) 
    {                       
        if(uart.readable()) 
        {
            char var = uart.getc();
            pc.putc(var);

            if (var == '0') 
            {
                printf("\nGot 0");
                    motor_clockwise();
            } 
            else if (var == '1') 
            {
                printf("\nGot 1");
                    motor_anticlockwise();
            } 
            else if (var == '2') 
            {
                    printf("\nGot 2");
                    float distance=ultra_start();
                    wait_us(5);
                    printf("\nDistance:%f",distance);
                    uart.printf("%d\n",(int)distance);
            } 
            else if (var == '3') 
            {
                    printf("\nGot 3");
                    float angle=mag_direction();
                    float x=mag_read_x();
                    float y=mag_read_y();
                    float z=mag_read_z();
                    mag_read();
                    printf("\nAngle:%f",angle);
                    printf("\nx:%f",x);
                    printf("\ny:%f",y);
                    printf("\nz:%f",z);

                    uart.printf("%d,",(int)x);
                    uart.printf("%d,",(int)y);
                    uart.printf("%d,",(int)z);
                    uart.printf("%d,\n",(int)angle);
            }
        }
    }
}