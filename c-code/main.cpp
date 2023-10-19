#include <wiringPiI2C.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <time.h>
#include <stdint.h>
#include <curl/curl.h>
#include <pthread.h>
#include <unistd.h>
#include <vector>
#include <memory>

#include "send_data.cpp"
#include "sensor.cpp"

#define Device_Address 0x68 /*Device Address/Identifier for MPU6050*/

#define PWR_MGMT_1 0x6B
#define SMPLRT_DIV 0x19
#define CONFIG 0x1A
#define GYRO_CONFIG 0x1B
#define INT_ENABLE 0x38
#define ACCEL_XOUT_H 0x3B
#define ACCEL_YOUT_H 0x3D
#define ACCEL_ZOUT_H 0x3F
#define GYRO_XOUT_H 0x43
#define GYRO_YOUT_H 0x45
#define GYRO_ZOUT_H 0x47

int fd;

void MPU6050_Init()
{
    wiringPiI2CWriteReg8(fd, SMPLRT_DIV, 0x07); /* Write to sample rate register */
    wiringPiI2CWriteReg8(fd, PWR_MGMT_1, 0x01); /* Write to power management register */
    wiringPiI2CWriteReg8(fd, CONFIG, 0);        /* Write to Configuration register */
    wiringPiI2CWriteReg8(fd, GYRO_CONFIG, 24);  /* Write to Gyro Configuration register */
    wiringPiI2CWriteReg8(fd, INT_ENABLE, 0x01); /*Write to interrupt enable register */
}

short read_raw_data(int addr)
{
    short high_byte, low_byte, value;
    high_byte = wiringPiI2CReadReg8(fd, addr);
    low_byte = wiringPiI2CReadReg8(fd, addr + 1);
    value = (high_byte << 8) | low_byte;
    return value;
}

void ms_delay(int val)
{
    int i, j;
    for (i = 0; i <= val; i++)
        for (j = 0; j < 1200; j++)
            ;
}

int main()
{

    float Acc_x, Acc_y, Acc_z;
    float Gyro_x, Gyro_y, Gyro_z;
    float Ax = 0, Ay = 0, Az = 0;
    float Gx = 0, Gy = 0, Gz = 0;
    
    fd = wiringPiI2CSetup(Device_Address); /*Initializes I2C with device Address*/
    MPU6050_Init();                        /* Initializes MPU6050 */

    time_t start_time = time(NULL);
    time_t current_time;

    const int duration = 2; /* Second Duration at which data is sent to the server*/
    const int delay_ms = 5; /* MilliSecond Delay between each reading of MPU6050 */

    std::vector<SensorData> sensorDataVector;

    while (1)
    {
        // Read raw values
        Acc_x = read_raw_data(ACCEL_XOUT_H);
        Acc_y = read_raw_data(ACCEL_YOUT_H);
        Acc_z = read_raw_data(ACCEL_ZOUT_H);

        Gyro_x = read_raw_data(GYRO_XOUT_H);
        Gyro_y = read_raw_data(GYRO_YOUT_H);
        Gyro_z = read_raw_data(GYRO_ZOUT_H);

        // Divide raw values by sensitivity scale factor
        Ax = Acc_x / 16384.0;
        Ay = Acc_y / 16384.0;
        Az = Acc_z / 16384.0;

        Gx = Gyro_x / 131;
        Gy = Gyro_y / 131;
        Gz = Gyro_z / 131;

        current_time = time(NULL);

        struct SensorData data;
        data.Gx = Gx;
        data.Gy = Gy;
        data.Gz = Gz;
        data.Ax = Ax;
        data.Ay = Ay;
        data.Az = Az;
        data.timestamp = current_time;
        
        
        sensorDataVector.push_back(data);


        // Print sensor values
       // printf("\n Gx=%.3f °/s\tGy=%.3f °/s\tGz=%.3f °/s\tAx=%.3f g\tAy=%.3f g\tAz=%.3f g\n", Gx, Gy, Gz, Ax, Ay, Az);
        
        

        if (current_time - start_time >= duration)
        {   
            start_time = current_time;
            printf("Sending Data! | Sample count: %d\n", sensorDataVector.size());
            
            auto dataCopy = std::unique_ptr<std::vector<SensorData>>(new std::vector<SensorData>());
            
            //std::create_unique<std::vector<SensorData>> dataCopy = std::make_unique<std::vector<SensorData>>(); // C++14 feature : not available here on raspberry-pi
            
            sensorDataVector.clear();

            pthread_t thread;
            pthread_create(&thread, NULL, (void *(*)(void *))sendSensorData, &dataCopy);
           
        }

        
        delay(delay_ms);
    }


    return 0;
}
