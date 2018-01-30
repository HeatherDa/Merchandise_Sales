def is_Float(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

def is_int(n):
    try:
        int(n)
        return True
    except ValueError:
        return False
