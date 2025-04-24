class quinary:
    def __init__(self, tval):
        self.terval = tval
        # convert ternary to int
        self.intval = int(tval, 5)
    
    def __str__(self):
        return str("0Q" + self.terval)
    
    def __int__(self):
        return self.intval
    
    def __float__(self):
        return float(self.intval)

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