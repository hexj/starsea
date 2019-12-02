#!/usr/bin/env python
# -*- coding: utf-8 -*-
#TODO
class SLOP:
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

def slop2():
    import numpy as np
    x = np.array([0,1,2,3])
    y = np.array([1,2,3,4])
    slope = ((len(x)*sum(x*y)) - (sum(x)*sum(y)))/(len(x)*(sum(x**2))-(sum(x)**2))
    print(slope)


def main():
    slop2()


def _time_analyze_(func):
    import time
    t1_start = time.perf_counter()
    func()
    t1_stop = time.perf_counter()
    print("Elapsed time: %s s" % (t1_stop - t1_start))


if __name__ == '__main__':
    _time_analyze_(main)
