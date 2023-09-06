#!/bin/sh
cd ./athena
./configure.py $1
make clean
make -j