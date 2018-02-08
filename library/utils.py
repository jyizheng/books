def to_str(s):
    if type(s) == unicode:
        return s.encode("utf-8")
    else:
        return str(s)



