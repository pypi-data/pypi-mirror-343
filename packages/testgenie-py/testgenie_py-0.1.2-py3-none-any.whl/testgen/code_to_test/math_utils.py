def categorize_number(n: int) -> str:
    if n < 0:
        return "negative"
    elif n == 0:
        return "zero"
    elif 0 < n < 10:
        return "small"
    elif 10 <= n < 100:
        return "medium"
    else:
        return "large"

def complex_divide(a: int, b: int) -> float:
    if b == 0:
        return float("inf")
    elif a == 0:
        return 0.0
    elif a == b:
        return 1.0
    elif a > b:
        return a / b
    else:
        return -1 * (a / b)
    
def pos_or_neg(i: int) -> int:
    if i > 0:
        sgn = 1
    else:
        sgn = -1
    if sgn > 0:
        return 1
    elif sgn < 0:
        return -1
    
def is_even(x: int) -> bool:
    if x % 2 == 0:
        return True
    else:
        return False
    
def is_odd(x: int) -> bool:
    if x % 2 != 0:
        return True
    else:
        return False
    

