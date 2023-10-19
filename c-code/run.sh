#!/bin/bash
gcc -Wall -o run main.c -lwiringPi -lm -lpthread -lcrypt -lrt && ./run
