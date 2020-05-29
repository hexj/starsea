from math import isfinite

class Indicator:
    def __init__(self, params = {}):
        self._name = params['name']
        self._period = params['period']
        self._id = params['id']
        self._args = params['args']
        self._data_type = params.get('data_type') or '*'
        self._data_key = params.get('data_key') or 'close'
        self.reset()

    def reset(self):
        self._values = []

    def l(self):
        return len(self._values)

    def v(self):
        if len(self._values) == 0:
            return None
        return self._values[-1]

    def prev(self, n = 1):
        if len(self._values) <= n:
            return None

        return self._values[-1 - n]

    def add(self, v):
        self._values.append(v)
        return v

    def update(self, v):
        if len(self._values) == 0:
            return self.add(v)

    self._values[-1] = v
        return v

    def crossed(self, target):
        if self.l() < 2: return False
        v = self.v()
        prev = self.prev()

        return (
            (v >= target and prev <= target) or
            (v <= target and prev >= target)
        )

    def ready(self):
        return len(self._values) > 0

    def get_period(self):
        return self._period

    def get_data_key(self):
        return self._data_key

    def get_data_type(self):
        return self._data_type

    def get_valid_index(self, start_index=0):
        if(start_index == 0):
            for i, val in enumerate(self._values):
                if val is not None:
                    return i
        return start_index
