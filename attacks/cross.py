#!/usr/bin/env python3
# Code from the paper: August Carlson, David Hasselquist, Ethan Witwer, Niklas
# Johansson, and Niklas Carlsson. "Understanding and Improving Video
# Fingerprinting Attack Accuracy under Challenging Conditions". 23rd Workshop
# on Privacy in the Electronic Society (WPES '24), 2024. If you use this code
# in your work, please include a reference to the paper.
# More details are available in README.md

import argparse
import os
import random

# Directory to save cross-validation splits to
# Files have the format "X.txt", where X is the number of subpages.
CROSS_VALIDATION_DIR = "cross-validation/"

def cross_validation():
    parser = argparse.ArgumentParser()
    parser.add_argument("c", type = int, default = 100, help = "the number of monitored videos (=classes)")
    parser.add_argument("p", type = int, default = 10, help = "the number of offsets")
    args = parser.parse_args()

    try:
        os.mkdir(CROSS_VALIDATION_DIR)
    except: pass

    with open(f"{CROSS_VALIDATION_DIR}{args.p}.txt", "w+") as results_file:
        for _ in range(args.c):
            # Pick a random testing/validation *offset* index.
            # All samples from this offset will be included.
            current = random.sample(range(0, args.p), 2)
            results_file.write(str(current[0]) + ",")
            results_file.write(str(current[1]) + "\n")

if __name__ == '__main__':
    cross_validation()
