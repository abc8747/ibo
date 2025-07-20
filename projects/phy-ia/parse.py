'''
This script does the following:
- read the list of videos from a specific folder
- for each video, process each frame:
    - for each frame, convert the frame to greyscale
    - perform canny edge detection
    - perform probabilistic hough line transform
    - for each possible location of the rod:
        - select the longest line
        - calculate the length of the rod (in pixels) using Pythagoras\
        - calculate the angle of the rod (in radians) using atan2
    - aggregate the temporal changes of the rod
- store the data in multiple CSV files for further processing
'''

from rich.progress import Progress
import numpy as np
import pandas as pd
import cv2
import os

class Line:
    def __init__(self, line):
        self.p1 = np.array(line[0][:2]).astype(int)
        self.p2 = np.array(line[0][2:4]).astype(int)

    def getLen(self):
        self.length = np.sqrt(np.sum((self.p1 - self.p2) ** 2, axis=0))
        return self

    def getAngle(self):
        self.angle = np.arctan2(
            self.p2[1] - self.p1[1],
            self.p2[0] - self.p1[0] if self.p1[0] < self.p2[0] else self.p1[0] - self.p2[0]
        )
        return self

with Progress() as progress:
    files = os.listdir('src')
    task0 = progress.add_task(f"[green]Processing files...", total=len(files))
    for filename in files: # process each video in the specified folder
        progress.update(task0, advance=1, description=f"[green]Processing {filename}...")
        capture = cv2.VideoCapture(os.path.join("src", filename))
        
        totalframecount = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        task1 = progress.add_task(f"[green]Parsing frames...", total=totalframecount)
        vals, framecount = [], 0
        while 1:
            success, frame = capture.read()
            if not success:
                break
            
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(image, 100, 100, L2gradient=True)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, maxLineGap=200)
            
            if lines is not None:
                l = Line(sorted(lines, key=lambda x:Line(x).getLen().length, reverse=True)[0]).getLen().getAngle()
                vals.append([framecount, l.length, l.angle])

            progress.update(task1, advance=1)
            framecount += 1
        
        df = pd.DataFrame(vals, columns=['frame', 'length', 'angle'])
        df.to_csv(os.path.join('output', f'{os.path.splitext(filename)[0]}.csv'), index=False)