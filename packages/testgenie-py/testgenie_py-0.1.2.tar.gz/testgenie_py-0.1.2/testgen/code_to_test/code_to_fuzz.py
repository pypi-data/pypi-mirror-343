from typing import List


def bin_and(a: bool, b: bool) ->bool:
    """"
    >>> bin_and(True, True)
    True
    >>> bin_and(True, False)
    False
    >>> bin_and(False, True)
    False
    >>> bin_and(False, False)
    False

    Examples:
    >>> bin_and(True, False)
    False"""
    if a == True:
        if b == True:
            return True
        else:
            return False
    else:
        return False


def bin_or(a: bool, b: bool) ->bool:
    """"
>>> bin_or(True, True)
True
>>> bin_or(True, False)
True
>>> bin_or(False, True)
True
>>> bin_or(False, False)
False

Examples:
>>> bin_or(False, True)
True"""
    return a | b


def bin_xor(a: bool, b: bool) ->bool:
    """>>> bin_xor(True, True)
False
>>> bin_xor(True, False)
True
>>> bin_xor(False, True)
True
>>> bin_xor(False, False)
False

Examples:
>>> bin_xor(True, True)
False"""
    return a ^ b


def bin_nand(a: bool, b: bool) ->bool:
    """>>> bin_nand(True, True)
False
>>> bin_nand(True, False)
True
>>> bin_nand(False, True)
True
>>> bin_nand(False, False)
True

Examples:
>>> bin_nand(True, False)
True"""
    return not (a and b)


def bin_nor(a: bool, b: bool) ->bool:
    """>>> bin_nor(True, True)
False
>>> bin_nor(True, False)
False
>>> bin_nor(False, True)
False
>>> bin_nor(False, False)
True

Examples:
>>> bin_nor(False, True)
False"""
    return not a | b


def mux(c1: bool, c2: bool, x0: bool, x1: bool, x2: bool, x3: bool) ->bool:
    """"
>>> mux(1, 1, True, False, False, False)
True
>>> mux(1, 0, False, True, False, False)
True
>>> mux(0, 1, False, False, True, False)
True
>>> mux(0, 0, False, False, False, True)
True
>>> mux(0, 0, False, False, False, False)
False

Examples:
>>> mux(False, False, False, False, False, True)
True"""
    return (c1 and c2 and x0) | (c1 and not c2 and x1) | (not c1 and c2 and x2
        ) | (not c1 and not c2 and x3)


def bin_and_bad(a: bool, b: bool) ->bool:
    """"
>>> bin_and(True, True)
True
>>> bin_and(True, False)
False
>>> bin_and(False, True)
False
>>> bin_and(False, False)
False

Examples:
>>> bin_and_bad(False, True)
True"""
    if a == True and b == True:
        return a and b
    return a or b


def bin_or_bad(a: bool, b: bool) ->bool:
    """"
>>> bin_or(True, True)
True
>>> bin_or(True, False)
True
>>> bin_or(False, True)
True
>>> bin_or(False, False)
False

Examples:
>>> bin_or_bad(True, True)
False"""
    return not a | b


def bit_converter_excep(num: int) ->List[int]:
    """>>> bit_converter_excep(30)
[1, 1, 1, 1, 0]"""
    bs = bin(num)
    binary_str = bs[2:]
    try:
        return [int(digit) for digit in binary_str]
    except Exception as e:
        print(binary_str)
        print(bs)
        print(f'Invalid Literal Exception in Bit Converter: {e}')
        return


def bit_converter(num: int) ->List[int]:
    """
    >>> bit_converter(25)
    [1, 1, 0, 0, 1]
    """
    binary_str: str = bin(num)[2:]
    print(bin(num)[2:])
    return [int(digit) for digit in binary_str]


def half_adder(a: bool, b: bool) ->tuple:
    """>>> half_adder(True, True)
(False, True)"""
    sum: bool = bin_xor(a, b)
    carry: bool = bin_and(a, b)
    return sum, carry


def full_adder(a: bool, b: bool, carry_in: bool) ->tuple:
    """>>> full_adder(True, False, False)
(True, False)"""
    sum1, carry = half_adder(a, b)
    sum2, carry_out = half_adder(sum1, carry_in)
    return sum2, carry or carry_out


def thirty_two_bit_adder_excep(x: int, y: int) ->List[int]:
    """>>> thirty_two_bit_adder_excep(9, 3)
None

Examples:
>>> thirty_two_bit_adder_excep(34, 1)
None"""
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
    """>>> thirty_two_bit_adder(8, 45)
None"""
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


def thirty_two_bit_adder_excep(x: int, y: int) ->List[int]:
    x_bits: List[int] = bit_converter(x)
    y_bits: List[int] = bit_converter(y)
    result: List[int] = [0] * 32
    carry: bool = False
    for i in range(32):
        sum_bit, carry = full_adder(x_bits[i], y_bits[i], carry)
        result[i] = sum_bit
    return result
