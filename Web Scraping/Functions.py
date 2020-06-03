def StringToNumber(s):
    if s != '-':
        if s[-1] == 'k':
            s = float(s[1:-1]) * (10 ** 3)
        elif s[-1] == 'M':
            s = float(s[1:-1]) * (10 ** 6)
        elif s[-1] == 'B':
            s = float(s[1:-1]) * (10 ** 9)
        else:
            s = float(s[1:])

    return s
