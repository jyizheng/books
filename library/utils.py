def to_str(s):
    if type(s) == unicode:
        return s.encode("utf-8")
    elif type(s) == list:
        return " , ".join([to_str(i) for i in s ])
    else:
        return str(s)



def to_unicode(s):
    if type(s)==unicode:
        return s
    return str(s).decode("utf-8")
    