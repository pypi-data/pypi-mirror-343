import random


def generate_thailand_identity_number(num_records: int = 1) -> list[str]:
    """
    Generates valid Thai national identity numbers.
    Each ID consists of 13 digits with a specific structure.
    """
    thai_id = []

    def generate_first_digit():
        return str(random.randint(1, 8))

    def generate_birth_area_code():
        return f'{random.randint(0, 9999):04d}'

    def generate_sequence_number():
        return f'{random.randint(0, 99999):05d}'

    def generate_additional_digits():
        return f'{random.randint(0, 99):02d}'

    def calculate_check_digit(id_number):
        total = 0
        for i in range(12):
            total += int(id_number[i]) * (13 - i)
        check_digit = (11 - (total % 11)) % 10
        return str(check_digit)

    def generate_thai_id():
        first_digit = generate_first_digit()
        birth_area_code = generate_birth_area_code()
        sequence_number = generate_sequence_number()
        additional_digit = generate_additional_digits()
        partial_id = first_digit + birth_area_code + sequence_number + additional_digit
        check_digit = calculate_check_digit(partial_id)
        return partial_id + check_digit

    for _ in range(num_records):
        id_number = generate_thai_id()
        thai_id.append(id_number)

    return thai_id
