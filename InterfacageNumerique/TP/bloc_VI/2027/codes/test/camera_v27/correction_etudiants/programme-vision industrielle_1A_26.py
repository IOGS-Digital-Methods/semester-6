"""camera_flux_lensepy_simple.py
Basler Camera video flux display (OpenCV)
.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
"""

from pypylon import pylon
import cv2
import numpy as np
import matplotlib.pyplot as plt

from lensepy.utils import get_screen_size
from lensepy.modules.basler.basler_models import init_first_camera

COLOR_MODE = "BayerRG8"  # "BayerRG8" / "Mono12"
DISPLAY_RATIO = 0.7
EXPOSURE_TIME = 20000

APPROX_FACTOR = 0.03 #0.02 bien
MIN_AREA=800
MAX_AREA=80000

def detect_shape(cnt):
    area = cv2.contourArea(cnt)
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, APPROX_FACTOR * peri, True)
    n = len(approx)

    if area < MIN_AREA or area>MAX_AREA:
        return None, None, None

    if n == 3:
        shape = "Triangle"
    elif n == 4:
        rect = cv2.minAreaRect(cnt)
        w, h = rect[1]
        if h == 0 or w == 0:
            shape = "Inconnu"
        else:
            ratio = max(w, h) / min(w, h)
            shape = "Carre" if 0.90 < ratio < 1.10 else "Rectangle"
    elif n == 5:
        shape = "Pentagone"
    else:
        shape = f"{n}-gon"

    return shape, approx, peri

approx_color=60
def color(pixel):
    lower_red1 = np.array([690, 70, 50])
    upper_red1 = np.array([690+approx_color, 255, 255])

    lower_jaun = np.array([540-approx_color, 70, 50])
    upper_jaun = np.array([540+approx_color, 255, 255])

    lower_blue = np.array([60-approx_color, 70, 50])
    upper_blue = np.array([60+approx_color, 255, 255])

    lower_green = np.array([220 - approx_color, 70, 50])
    upper_green = np.array([220 + approx_color, 255, 255])

    if lower_red1[0]<=pixel[0][0]<=upper_red1[0]:
        return "ROUUUGE"
    if lower_jaun[0]<=pixel[0][0]<=upper_jaun[0]:
        return "jaun"
    if lower_blue[0]<=pixel[0][0]<=upper_blue[0]:
        return "BLEUU"
    if lower_green[0] <= pixel[0][0] <= upper_green[0]:
        return "VEERT"
    else:
        return "regarde a gauche"


    mask_hsv = cv2.bitwise_or(mask_hsv1, mask_hsv2)


def moy_color(frame, list_bary, N):
    x,y=list_bary
    col=[0,0,0]
    for ix in range(max(0,x-N),min(x+N,len(frame))):
        for iy in range(max(0,y-N),min(y+N,len(frame[0]))):
            col[0]=col[0]+frame[ix,iy,0]/N**2
            col[1] = col[1] + frame[ix, iy, 1] / N ** 2
            col[2] = col[2] + frame[ix, iy, 2] / N ** 2
    return col

def numshape(shape):
    if shape =='Rectangle' or shape=='Carre':
        return 4
    if shape == 'Triangle':
        return 3
    if shape == "6-gon":
        return 0

def iswinning(matrix):

    for k in range(len(matrix)):
        numk=matrix[k][0]
        nrow = 1
        for j in range(1,len(matrix)):

            if matrix[k][j]!=numk:
                nrow=0
            else:
                nrow=nrow+1
        if nrow==3 and numk!=20:
            return numk
    for k in range(len(matrix)):
        numk = matrix[0][k]
        nrow = 1
        for j in range(1, len(matrix)):
            if matrix[j][k] != numk:
                nrow = 0
            else:
                nrow = nrow + 1
        if nrow == 3 and numk !=20:
            return numk
    if matrix[0][0]==matrix[1][1]==matrix[2][2] and matrix[0][0]!=20:
        return matrix[1][1]
    if matrix[0][2]== matrix[1][1]==matrix[2][0] and matrix[1][1]!=20:
        return matrix[1][1]
    return 100




def main():
    # ---
    height, width = get_screen_size()
    mode = 'z'
    # --- Find camera
    camera = init_first_camera('./config/camera_vi.ini')
    if camera is None:
        cv2.destroyAllWindows()
        return
    # --- Camera parameters
    camera.set_parameter('PixelFormat', COLOR_MODE)
    camera.set_parameter('ExposureTime', EXPOSURE_TIME)
    # --- Start acquisition    
    camera.open()
    camera.camera_acquiring = True
    
    print("Appuyez sur 'q' pour quitter")
    
    # --- Boucle d'acquisition ---
    while camera.camera_acquiring:
        # --- Get Image ---
        frame_raw = camera.get_image()
        # --- Image conversion ---
        if COLOR_MODE == 'Mono12':
            # Conversion 12 bits to 8 bits
            frame8 = (frame_raw / 16).astype(np.uint8)
        elif COLOR_MODE == 'BayerRG8':
            frame8 = frame_raw
            frame8 = cv2.cvtColor(frame8, cv2.COLOR_BGR2RGB)
        else:
            frame8 = frame_raw
            
        # --- Processing ---
        if mode == ord('a'):    # Canny
            final_output = cv2.Canny(frame8, 100, 150)
        elif mode == ord('g'):  # Gaussian Blur
            final_output = cv2.GaussianBlur(frame8, (15, 15), 4)
        elif mode == ord('i'):  # Inverse image
            final_output = 255 - frame8
        elif mode == ord('c'):  # Change colors of image
            final_output = frame8[:, :, [2, 1, 0]]


        elif mode == ord('e'): #fait tout
            #frame_blur = cv2.GaussianBlur(frame8, (10, 10), 2)
            #detect couleur PUE

            barycentres_shapes=[]
            shapes=[]

            "SHAPE DETECTION"

            N = 5
            sigma = 10
            img_gray = cv2.cvtColor(frame8, cv2.COLOR_RGB2GRAY)
            img_gray = cv2.GaussianBlur(img_gray, (N, N), sigma)
            #img_gray=255-img_gray                                             #inverted
            thre, img_thresh = cv2.threshold(
                img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )


            #erode
            N2 = 2
            square_kernel_3 = cv2.getStructuringElement(cv2.MORPH_RECT, (N2, N2))
            img_thresh = cv2.morphologyEx(img_thresh, cv2.MORPH_OPEN, square_kernel_3)

            #img_gray=img_thresh

            contours, _ = cv2.findContours(img_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            for cnt in contours:
                area = cv2.contourArea(cnt)
                shape, approx, peri = detect_shape(cnt)
                if shape is not None:
                    cv2.drawContours(img_gray, [approx], -1, (255, 0, 0), 2)

                    # Centre du contour
                    M = cv2.moments(cnt)
                    if M["m00"] != 0:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        barycentres_shapes.append([cX,cY])
                        shapes.append(shape)
                        #print(f'Shape : {shape} / cX: {cX} - cY: {cY} / Area : {area}')
                        cv2.putText(img_gray, shape, (cX - 30, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            circles = cv2.HoughCircles(
                img_gray,
                cv2.HOUGH_GRADIENT,
                dp=1.2,
                minDist=50,
                param1=90, #90- 65 p1 -p2
                param2=65,  #change nb cercle
                minRadius=50,
                maxRadius=200
            )

            if circles is not None:
                circles = np.round(circles[0, :]).astype("int")
                for (x, y, r) in circles:
                    cv2.circle(img_gray, (x, y), r, (0, 255, 0), 3)
                    cv2.putText(img_gray, "Cercle", (x - 20, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


            "DETECTION COULEUR"


            #frame_raw=frame_raw.astype(np.uint8)
            color_frame= cv2.cvtColor(frame8,cv2.COLOR_BGR2HSV)
            color_hsv_moy=[]
            for barycentres in barycentres_shapes:
                color_hsv_moy.append(moy_color(color_frame, barycentres, 5))
                #print(color_hsv_moy)
                col_str=color(color_hsv_moy)
                cv2.putText(img_gray, col_str , (barycentres[0] - 30, barycentres [1]+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            "ESPACE MORPION"
            #barycentres_shapes
            #shapes
            matrix=[[20,20,20],[20,20,20],[20,20,20]]

            dy=len(frame8)//3
            dx=len(frame8[0])//3
            for k in range(len(barycentres_shapes)):
                xcol,ycol=barycentres_shapes[k][0]//dx,barycentres_shapes[k][1]//dy

                matrix[xcol][ycol] = numshape(shapes[k])
            print(matrix)

            if iswinning(matrix)<50:
                print(f'{iswinning(matrix)}-gon a gagné')
            






            final_output= img_gray

        else:
            final_output = frame8
        
        # --- Image display ---
        max_w = int(width * DISPLAY_RATIO)
        max_h = int(height * DISPLAY_RATIO)
        h_src, w_src = final_output.shape[:2]
        scale = min(max_w / w_src, max_h / h_src)
        new_w = int(w_src * scale)
        new_h = int(h_src * scale)
        display = cv2.resize(final_output, (new_w, new_h))
        cv2.imshow("Flux Basler a2A1920", display)

        # --- Mode management ---
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            camera.camera_acquiring = False
            camera.close()
        elif key != 255:    # No key
            mode = key

    camera.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
