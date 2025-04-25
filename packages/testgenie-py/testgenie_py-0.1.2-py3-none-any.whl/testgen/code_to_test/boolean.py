from typing import List


def bin_and(a: bool, b: bool) ->bool:
    """
    >>> bin_and(True, False)
    False

    >>> bin_and(False, True)
    False

    >>> bin_and(False, False)
    False

    >>> bin_and(True, True)
    True
    """
    if a == True:
        if b == True:
            return True
        else:
            return False
    else:
        return False


def bin_xor(a: bool, b: bool) ->bool:
    """
    >>> bin_xor(True, True)
    False

    >>> bin_xor(True, False)
    True

    >>> bin_xor(False, False)
    False

    >>> bin_xor(False, True)
    True
    """
    if a == True:
        if b == True:
            return False
        else:
            return True
    elif b == True:
        return True
    else:
        return False


def status_flags(active: bool, verified: bool, admin: bool) ->str:
    """
    >>> status_flags(False, False, False)
    'inactive'

    >>> status_flags(False, False, True)
    'admin-unverified'

    >>> status_flags(True, True, False)
    'user-verified'

    >>> status_flags(True, True, True)
    'admin-verified'

    >>> status_flags(True, False, False)
    'user-unverified'

    >>> status_flags(False, True, True)
    'admin-verified'

    >>> status_flags(False, True, False)
    'inactive'

    >>> status_flags(True, False, True)
    'admin-unverified'
    """
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


"""def half_adder(a: bool, b: bool) ->tuple:
    sum: bool = bin_xor(a, b)
    carry: bool = bin_and(a, b)
    return sum, carry


def full_adder(a: bool, b: bool, carry_in: bool) ->tuple:
    sum1, carry = half_adder(a, b)
    sum2, carry_out = half_adder(sum1, carry_in)
    return sum2, carry or carry_out


def thirty_two_bit_adder_excep(x: int, y: int) ->List[int]:
    x_bits: List[int] = bit_converter(x)
    y_bits: List[int] = bit_converter(y)
    result: List[int] = [0] * 32
    carry: bool = False
    for i in range(32):
        try:
            sum_bit, carry = full_adder(x_bits[i], y_bits[i], carry)
            result[i] = sum_bit
        except IndexError as e:
            print(f'Index Out of Bounds Error In ThirtyTwoBitAdder: {e}')
            result = [1] * 32
        if carry:
            return OverflowError('Sum exceeds 32 bits')
    return result


def thirty_two_bit_adder(x: int, y: int) ->List[int]:
    print(x.bit_length() - 1)
    print(y.bit_length() - 1)
    x_bits: List[int] = bit_converter(x)
    y_bits: List[int] = bit_converter(y)
    result: List[int] = [0] * 32
    carry: bool = False
    for i in range(32):
        sum_bit, carry = full_adder(x_bits[i], y_bits[i], carry)
        result[i] = sum_bit
    return result

def bit_converter(num: int) ->List[int]:
    binary_str: str = bin(num)[2:]
    print(bin(num)[2:])
    return [int(digit) for digit in binary_str]

def thirty_two_bit_adder_excep(x: int, y: int) ->List[int]:
    x_bits: List[int] = bit_converter(x)
    y_bits: List[int] = bit_converter(y)
    result: List[int] = [0] * 32
    carry: bool = False
    for i in range(32):
        sum_bit, carry = full_adder(x_bits[i], y_bits[i], carry)
        result[i] = sum_bit
    return result"""
