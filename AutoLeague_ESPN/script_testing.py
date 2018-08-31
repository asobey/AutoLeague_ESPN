def solution(n):
    roman_out = ""
    digits = len(str(n))

    if digits == 4:
        if n // 1000 > 3:
            return 'out of range'
        else:
            roman_out += 'M' * (n//1000)
        n = n - n // 1000 * 1000
        digits = len(str(n))
    if digits == 3:
        if n // 100 == 9:
            roman_out += 'CM'
        elif n // 100 < 9 and n // 100 > 4:
            roman_out += ('D' + 'C' * (n // 100 - 5))
        elif n // 100 == 4:
            roman_out += 'CD'
        else:
            roman_out += 'C' * (n // 100)
        n = n - n // 100 * 100
        digits = len(str(n))
    if digits == 2:
        if n // 10 == 9:
            roman_out += 'XC'
        elif n // 10 < 9 and n // 10 > 4:
            roman_out += ('L' + 'X' * (n // 10 - 5))
        elif n // 10 == 4:
            roman_out += 'XL'
        else:
            roman_out += 'X' * (n // 10)
        n = n - n // 10 * 10
        digits = len(str(n))
    if digits == 1:
        if n == 9:
            roman_out += 'IX'
        elif n < 9 and n > 4:
            roman_out += ('V' + 'I' * (n - 5))
        elif n == 4:
            roman_out += 'IV'
        else:
            roman_out += 'I' * n
    return roman_out

if __name__ == '__main__':
    assert solution(1) == 'I', "solution(1),'I'"
    assert solution(4) == 'IV', "solution(4),'IV'"
    assert solution(6) == 'VI', "solution(6),'VI'"
    assert solution(14) == 'XIV', "solution(14),'XIV'"
    assert solution(21) == 'XXI', "solution(21),'XXI'"
    assert solution(91) == 'XCI', "solution(91),'XCI'"
    assert solution(984) == 'CMLXXXIV', "solution(984),'CMLXXXIV'"
    assert solution(1000) == 'M', 'solution(1000), M'
    assert solution(1889) == 'MDCCCLXXXIX', "solution(1889),'MDCCCLXXXIX'"
    assert solution(1989) == 'MCMLXXXIX', "solution(1989),'MCMLXXXIX'"