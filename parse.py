import numpy as np
import cv2
import csv
import os
import math
import pandas as pd

def resize(image):
    return cv2.resize(image, (1080, 720), interpolation=cv2.INTER_AREA)

class Line:
    def __init__(self, line):
        self.p1 = np.array(line[0][:2]).astype(int)
        self.p2 = np.array(line[0][2:4]).astype(int)
    
    def getLen(self):
        self.length = np.sqrt(np.sum((self.p1 - self.p2) ** 2, axis=0))
        return self
    
    def getAngle(self):
        # assuming p1 = bottom left
        self.angle = np.arctan2(
            self.p2[1] - self.p1[1],
            self.p2[0] - self.p1[0] if self.p1[0] < self.p2[0] else self.p1[0] - self.p2[0]
        )
        return self

for filename in os.listdir('src'):
    capture = cv2.VideoCapture(os.path.join("src", filename))
    totalframecount = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    
    vals = []
    framecount = 0
    success = True
    while success:
        success, frame = capture.read()
        if not success or framecount==100:
            break
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(image, 100, 100, L2gradient=False)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, maxLineGap=200)
        
        if lines is not None:
            l = Line(sorted(lines, key=lambda x:Line(x).getLen().length, reverse=True)[0])
            l.getLen().getAngle()

            # for l0 in lines:
                # l0 = Line(l0)
                # cv2.line(edges, l0.p1, l.p2, (255, 255, 255), 1)
            # cv2.line(edges, l.p1, l.p2, (255, 255, 255), 3)
            # cv2.putText(edges, f'fc: {framecount}, l: {l.length:.6}, t: {l.angle:.6}', (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))

            vals.append([framecount, l.length, l.angle])

        print(framecount, totalframecount)
        framecount += 1

        # cv2.imshow('IMG', resize(edges))
        # if cv2.waitKey(200) == ord('q'):
        #     break
    
    df = pd.DataFrame(vals, columns=['frame', 'length', 'angle'])
    df.reset_index()
    df.to_csv(os.path.join('output', f'{os.path.splitext(filename)[0]}.csv'), index=False)
    # with open(, mode='w+', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(vals)

    # cv2.destroyAllWindows()
    break