from .stations import Station
from .offset import Offset
from math import sqrt

class Point:
    def __init__(self, station: Station, offset = None)->None:
        if offset is None:
            offset = Offset(0)
        try:
            self.station=Station(station)
            self.offset = Offset(offset)
        except (TypeError, ValueError) as e:
            raise ValueError ("Invalid Station or Offset") from e 
        
    def __str__(self):
        return f"{str(self.station)} {str(self.offset)}"
    
    def __repr__(self):
        return self.__str__()    

    def __sub__(self, subtracted_val):
        return self.distance(subtracted_val)
    
    def __rsub__(self, subtracted_val):
        return self.distance(subtracted_val)
    
    def distance(self, other)->float:
        if isinstance(other, Station):
            other=Point(other)
        if not isinstance(other, Point):
            raise ValueError("Must use two Point objects to get distance.")
        
        xdist=float(self.station-other.station)
        ydist=float(self.offset-other.offset)
        return sqrt((xdist**2) + (ydist**2))
        
    

    