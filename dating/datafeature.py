from numpy import array
class DataFeature:
    def __init__(self, name, minVal=None, interval=None, maxVal=None):
        self.name = name
        self.minVal = minVal
        if interval is not None: #check if a value of this feature needs to be preprocess
            if isinstance(interval,list):#the interval-length are not the same
                pass
                self.intv = interval
            else:# value is equally spread to same-length interval
                self.intv = interval
        pass #deal with max value
    
            