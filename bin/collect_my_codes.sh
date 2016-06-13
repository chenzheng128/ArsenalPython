#!/bin/bash

#ryu codes
cd ~/PycharmProjects/ryu
git branch zhchen #切换至 zhchen 分支
rsync -avv ./cuc/ ~/PycharmProjects/ArsenalPython/sdn/ryu-cuc

