import cv2


def invert_image(image):
    return 255 - image

def canny(image):
    result = cv2.Canny(image, 100, 150)
    return result
    
