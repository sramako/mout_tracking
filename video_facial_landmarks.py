# USAGE
# python video_facial_landmarks.py --shape-predictor shape_predictor_68_face_landmarks.dat
# python video_facial_landmarks.py --shape-predictor shape_predictor_68_face_landmarks.dat --picamera 1

# import the necessary packages
from imutils.video import VideoStream
from imutils import face_utils
import datetime
import argparse
import imutils
import time
import dlib
import cv2
import time
import numpy as np
import os
import math
import string
import cPickle
import gzip

def load(file_name):
    # load the model
    stream = gzip.open(file_name, "rb")
    model = cPickle.load(stream)
    stream.close()
    return model


def save(file_name, model):
    # save the model
    stream = gzip.open(file_name, "wb")
    cPickle.dump(model, stream)
    stream.close()

file = open('/home/ako/hcode/real-time-facial-landmarks/raw_lip', 'r')
def ed(a,b):
    a = map(lambda x:int(x),a)
    b = map(lambda x:int(x),b)
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
                help="path to facial landmark predictor")
ap.add_argument("-r", "--picamera", type=int, default=-1,
                help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] camera sensor warming up...")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2)

rl = open("raw_lip", 'w')

os.system('./audio.sh &')

# loop over the frames from the video stream
for j in range(0,60):
    # grab the frame from the threaded video stream, resize it to
    # have a maximum width of 400 pixels, and convert it to
    # grayscale
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale frame
    rects = detector(gray, 0)

    # loop over the face detections
    for rect in rects:
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # loop over the (x, y)-coordinates for the facial landmarks
        # and draw them on the image
        width = ed(shape[48], shape[54])
        height = ed(shape[51], shape[57])
        rat = width/height
        rat=rat*100
        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
        # rl.write(np.array2string(shape[49:50,55:56,52:53,58:59],separator=',',suppress_small=True).replace('\n','')[1:-1])
        rl.write(str(rat))
        rl.write('\n')

        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
    # time.sleep(3)

    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
os.system("killall arecord")
