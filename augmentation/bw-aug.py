#!/usr/bin/env python3
# Code from the paper: August Carlson, David Hasselquist, Ethan Witwer, Niklas
# Johansson, and Niklas Carlsson. "Understanding and Improving Video
# Fingerprinting Attack Accuracy under Challenging Conditions". 23rd Workshop
# on Privacy in the Electronic Society (WPES '24), 2024. If you use this code
# in your work, please include a reference to the paper.
# More details are available in README.md

import argparse
import math
import os
import random

import bw_params

from tqdm import tqdm

# Adjust based on targeted dataset
SWITCH_PROBABILITY = 10 # % chance of changing qualities at each segment
QUALITY_PARAM_1 = 22    # % chance of switching from 1 to 4, if switching
QUALITY_PARAM_2 = 36    # % chance of switching from 2 to 4, if switching
QUALITY_PARAM_4 = 79    # % chance of switching from 4 to 2, if switching

def do_augmentation(path_in, path_out):
    os.mkdir(path_out)

    print("Loading parameters...")
    file = open(parameters.SEGMENT_DURATION_OUTPUT)
    segment_durations = file.readlines() # slurp
    segment_durations.pop(-1)

    file = open(parameters.INTER_ARRIVAL_OUTPUT)
    segment_ipts = file.readlines() # slurp
    segment_ipts.pop(-1) 

    for video in tqdm(range(100), desc = "Processing videos", unit = "video"):
        os.mkdir(os.path.join(path_out, str(video)))

        for offset in range(10):
            new_sample = 0

            for sample in range(10):
                for i in range(1): # how many times each trace is duplicated and augmented
                    fin = open(os.path.join(path_in, str(video), f"{video:04}-{offset:04}-{sample:04}.log"))
                    fout = open(os.path.join(path_out, str(video), f"{video:04}-{offset:04}-{new_sample:04}.log"), "w+")
                    new_sample += 1
                    
                    lines = fin.readlines()

                    # All segments
                    segment_sizes = []
                    start_times = []

                    # Current segment
                    start_segment = True
                    current_size = 0
                    current_end = 2*1000*1000*1000 # 2 seconds
                    
                    # Gather segment data from original trace
                    for line in lines:
                        parts = line.split(",")
                        if len(parts) < 3:
                            continue

                        if parts[1] == "s": # outgoing from client
                            continue
                            
                        if start_segment:
                            start_times.append(float(parts[0]))
                            start_segment = False
                        
                        if float(parts[0]) < current_end:
                            current_size += float(parts[2]) - 52 # remove packet overhead
                        else:
                            segment_sizes.append(current_size)
                            start_segment = True
                            current_size = 0
                            current_end += 2*1000*1000*1000 # 2 seconds

                    start_times.pop(0)

                    # Perform the augmentation segment-by-segment
                    quality = 2 # start with median quality
                    current_time = 0

                    for i in range(len(segment_sizes)):
                        segment_size = segment_sizes[i]

                        # Pick a quality for this segment
                        quality = pick_new_quality(quality)

                        # Scale segment size based on quality
                        segment_size *= quality / 4 

                        # Pick segment size
                        duration_index = random.randint(0, len(segment_durations) - 1)
                        segment_duration = float(segment_durations[duration_index])

                        # Calculate required packets
                        packets = segment_size / (1500 - 52) # -52
                        packets = int(math.ceil(packets)) # Convert to whole packets

                        # Time per packet
                        default_ipt = segment_duration / packets

                        # If gap between chunks, apply gap
                        if current_time < start_times[i]:
                            current_time = start_times[i]
                        
                        packet_string = ""
                        while True:
                            # Pick random factor from inter-arrival times
                            inter_arrival_index = random.randint(0, len(segment_ipts) - 1)
                            inter_arrival_factor = float(segment_ipts[inter_arrival_index])

                            current_time += default_ipt * inter_arrival_factor

                            packet_string += str(int(current_time))

                            if segment_size > 1500 - 52: # -52
                                packet_string += ",r,1500"           
                                packet_string += "\n"
                                fout.write(packet_string)
                                packet_string = ""
                                segment_size -= 1500 - 52
                            else:
                                packet_string += f",r,{int(segment_size) + 52}" # +52
                                packet_string += "\n"
                                fout.write(packet_string)
                                packet_string = ""
                                break

# Pick a new quality based on the chosen parameters and the current quality.
def pick_new_quality(quality):
    if random.randint(0, 99) < SWITCH_PROBABILITY:
        quality_random = random.randint(0, 99)
        if quality == 1:
            if quality_random < QUALITY_PARAM_1:
                quality = 4
            else:
                quality = 2
        elif quality == 2:
            if quality_random < QUALITY_PARAM_2:
                quality = 4
            else:
                quality = 1
        else:
            if quality_random < QUALITY_PARAM_4:
                quality = 2
            else:
                quality = 1
    
    return quality

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path_in', help = 'path to dataset root, original')
    parser.add_argument('path_out', help = 'path to dataset root, augmented')
    args = parser.parse_args()

    do_augmentation(args.path_in, args.path_out)
