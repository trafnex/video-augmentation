# video-augmentation

This repository contains code from the following paper:
 - August Carlson, David Hasselquist, Ethan Witwer, Niklas Johansson, and Niklas Carlsson. "Understanding and Improving Video Fingerprinting Attack Accuracy under Challenging Conditions". 23rd Workshop on Privacy in the Electronic Society (WPES '24), 2024

If you use the code in this repository or the linked datasets in your work, please include a reference to the paper.
Some of the code is based on other research, as noted below - please cite any other relevant papers as well to credit their authors.

## Overview

We provide implementations of these video fingerprinting attacks:
 - Deep Fingerprinting (DF) [1] + Video-Adapted DF
 - Robust Fingerprinting (RF) [2] + Video-Adapted RF

*Code for these attacks is currently not available. It will be uploaded as soon as possible.* An implementation of the other attack mentioned in the paper, Beauty and the Burst (BnB) [3], can be found [here](https://github.com/trafnex/raising-the-bar).

Our augmentation techniques are also included in the repository:
 - Bandwidth augmentation (`augmentation/bw-{aug,params}.py`)
 - Offset augmentation (`augmentation/offset.py`)

**Attacks and augmentation techniques are provided for research purposes only.**

## Setup Tasks

You will need `python3`/`pip` to run the code; they can be downloaded via your distribution's package manager. For example:

```bash
  sudo apt update
  sudo apt install python3 python3-pip
```

Next, use `pip` to install the modules specified in `requirements.txt`. We strongly recommend a CUDA-enabled GPU if you intend to run the attacks.

```bash
  sudo pip3 install -r requirements.txt
```

## Code Usage

### Augmentation

The augmentation techniques work by generating a new dataset from a provided dataset.

For the bandwidth augmentation, first run `python3 bw-params.py` (from the `augmentation` directory), providing the path to the dataset root as a positional argument. Note that this is the *target* dataset, which must be representative of the bandwidth conditions that the augmentation should be tailored to. Next, run `python3 bw-aug.py`, providing the path to the *constant bandwidth* dataset and an output path as positional arguments.

For the offset augmentation, run `python3 offset.py`, providing the path to the dataset root and an output path as positional arguments. You must also provide either the `-k` argument, to generate a training dataset in the way described in the paper, or the `--test` argument, to generate a testing dataset.

## Datasets

As described in the paper, we provide an extended version of the _LongEnough_ dataset, which contains traffic traces and QoE metric data for three additional bandwidth scales.

It is available in the same location as the original _LongEnough_ dataset: [https://liuonline-my.sharepoint.com/:f:/g/personal/davha914_student_liu_se/ErK6esYd5IdOiuvfLnXK6NoBEdlj579MlXBvG2wkfQEozg?e=sCHtWp](https://liuonline-my.sharepoint.com/:f:/g/personal/davha914_student_liu_se/ErK6esYd5IdOiuvfLnXK6NoBEdlj579MlXBvG2wkfQEozg?e=sCHtWp)

More details are provided in the dataset README.

## License Info

The code in this repository is available under the terms of the BSD-3-Clause license.

## References
 [1] Payap Sirinam et al. "Deep Fingerprinting: Undermining Website Fingerprinting Defenses with Deep Learning." ACM CCS. October 2018. (https://dl.acm.org/doi/10.1145/3243734.3243768)  
 [2] Meng Shen et al. "Subverting Website Fingerprinting Defenses with Robust Traffic Representation". USENIX Security. August 2023. (https://www.usenix.org/conference/usenixsecurity23/presentation/shen-meng)  
 [3] Roei Schuster, Vitaly Shmatikov, and Eran Tromer. "Beauty and the Burst: Remote Identification of Encrypted Video Streams". USENIX Security. August 2017. (https://www.usenix.org/conference/usenixsecurity17/technical-sessions/presentation/schuster)
