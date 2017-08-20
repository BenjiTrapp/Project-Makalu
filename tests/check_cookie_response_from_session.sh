#!/usr/bin/env bash
# Make sure, that the application is running

curl -c - 127.0.0.1:4711/login | grep vsessid

# The curl command shall return something like this
#% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                 Dload  Upload   Total   Spent    Left  Speed
#100   824  100   824    0     0  51500      0 --:--:-- --:--:-- --:--:-- 51500
#127.0.0.1       FALSE   /       FALSE   0       vsessid f7391a6f-e185-4d47-beb9-c527ed2af915
