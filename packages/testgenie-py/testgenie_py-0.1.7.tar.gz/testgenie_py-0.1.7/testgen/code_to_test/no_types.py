def bin_and(a, b):
    if a == True:
        if b == True:
            return True
        else:
            return False
    else:
        return False


def bin_xor(a, b):
    if a == True:
        if b == True:
            return False
        else:
            return True
    elif b == True:
        return True
    else:
        return False


def status_flags(active, verified, admin):
    if admin:
        if verified:
            return 'admin-verified'
        else:
            return 'admin-unverified'
    elif active:
        if verified:
            return 'user-verified'
        else:
            return 'user-unverified'
    else:
        return 'inactive'