import numpy as np
import cv2

def main():
    print("loading images...")
    imgL= cv2.imread("tigerking.jpg")
    imgL = cv2.resize(imgL, (1200, 800),
               interpolation = cv2.INTER_LINEAR)
    imgR= cv2.imread("finedog.jpeg")
    imgR = cv2.resize(imgR, (1200, 800),
               interpolation = cv2.INTER_LINEAR)
    h, w = imgL.shape[:2]
    print(str(h)+","+str(w))
    cv2.imshow('', interlace(imgL, imgR, h, w))
    cv2.waitKey()
    cv2.destroyAllWindows()


def interlace(imgL, imgR, h, w):
    inter = np.empty((h, w, 3), imgL.dtype)
    inter[:h, :w:2, :] = imgL[:h, :w:2, :]
    inter[:h, 1:w:2, :] = imgR[:h, 1:w:2, :]
    
    return inter.astype(np.float32) / 255


if __name__ == "__main__":
    main()