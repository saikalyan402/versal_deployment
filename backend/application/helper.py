import numpy as np

def replace_nan_with_placeholder(d):
    if isinstance(d,dict):
        return {k: replace_nan_with_placeholder(v) for k,v in d.items()}
    elif isinstance(d,list):
        return [replace_nan_with_placeholder(i) for i in d]
    elif isinstance(d,float) and np.isnan(d):
        return '--'
    elif d is None:
        return '--'
    elif d == '-':
        return '--'
    elif d == 'NAN':
        return '--'
    return d