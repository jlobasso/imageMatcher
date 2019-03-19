documentacion:
sudo apt install python-opencv
sudo apt install python-pip
pip install matplotlib
sudo apt-get install python-tk

sudo apt-get install python3-matplotlib

##############################
### INSTALAR OPENCV 3 EN PYTHON CON UBUNTU
### https://www.pyimagesearch.com/2018/05/28/ubuntu-18-04-how-to-install-opencv/
##############################


$ python3 --version

$ sudo apt-get update
$ sudo apt-get upgrade

### installing developer tools:
	
$ sudo apt-get install build-essential cmake unzip pkg-config

### You most likely already have pkg-config  installed on Ubuntu 18.04, but be sure to include it in the install command for sanity.

### Next, we need to install some OpenCV-specific prerequisites. OpenCV is an image processing/computer vision library and therefore it needs to be able to load standard image file formats such as JPEG, PNG, TIFF, etc. The following image I/O packages will allow OpenCV to work with image files:

$  sudo apt-get install libjpeg-dev libpng-dev libtiff-dev

### Similarly, let’s include video I/O packages as we often work with video on the PyImageSearch blog. You’ll need the following packages so you can work with your camera stream and process video files:

$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
$ sudo apt-get install libxvidcore-dev libx264-dev

### OpenCV’s highgui module relies on the GTK library for GUI operations. The highgui module will allow you to create elementary GUIs which display images, handle kepresses/mouse clicks, and create sliders and trackbars. Advanced GUIs should be built with TK, Wx, or QT. See this blog post to learn how to make an OpenCV GUI with TK.

###Let’s install GTK:

$ sudo apt-get install libgtk-3-dev

### I always recommend the following two libraries which will optimize various OpenCV functions:

$ sudo apt-get install libatlas-base-dev gfortran

### And finally, our last requirement is to install Python 3 headers and libraries:

$ sudo apt-get install python3-dev

### Update 2018-12-20: These instructions have been updated to work with OpenCV 3.4.4. These  instructions should continue to work with future OpenCV 3.x versions as well.

### Since we’re continuing to work in the terminal, let’s download the official OpenCV ### release using wget :

$ cd ~
$ wget -O opencv.zip https://github.com/opencv/opencv/archive/3.4.4.zip

### Followed by the opencv_contrib  module:

$ wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.4.4.zip

### Note: If your browser is cutting off the full command either use the “<>” button in the toolbar above to expand the code block or copy and paste the following URL: https://github.com/opencv/opencv_contrib/archive/3.4.4.zip

### So, what’s the contrib repo?

### The contrib repository contains algorithms such as SIFT, SURF, and others. In the past, these implementations were included in the default installation of OpenCV 2.4; however, they were moved beginning with OpenCV 3+.

### Modules that are actively being developed and/or modules that are patented (not free for commercial/industry use) are included in the contrib module. SIFT and SURF fall into this category. You can learn more about the thought process behind this move in the following blog post: Where did SIFT and SURF go in OpenCV 3?

### Important: Both opencv  and opencv_contrib  versions must be identical. Notice that both URLs point to 3.4.4. Feel free to install a different version while still using this guide — just be sure to update both URLs.

### Now, let’s unzip the archives:

$ unzip opencv.zip
$ unzip opencv_contrib.zip

$ mv opencv-3.4.4 opencv
$ mv opencv_contrib-3.4.4 opencv_contrib

Configure your Python 3 environment
### The first step we’re taking to configure our Python 3 development environment is to install pip, a Python Package Manager.

### To install pip, simply enter the following in your terminal:

$ wget https://bootstrap.pypa.io/get-pip.py
$ sudo python3 get-pip.py

### Making use of virtual environments for Python development
### If you are familiar with my blog and install guides therein, the following statement might make me sound like a broken record but I’ll repeat it anyway:

### I use both virtualenv and virtualenvwrapper daily and you should too unless you have a very specific reason not to. These two Python packages facilitate creating independent Python environments for your projects.

### It is a best practice to use virtual environments.

### Why?

### Virtual environments allow you to work on your projects in isolation without spinning up resource hogs such as VMs and Docker images (I definitely do use both VirtualBox and Docker — they have their place).

### For example, maybe you have a Python + OpenCV project that requires an older version of scikit-learn (v0.14) but you want to keep using the latest version of scikit-learn (0.19) for all of your newer projects.

### Using virtual environments, you could handle these two software version dependencies separately, something that is not possible using just the system install of Python.

### If you would like more information about Python virtual environments take a look at this article on RealPython or read the first half of the this blog post on PyImageSearch.

### Let’s go ahead and install   virtualenv  and virtualenvwrapper  now:

$ sudo pip install virtualenv virtualenvwrapper
$ sudo rm -rf ~/get-pip.py ~/.cache/pip

### To finish the install we need to update our  ~/.bashrc  file.

### Using a terminal text editor such as vi / vim  or nano , add the following lines to your ~/.bashrc :

# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh

### Alternatively, you can append the lines directly via bash commands:

$ echo -e "\n# virtualenv and virtualenvwrapper" >> ~/.bashrc
$ echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
$ echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
$ echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc

### Next, source the ~/.bashrc  file:
$ source ~/.bashrc


### Creating a virtual environment to hold OpenCV and additional packages
### Ok, while that may have seemed like a lot of work, we’re at the point where we can create your Python 3 virtual environment for OpenCV:


$ mkvirtualenv cv -p python3

### This line simply creates a Python 3 virtual environment named cv . You can name your environment(s) whatever you’d like — I like to keep them short and sweet while also providing enough information so I’ll remember what they are for. You can have as many virtual environments on your system as you’d like!

### Let’s verify that we’re in the cv environment by using the workon command:

$ workon cv

### Install NumPy in your environment
### Let’s install our first package into the environment: NumPy. NumPy is a requirement for working with Python and OpenCV. We simply use pip (while the cv  Python virtual environment is active):

$ pip install numpy

### Puedes instalar opencv usando el paquete oficial pre-construido de los fuentes

### Para instalar opencv únicamente
pip install opencv-python
#numpy-1.16.2 opencv-python-4.0.0.21

### Para agregar el paquete contrib
pip install opencv-contrib-python
#numpy-1.16.2 opencv-contrib-python-4.0.0.21


### Step #4: Configure and compile OpenCV for Ubuntu 18.04
### Now we’re moving. We’re ready to compile and install OpenCV.

### Before we begin though, let’s ensure that we’re in the cv virtual environment:

$ workon cv

### It is very important that the virtual environment is active (you are “inside” the virtual environment) which is why I keep reiterating it. If you are not in the cv  Python virtual environment before moving on to the next step your build files will not be generated properly.

### Configure OpenCV with CMake
### Let’s set up our OpenCV build using cmake :


$ cd ~/opencv
$ mkdir build
$ cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE -D BUILD_PYTHON_SUPPORT=ON -D INSTALL_PYTHON_EXAMPLES=ON -D WITH_XINE=ON -D WITH_OPENGL=ON -D INSTALL_C_EXAMPLES=OFF -D WITH_TBB=ON -D BUILD_EXAMPLES=ON -D BUILD_NEW_PYTHON_SUPPORT=ON -D OPENCV_ENABLE_NONFREE=ON -D WITH_V4L=ON -D CMAKE_INSTALL_PREFIX=/usr/local -D OPENCV_EXTRA_MODULES_PATH= /home/mich/workspace/opencv3.4/opencv_contrib/ -D PYTHON_EXECUTABLE=~/.virtualenvs/cv/bin/python -D ENABLE_PRECOMPILED_HEADERS=OFF  ..

make -j4

### This process may take 30 minutes or longer, so go for a nice walk if you are able.

### If your compile chokes and hangs, it may be due to a threading race condition. In the event you run into this problem, simply delete your build  directory, recreate it, and re-run cmake  and make . This time do not include the flag next to make .

### Installing and verifying OpenCV
### Upon a successful, 100% complete compile you can now install OpenCV:

$ sudo make install
$ sudo ldconfig

### To verify the install, sometimes I like to enter the following command in the terminal:

$ pkg-config --modversion opencv
### 3.4.4

### Update 2018-12-20: The following paths have been updated. Previous versions of OpenCV installed the bindings in a different location ( /usr/local/lib/python3.6/site-packages ), so be sure to take a look at the paths below carefully.

### At this point, your Python 3 bindings for OpenCV should reside in the following folder:

$ ls /usr/local/python/cv2/python-3.6
cv2.cpython-36m-x86_64-linux-gnu.so

### Let’s rename them to simply cv2.so :

$ cd /usr/local/python/cv2/python-3.6
$ sudo mv cv2.cpython-36m-x86_64-linux-gnu.so cv2.so

### Pro-tip: If you are installing OpenCV 3 and OpenCV 4 alongside each other, instead of renaming the file to cv2.so, you might consider naming it cv2.opencv3.4.4.so  and then in the next sub-step sym-link appropriately from that file to cv2.so  as well.

### Our last sub-step is to sym-link our OpenCV cv2.so  bindings into our cv  virtual environment:

$ cd ~/.virtualenvs/cv/lib/python3.6/site-packages/
$ ln -s /usr/local/python/cv2/python-3.6/cv2.so cv2.so

### Verifica la instalación de opencv entrando a la terminal con
$ cd ~
$ workon cv
$ python
Python 3.6.5 (default, Apr 1 2018, 05:46:30)
[GCC 7.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
import cv2
cv2.__version__
'3.4.4'
quit()

### Install matplotlib. We use pip (while the cv  Python virtual environment is active):
pip install matplotlib