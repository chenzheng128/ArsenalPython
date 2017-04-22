#!/bin/sh
sudo ./pair_intervals.py --counts 2,2,2 --time 10 -o results/links2.out
sudo ./pair_intervals.py --counts 3,3,3 --time 10 -o results/links3.out

./plot_pair_intervals.py -lr results/links*.out
