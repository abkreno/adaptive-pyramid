import cv2
from sys import stdout
import numpy as np
from math import exp
from matplotlib import pyplot as plt
from segmant import Segmant
from pprint import pprint
from utils import has_more_candidates, min_mean, get_result_image

alpha         = 0.4
min_contrast  = 200
min_size      = 10
h             = 0
MAX_LEVEL     = 2
path          = 'images/house.bmp'
input_image   = cv2.imread(path, 0)
#input_image   = cv2.resize(input_image, (200, 200), interpolation=cv2.INTER_CUBIC)
rows, cols    = input_image.shape
image         = [[Segmant(j + i * cols, i, j, 1.0 * input_image[i][j]) for j in range(cols)] for i in range(rows)]
result_images = [input_image]
# Calculating (Mean, Variance, A, and Support) for each cell
nRow          = [-1, -1, -1,  0,  0,  1,  1,  1]
nCol          = [-1,  0,  1, -1,  1, -1,  0,  1]
graph         = []
for row in range(rows):
    for col in range(cols):
        for k in range(8):
            nrow = row + nRow[k]
            ncol = col + nCol[k]
            if(nrow < rows and nrow >= 0 and ncol < cols and ncol >= 0):
                image[row][col].support.append(image[nrow][ncol])
        image[row][col].initVals()
        graph.append(image[row][col])
    #print(image[row])
while(h < MAX_LEVEL):
    # Extracting local/sub minima
    while has_more_candidates(graph):
        for cell in graph:
            if(cell.q):
                # check if the cell mean is the minimum among all neighbours
                if(cell.mean <= min_mean(cell.support)):
                    # the cell will survive
                    cell.p = 1
                    cell.q = False
                    # mark all neighbours as nonsurviving
                    for ncell in cell.support:
                        ncell.q = False
    for cell in graph:
        if(cell.p == 1):
            del cell.support[:]
    # finding the roots and updating the mean/variance of the surviving
    for cell in graph:
        if(cell.p == 0):
            surv = None
            # find the closest surviving
            for ncell in cell.support:
               if(ncell.p == 1):
                 if(surv == None or abs(ncell.mean - cell.mean) < abs(surv.mean - cell.mean)):
                    surv = ncell
            min_c     = min_contrast if cell.a > min_size else min_contrast*exp(alpha*(min_size-cell.a))
            # mean_diff = 1000 if surv == None else abs(surv.mean - cell.mean)
            mean_diff = abs(surv.mean - cell.mean)
            if(mean_diff > min_c):
                # the cell is a root
                cell.p = 2
            else:
                cell.parent = surv
    # connect the nonsurviving to the surviving
    for cell in graph:
        if(cell.p == 0):
            for ncell in cell.support:
                if(ncell.p == 1 and ncell.index != cell.parent.index):
                    cell.parent.support.append(ncell)
                    ncell.support.append(cell.parent)
        elif(cell.p == 2):
            # if the cell is a root connect it to the surviving neighbours
            cell.p = 1
            nsupport = []
            for ncell in cell.support:
                if(ncell.p != 0):
                    nsupport.append(ncell)
                    ncell.support.append(cell)
            del cell.support[:]
            cell.support = nsupport
    # keep only regions such that p = 1
    ngraph = []
    for cell in graph:
        if(cell.p == 1):
            cell.p = 0
            cell.q = True
            cell.initVals()
            ngraph.append(cell)
    print("number of the old cells:",len(graph))
    print("number of the surviving:",len(ngraph))
    del graph[:]
    graph = ngraph
    h     = h + 1
    result_images.append(get_result_image(image, input_image, h))
#pprint(result_images)
fig = plt.figure()
# for i in range(len(result_images)):
#  fig.add_subplot(2, 2, i+1) # (height, width, count)
#  plt.axis("off")
#  plt.imshow(result_images[i], cmap='gray')
fig.add_subplot(1, 2, 1)
plt.axis("off")
plt.imshow(result_images[0], cmap='gray')
fig.add_subplot(1, 2, 2)
plt.axis("off")
plt.imshow(result_images[len(result_images)-1], cmap='gray')

plt.show()
