# InteractiveClock
Python app that displays a modified digital clock in full screen, interacting with viewers detected by a webcam. Preferably to be run on an iMac. Designed for the art exhibition of [Xiaojun Song](http://xiaojunsong.net) at the [United Art Museum](http://www.whuam.com/#/show/detail?id=2cb86e56-83b0-47b6-8159-2d260147ee34), Wuhan, China.

Install the OpenCV library on your Mac
--------------------------------------
Go to the [OpenCV website](https://opencv.org/) for more information about the library

Requires Xcode

From the terminal: USERNAME$

Install Homebrew:  
`> sudo xcode-select --install`  
`> ruby -e "$(curl -fsSL 	https://raw.githubusercontent.com/Homebrew/install/master/install)"`

Check update:  
`> brew update`

Put the following lines in a .bash_profile file at the root USERNAME$:  
`# Homebrew`  
`export PATH=/usr/local/bin:$PATH`

Link the bash_profile:  
`> source ~/.bash_profile`

Install OpenCV:  
`> brew tap homebrew/core`  
`> brew install opencv3 --with-contrib --with-python3`

Link the cv2 library with Python3:  
`> echo 'import sys; sys.path.insert(1, "/usr/local/lib/python3.7/site-packages")' >> /Users/USERNAME/Anaconda3/lib/python3.7/site-packages/homebrew.pth`

Bundle the app with PyInstaller
-------------------------------
Set the right path for python (e.g. Python3 from Anaconda here):  
`(BASH) export PATH=/Users/USERNAME/anaconda3/bin:$PATH`

Create a virtual environment:  
`(BASH) python3 -m venv myvenv3`

Load your environment:  
`(BASH) source myvenv3/bin/activate`

Check the python path (should give the path of your venv):  
`(BASH-myvenv) which python3`  
`(BASH-myvenv) echo $PATH`

Install the required modules in your venv:  
`(BASH-myvenv) pip install numpy`  
`(BASH-myvenv) pip install pyinstaller`  
`(BASH-myvenv) pip install Pillow`  
`(BASH-myvenv) pip install opencv-python` 

numpy is already included in the system python, but installing it in the venv prevents broken module imports.  
tkinter 8.6 can be directly imported from /Users/USERNAME/anaconda3/lib, check the module path with:  
`(BASH-myvenv) python3`  
`>>>> import tkinter`  
`>>>> print(tkinter)`  
`>>>> print(tkinter.TkVersion) # check tk version, should be > 8.6`

Bundle your app with pyinstaller (this will create the spec file):  
`(BASH-myvenv) pyinstaller interactiveclock.py`

Add data and binary files in the spec file.  
The OpenCV binaries can be found in /usr/local/Cellar/opencv/4.0.1/lib/, copy all of them and put them in a bin/ folder in your working directory.  
The script also requires the lbpcascade_frontalface.xml file which can be found in /usr/local/Cellar/opencv/4.0.1/share/opencv4/lbpcascades, and the PNG images designed for the app.  
Update the following lines in the spec file:  
`binaries=[('/Users/USERNAME/interactiveclock/bin/*.dylib','.')],`  
`datas=[('/Users/USERNAME/interactiveclock/*.png','.'),('/Users/USERNAME/interactiveclock/*.xml','.')],`

Bundle the app again with the spec file (to get one .app file, but seems to be equivalent as the onedir option...):  
`(BASH-myvenv) pyinstaller --onefile --windowed interactiveclock.spec`
