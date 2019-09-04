#!/usr/bin/env python
# -*- coding: utf-8 -*-

class dfhelper:
    def between(df, colname, valmin, valmax):
        return df[df[colname]>=valmin & df[colname]<=valmax]
