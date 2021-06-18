import numpy as np
import matplotlib.pyplot as plt
import cv2
import csv
import os

files = os.listdir('src')
# print(files)
for filename in files:
    capture = cv2.VideoCapture(f'src/{filename}')

    color = 'gray'
    bins = 256
    resizedWidth = 1080
    show = True

    if show:
        fig, ax = plt.subplots()
        ax.set_title('Grayscale Histogram')
        ax.set_xlabel('value')
        ax.set_ylabel('Frequency')

        lw = 3
        alpha = 0.5
        lineGray, = ax.plot(np.arange(bins), np.zeros((bins,1)), c='k', lw=lw, label='intensity')
        ax.set_xlim(0, 20) # bins-1
        ax.set_ylim(0, 1)
        ax.legend()
        plt.ion()
        plt.show()

    success, prev = capture.read()
    fn = 0

    brightnesses = []
    while True:
        success, next = capture.read()
        if not success:
            break
        
        frame = cv2.absdiff(prev, next)

        # histogram
        numPixels = np.prod(frame.shape[:2])
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        histogram = cv2.calcHist([gray], [0], None, [bins], [0, 255])
        brightnesses.append((fn, sum([i*j[0] for i, j in enumerate(histogram)]) / numPixels))

        if show:
            lineGray.set_ydata(histogram)
            fig.canvas.draw()
            (height, width) = frame.shape[:2]
            resizedHeight = int(float(resizedWidth / width) * height)
            frame = cv2.resize(frame, (resizedWidth, resizedHeight),interpolation=cv2.INTER_AREA)
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) == ord('q'):
                break

        prev = next
        fn += 1

    with open(f'output/{filename}.csv', mode='w+', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(brightnesses)
        print(f'{filename} is done.')

    capture.release()
    cv2.destroyAllWindows()