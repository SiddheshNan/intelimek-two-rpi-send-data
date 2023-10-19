#!/bin/bash
gcc -Wall -o run main.cpp -lwiringPi -lm -lpthread -lcrypt -lrt -lcurl -lstdc++ && ./run
