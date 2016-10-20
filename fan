#!/bin/bash

fanspeed=$(cat /proc/acpi/ibm/fan | awk 'NR==2 {print $2}')

echo $fanspeed "rpm"
