/*
This Code is for RADAR SYSTEM: MAGNETOMETER API.
Course: CSE291E ( Robotics/Embedded Systems)
Assignment: 5
Last Modified: 05-Nov-2015
Team: CodeIT
Developers: Abhinav Garg; Abhijit Tripathi; Pulkit Bhatnagar
University of California, San Diego
*/

#include "mbed.h"
#include "magnetometer.h"
#include "math.h"

#define MAG_ADDR 0x3C

#define CRA_REG_M 0x18 //00
#define MR_REG_M 0x02

#define OUT_X_L_M 0x04
#define OUT_X_H_M 0x03
#define OUT_Y_L_M 0x08
#define OUT_Y_H_M 0x07
#define OUT_Z_L_M 0x06
#define OUT_Z_H_M 0x05

const float Pi = 3.14159;

//Max and Min values used for calibration 
static int maxMagX = 414;
static int minMagX = -354;

static int minMagY = -909;
static int maxMagY  = -551;

bool first_pass = true;
float true_angle = 0.0;

I2C i2c(p9, p10); //SDA, SCL
Serial terminal(USBTX, USBRX);
Ticker magt;

short x=0;
short y=0;
short z=0;

bool magflag = false;

char read_byte_i2c(int addr, int reg)
{
    char result;
    
    i2c.start();
    i2c.write(addr);                            // Slave/Device address
    i2c.write(reg);                             // Subaddress (register addess)
    
    i2c.start();                                // Change bus direction
    i2c.write(addr + 1);                        // Slave address with direction=read [bit0=1]
    
    result = i2c.read(0);
    i2c.stop();
    return result;
}
    
void write_byte_i2c(int addr, int reg,char value)             // Write one byte to an I2C bus START-->ADDR-->SUBADDR-->DATA-->STOP 
{    
    i2c.start();
    i2c.write(addr);                                          // Slave/Device address
    i2c.write(reg);                                         // Subaddress (register addess)
    i2c.write(value);
    i2c.stop();
}

void mag_read()
{        
    char xL, xH, yL, yH, zL, zH;
    
    xL = read_byte_i2c(MAG_ADDR, OUT_X_L_M);
    xH = read_byte_i2c(MAG_ADDR, OUT_X_H_M);
    yL = read_byte_i2c(MAG_ADDR, OUT_Y_L_M);
    yH = read_byte_i2c(MAG_ADDR, OUT_Y_H_M);
    zL = read_byte_i2c(MAG_ADDR, OUT_Z_L_M);
    zH = read_byte_i2c(MAG_ADDR, OUT_Z_H_M);
        
    x =  (xH << 8) | (xL) ; //Combine MSB and LSB
    y =  (yH << 8) | (yL) ;
    z =  (zH << 8) | (zL) ;
      
    terminal.printf("\nMAGNETOMETER:\t X:%d \t Y:%d \t Z:%d \n", x, y, z);
    //fprintf(stderr, "\n%d \t %d \n", x, y);
}

short mag_read_x()
{
    return x;
}

short mag_read_y()
{
    return y;
}


short mag_read_z()
{
    return z;
}


//Magnetometer calibration: Works well without motor magnetic interference!s
int mag_direction()
{
    float angle;
    float xActual,yActual;
    float rx = 0.5*(maxMagX-minMagX);//1/2 range calculation
    float zx = maxMagX -rx; // Zero Crossing calculation
    xActual = (x-zx)/rx;
    
    float ry = 0.5*(maxMagY-minMagY);//1/2 range calculation
    float zy = maxMagY -ry; // Zero Crossing calculation
    yActual = (y-zy)/ry;
      
    if((yActual == 0.0)&&(xActual >= 0.0))
        angle = 0;
    else if((yActual ==0.0)&&(xActual < 0.0))
        angle = 180;
    else     
        angle = atan2(yActual,xActual)*180/Pi;
        
//if (first_pass || (abs(angle - true_angle)<5.0)) 
    true_angle = (angle);
    first_pass = false;
    return true_angle;
}

void mag_init(float delay)
{
    write_byte_i2c(MAG_ADDR, CRA_REG_M, 0x04);
    write_byte_i2c(MAG_ADDR, MR_REG_M, 0x00);
}