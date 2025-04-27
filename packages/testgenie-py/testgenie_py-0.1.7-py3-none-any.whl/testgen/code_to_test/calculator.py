class AdvancedCalculator:

    def evaluate(self, a: int, b: int, op: str) ->(int | float | str):
        """>>> AdvancedCalculator().evaluate(16, 56, 'abc')
'invalid'"""
        if op == 'add':
            return a + b
        elif op == 'sub':
            return a - b
        elif op == 'mul':
            return a * b
        elif op == 'div':
            if b == 0:
                return 'undefined'
            return a / b
        else:
            return 'invalid'

    def is_in_range(self, val: float) ->str:
        """>>> AdvancedCalculator().is_in_range(0.4023417704905361)
'fractional'"""
        if val < 0.0:
            return 'below zero'
        elif 0.0 <= val < 1.0:
            return 'fractional'
        elif 1.0 <= val <= 100.0:
            return 'valid'
        else:
            return 'out of range'
