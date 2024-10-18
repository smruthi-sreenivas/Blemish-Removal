''' remove blemishes from skin images. when you click on the images, its gone.
1. Find the lowest gradient around the blemish patch.
2 Clone the new patch on top of this blemish patch.
You dont find any differences in the skin image. It should look seamless.
There should be no variations in texture and gradient'''

import cv2
import pandas as pd
import  numpy as np
import matplotlib.pyplot as plt

def selectedBlemish(x,y,r):
    #crop the blemish patch
    croppedImage = image[y:(y+2*r),x:(x+2*r)]
    return identifyBestPatch(x,y,r)

def identifyBestPatch(x,y,r):
    #go through all 8 directions to identify the new patch with lowest gradient
    patches = {}

    key1tup = appendDictionary(x+2*r,y)
    patches['Key1'] = (x+2*r,y,key1tup[0],key1tup[1])

    key2tup = appendDictionary(x + 2 * r, y+r)
    patches['Key2'] = (x + 2 * r, y+r, key2tup[0], key2tup[1])

    key3tup = appendDictionary(x - 2 * r, y)
    patches['Key3'] = (x - 2 * r, y, key3tup[0], key3tup[1])

    key4tup = appendDictionary(x - 2 * r, y - r)
    patches['Key4'] = (x - 2 * r, y-r, key4tup[0], key4tup[1])

    key5tup = appendDictionary(x , y+2*r)
    patches['Key5'] = (x , y+2*r, key5tup[0], key5tup[1])
    key6tup = appendDictionary(x + r, y+2*r)
    patches['Key6'] = (x + r, y+2*r, key6tup[0], key6tup[1])

    key7tup = appendDictionary(x, y-2*r)
    patches['Key7'] = (x, y-2*r, key7tup[0], key7tup[1])

    key8tup = appendDictionary(x - r, y-2*r)
    patches['Key8'] = (x - r, y-2*r, key8tup[0], key8tup[1])

    print(patches)
    findlowx = {}
    findlowy = {}

    for key,(x,y,gx,gy) in patches.items():
        findlowx[key] = gx
        findlowy[key] = gy

    print(findlowx)
    print(findlowy)

    y_key_min = min(findlowy.keys() , key = (lambda k:findlowy[k]))
    x_key_min = min(findlowx.keys(), key = (lambda k: findlowx[k]))

    if x_key_min == y_key_min:
        return patches[x_key_min][0],patches[x_key_min][1]
    else:
        return patches[x_key_min][0],patches[x_key_min][1]

def appendDictionary(x,y):
    croppedImage = image[y:(y+2*r),x:(x+2*r)]
    #find the new patch with lowest gradient
    gradient_x,gradient_y = sobelfilter(croppedImage)
    return gradient_x,gradient_y

def sobelfilter(croppedImage):
    sobelx64f = cv2.Sobel(croppedImage,cv2.CV_64F,1,0,ksize = 3)
    abs_xsobel64f = np.absolute(sobelx64f)
    sobel_x8u = np.uint8(abs_xsobel64f)
    gradient_x = np.mean(sobel_x8u)

    sobely64f = cv2.Sobel(croppedImage, cv2.CV_64F, 0, 1, ksize=3)
    abs_ysobel64f = np.absolute(sobely64f)
    sobel_y8u = np.uint8(abs_ysobel64f)
    gradient_y = np.mean(sobel_y8u)

    return gradient_x,gradient_y

def blemishRemoval(action, x, y, flags, userdata):
    #referencing global variables
    global r,image
    #action to be taken when left mousebutton is pressed
    if action == cv2.EVENT_LBUTTONDOWN:
        #mark the center
        blemishLocation = (x,y)
        print(blemishLocation)
        newX, newY = selectedBlemish(x, y, r)
        newPatch = image[newY:(newY+2*r), newX:(newX+2*r)]
        cv2.imwrite('newPatch.png', newPatch)
        #create mask for the new patch
        mask = 255*np.ones(newPatch.shape, newPatch.dtype)
        image = cv2.seamlessClone(newPatch,image,mask,blemishLocation,cv2.NORMAL_CLONE)
        cv2.imshow("Blemish Removal App", image)

    elif action == cv2.EVENT_LBUTTONUP:
        cv2.imshow("Blemish Removal App", image)





r = 15
i = 0
image = cv2.imread('blemish.png',cv2.IMREAD_COLOR)
#make a dummy image, it will be useful to clear the drawing
dummy = image.copy()
cv2.namedWindow('Blemish Removal App')
print('Using a patch of radius 15')
#highgui functions called when mouse events occur
cv2.setMouseCallback('Blemish Removal App',blemishRemoval)
k = 0
#loop until escape button pressed
while k!=27:
    cv2.imshow('Blemish Removal App', image)
    k = cv2.waitKey(20) & 0xFF
    if k==99:
        image = dummy.copy()
cv2.destroyAllWindows()

