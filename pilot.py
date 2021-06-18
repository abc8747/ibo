import math
import cv2

g = 9.81
def getMomentOfInertia(m, L): # rod
    return m*L**2/12
def getPeriod(r, l, L):
    m = 1
    I = getMomentOfInertia(m, L)
    return 2*math.pi/r*math.sqrt(l*I/g)

print(getPeriod(15/100/2, 0.494, 0.1982))

'''
7 | 97.4 507 513 522
6 | 89.4 506 515 523
5 | 81.4 508 516 506
4 | 73.4 509 517 507
3 | 65.4 510 518 508
2 | 57.4 511 519 509
1 | 49.4 512 521 510



'''
