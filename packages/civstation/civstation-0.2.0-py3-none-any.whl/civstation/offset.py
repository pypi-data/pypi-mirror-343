from .stations import Station

class Offset(Station):
    #TODO: Refactor this, it's too complex. But it does work.
    #get rid of repeated calls to .lower().
    def __init__ (self, offset, decimal_places = 2, return_float_on_sub = True) ->None:
            self.decimal_places = decimal_places
            self.return_float_on_sub = return_float_on_sub
            if isinstance(offset, Offset):
                self.val=float(offset)
            elif "rt" in str(offset).lower() or "lt" in str(offset).lower():
                negative=False
                if "rt" in str(offset).lower()[-2:]:
                    if "'" in str(offset):
                        endnum=str(offset).index("'")
                    else: endnum=str(offset).lower().index("r")
                if "lt" in str(offset).lower()[-2:]:
                    negative=True
                    if "'" in str(offset):
                        endnum=str(offset).index("'")
                    else: endnum=str(offset).lower().index("l")                
                try:
                    self.val=float(str(offset)[:endnum])
                except: raise ValueError("Not a valid Offset")
                if negative: self.val=-self.val
            else:
                try: self.val = float(offset)
                except: raise ValueError("Not a valid offset.")
    
    def __str__(self):
        offset = f"{round(abs(self.val), self.decimal_places):.{self.decimal_places}f}"
        if self.val <0: return offset+"LT"
        elif self.val >0: return offset+"RT"
        else: return "" 

    def __neg__(self):
        return Offset(-self.val)    

class Point:
    def __init__ (self,station,offset):
        #This class will put Station and Offset together as a 2D grid.
        #maybe put this in a separate file.
        pass        