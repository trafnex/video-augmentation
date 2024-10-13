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

INTER_ARRIVAL_OUTPUT = "ipts.txt"
SEGMENT_DURATION_OUTPUT = "durations.txt"

# Compute augmentation parameters from the given dataset (quality switches,
# segment transmission durations, and normalized inter-packet delays) and write
# them to the paths specified in the constants above. This function can be used
# as a model to extract parameters from datasets other than LongEnough.
def write_params(dataset_path): #"../../data/dataset-var/none-none-bw1/"
    segment_ipts = []
    segment_durations = []

    for video in tqdm(range(100), desc = "Processing videos", unit = "video"):
        for offset in range(10):
            for sample in range(1):
                file = open(os.path.join(dataset_path, str(video), f"{video:04}-{offset:04}-{sample:04}.log"))
                lines = file.readlines() # slurp

                previous_time = 0
                current_time = 0

                # All segments
                ipts = []
                durations = []
                start_times = []

                # Current segment
                segment_time = 0

                # Get segment sizes based on client requests
                for line in lines:
                    parts = line.strip().split(",")
                    if len(parts) < 3:
                        continue

                    current_time = float(parts[0])

                    if parts[1] == "s": # outgoing from client
                        if 148 < int(parts[2]) < 155 and current_time - segment_time > 1*1000*1000*1000: # 1 second
                            if segment_time == 0:
                                ipts.append([])
                                segment_time = current_time
                            else:
                                ipts.append([])
                                durations.append(previous_time - segment_time)
                                start_times.append(segment_time)
                                segment_time = current_time
                            previous_time = current_time
                        continue

                    if len(ipts) > 0:
                        ipts[-1].append(current_time - previous_time)
                    previous_time = current_time
                
                # Add data for last segment
                durations.append(previous_time - segment_time)

                # Filter out rerequests
                while len(durations) > 300 - (offset * 30): # adjust expected segments based on offset
                    start_time_diffs = segment_start_time_diffs(start_times)
                    smallest_diff_index = start_time_diffs.index(min(start_time_diffs[1:]))

                    durations[smallest_diff_index - 1] += durations[smallest_diff_index]
                    durations.pop(smallest_diff_index)

                    ipts[smallest_diff_index - 1] += ipts[smallest_diff_index]
                    ipts.pop(smallest_diff_index)

                    start_times.pop(smallest_diff_index)
                
                segment_ipts += ipts
                segment_durations += durations

    # Normalize inter-arrival times
    normalized_ipts = []

    for ipts in segment_ipts:
        if ipts:
            avg = sum(ipts) / len(ipts)
            for ipt in ipts:
                normalized_ipts.append(ipt / avg)

    normalized_ipts.sort()

    # Write out results to files
    file = open(INTER_ARRIVAL_OUTPUT, "w+")
    for value in normalized_ipts:
        file.write(str(value))
        file.write("\n")

    segment_durations.sort()
    file = open(SEGMENT_DURATION_OUTPUT, "w+")
    for value in segment_durations:
        file.write(str(value))
        file.write("\n")

# Get the differences between segment start times.
def segment_start_time_diffs(start_times):
    diffs = [start_times[0]]
    for i in range(1, len(start_times)):
        diffs.append(start_times[i] - start_times[i - 1])     
    return diffs

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help = 'path to dataset root')
    args = parser.parse_args()

    write_params(args.path)
