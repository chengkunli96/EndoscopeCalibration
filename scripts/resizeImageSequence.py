import numpy as np
import cv2 as cv
import glob
import os
from os.path import join as opj
import argparse
import shutil
import sys


def get_args():
    parser = argparse.ArgumentParser(description='check the properties of stereo video.')
    parser.add_argument('--dir', dest='dir', type=str, required=True)
    parser.add_argument('--save', dest='save', type=str, required=True)
    parser.add_argument('--resize', dest='resize', nargs='+', type=int, help='resize_w resize_h', required=True)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()
    src_dir = args.dir
    sv_dir = args.save

    if not os.path.exists(sv_dir):
        os.makedirs(sv_dir)
    
    included_extensions = ['jpg', 'jpeg', 'png']
    file_names = [fn for fn in os.listdir(src_dir)
        if any(fn.endswith(ext) for ext in included_extensions)]
    file_names.sort()

    for fn in file_names:
        source = opj(src_dir, fn)
        target = opj(sv_dir, fn)

        img = cv.imread(source)
        rs_img = cv.resize(img, (args.resize[0], args.resize[1]))
        cv.imwrite(target, rs_img)

 

