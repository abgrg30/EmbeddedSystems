/*
This Code is for RADAR SYSTEM: RADAR OLED API.
Course: CSE291E ( Robotics/Embedded Systems)
Assignment: 5
Last Modified: 05-Nov-2015
Team: CodeIT
Developers: Abhinav Garg; Abhijit Tripathi; Pulkit Bhatnagar
University of California, San Diego
*/

#include "mbed.h"
#include "Adafruit_SSD1306.h"
#include "font_5x7.h"
#include "radar.h"
#define PI 3.142

// an I2C sub-class that provides a constructed default
class I2CPreInit : public I2C
{
public:
    I2CPreInit(PinName sda, PinName scl) : I2C(sda, scl)
    {
        frequency(400000);          //400Khz
        start();
    };
}; 

I2CPreInit comm(p28,p27);
Adafruit_SSD1306_I2c gOled(comm, p29);

//float xTable[]={126,123,117,107,94,79,63,46,31,18,2,0,0,2,8,18,31,46,63,79,94,107,117,123,126}; //13steps
//float yTable[]={63,46,31,18,8,2,0,2,8,18,31,46,63,63,79,94,107,117,123,126,123,117,107,94,79,63};    //13steps

//26+26 steps
//float xTable[]={126 ,125 ,124 ,121 ,118 ,114 ,109 ,104 ,98 ,91 ,84 ,77 ,69 ,61 ,54 ,46 ,39 ,32 ,25 ,20 ,14 ,10 ,6 ,3 ,1 ,0 ,0 ,0 ,1 ,3 ,6 ,10 ,14 ,20 ,25 ,32 ,39 ,46 ,54 ,61 ,69 ,77 ,84 ,91 ,98 ,104 ,109 ,114 ,118 ,121 ,124 ,125 ,126 };
//float yTable[]= {63 ,55 ,47 ,40 ,33 ,26 ,20 ,15 ,10 ,6 ,3 ,1 ,0 ,0 ,0 ,2 ,4 ,7 ,12 ,16 ,22 ,28 ,35 ,42 ,49 ,57 ,65 ,57 ,49 ,42 ,35 ,28 ,22 ,16 ,12 ,7 ,4 ,2 ,0 ,0 ,0 ,1 ,3 ,6 ,10 ,15 ,20 ,26 ,33 ,40 ,47 ,55 ,63};   

float distan;
int step;
float theta;
float theta_rad;
Ticker rtick;
bool rflag = false;

int x1=0,y1=0;
int x2=0,y2=0;
int x3=0,y3=0;
int x4=0,y4=0;
int r = 63;
int x0 = 63;
int y0 = 63;
int counter=0;
int prevcounter = 0;
int prevstep=26;
int xmy,ymy,xmy_prev,ymy_prev;
void display_radar(float dist,float t)
{
    distan = dist;
    step=t;
    theta = (t*3.5); //52 motor steps*3.5degree for display
   if(theta>180) {theta=180;}  //For rounding-off motor step size
   if(theta<0) {theta=0;} 
    theta_rad = (theta)*PI/180; //radians
    rflag = true;
}

int buf[53][2]={0,};            //Buffer to store object location on radar display!
void algo_radar()
{   
    //Print radar circles
    gOled.drawCircle(x0,y0,r,1);
    gOled.drawCircle(x0,y0,2*r/4,1);
    gOled.drawCircle(x0,y0,3*r/4,1);
    gOled.drawCircle(x0,y0,r/4,1);
    //gOled.drawLine(0,y0-1,127,y0-1,WHITE);
    
    //Check for buffer value: if object removed, remove blip from radar
    if (buf[step][0] != 0 || buf[step][1] != 0)
    {
    gOled.drawPixel(buf[step][0],buf[step][1],BLACK);
    gOled.drawPixel(buf[step][0]+1,buf[step][1],BLACK);
    gOled.drawPixel(buf[step][0],buf[step][1]+1,BLACK);
    gOled.drawPixel(buf[step][0]+1,buf[step][1]+1,BLACK);
    buf[step][0] = 0;
    buf[step][1] = 0;
    }   

//  gOled.drawLine(x0,y0,xTable[prevstep],yTable[prevstep],BLACK);  
    gOled.drawLine(x0,y0,x1,y1,BLACK);  
    
    //Object Mapping Algorithm
    //Scale distance from Ultasonic to radar Display.
    //Max Distance detectable set to: 20cm.
    //Radar Screen diameter of outer circle: 63 pix
    //so, 20cm scaled to 63pix as blip => distance/20*63
    
    float rScaled = (distan/20)*63;
    if(distan < 20) {                        //Filter object > 20cm away
      
        x1 = x0 + (int)(rScaled*cos(theta_rad));        //coordinate of point in terms of rscaled and theta/angle
        y1 = y0 - (int)(rScaled*sin(theta_rad));
        
    //printf("\nrscaled=%f\t theta_rad=%f\t cos=%f\t sin=%f\t x1=%d\t y1=%d\n",rScaled,theta_rad,cos(theta_rad),sin(theta_rad),x1,y1);
      
    x2 = x1+1;
    y2 = y1;
    
    x3 = x1+1;
    y3 = y1+1;
        
    x4 = x1;
    y4 = y1+1;

    //Display 2x2 pixel spot on screen
    gOled.drawPixel(x1,y1,WHITE);
    gOled.drawPixel(x2,y2,WHITE);
    gOled.drawPixel(x3,y3,WHITE);
    gOled.drawPixel(x4,y4,WHITE);
    gOled.display();
    buf[step][0] = x1;
    buf[step][1] = y1;
    }

    //Display Heading/Angle on right top of OLED
    gOled.fillRect(90,0,37,8,BLACK);
    gOled.setTextCursor(90,0);
    gOled.printf(" %d`N",(int(theta)-90));
    
    //Sweep radar
    //gOled.drawLine(x0,y0,xTable[step],yTable[step],WHITE); 

    x1 = x0 + (int)(r*cos(theta_rad));
    y1 = y0 - (int)(r*sin(theta_rad)); 
    gOled.drawLine(x0,y0,x1,y1,WHITE);
    
    gOled.display();
    
    prevcounter = counter;
    prevstep=step;
    counter = (counter + 1)%52;
 }

void radar_attach()
{
    if(rflag)
    {
        rflag = false;
        algo_radar();
    }
}

void radar_init()
{
    distan = 0.0;
    theta = 0.0;
    
    gOled.clearDisplay();
    gOled.setTextCursor(70,0);
    gOled.drawCircle(x0,y0,r,1);
    gOled.drawCircle(x0,y0,2*r/4,1);
    gOled.drawCircle(x0,y0,3*r/4,1);
    gOled.drawCircle(x0,y0,r/4,1);
    //gOled.drawLine(0,y0-1,127,y0-1,WHITE);
          
    rtick.attach(radar_attach, 0.5);
}