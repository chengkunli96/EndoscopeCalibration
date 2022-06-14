import numpy as np
import cv2 as cv
import os
import sys
import argparse
import time

def get_args():
    parser = argparse.ArgumentParser(description='check the properties of stereo video.')
    parser.add_argument('--file', dest='file', type=str, required=True)
    parser.add_argument('--save', dest='save', type=str, required=True)
    parser.add_argument('--roi', dest='roi', nargs='+', type=int, required=True, help='leftpoint_x leftpoint_y rect_w rect_h')
    parser.add_argument('--resize', dest='resize', nargs='+', type=int, help='resize_w resize_h')
    
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()
    video_pth = args.file
    if not os.path.isabs(video_pth):
        video_pth = os.path.abspath(video_pth)

    video_name = os.path.basename(video_pth).split('.')[0]
    video_dir = os.path.dirname(video_pth)

    cap = cv.VideoCapture(video_pth)
    frame_count = cap.get(cv.CAP_PROP_FRAME_COUNT)
    frame_fps = cap.get(cv.CAP_PROP_FPS)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    save_pth = args.save
    if not os.path.isabs(save_pth):
        save_pth = os.path.abspath(save_pth)
    if not os.path.exists(save_pth):
        os.makedirs(save_pth)

    valid_row_range = [args.roi[1], args.roi[1] + args.roi[3]]
    valid_col_range = [args.roi[0], args.roi[0] + args.roi[2]]

    count = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret != True:
            break

        img = frame[valid_row_range[0]:valid_row_range[1], valid_col_range[0]:valid_col_range[1]]

        if args.resize is not None:
            img = cv.resize(img, (args.resize[0], args.resize[1]))

        if (count + 1) % 3 == 0:
            cv.imwrite(os.path.join(save_pth, '{:0>6d}.jpg'.format(count)), img)
        
        cv.imshow('original', frame)
        cv.imshow('proc', img)

        count += 1
        print('\rVideo Process Rate {}/{} ...'.format(count, int(frame_count)), end='', flush=True)
        
        if cv.waitKey(1) == ord('q'):
            break

        
cap.release()
cv.destroyAllWindows()        

