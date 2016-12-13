import numpy as np

def has_more_candidates(graph=None):
    if(graph==None):
        return False
    for cell in graph:
        if(cell.q):
            return True
    return False

def min_mean(support=[]):
    mm = 1000000
    for cell in support:
        if(cell.q):
            mm = min(mm, cell.mean)
    return mm

def get_result_image(graph=None, image=None, level=0):
    if(graph == None or image == None):
        return []
    result = np.zeros(image.shape, dtype=np.uint8)
    rows,cols = image.shape
    c = 0
    x = 0
    for row in range(rows):
        for col in range(cols):
            cell = graph[row][col]
            l = 0
            while(cell.parent!=None):
                cell = cell.parent
                l+=1
                c+=1
            if(l==level):
                x+=1
            result[row][col] = cell.val
    print("number of cells with parent",c)
    print("number of cells at level",level,"=",x)
    return result
