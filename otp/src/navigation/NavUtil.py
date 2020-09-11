# Miscellaneous utility classes!

import bisect

class QuadTree(object):
    '''
    Used for subdivision of a uniform free-space grid into squares of varying size.
    '''
    def __init__(self,width):
        self.full = False
        self.empty = True
        self.width = width

        offset = width / 2


    def fill(self,x,y):
        if self.empty:
            self.empty = False
            if self.width > 1:
                offset = self.width / 2
                self.UL = QuadTree(offset)
                self.UR = QuadTree(offset)
                self.LL = QuadTree(offset)
                self.LR = QuadTree(offset)                
        
        if self.width == 1:
            assert x == 0
            assert y == 0
            self.full = True
            return

        offset = self.width / 2

        if self.width == 2:
            if x >= 0:
                if y >= 0:
                    self.UR.fill(0,0)
                else:
                    self.LR.fill(0,0)
            else:
                if y >= 0:
                    self.UL.fill(0,0)
                else:
                    self.LL.fill(0,0)
        else:
            moveAmt = offset / 2
            if x >= 0:
                if y >= 0:
                    self.UR.fill(x-moveAmt,y-moveAmt)
                else:
                    self.LR.fill(x-moveAmt,y+moveAmt)
            else:
                if y >= 0:
                    self.UL.fill(x+moveAmt,y-moveAmt)
                else:
                    self.LL.fill(x+moveAmt,y+moveAmt)

        if self.UR.full and self.LR.full and self.UL.full and self.LL.full:
            self.full = True

    def squarify(self):
        offset = self.width / 2
        if self.empty:
            return []
        
        if self.width == 1:
            if self.full:
                return [(0,0,0,0),]
            else:
                return []
        elif self.full:
            return [(-1*offset,-1*offset,offset-1,offset-1),]
        else:
            ul = self.UL.squarify()
            ur = self.UR.squarify()
            ll = self.LL.squarify()
            lr = self.LR.squarify()

            res = []

            if self.width == 2:
                for s in ur:
                    res.append((0,0,0,0))
                for s in ul:
                    res.append((-1,0,-1,0))
                for s in lr:
                    res.append((0,-1,0,-1))
                for s in ll:
                    res.append((-1,-1,-1,-1))

            else:
                moveAmt = offset / 2
                for s in ur:
                    res.append((s[0]+moveAmt,s[1]+moveAmt,s[2]+moveAmt,s[3]+moveAmt))
                for s in ul:
                    res.append((s[0]-moveAmt,s[1]+moveAmt,s[2]-moveAmt,s[3]+moveAmt))
                for s in lr:
                    res.append((s[0]+moveAmt,s[1]-moveAmt,s[2]+moveAmt,s[3]-moveAmt))
                for s in ll:
                    res.append((s[0]-moveAmt,s[1]-moveAmt,s[2]-moveAmt,s[3]-moveAmt))

            return res


class PriQueue(list):
    def push(self, item):
        bisect.insort(self, item)

    def remove(self, item):
        self.pop(bisect.bisect_left(self,item))
        

class FIFOCache(object):
    def __init__(self, maxSize=1):
        assert maxSize > 0
        self.maxSize = maxSize
        self.lastItem = None
        self.firstItem = None
        self.lookup = {}

        self.insertCount = 0

    def insert(self, key, value):
        self.insertCount += 1
        # 0 - data
        # 1 - prev
        # 2 - next
        if self.firstItem is not None:
            self.lookup[self.firstItem][1] = key

        # data, next, prev
        self.lookup[key] = [value,None,self.firstItem]
        
        self.firstItem = key
        if self.lastItem is None:
            self.lastItem = key
            
        if len(self.lookup) > self.maxSize:
            nextToLast = self.lookup[self.lastItem][1]
            assert nextToLast is not None
            self.lookup[nextToLast][2] = None
            del self.lookup[self.lastItem]
            self.lastItem = nextToLast
            
    def get(self, key, default):
        return self.lookup.get(key,(default,None,None))[0]

    def __contains__(self, key):
        return key in self.lookup
