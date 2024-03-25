#!/bin/bash

pid=$$

echo -e "CURRENT PROCESS \n $(ps -p $$ -o cmd=) \n"

echo "PROCESS ANCESTORS"


while [ "$pid" -ne 1 ]; do
    read ppid command <<< "$(ps -p $pid -o ppid=,cmd=)"
    echo "PID: $pid | Command: $command"
    pid=$ppid
done


echo "PID: 1 | Command: $(ps -p 1 -o cmd=)"  # Print information for the root process (init/systemd)
echo " "


echo "PROCESS DESCENDANTS"

