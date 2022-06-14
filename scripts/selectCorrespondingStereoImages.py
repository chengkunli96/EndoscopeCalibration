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
    parser.add_argument('--ref', dest='ref', type=str, required=True)
    parser.add_argument('--fromdir', dest='fromdir', type=str, required=True)
    parser.add_argument('--todir', dest='todir', type=str, required=True)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()
    select_ref = args.ref
    select_from = args.fromdir

    select_to = args.todir
    if not os.path.isabs(select_to):
        select_to = os.path.abspath(select_to)
    if not os.path.exists(select_to):
        os.makedirs(select_to)
    
    included_extensions = ['jpg', 'jpeg', 'png']
    file_names = [fn for fn in os.listdir(select_ref)
        if any(fn.endswith(ext) for ext in included_extensions)]
    file_names.sort()

    for fn in file_names:
        source = opj(select_from, fn)
        target = opj(select_to, fn)
        # print('copy file {:s}'.format(fn))
        try:
            shutil.copy(source, target)
        except IOError as e:
            print("Unable to copy file. %s" % e)
        except:
            print("Unexpected error:", sys.exc_info())

 

