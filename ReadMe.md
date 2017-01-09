#Text Recognition in Business Cards

This python application deals with the problems of word spotting recognition in business cards. The goal is to find three distinct strings - Name, Phone number and E-mail address. 

Tools used
----------
[OpenCV 3.1](https://opencv-python-tutroals.readthedocs.io/en/latest/)

[pytesseract](https://pypi.python.org/pypi/pytesseract/0.1)

Installation
------------
* Python-tesseract is an optical character recognition (OCR) tool for python by [google](http://code.google.com/p/tesseract-ocr/). In order to install the same, go through the documentation [here](https://github.com/tesseract-ocr/tesseract)
* Python-tesseract requires python 2.5 or later or python 3
* You will need the Python Imaging Library (PIL) as well
* Also make sure to add `tessdata` to environment variable and overwrite `tesseract_cmd` variable in python to the install path. For example `pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract`

Code Usage
----------
python buss_text.py *path_to_test_image* *path_to_output*

example: 

python buss_text.py D:\Project\001.jpg D:\Project\result_001.jpg
