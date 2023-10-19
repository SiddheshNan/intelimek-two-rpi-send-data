#pragma once
#include <curl/curl.h>
#include <pthread.h>
#include <string.h>
#include <time.h>
#include <stdio.h>
#include <vector>
#include <iostream>
#include <memory>
#include <nlohmann/json.hpp>

#include "sensor.cpp"

const std::string API_URL  = "http://localhost:8888/api/sensor/MPU6050";

// ToDo: serialize JSON to std::string using nlohmann::json and send using HTTP POST

void sendSensorData(const std::vector<SensorData> *sensorDataVector )
{
    
  //  std::cout << "Sending HTTP POST" << std::endl;
    
   /*  for (const SensorData& data : *sensorDataVector) { // TODO: causing segfault
        // Print the sensor data to std::cout
        std::cout << "timestamp: " << data.timestamp << " | Gx: " << data.Gx << " Gy: " << data.Gy << " Gz: " << data.Gz
                  << " Ax: " << data.Ax << " Ay: " << data.Ay << " Az: " << data.Az << std::endl;
    }*/
    
    
    
    /*CURL *curl = curl_easy_init();
    if (curl)
    {
        // Set the URL of your REST API
        curl_easy_setopt(curl, CURLOPT_URL, API_URL);

        // Set the HTTP method to POST
        curl_easy_setopt(curl, CURLOPT_POST, 1);

        // Set the POST data
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);

        // Perform the request
        CURLcode res = curl_easy_perform(curl);

        // Check for errors
        if (res != CURLE_OK)
        {
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        }
        else
        {

            time_t t = time(NULL);
            struct tm tm = *localtime(&t);
            printf("%d-%d-%d %d:%d:%d Data sent successfully!\n", tm.tm_year + 1900, tm.tm_mon + 1,
                   tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);
        }

        // Cleanup
        curl_easy_cleanup(curl);
    }*/
}
