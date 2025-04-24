import random

def _calculate_checksum(digits: str, prefix: str) -> str:
    weights = [2, 7, 6, 5, 4, 3, 2]
    sum_product = sum(int(d) * w for d, w in zip(digits, weights))

    if prefix in ['S', 'T']:
        checksum_chars = 'JZIHGFEDCBA'
    elif prefix in ['F', 'G']:
        checksum_chars = 'XWUTRQPNMLK'

    index = sum_product % 11
    return checksum_chars[index]

def _generate_nric_number() -> str:
    prefix = random.choice(['S', 'T', 'F', 'G'])
    digits = ''.join(str(random.randint(0, 9)) for _ in range(7))
    suffix = _calculate_checksum(digits, prefix)
    return f"{prefix}{digits}{suffix}"