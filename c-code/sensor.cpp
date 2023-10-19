#pragma once

#include <time.h>

struct SensorData
{
    float Gx;
    float Gy;
    float Gz;
    float Ax;
    float Ay;
    float Az;
    time_t timestamp;
};
