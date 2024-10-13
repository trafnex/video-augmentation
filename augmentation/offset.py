#!/usr/bin/env python3
# Code from the paper: August Carlson, David Hasselquist, Ethan Witwer, Niklas
# Johansson, and Niklas Carlsson. "Understanding and Improving Video
# Fingerprinting Attack Accuracy under Challenging Conditions". 23rd Workshop
# on Privacy in the Electronic Society (WPES '24), 2024. If you use this code
# in your work, please include a reference to the paper.
# More details are available in README.md

import argparse
import os

from tqdm import tqdm

def generate_training_dataset(path_in, path_out, k):
    os.mkdir(path_out)

    num_samples = 2**(k-1)
    interval_slice = 20 / (num_samples + 1)

    for video in tqdm(range(100), desc = "Processing videos", unit = "video"):
        os.mkdir(os.path.join(path_out, str(video)))

        for offset in range(10):
            new_sample = 0

            for sample in range(10):
                for i in range(num_samples):
                  fin = open(os.path.join(path_in, str(video), f"{video:04}-{offset:04}-{sample:04}.log"))
                  fout = open(os.path.join(path_out, str(video), f"{video:04}-{offset:04}-{sample:04}.log"), "w+")
                  new_sample += 1

                  lines = fin.readlines()
                  lines.reverse()

                  last_time = 0
                  # 10 is no offset here - this is how much we cut from the end
                  offs = 1000*1000*1000 * (20 - (i + 1) * interval_slice)
                  
                  for line in lines:
                      parts = line.split(",")
                      if len(parts) < 3:
                          continue
                      
                      if last_time == 0:
                          last_time = float(parts[0])
                          
                      if float(parts[0]) > last_time - offs:
                          continue

                      time = last_time - offs - float(parts[0]) 

                      if time > 40*1000*1000*1000: # 40-second long trace 
                          break

                      fout.write(f"{int(time)},{parts[1]},{parts[2]}\n")

def generate_testing_dataset(path_in, path_out):
    os.mkdir(path_out)

    num_samples = 11
    interval_slice = 2

    for video in tqdm(range(100), desc = "Processing videos", unit = "video"):
        os.mkdir(os.path.join(path_out, str(video)))

        for offset in range(10):
            new_sample = 0

            for sample in range(10):
                for i in range(num_samples):
                  fin = open(os.path.join(path_in, str(video), f"{video:04}-{offset:04}-{sample:04}.log"))
                  fout = open(os.path.join(path_out, str(video), f"{video:04}-{offset:04}-{sample:04}.log"), "w+")
                  new_sample += 1

                  lines = fin.readlines()
                  lines.reverse()

                  last_time = 0
                  # 10 is no offset here - this is how much we cut from the end
                  offs = 1000*1000*1000 * (20 - i * interval_slice)
                  
                  for line in lines:
                      parts = line.split(",")
                      if len(parts) < 3:
                          continue
                      
                      if last_time == 0:
                          last_time = float(parts[0])
                          
                      if float(parts[0]) > last_time - offs:
                          continue

                      time = last_time - offs - float(parts[0]) 

                      if time > 40*1000*1000*1000: # 40-second long trace 
                          break

                      fout.write(f"{int(time)},{parts[1]},{parts[2]}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path_in', help = 'path to dataset root, original')
    parser.add_argument('path_out', help = 'path to dataset root, augmented')
    parser.add_argument('-k', type = int, default = 0,
        help = 'split interval into 2^(k-1)+1 partitions')
    parser.add_argument('--test', action = 'store_true',
        help = 'generate testing dataset with 2s offsets')
    args = parser.parse_args()

    if args.test:
        generate_testing_dataset(args.path_in, args.path_out)
    elif args.k > 0:
        generate_training_dataset(args.path_in, args.path_out, args.k)
    else:
        print("Specify either -k or --test, run with --help for details.")
