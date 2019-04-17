#######################
#### REQUERIMIENTOS ###
#######################

apt-get update && \
        apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libavformat-dev \
        libpq-dev \
        python3-dev
        nginx \
  

pip install virtualenv virtualenvwrapper
sudo rm -rf ~/get-pip.py ~/.cache/pip

#ojo donde definimos $HOME porque va a ser donde reside .virtualenvs#
echo -e "\n# virtualenv and virtualenvwrapper" >> ~/.bashrc
en el caso de analisis-imagenes 
echo "export WORKON_HOME=/home/image-matcher/imageMatcher/backend/.virtualenvs" >> ~/.bashrc

echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
o bien : echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python" >> ~/.bashrc 
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc

#creamos el virtualenv imageMatcher
mkvirtualenv imageMatcher -p python3
#nos metemos en el virtualenv imageMatcher
workon imageMatcher

##Esto va dentro del virtualenv imageMatcher

pip install opencv-python==3.3.0.10
pip install opencv-contrib-python==3.3.0.10
pip install numpy 
pip install flask 
pip install flask_restful 
pip install flask_cors 
pip install matplotlib 
pip install pymongo 
pip install tensorflow==2.0.0-alpha0 
pip install Keras-Applications
pip install pillow
pip install uwsgi


#Si faltara instalar algo con pip, siempre iniciar el virtualenv con 
workon imageMatcher



######################################
## CONFIGURACION DE NGINX CON FLASK ##
######################################
Ya está instalado nginx en realidad pero ver como referencia https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04

nginx usa www-data como usuario, 
asi que es conveniente que el código tenga,
como owner al grupo www-data

#Ver si está corriendo, pararlo, iniciarlo o recargarlo:
systemctl status nginx
systemctl stop nginx
systemctl start nginx
systemctl restart nginx 





##############################
### INSTALAR OPENCV 3 EN PYTHON CON UBUNTU
### https://www.pyimagesearch.com/2018/05/28/ubuntu-18-04-how-to-install-opencv/
##############################

documentacion:
sudo apt install python-opencv python-pip install python-tk

$ python3 --version

$ sudo apt-get update
$ sudo apt-get upgrade

### installing developer tools:
	
$ sudo apt-get install build-essential cmake unzip pkg-config libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libatlas-base-dev gfortran

### And finally, our last requirement is to install Python 3 headers and libraries:
$ sudo apt-get install python3-dev

### Update 2018-12-20: These instructions have been updated to work with OpenCV 3.4.4. These  instructions should continue to work with future OpenCV 3.x versions as well.
$ cd ~
$ wget -O opencv.zip https://github.com/opencv/opencv/archive/3.4.4.zip

### Followed by the opencv_contrib  module:
$ wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.4.4.zip

$ unzip opencv.zip
$ unzip opencv_contrib.zip

$ mv opencv-3.4.4 opencv
$ mv opencv_contrib-3.4.4 opencv_contrib

### To install pip, simply enter the following in your terminal:
$ wget https://bootstrap.pypa.io/get-pip.py
$ sudo python3 get-pip.py

### Let’s go ahead and install   virtualenv  and virtualenvwrapper  now:
$ sudo pip install virtualenv virtualenvwrapper
$ sudo rm -rf ~/get-pip.py ~/.cache/pip

### Using a terminal text editor such as vi / vim  or nano , add the following lines to your ~/.bashrc :
# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
ó bien: export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python
source /usr/local/bin/virtualenvwrapper.sh

### Alternatively, you can append the lines directly via bash commands:
$ echo -e "\n# virtualenv and virtualenvwrapper" >> ~/.bashrc
$ echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
$ echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
$ echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc

### Next, source the ~/.bashrc  file:
$ source ~/.bashrc

### Creating a virtual environment to hold OpenCV and additional packages
$ mkvirtualenv cv -p python3

### Let’s verify that we’re in the cv environment by using the workon command:
$ workon cv

### Install NumPy in your environment
$ pip install numpy

### Para instalar opencv únicamente
pip install opencv-python==3.3.0.10

### Para agregar el paquete contrib
pip install opencv-contrib-python==3.3.0.10

### Before we begin though, let’s ensure that we’re in the cv virtual environment:
$ workon cv

### Configure OpenCV with CMake
### Let’s set up our OpenCV build using cmake :
$ cd ~/opencv
$ mkdir build
$ cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE -D BUILD_PYTHON_SUPPORT=ON -D INSTALL_PYTHON_EXAMPLES=ON -D WITH_XINE=ON -D WITH_OPENGL=ON -D INSTALL_C_EXAMPLES=OFF -D WITH_TBB=ON -D BUILD_EXAMPLES=ON -D BUILD_NEW_PYTHON_SUPPORT=ON -D OPENCV_ENABLE_NONFREE=ON -D WITH_V4L=ON -D CMAKE_INSTALL_PREFIX=/usr/local -D OPENCV_EXTRA_MODULES_PATH= /home/mich/workspace/opencv3.4/opencv_contrib/modules -D PYTHON_EXECUTABLE=~/.virtualenvs/cv/bin/python -D ENABLE_PRECOMPILED_HEADERS=OFF  ..

make -j4

### Upon a successful, 100% complete compile you can now install OpenCV:
$ sudo make install
$ sudo ldconfig

### To verify the install, sometimes I like to enter the following command in the terminal:
$ pkg-config --modversion opencv

### At this point, your Python 3 bindings for OpenCV should reside in the following folder:
$ ls /usr/local/python/cv2/python-3.6
cv2.cpython-36m-x86_64-linux-gnu.so

### Let’s rename them to simply cv2.so :
$ cd /usr/local/python/cv2/python-3.6
$ sudo mv cv2.cpython-36m-x86_64-linux-gnu.so cv2.so


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
'3.4.4' __### tengo la '4.0.0'__
quit()

### Install matplotlib. We use pip (while the cv  Python virtual environment is active):
pip install matplotlib