#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from indicators.indicator import Indicator

class EMA(Indicator):
    def __init__(self, args = []):
        [ period ] = args

    super().__init__({
      'args': args,
      'id': 'ema',
      'name': 'EMA(%f)' % (period),
      'seed_period': period
    })

    self._a = 2 / (period + 1)

    def update(self, v):
        if self.l() < 2:
        super().update(v)
        else:
        super().update((self._a * v) + ((1 - self._a) * self.prev()))

        return self.v()

    def add(self, v):
        if self.l() == 0:
        super().add(v)
        else: 
        super().add((self._a * v) + ((1 - self._a) * self.v()))

        return self.v()

    def ema(self):  # 起始值为0:n-1的last
        start_index = _get_valid_index(self._values, start_index, n)
        emacol = series.copy()
        if(start_index > 0):
            lep = start_index - 1
            emacol[:lep] = None
        return emacol.ewm(span=n, adjust=False).mean()

