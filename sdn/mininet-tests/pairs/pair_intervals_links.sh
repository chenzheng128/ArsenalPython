#!/bin/sh
sudo ./pair_intervals.py --counts 10,10,10 --time 60 -o results/links10.out
sudo ./pair_intervals.py --counts 20,20,20 --time 60 -o results/links20.out
sudo ./pair_intervals.py --counts 40,40,40 --time 60 -o results/links40.out
sudo ./pair_intervals.py --counts 80,80,80 --time 60 -o results/links80.out

# orignal
# ./plot_pair_intervals.py --all results/links*.out

./plot_pair_intervals.py -lr results/links*.out
