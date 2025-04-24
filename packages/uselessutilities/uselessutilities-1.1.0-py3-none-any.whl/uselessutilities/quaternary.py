class quaternary:
    def __init__(self, tval):
        self.quatval = tval
        # convert quaternary to int
        self.intval = int(tval, 4)
    
    def __str__(self):
        return str("0q" + self.quatval)
    
    def __int__(self):
        return self.intval
    
    def __float__(self):
        return float(self.intval)
    
    def __eq__(self, other):
        if isinstance(other, quaternary):
            return self.intval == other.intval
        elif hasattr(other, 'intval'):
            return self.intval == other.intval
        else:
            return self.intval == int(other)

    def __add__(self, other):
        if isinstance(other, quaternary):
            return quat(self.intval + other.intval) # handle self-to-self adding
        elif hasattr(other, 'intval'):
            return quat(self.intval + other.intval) # handle mixed adding
        elif isinstance(other, float):
            return quat(self.intval + other) # handle floats
        else:
            return quat(self.intval + int(other)) # handle non-uselessutilities adding

    def __sub__(self, other):
        if isinstance(other, quaternary):
            return quat(self.intval - other.intval) # handle self-to-self subtracting
        elif hasattr(other, 'intval'):
            return quat(self.intval - other.intval) # handle mixed subtracting
        elif isinstance(other, float):
            return quat(self.intval - other) # handle floats
        else:
            return quat(self.intval - int(other)) # handle non-uselessutilities subtracting

    def __mul__(self, other):
        if isinstance(other, quaternary):
            return quat(self.intval * other.intval) # handle self-to-self multiplying
        elif hasattr(other, 'intval'):
            return quat(self.intval * other.intval) # handle mixed multiplying
        elif isinstance(other, float):
            return quat(self.intval * other) # handle floats
        else:
            return quat(self.intval * int(other)) # handle non-uselessutilities multiplying

    def __truediv__(self, other):
        if isinstance(other, quaternary):
            return quat(int(self.intval) // other.intval) # handle self-to-self dividing
        elif hasattr(other, 'intval'):
            return quat(int(self.intval) // other.intval) # handle mixed dividing
        elif isinstance(other, float):
            return quat(int(self.intval) // other) # handle floats
        else:
            return quat(int(self.intval) // int(other)) # handle non-uselessutilities dividing

    def __mod__(self, other):
        if isinstance(other, quaternary):
            return quat(self.intval % other.intval) # handle self-to-self modulo
        elif hasattr(other, 'intval'):
            return quat(self.intval % other.intval) # handle mixed modulo
        elif isinstance(other, float):
            return quat(self.intval % other) # handle floats
        else:
            return quat(self.intval % int(other)) # handle non-uselessutilities modulo

def quat(n):
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, 4)
        nums.append(str(r))
    out = ''.join(reversed(nums))
    t = quaternary(out)
    return t