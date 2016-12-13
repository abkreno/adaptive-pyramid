# Only holds info about the segmant
# Don't calculate anything here


class Segmant(object):

    def __init__(self, index, row, col, val):
        super(Segmant, self).__init__()
        self.index   = index
        self.row     = row
        self.col     = col
        self.val     = val
        self.mean    = 0.0
        self.var     = 0.0
        self.a       = 0
        self.p       = 0
        self.q       = False
        self.support = []
        self.parent  = None

    # To String method
    def __repr__(self):
        s = str(self.index)+"=>"
        for x in self.support:
             s+= ", ("+str(x.row)+","+str(x.col)+")"
        #return str(self.p) if self.parent == None else "L"
        return str(int(self.mean))

    def initVals(self):
        self.p    = 0
        self.q    = True
        self.mean = self.val
        self.a    = len(self.support)
        for seg in self.support:
            self.mean += seg.val
        self.mean /= self.a
        self.var   = (self.val - self.mean)**2
        for seg in self.support:
            self.var += (seg.val - self.mean)**2
        self.var /= self.a
