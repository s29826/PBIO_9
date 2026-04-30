import random


def validate_length_of_sequence() -> int:
    not_validate = True

    while not_validate:
        sequence = input("Podaj długość sekwencji: ")
        if sequence.isdigit() and 1 <= int(sequence) <= 100000:
            not_validate = False
        else:
            print("Błąd: wartość musi być liczbą całkowitą z zakresu [1, 100000]")

    return int(sequence)


def generate_sequence(length: int) -> str:
    codes = ['A', 'C', 'T', 'G']
    output = ""

    for _ in range(length):
        output += random.choice(codes)

    return output


def calculate_stats(sequence: str) -> dict:

    return None


def insert_name(sequence: str, name: str) -> str:

    return None


def format_fasta(seq_id: str, description: str,
                 sequence: str, line_width: int = 80) -> str:

    return ""


def validate_positive_int(prompt: str,
                          min_val: int = 1,
                          max_val: int = 100_000) -> int:

    return 0


def main():
    print(generate_sequence(validate_length_of_sequence()))


if __name__ == '__main__':
    main()
