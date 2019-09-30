# PYCVSS

### This is a python module for the CVSS architecture designed for research and service provision :computer:

## Quick installation guide for the PYCVSS module :coffee: :eyeglasses:
```Shell
pip install -r requirements.txt --user
pip install -e . --user
```

## Pipenv can also be used to install the module and it's dependencies
```Shell
pip install pipenv --user
pipenv install -dev
pipenv install -e .

## Open up a pipenv shell (this will enable your virtual environment)
pipenv shell
## Run scripts within the shell
## Exit the shell when finished
exit
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

# Running a service:
To list all available services:
```Shell
py run_service.py services
```
Service commands take on the following format:
```Shell
py run_service.py {service_name_subarg} {-arg}
```
Running the motioncapture service:
```Shell
## To show the help menu for a specific service
py run_service.py motioncapture --help

## Running the service
py run_service.py motioncapture -i path/to/input_file.mp4 -o output_file.mp4
```


#
## TODO
This is the current TODO list for improvements to the PYCVSS module:
- Still to come:
  * [x] Initial implementation of Service Management object and module entry point
  * [x] Initial implementation of motion capture and detection services
  * [ ] Implementation of FFMPEG calls (such as grayscale conversion, etc.) as services on the management object
  * [ ] Additional FFPEG bindings / process arg calls
