class ternary:
    def __init__(self, tval, isnegative=False):
        self.terval = tval
        self.intval = int(tval, 3)
        self.length = len(tval)
        self.isnegative = isnegative
        self.digits = list(str(tval))
        self.true_intval = self.intval if not self.isnegative else -self.intval

    def __str__(self):
        return str("0t" + self.terval)
    
    def __int__(self):
        return self.true_intval
    
    def __float__(self):
        return float(self.true_intval)

    def __eq__(self, other):
        if isinstance(other, ternary):
            return self.true_intval == other.true_intval
        elif hasattr(other, 'true_intval'):
            return self.true_intval == other.true_intval
        else:
            return self.true_intval == int(other)

    def __add__(self, other):
        if isinstance(other, ternary):
            return ter(self.true_intval + other.true_intval) # handle self-to-self adding
        elif hasattr(other, 'true_intval'):
            return ter(self.true_intval + other.true_intval) # handle mixed adding
        elif isinstance(other, float):
            return ter(self.true_intval + other) # handle floats
        else:
            return ter(self.true_intval + int(other)) # handle non-uselessutilities adding
    
    def __sub__(self, other):
        if isinstance(other, ternary):
            return ter(self.true_intval - other.true_intval) # handle self-to-self subtracting
        elif hasattr(other, 'true_intval'):
            return ter(self.true_intval - other.true_intval) # handle mixed subtracting
        elif isinstance(other, float):
            return ter(self.true_intval - other) # handle floats
        else:
            return ter(self.true_intval - int(other)) # handle non-uselessutilities subtracting

    def __mul__(self, other):
        if isinstance(other, ternary):
            return ter(self.true_intval * other.true_intval) # handle self-to-self multiplying
        elif hasattr(other, 'true_intval'):
            return ter(self.true_intval * other.true_intval) # handle mixed multiplying
        elif isinstance(other, float):
            return ter(self.true_intval * other) # handle floats
        else:
            return ter(self.true_intval * int(other)) # handle non-uselessutilities multiplying

    def __truediv__(self, other):
        if isinstance(other, ternary):
            return ter(int(self.true_intval) // other.true_intval) # handle self-to-self dividing
        elif hasattr(other, 'true_intval'):
            return ter(int(self.true_intval) // other.true_intval) # handle mixed dividing
        elif isinstance(other, float):
            return ter(int(self.true_intval) // other) # handle floats
        else:
            return ter(int(self.true_intval) // int(other)) # handle non-uselessutilities dividing

    def __mod__(self, other):
        if isinstance(other, ternary):
            return ter(self.true_intval % other.true_intval) # handle self-to-self modulo
        elif hasattr(other, 'true_intval'):
            return ter(self.true_intval % other.true_intval) # handle mixed modulo
        elif isinstance(other, float):
            return ter(self.true_intval % other) # handle floats
        else:
            return ter(self.true_intval % int(other)) # handle non-uselessutilities modulo

def ter(n):
    neg = False
    if n < 0:
        neg = True
        n = abs(n)
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    out = ''.join(reversed(nums))
    t = ternary(out, isnegative=neg)
    return t