<style>
img[src*="#width-full"] {
  width: 100%;
  margin: auto;
  display: block;
}
</style>

# Calibration for Endoscope
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![GitHub stars](https://img.shields.io/github/stars/chengkunli96/EndoscopeCalibration.svg?style=social)](https://github.com/chengkunli96/EndoscopeCalibration/stargazers)

This reporsitory aims to provide some scripts for easily doing calibration for stereo camera. Here, I use endoscope calibration case as example. And the nessary steps could be found below.

## Checkerboard Type
Our lab's [checkerboard](./docs/images/checker_board_type.jpg#width-full) could be found here.

## Prepare for calibration
``` bash
cd script
``` 

![stereo_video](./docs/images/stereo_video.png#width-full)
For stereo video file, we do following.
``` bash
# this script will output the information about this stereo video
python checkStereoVideo.py --file stereo_video_file

# follow the information obtained by the previous script
# do the following, and it will seperate the stereo file into left image sequence and right image sequence
python convertStereoVideo2Images.py --file stereo_video_file  --save img_sequence_dir --leftroi roix roiy roiw roih --rightroi roix roiy roiw roih [--resize resw resh]
```
![two_mono_video](./docs/images/left_right_video.png#width-full)
For left video and right video (left view and right view are stored in two videos respectively), we do following.
```bash
# check the black boundary of the video
python checkMonoVideo.py --file video0_file
python checkMonoVideo.py --file video1_file

# removing the black boundary and save frames as image sequence
pyhton convertStereoVideo2Images.py --file stereo_video_file  --save img_sequence_dir --roi roix roiy roiw roih --rightroi roix roiy roiw roih [--resize resw resh]
```

There are some other useful script for us to use, like resize an image sequece or select suitable images to calibrate.
``` bash
# run this for easily select the corresponding images which have the same file name with images in the seleted dir.
python selectCorrespondingStereoImages.py  --ref selected_dir --fromdir source_sequence_dir --todir target_selected_dir

# For every image in the sequece, do resize operation and save them.
python resizeImageSequence.py --dir img_seq_dir --save proc_sv_dir --resize resw resh
```

## Calibrate by Matlab 
![stereo_calibration_matlab](./docs/images/stereo_calibration_matlab.png#width-full)
1. Open matlab find `APP/Stereo Camera Calibrator`.
2. `Add Images`, input left and right images sequences dir path. Input your checkerboard size.
3. Select `3 Coefficients`, `Tangential Distortion`, `Skew` (this option is not necessary). And print `Calibrate` button.
4. You will see the error result in `Reprojection Errors` window. Drop the red line in this window to select the outlier which you want to delete.
5. Then right click on the image pair you selected, click `Remove and Recalibrate`. Please notice, sometimes, error happens and it maybe do not do recalibrate automatically. In this strange case, you can print `Calibrate` button manually (by check or non-check skew, this button will reactivate). 
6. Finally, print `Export Camera Parameters/Export to workspace`, and make sure the stereo parameters variable is `stereoParams` and press `OK`.
7. In the workspace of matlab, make sure the workspace path is in _./scripts/matlab2OpencvYaml_, run script `saave2yaml`. And you will find an _endoscope_calibration.yaml_ file in _./scripts/matlab2OpencvYaml/out_.

## Other instruction
1. The camera parameters will change when you do crop or resize operation: For cropping, `cx, cy` which change, and `cx, cy, fx, fy` will change basing on resize ratio in the case of resize. However, `baseline` parameter will never be changed.
2. The unit of the camera parameters: by our `save2yaml.m` script, the unit of `cx, cy, f` is pixel. Differently, the unit of `baseline` of stereo camera is millimeter. 


