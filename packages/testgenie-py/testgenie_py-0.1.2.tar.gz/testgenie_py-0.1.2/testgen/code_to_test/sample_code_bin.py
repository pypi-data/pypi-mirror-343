from typing import List

class SampleCodeBin:
    def bin_and(self, a: bool, b: bool) -> bool:
        """
        >>> SampleCodeBin().bin_and(False, False)
        False
        """
        return a and b

    def bin_or(self, a: bool, b: bool) -> bool:
        """
        >>> SampleCodeBin().bin_or(False, False)
        False
        """
        return a | b

    def bin_xor(self, a: bool, b: bool) -> bool:
        """
        >>> SampleCodeBin().bin_xor(True, True)
        False
        """
        return a ^ b

    def bin_nand(self, a: bool, b: bool) -> bool:
        """
        >>> SampleCodeBin().bin_nand(True, False)
        True
        """
        return not(a and b)

    def bin_nor(self, a: bool, b:bool) -> bool:
        """
        >>> SampleCodeBin().bin_nor(True, False)
        False
        """
        return not(a | b)

    def mux(self, c1: bool, c2: bool, x0: bool, x1: bool, x2: bool, x3: bool) -> bool:
        """
        >>> SampleCodeBin().mux(True, True, True, False, True, False)
        True
        """
        return (c1 and c2 and x0) | (c1 and (not(c2)) and x1) | (not(c1) and c2 and x2) | (not(c1) and not(c2) and x3)

    def bin_and_bad(self, a: bool, b: bool) -> bool:
        """
        >>> SampleCodeBin().bin_and_bad(True, True)
        True
        >>> SampleCodeBin().bin_and_bad(False, True)
        True
        """
        if(a == True and b == True):
            return a and b
        return a or b

    def bin_or_bad(self, a: bool, b: bool) -> bool:
        """
        >>> SampleCodeBin().bin_or_bad(False, False)
        True
        """
        return not(a | b)

    """def bit_converter_excep(self, num: int) -> List[int]:
        # binary_str: str = bin(num)[2:]
        bs = bin(num)
        binary_str = bs[2:]
        try:
            return [int(digit) for digit in binary_str]
        except Exception as e:
            print(binary_str)
            print(bs)
            print(f"Invalid Literal Exception in Bit Converter: {e}")
            return

    def bit_converter(self, num: int) -> List[int]:
        binary_str: str = bin(num)[2:]
        return [int(digit) for digit in binary_str]

    def half_adder(self, a: bool, b: bool) -> tuple:
        sum: bool = self.bin_xor(a, b)
        carry: bool = self.bin_and(a, b)
        return (sum, carry)

    def full_adder(self, a: bool, b: bool, carry_in: bool) -> tuple:
        sum1, carry = self.half_adder(a, b)
        sum2, carry_out = self.half_adder(sum1, carry_in)
        return (sum2, carry or carry_out)

    def thirty_two_bit_adder_excep(self, x: int, y: int) -> List[int]:
        x_bits: List[int] = self.bit_converter(x)
        y_bits: List[int] = self.bit_converter(y)
        result: List[int] = [0] * 32
        carry: bool = False

        for i in range(32):
            try: 
                sum_bit, carry = self.full_adder(x_bits[i], y_bits[i], carry)
                result[i] = sum_bit
            except IndexError as e:
                print(f"Index Out of Bounds Error In ThirtyTwoBitAdder: {e}")
                result = [1] * 32

            if carry:
                return OverflowError("Sum exceeds 32 bits")

        return result

    def thirty_two_bit_adder(self, x: int, y: int) -> List[int]:
        print(x.bit_length() - 1)
        print(y.bit_length() -1)
        x_bits: List[int] = self.bit_converter(x)
        y_bits: List[int] = self.bit_converter(y)

        #if(len(x_bits) > 32 or len(y_bits) >= 32):
        #    print(f"Length of bit list greater than 32")

        result: List[int] = [0] * 32
        carry: bool = False

        for i in range(32):
            sum_bit, carry = self.full_adder(x_bits[i], y_bits[i], carry)
            result[i] = sum_bit

        return result


    def thirty_two_bit_adder_excep(self, x: int, y: int) -> List[int]:
        #print(x.bit_length - 1)
        #peint(x.bit_length - 1)
        x_bits: List[int] = self.bit_converter(x)
        y_bits: List[int] = self.bit_converter(y)

        result: List[int] = [0] * 32
        carry: bool = False

        for i in range(32):
            sum_bit, carry = self.full_adder(x_bits[i], y_bits[i], carry)
            result[i] = sum_bit

        return result"""