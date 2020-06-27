import cv2
import numpy as np
import tkinter as tk
import pytesseract
from pytesseract import Output
from tkinter import filedialog
from PIL import ImageTk, Image

img = np.array([0], dtype = np.uint8)
cropped = np.array([0], dtype = np.uint8)
display = np.array([0], dtype = np.uint8)
clicks = np.zeros(shape = (4, 2), dtype = np.float32)
index = 0

def openImage():
    global img

    img_name = filedialog.askopenfilename(initialdir = '/Users/riyaj/Desktop', title = 'Select Image', filetypes = (('JPG', '*.jpg'), ('All files', '*.*')))
    img = cv2.imread(img_name)

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image', img)

def autoCrop():

    global img
    ratio = img.shape[1]/img.shape[0]
    height = int(1100/ratio)
    NewImage = cv2.resize(img,(1100,height))

    img_gray = cv2.cvtColor(NewImage,cv2.COLOR_BGR2GRAY)
    adaptive = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,55,3)
    canny = cv2.Canny(adaptive,150,250)

    contours, hierarchy = cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    area = [cv2.contourArea(x) for x in contours]
    maximumIndex = np.argmax(area)
    maximumContour = contours[maximumIndex]
    perimeter = cv2.arcLength(maximumContour,True)
    ROI = cv2.approxPolyDP(maximumContour,0.01*perimeter,True)


    if len(ROI) == 4:

        
        lst = [ROI[1],ROI[0],ROI[2],ROI[3]]
        pt1 = np.array(lst,np.float32)
        pt2 = np.array ([(0, 0), (1500, 0), (0, 2000), (1500, 2000)], dtype = np.float32)

        perspective = cv2.getPerspectiveTransform(pt1,pt2)
        transformed = cv2.warpPerspective(NewImage, perspective, (1500,2000)) 

    global display
    display = transformed
    displayImage()

def manualCrop():
    textFound = ' To crop the image click the corners in this manner : \n 1. top left \n 2. top right \n 3. bottom left \n 4. bottom right'
    text.insert('1.0', textFound)
    cv2.setMouseCallback('image', onClick)


def onClick(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global index
        global clicks
        global img

        if (index < 4):
            clicks[index] = [x, y]
            index += 1
            imgCopy = np.copy (img)
            cv2.circle(imgCopy, (x, y), 30, (0, 255, 0), -1)
            cv2.imshow('image', imgCopy)

            if np.all (clicks):
                warpImage ()
        else:
            pass


def warpImage ():
    global clicks
    global img
    global cropped

    warpedPoints = np.array ([(0, 0), (1500, 0), (0, 2000), (1500, 2000)], dtype = np.float32)

    perspective = cv2.getPerspectiveTransform (clicks, warpedPoints)
    warped = cv2.warpPerspective(img, perspective, (1500, 2000))

    global display
    display = warped
    displayImage()
    cropped = warped


def getText ():
    global cropped
    global img
    global text

    if cropped.size > 1:
        croppedGrey = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    else:
        croppedGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold (croppedGrey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 201, 35)
    textFound = pytesseract.image_to_string(img, lang = 'eng')
    text.delete ('1.0', tk.END)
    text.insert ('1.0', textFound)

    global display
    display = thresh
    displayImage()


def showText ():
    global cropped

    croppedGrey = cv2.cvtColor (cropped, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold (croppedGrey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 201, 35)
    data = pytesseract.image_to_data (thresh, output_type = Output.DICT)
    numberWord = len (data['text'])

    for i in range (numberWord):
        x, y, width, height = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        cv2.rectangle (cropped, (x, y), (x+width, y+height), (255, 0, 0), 1)

    global display
    display = cropped
    displayImage()


def displayImage():
    global display

    
    cv2.namedWindow ('image modified', cv2.WINDOW_NORMAL)
    cv2.imshow ('image modified', display)


def saveImage ():
    global display
    filename = ''
    filename = filedialog.asksaveasfilename (initialdir = '/Users/riyaj', title = 'Save File', filetypes = (('JPG', '*.jpg'), ('All files','*.*')))
    print (filename)

    if filename != '':
        cv2.imwrite (filename, display)

def blurImage():
    global img
    
    blurred = cv2.GaussianBlur(img,(13,13),cv2.BORDER_DEFAULT)

    global display
    display = blurred
    displayImage()


def closeAllWindows():
    cv2.destroyAllWindows()


root = tk.Tk ()

canvas = tk.Canvas(root, height = 1000, width = 1000, bg = 'purple')
canvas.pack()

centerFrame = tk.Frame(canvas, bg = 'white')
centerFrame.place (relx = 0.5, rely = 0.05, relwidth = 0.6, relheight = 0.9, anchor = 'n')

title = tk.Label(centerFrame, text = 'Detected Text', fg='darkblue' ,bg ='white' ,font = ('Arial', '30'))
title.place(relx = 0.5, rely = 0.25, anchor = 'n')

text = tk.Text(centerFrame, bg = 'PowderBlue')
text.place(relx = 0.5, rely = 0.4, relwidth = 0.75, relheight = 0.5, anchor = 'n')

openImage = tk.Button(canvas, text = 'Open Image', padx = 10, pady = 10, command = openImage)
openImage.place (relx = 0.1, rely = 0.05, anchor = 'n')

autoCrop = tk.Button (canvas, text = 'Auto Crop', padx = 10, pady = 10, command = autoCrop)
autoCrop.place (relx = 0.1, rely = 0.3, anchor = 'n')

manualCrop = tk.Button (canvas, text = 'Manual Crop', padx = 10, pady = 10, command = manualCrop)
manualCrop.place (relx = 0.1, rely = 0.6, anchor = 'n')

saveImage = tk.Button (canvas, text = 'Save Image', padx = 10, pady = 10, command = saveImage)
saveImage.place (relx = 0.1, rely = 0.9, anchor = 'n')

getText = tk.Button (canvas, text = 'Detect Text', padx = 10, pady = 10, command = getText)
getText.place (relx = 0.9, rely = 0.05, anchor = 'n')

showText = tk.Button (canvas, text = 'Show Text', padx = 10, pady = 10, command = showText)
showText.place (relx = 0.9, rely = 0.3, anchor = 'n')

blur = tk.Button (canvas, text = 'Blur image', padx = 10, pady = 10, command = blurImage)
blur.place (relx = 0.9, rely = 0.6, anchor = 'n')

closeWindows = tk.Button (canvas, text = 'Close All Windows', padx = 10, pady = 10, command = closeAllWindows)
closeWindows.place (relx = 0.9, rely = 0.9, anchor = 'n')

root.mainloop ()