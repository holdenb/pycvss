# PYCVSS

### This is a python module for the CVSS architecture designed for research and service provision :computer:

## Quick installation guide for the PYCVSS module :coffee: :eyeglasses:
```Shell
pip install -r requirements_dev.txt
pip install -e .
```

### Note: You will need to install both pytorch and ffmpeg:
- FFmpeg: https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg
- Pytorch: https://pytorch.org/get-started/locally/

# Using a pre-trained SSD network for detection

#### Download a pre-trained network
- Currently, the following PyTorch models are available from Max deGroot & Ellis Brown:
    * SSD300 trained on VOC0712 (newest PyTorch weights)
      - https://s3.amazonaws.com/amdegroot-models/ssd300_mAP_77.43_v2.pth
    * SSD300 trained on VOC0712 (original Caffe weights)
      - https://s3.amazonaws.com/amdegroot-models/ssd_300_VOC0712.pth

### Once downloaded, place the chosen training file within the ssd/training_files/ directory.

# Running the example scripts
Theres currently an example_scripts directory that contains code on how to run:
 - Motion capture (FDCM single video input)
 - Static SSD object detection (frame by frame, single input)
 - Live SSD object detection (Note: GPU Acceleration is strongly advised)
 - FFMPEG benchmarking test suite

#
## Example test:
From the pycvss directory:
```Shell
./run_ssd_detector.py -p ssd/training_files/ssd300_mAP_77.43_v2.pth
```
This will use a default sample video for detection.

#
## TODO
This is the current TODO list for improvements to the PYCVSS module:
- Still to come:
  * [x] Initial implementation of Service Management object and module entry point
  * [ ] Initial implementation of motion capture and detection services
  * [ ] Implementation of FFMPEG calls (such as grayscale conversion, etc.) as services on the management object
  * [ ] Additional FFPEG bindings / process arg calls
