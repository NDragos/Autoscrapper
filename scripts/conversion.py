import re

def str_to_int(s):
    s = re.sub("[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ., ]", "", s)
    return int(s)

def str_to_float(s):
    s = s.replace(",", ".")
    s = re.sub("[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ]", "", s)
    return float(s)

def delete_let(s):
    s = re.sub("[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ]", "", s)
    return s