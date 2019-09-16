For labelling image software :
1. Install Tkinter on the system.
   Activate virtualenv
2. git clone https://github.com/tzutalin/labelImg.git
3. cd labelImg
4. sudo apt-get install pyqt5-dev-tools
5. pip install -r requirements/requirements-linux-python3.txt
6. make qt5py3
7. python labelImg.py

	NOTE : Use PascalVOC format only.
8. Open input folder for image fetching in software.
9. Choose Save dir as XMLs.
10. May use https://github.com/ssaru/convert2Yolo.git for annotation type conversion.

. python augmentationPy.py

	NOTE:  Total images = size input x number of angles x number of images per angle

	example:		Enter number of images for angle : 5
					Input angle with spaces : 0 30 60 90

. Alter filter_addition() in augmentationPy.py for image filters.