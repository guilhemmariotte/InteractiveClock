#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 03:44:26 2019

author: Guilhem Mariotte

---

This script requires opencv, numpy, tkinter 8.6, PIL (Pillow), graphics

The OpenCV library must be already installed on your computer (see README)

Use a virtual environment to bundle your app using PyInstaller (see README)

"""

import os
import sys
from PIL import Image as Img
from graphics import *
import tkinter
import numpy
import cv2


# Define the correct path for data when bundling the app
#------------------------------------------------------------------------------
def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Main
#------------------------------------------------------------------------------
def launch_clock():
    root = tkinter.Tk()
    winwidth = root.winfo_screenwidth()
    winheight = root.winfo_screenheight()
    root.quit()
    root.destroy()
    
    win = GraphWin("InteractiveClock", winwidth, winheight)
    win.master.attributes("-fullscreen", True)
    
    win.setBackground("black")
    #win.setBackground(color_rgb(53,53,53))
    winwidth2 = 1000
    winscale = winwidth2/winwidth
    winheight2 = winheight*winscale
    win.setCoords(0,0,winwidth2,winheight2)
    x0 = winwidth2/2
    y0 = winheight2/2
    
    # Load original images and save resized images (adapted for the screen resolution)
    img_temp = Img.open(resource_path('clock2.png'))
    imgscale = 0.9*winwidth/img_temp.size[0]
    w_temp = int(imgscale*img_temp.size[0])
    h_temp = int(imgscale*img_temp.size[1])
    img_temp = img_temp.resize((w_temp, h_temp), Img.ANTIALIAS)
    img_temp.save('temp_clock.png')
    
    img_temp = Img.open(resource_path('clock_block3_none.png'))
    w_temp = int(imgscale*img_temp.size[0])
    h_temp = int(imgscale*img_temp.size[1])
    img_temp = img_temp.resize((w_temp, h_temp), Img.ANTIALIAS)
    img_temp.save('temp_clock_block_none.png')
    
    img_temp = Img.open(resource_path('clock_block3_bu.png'))
    w_temp = int(imgscale*img_temp.size[0])
    h_temp = int(imgscale*img_temp.size[1])
    img_temp = img_temp.resize((w_temp, h_temp), Img.ANTIALIAS)
    img_temp.save('temp_clock_block_bu.png')
    
    img_temp = Img.open(resource_path('clock_block3_ke.png'))
    w_temp = int(imgscale*img_temp.size[0])
    h_temp = int(imgscale*img_temp.size[1])
    img_temp = img_temp.resize((w_temp, h_temp), Img.ANTIALIAS)
    img_temp.save('temp_clock_block_ke.png')
    
    img_temp = Img.open(resource_path('clock_block3_jian.png'))
    w_temp = int(imgscale*img_temp.size[0])
    h_temp = int(imgscale*img_temp.size[1])
    img_temp = img_temp.resize((w_temp, h_temp), Img.ANTIALIAS)
    img_temp.save('temp_clock_block_jian.png')
    
    # Load resized images
    # Load and place the clock background
    img_clock = Image(Point(x0,y0),resource_path('temp_clock.png'))
    w_clock = img_clock.getWidth()
    w_clock = w_clock*winscale
    h_clock = img_clock.getHeight()
    h_clock = h_clock*winscale
    
    # Load and place the clock blocks
    xblock = [-753,-283,288,757]
    yblock = [3,3,3,3]
    xblock = [winscale*imgscale*x for x in xblock]
    yblock = [winscale*imgscale*x for x in yblock]
    
    img_none1 = Image(Point(x0+xblock[0],y0+yblock[0]),resource_path('temp_clock_block_none.png'))
    h_block = img_none1.getHeight()
    h_block = h_block*winscale
    #print('image height: {res}'.format(res=h_block))
    img_none2 = Image(Point(x0+xblock[1],y0+yblock[1]),resource_path('temp_clock_block_none.png'))
    img_none3 = Image(Point(x0+xblock[2],y0+yblock[2]),resource_path('temp_clock_block_none.png'))
    img_none4 = Image(Point(x0+xblock[3],y0+yblock[3]),resource_path('temp_clock_block_none.png'))
    
    img_bu1 = Image(Point(x0+xblock[0],y0+yblock[0]+h_block),resource_path('temp_clock_block_bu.png'))
    img_ke2 = Image(Point(x0+xblock[1],y0+yblock[1]+h_block),resource_path('temp_clock_block_ke.png'))
    img_bu3 = Image(Point(x0+xblock[2],y0+yblock[2]+h_block),resource_path('temp_clock_block_bu.png'))
    img_jian4 = Image(Point(x0+xblock[3],y0+yblock[3]+h_block),resource_path('temp_clock_block_jian.png'))
    
    rect_top = Rectangle(Point(0,winheight2), Point(winwidth2,winheight2/2+h_block/2))
    rect_top.setFill("black")
    rect_bottom = Rectangle(Point(0,0), Point(winwidth2,winheight2/2-h_block/2))
    rect_bottom.setFill("black")
    
    # Draw all elements
    img_none1.draw(win)
    img_none2.draw(win)
    img_none3.draw(win)
    img_none4.draw(win)
    img_bu1.draw(win)
    img_ke2.draw(win)
    img_bu3.draw(win)
    img_jian4.draw(win)
    rect_top.draw(win)
    rect_bottom.draw(win)
    img_clock.draw(win)
    
    # LBP classifier
    classifier = cv2.CascadeClassifier(resource_path('lbpcascade_frontalface.xml'))
    # Access the webcam device
    video_cap = cv2.VideoCapture(0)
    
    # Elapsed time between clock changes [s]
    elapsedtime = 7
    
    while True:
        numfaces = countfaces(video_cap,classifier)
        
        if numfaces > 1:
            # if at least 2 persons are detected by the webcam
            # Successively show [X X : X jian], [X ke : X jian], [bu ke : bu jian], [X ke : bu jian], [X X : X X]
            numfaces = 0
            showblock(img_jian4,img_none4,h_block,winheight2)
            numfaces = countfacestime(video_cap,classifier,elapsedtime)
            
            showblock(img_ke2,img_none2,h_block,winheight2)
            numfaces = countfacestime(video_cap,classifier,elapsedtime)
            
            showblock(img_bu1,img_none1,h_block,winheight2)
            showblock(img_bu3,img_none3,h_block,winheight2)
            numfaces = countfacestime(video_cap,classifier,elapsedtime)
            
            hideblock(img_bu1,img_none1,h_block,winheight2)
            numfaces = countfacestime(video_cap,classifier,elapsedtime)
            
            hideblock(img_bu3,img_none3,h_block,winheight2)
            hideblock(img_ke2,img_none2,h_block,winheight2)
            hideblock(img_jian4,img_none4,h_block,winheight2)
            numfaces = countfacestime(video_cap,classifier,elapsedtime)
            
        elif numfaces > 0:
            # if at least one person is detected by the webcam
            # Successively show [X X : X jian], [X ke : X jian], [X X : X X]
            numfaces = 0
            showblock(img_jian4,img_none4,h_block,winheight2)
            numfaces = countfacestime(video_cap,classifier,elapsedtime)
            
            showblock(img_ke2,img_none2,h_block,winheight2)
            numfaces = countfacestime(video_cap,classifier,elapsedtime)
            
            hideblock(img_ke2,img_none2,h_block,winheight2)
            hideblock(img_jian4,img_none4,h_block,winheight2)
            numfaces = countfacestime(video_cap,classifier,elapsedtime)
            
        else:
            # if noboby is detected by the webcam:
            # Successively show [X X : bu jian], [bu ke : X jian], [X X : X X]
            numfaces = 0
            showblock(img_jian4,img_none4,h_block,winheight2)
            showblock(img_bu3,img_none3,h_block,winheight2)
            numfaces = countfacestime(video_cap,classifier,elapsedtime)
            
            hideblock(img_bu3,img_none3,h_block,winheight2)
            showblock(img_ke2,img_none2,h_block,winheight2)
            showblock(img_bu1,img_none1,h_block,winheight2)
            numfaces = countfacestime(video_cap,classifier,elapsedtime)
            
            hideblock(img_bu1,img_none1,h_block,winheight2)
            hideblock(img_ke2,img_none2,h_block,winheight2)
            hideblock(img_jian4,img_none4,h_block,winheight2)
            numfaces = countfacestime(video_cap,classifier,elapsedtime)
            
        if win.checkKey() != '':
            # exit when a key is pressed
            break

    #win.getMouse() # pause for click in window
    video_cap.release()
    win.close()
    win.master.destroy()
    

# Return the number of faces (people) detected by the webcam
#------------------------------------------------------------------------------
def countfaces(cam,classifier):
    ret, frame_color = cam.read()
    frame_gray = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY)
    frame_faces = classifier.detectMultiScale(frame_gray, 1.3, 5)
    return len(frame_faces)

# Return the number of faces (people) detected by the webcam during a given elapsed time
#------------------------------------------------------------------------------
def countfacestime(cam,classifier,elapsedtime):
    numfaces = 0
    t0 = time.process_time()
    while time.process_time() - t0 < elapsedtime:
        ret, frame_color = cam.read()
        frame_gray = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY)
        frame_faces = classifier.detectMultiScale(frame_gray, 1.3, 5)
        if len(frame_faces) > 0:
            numfaces = len(frame_faces)
    return numfaces

# Show an image block (mimic a clock change, the block seems to roll down from the top)
#------------------------------------------------------------------------------
def showblock(img,img_n,hb,hw):
    movespeed = 0.5 # time to move the block, s
    framerate = 30 # window update, fps
    numframes = int(movespeed*framerate)
    
    pt_img = img.getAnchor()
    if pt_img.getY() < hw/2:
        img.move(0,2*hb)
    
    for i in range(numframes):
        img_n.move(0,-hb/numframes)
        img.move(0,-hb/numframes)
        update(framerate)
    
# Hide an image block (mimic a clock change, the block seems to roll down to the bottom)
#------------------------------------------------------------------------------
def hideblock(img,img_n,hb,hw):
    movespeed = 0.5 # time to move the block, s
    framerate = 30 # window update, fps
    numframes = int(movespeed*framerate)
        
    pt_img_n = img_n.getAnchor()
    if pt_img_n.getY() < hw/2:
        img_n.move(0,2*hb)
    
    for i in range(numframes):
        img_n.move(0,-hb/numframes)
        img.move(0,-hb/numframes)
        update(framerate)

# Launch the main
launch_clock()
