import cv2
import pytesseract
from PIL import ImageEnhance,Image as Img
import re
import sys


def get_contours(image_final,intensity = 1): # finding curves joining continuous points along the boundaries
    if intensity:
        ret, new_img = cv2.threshold(image_final, 230 , 255, cv2.THRESH_BINARY)  # if text is white
    else:
        ret, new_img = cv2.threshold(image_final, 230 , 255, cv2.THRESH_BINARY_INV)  # if text is black
    
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(4 , 2)) # in order to manipulate the orientation
    dilated = cv2.dilate(new_img,kernel,iterations = 9)
    im2, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    return contours
    
def extract_text(contours):  # extracting the text from the sections of image obtained from get_contours
    x1,y1 = 10,30  # position of the text to be displayed as result
    out = []
    for i in range(len(contours)):
            cnt = contours[i]
            n,p,e = [],[],[] # stores the text and location of name, position and email address
            x,y,w,h = cv2.boundingRect(cnt)
            if x<9: x= x+9
            if y<9: y = y+9
            check_im = 'check_im.jpg'
            cv2.imwrite(check_im,im[y-9:y+h,x-9:x+w]) # cropped section obtained from contours
            try: # using tesseract for scene to text recognition
                check_im = Img.open(check_im)
                enhancer = ImageEnhance.Contrast(check_im)
                imc = enhancer.enhance(2)
                imc = imc.convert('1')
                text = pytesseract.image_to_string(imc)
                #print text
                #print "----"
                out = draw_bbox(text,[x,y,w,h],x1,y1) # drawing bbox for the required section
                y1 = y1+30 # position of next text 
            except: #(IOError,IndexError):
                pass
    return out

def draw_bbox(text,rect,x1,y1): # to draw bounding box across the required section.
    [x,y,w,h] = rect
    font = cv2.FONT_HERSHEY_SIMPLEX
    namePattern = re.compile("^[a-zA-Z ]*$") # regular expression for names
    newlinepattern = re.compile('\s*[,\n]\s*')
    phonePattern = re.compile(r''' # regular expression for phone numbers
                    # don't match beginning of string, number can start anywhere
        (\d{3})     # area code is 3 digits (e.g. '800')
        \D*         # optional separator is any number of non-digits
        (\d{3})     # trunk is 3 digits (e.g. '555')
        \D*         # optional separator
        (\d{4})     # rest of number is 4 digits (e.g. '1212')
        \D*         # optional separator
        (\d*)       # extension is optional and can be any number of digits
        $           # end of string
        ''', re.VERBOSE)
    emailPattern = re.compile("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-+ ]+.[a-zA-Z]{2,6}$") # regular expression for email ids
    if len(text)>8 and text != '' and not(newlinepattern.search(text)):
        if namePattern.search(text):
            out = cv2.rectangle(im,(x-9,y-9),(x+w,y+h),(0,0,255),2)
            out = cv2.putText(out,text,(x1,y1), font, 1,(0,0,255),2)
            
        if phonePattern.search(text):
            out = cv2.rectangle(im,(x-9,y-9),(x+w,y+h),(0,0,255),2)
            out = cv2.putText(out,text,(x1,y1), font, 1,(0,0,255),2)

        if emailPattern.search(text):
            out = cv2.rectangle(im,(x-9,y-9),(x+w,y+h),(0,0,255),2)
            out = cv2.putText(out,text,(x1,y1), font, 1,(0,0,255),2)
    return out

if __name__ == '__main__':
    myimage = sys.argv[1]
    myout = sys.argv[2]
    im  = cv2.imread(myimage)
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
    image_final = cv2.bitwise_and(gray , gray , mask =  mask)
    c1 = get_contours(image_final)
    c2 = get_contours(image_final,0)
    contours = c1+c2
    out = extract_text(contours)
    cv2.imshow(myout,out)
