from ._internal import _generate_nric_number

def generate_nric(count: int = 1) -> list[str]:
    return [_generate_nric_number() for _ in range(count)]