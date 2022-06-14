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
    parser.add_argument('--leftroi', dest='leftroi', nargs='+', type=int, required=True, help='leftpoint_x leftpoint_y rect_w rect_h')
    parser.add_argument('--rightroi', dest='rightroi', nargs='+', type=int, required=True, help='leftpoint_x leftpoint_y rect_w rect_h')
    parser.add_argument('--resize', dest='resize', nargs='+', type=int, help='resize_w resize_h')
    
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()
    stereo_video_pth = args.file
    if not os.path.isabs(stereo_video_pth):
        stereo_video_pth = os.path.abspath(stereo_video_pth)

    stereo_video_name = os.path.basename(stereo_video_pth).split('.')[0]
    stereo_video_dir = os.path.dirname(stereo_video_pth)

    cap = cv.VideoCapture(stereo_video_pth)
    frame_count = cap.get(cv.CAP_PROP_FRAME_COUNT)
    frame_fps = cap.get(cv.CAP_PROP_FPS)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    save_pth = args.save
    if not os.path.isabs(save_pth):
        save_pth = os.path.abspath(save_pth)
    save_left_pth = os.path.join(save_pth, 'left')
    save_right_pth = os.path.join(save_pth, 'right')
    if not os.path.exists(save_pth):
        os.makedirs(save_pth)
        os.makedirs(save_left_pth)
        os.makedirs(save_right_pth)

    left_row_range = [args.leftroi[1], args.leftroi[1] + args.leftroi[3]]
    left_col_range = [args.leftroi[0], args.leftroi[0] + args.leftroi[2]]
    right_row_range = [args.rightroi[1], args.rightroi[1] + args.rightroi[3]]
    right_col_range = [args.rightroi[0], args.rightroi[0] + args.rightroi[2]]

    count = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret != True:
            break

        left_img = frame[left_row_range[0]:left_row_range[1], left_col_range[0]:left_col_range[1]]
        right_img = frame[right_row_range[0]:right_row_range[1], right_col_range[0]:right_col_range[1]]

        if args.resize is not None:
            left_img = cv.resize(left_img, (args.resize[0], args.resize[1]))
            right_img = cv.resize(right_img, (args.resize[0], args.resize[1]))

        if (count + 1) % 3 == 0:
            cv.imwrite(os.path.join(save_left_pth, '{:0>6d}.jpg'.format(count)), left_img)
            cv.imwrite(os.path.join(save_right_pth, '{:0>6d}.jpg'.format(count)), right_img)
        
        cv.imshow('original', frame)
        cv.imshow('left', left_img)
        cv.imshow('right', right_img)

        count += 1
        print('\rVideo Process Rate {}/{} ...'.format(count, int(frame_count // 2)), end='', flush=True)
        
        if cv.waitKey(1) == ord('q'):
            break

        
cap.release()
cv.destroyAllWindows()        

