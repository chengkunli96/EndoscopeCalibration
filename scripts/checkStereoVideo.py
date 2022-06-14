import cv2
import numpy as np
import cv2 as cv
import os
import sys
import argparse
from scipy import stats


def get_args():
    parser = argparse.ArgumentParser(description='check the properties of stereo video.')
    parser.add_argument('--file', dest='file', type=str, required=True)
    args = parser.parse_args()
    return args

def rmBlackBolder(frame: cv2.Mat):
    h, w, _ = frame.shape
    ret, biimg = cv2.threshold(frame, 10, 255, cv2.THRESH_BINARY)
    biimg = cv2.cvtColor(biimg, cv2.COLOR_BGR2GRAY)

    # left and up
    edges_x = []
    edges_y = []
    for i in range(h // 2):
        for j in range(w // 2 - 1):
            if j == 0:
                if biimg[i][j] > 0 and biimg[i][j+1] > 0:
                    edges_x.append(j)
                    break
            else:
                if biimg[i][j] == 0 and biimg[i][j+1] > 0:
                    edges_x.append(j + 1)
                    break
    left_edge = stats.mode(edges_x)[0][0]

    for i in range(left_edge, w // 2):
        for j in range(h // 2 - 1):
            if j == 0:
                if biimg[j][i] > 0 and biimg[j+1][i] > 0:
                    edges_y.append(j)
                    break
            else:
                if biimg[j][i] == 0 and biimg[j+1][i] > 0:
                    edges_y.append(j + 1)
                    break
    up_edge = stats.mode(edges_y)[0][0]
    
    # right and bottom
    edges_x = []
    edges_y = []
    for i in range(h - 1, h // 2, -1):
        for j in range(w - 1, w // 2 + 1, -1):
            if j == w - 1:
                if biimg[i][j] > 0 and biimg[i][j-1] > 0:
                    edges_x.append(j+1)
                    break
            else:
                if biimg[i][j] == 0 and biimg[i][j-1] > 0:
                    edges_x.append(j)
                    break
    right_edge = stats.mode(edges_x)[0][0]

    for i in range(right_edge - 1, w // 2 - 1, -1):
        for j in range(h - 1, h // 2 - 1, -1):
            if j == h - 1:
                if biimg[j][i] > 0 and biimg[j-1][i] > 0:
                    edges_y.append(j+1)
                    break
            else:
                if biimg[j][i] == 0 and biimg[j-1][i] > 0:
                    edges_y.append(j)
                    break
    down_edge = stats.mode(edges_y)[0][0]

    return [up_edge, down_edge, left_edge, right_edge]
 
    

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
    
    # Run first time
    ret, frame = cap.read() # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        exit()
    ret, frame = cap.read()
    h, w, _= frame.shape
    left_img = frame[:, :w // 2, :]
    right_img = frame[:, w // 2:, :]
    left_edges = rmBlackBolder(left_img)
    right_edges = rmBlackBolder(right_img)
    left_leftpoint = [left_edges[2], left_edges[0]]
    left_imgsize = [left_edges[3] - left_edges[2], left_edges[1] - left_edges[0]]
    right_leftpoint = [right_edges[2] + w // 2, right_edges[0]]
    right_imgsize = [right_edges[3] - right_edges[2], right_edges[1] - right_edges[0]]

    print('------------------------------------')
    print('Stereo Video Abs Path: {}'.format(stereo_video_pth))
    print('Frame Count: {:d}'.format(int(frame_count // 2)))
    print('FPS: {:d}'.format(int(frame_fps)))
    print('Frame Size (W x H): [{}, {}]'.format(frame.shape[1], frame.shape[0]))
    print('Opencv Rect Format: leftpoint(x, y), imgsize(w, h)')
    print('Left Rect: leftpoint{}, imgsize{}'.format(left_leftpoint, left_imgsize))
    print('Right Rect: leftpoint{}, imgsize{}'.format(right_leftpoint, right_imgsize))
    print('------------------------------------')
    
    count = 1

    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret != True:
            break
        count += 1
        
        h, w, _ = frame.shape
        left_img = frame[:, :w // 2, :]
        right_img = frame[:, w // 2:, :]
        
        left_edges = rmBlackBolder(left_img)
        right_edges = rmBlackBolder(right_img)

        left_leftpoint_tmp = [left_edges[2], left_edges[0]]
        left_imgsize_tmp = [left_edges[3] - left_edges[2], left_edges[1] - left_edges[0]]
        right_leftpoint_tmp = [right_edges[2] + w // 2, right_edges[0]]
        right_imgsize_tmp = [right_edges[3] - right_edges[2], right_edges[1] - right_edges[0]]

        if (left_leftpoint != left_leftpoint_tmp or left_imgsize != left_imgsize_tmp or 
            right_leftpoint != right_leftpoint_tmp or right_imgsize != right_imgsize_tmp):
            print('LEFT: leftpoint{}, imgsize{}\t RIGHT: leftpoint{}, imgsize{}'.format(left_leftpoint_tmp,
                left_imgsize_tmp, right_leftpoint_tmp, right_imgsize_tmp))


        # left_non_edge_img = left_img[left_edges[0]:left_edges[1], left_edges[2]:left_edges[3], :]
        # right_non_edge_img = right_img[right_edges[0]:right_edges[1], right_edges[2]:right_edges[3], :]

        # cv2.imshow('stereo', frame)
        # cv2.imshow('left', left_img)
        # cv2.imshow('right', right_img)
        # cv2.imshow('left_non_edge', left_non_edge_img)
        # cv2.imshow('right_non_edge', right_non_edge_img)
        # cv2.waitKey(1) 
    cap.release()





    
    




