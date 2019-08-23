#TODO
def slope(self, values, n):
    result = []
    for i,e in enumerate(values):
        if i < n-1:
            result.append(None)
            continue
        window = values[i-n+1:i+1]
        if self.has_none(window):
            result.append(None)
            continue
        xys = [(x,y) for x,y in enumerate(window)]
        xs = [x for x,y in xys]
        ys = [y for x,y in xys]
        a = sum([x*y for x,y in xys])
        b = n * self.average(xs) * self.average(ys)
        c = sum([x**2 for x in xs])
        r = (a-b)/(c-n*self.average(xs)**2)
        result.append(r)
    return result