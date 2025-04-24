class senary:
    def __init__(self, tval):
        self.senval = tval
        # convert ternary to int
        self.intval = int(tval, 6)
    
    def __str__(self):
        return str("0s" + self.senval)
    
    def __int__(self):
        return self.intval
    
    def __float__(self):
        return float(self.intval)

def sen(n):
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, 6)
        nums.append(str(r))
    out = ''.join(reversed(nums))
    t = senary(out)
    return t