def password_strength(pwd: str) ->str:
    """>>> password_strength('abc')
'weak'"""
    if len(pwd) < 6:
        return 'weak'
    elif len(pwd) < 10:
        if any(c.isdigit() for c in pwd):
            return 'medium'
        else:
            return 'weak'
    elif any(c.isdigit() for c in pwd) and any(c.isupper() for c in pwd):
        return 'strong'
    else:
        return 'medium'


def email_type(email: str) ->str:
    """>>> email_type('abc')
'invalid'"""
    if not email or '@' not in email:
        return 'invalid'
    elif email.endswith('@school.edu'):
        return 'school'
    elif email.endswith('@company.com'):
        return 'work'
    elif email.endswith('@gmail.com') or email.endswith('@yahoo.com'):
        return 'personal'
    else:
        return 'unknown'


def http_code(code: int) ->str:
    """>>> http_code(85)
'invalid'"""
    if code < 100 or code > 599:
        return 'invalid'
    elif 100 <= code < 200:
        return 'informational'
    elif 200 <= code < 300:
        return 'success'
    elif 300 <= code < 400:
        return 'redirection'
    elif 400 <= code < 500:
        return 'client error'
    else:
        return 'server error'


def add_or_subtract(x: int, y: int) ->int:
    """>>> add_or_subtract(87, 100)
187"""
    result = x
    if x < y:
        result += y
    else:
        result -= y
    return result
