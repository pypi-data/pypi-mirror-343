class quinary:
    def __init__(self, tval):
        self.quinval = tval
        # convert quinary to int
        self.intval = int(tval, 5)
    
    def __str__(self):
        return str("0Q" + self.quinval)
    
    def __int__(self):
        return self.intval
    
    def __float__(self):
        return float(self.intval)
    
    def __eq__(self, other):
        if isinstance(other, quinary):
            return self.intval == other.intval
        elif hasattr(other, 'intval'):
            return self.intval == other.intval
        else:
            return self.intval == int(other)

    def __add__(self, other):
        if isinstance(other, quinary):
            return quin(self.intval + other.intval) # handle self-to-self adding
        elif hasattr(other, 'intval'):
            return quin(self.intval + other.intval) # handle mixed adding
        elif isinstance(other, float):
            return quin(self.intval + other) # handle floats
        else:
            return quin(self.intval + int(other)) # handle non-uselessutilities adding

    def __sub__(self, other):
        if isinstance(other, quinary):
            return quin(self.intval - other.intval) # handle self-to-self subtracting
        elif hasattr(other, 'intval'):
            return quin(self.intval - other.intval) # handle mixed subtracting
        elif isinstance(other, float):
            return quin(self.intval - other) # handle floats
        else:
            return quin(self.intval - int(other)) # handle non-uselessutilities subtracting

    def __mul__(self, other):
        if isinstance(other, quinary):
            return quin(self.intval * other.intval) # handle self-to-self multiplying
        elif hasattr(other, 'intval'):
            return quin(self.intval * other.intval) # handle mixed multiplying
        elif isinstance(other, float):
            return quin(self.intval * other) # handle floats
        else:
            return quin(self.intval * int(other)) # handle non-uselessutilities multiplying

    def __truediv__(self, other):
        if isinstance(other, quinary):
            return quin(int(self.intval) // other.intval) # handle self-to-self dividing
        elif hasattr(other, 'intval'):
            return quin(int(self.intval) // other.intval) # handle mixed dividing
        elif isinstance(other, float):
            return quin(int(self.intval) // other) # handle floats
        else:
            return quin(int(self.intval) // int(other)) # handle non-uselessutilities dividing

    def __mod__(self, other):
        if isinstance(other, quinary):
            return quin(self.intval % other.intval) # handle self-to-self modulo
        elif hasattr(other, 'intval'):
            return quin(self.intval % other.intval) # handle mixed modulo
        elif isinstance(other, float):
            return quin(self.intval % other) # handle floats
        else:
            return quin(self.intval % int(other)) # handle non-uselessutilities modulo

def quin(n):
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, 5)
        nums.append(str(r))
    out = ''.join(reversed(nums))
    t = quinary(out)
    return t