import numpy as np
import cv2
import csv
import os

for filename in os.listdir('src'):
    capture = cv2.VideoCapture(os.path.join("src", filename))
    brightnesses = []

    success, prev = capture.read()
    while success:
        success, next = capture.read()
        if not success:
            break

        # compute frame difference from next and convert it to greyscale        
        frame = cv2.cvtColor(cv2.absdiff(prev, next), cv2.COLOR_BGR2GRAY)

        # sum up the differences.
        numPixels = np.prod(frame.shape[:2])
        histogram = cv2.calcHist([frame], [0], None, [256], [0, 255])
        brightnesses.append(sum(i*j[0] for i, j in enumerate(histogram)) / numPixels)

        prev = next
    
    capture.release()

    with open(os.path.join('output', f'{os.path.splitext(filename)[0]}.csv'), mode='w+', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([(i, j) for i, j in enumerate(brightnesses)])