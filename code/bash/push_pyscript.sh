#!/bin/bash
cat $1 | ssh daniel@ec2-184-72-234-254.compute-1.amazonaws.com "cat> $1 ;scp $1 ec2-50-16-142-215.compute-1.amazonaws.com:~/dump/scripts/"
#ssh daniel@ec2-184-72-234-254.compute-1.amazonaws.com "ls -l "
