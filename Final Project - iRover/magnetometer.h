#ifndef MAGNETOMETER_H
#define MAGNETOMETER_H

void mag_init(float delay);
void mag_read();
short mag_read_x();
short mag_read_y();
short mag_read_z();
void mag_start();
int mag_direction();
#endif