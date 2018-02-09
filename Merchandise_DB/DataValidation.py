def is_Float(n):
    try:
        if float(n):
            return True
    except ValueError:
        return False

def is_int(n):
    try:
        int(n)
        return True
    except ValueError:
        return False
