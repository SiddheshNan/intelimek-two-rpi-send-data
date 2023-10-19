#pragma once
#include <curl/curl.h>
#include <pthread.h>
#include <string.h>
#include "sensor.h"
#include <time.h>
#include <stdio.h>
#include <vector>
#include <memory>

const char *API_URL = "your_api_url_here";

void sendSensorData(const std::vector<SensorData> *data)
{
    // Initialize libcurl
    // CURL *curl = curl_easy_init();
    // if (curl)
    // {
    //     // Set the URL of your REST API
    //     curl_easy_setopt(curl, CURLOPT_URL, API_URL);

    //     // Set the HTTP method to POST
    //     curl_easy_setopt(curl, CURLOPT_POST, 1);

    //     // Set the POST data
    //     curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);

    //     // Perform the request
    //     CURLcode res = curl_easy_perform(curl);

    //     // Check for errors
    //     if (res != CURLE_OK)
    //     {
    //         fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
    //     }
    //     else
    //     {

    //         time_t t = time(NULL);
    //         struct tm tm = *localtime(&t);
    //         printf("%d-%d-%d %d:%d:%d Data sent successfully!\n", tm.tm_year + 1900, tm.tm_mon + 1,
    //                tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);
    //     }

    //     // Cleanup
    //     curl_easy_cleanup(curl);
    // }
}