# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     config
   Description :
   Author :       simplefly
   date：          2017/12/21
-------------------------------------------------
   Change Activity:
                   2017/12/21:
-------------------------------------------------
"""
__author__ = 'simplefly'

import conf.config_default

class Dict(dict):
    '''
    Simple dict but support access as x.y style.
    '''
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)
    def __setattr__(self, key, value):
        self[key] = value

def merge(defaults, override):
    r = {}
    for k,v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r

def toDict(d):
    D = Dict()
    for k, v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D

configs = conf.config_default.configs

try:
    import conf.config_override
    configs = merge(configs, conf.config_override.configs)
except ImportError:
    pass

configs = toDict(configs)