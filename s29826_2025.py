# Numer albumu: 29826
# Data: 06.05.2026
# Opis programu: Generator losowych sekwencji DNA w formacie FASTA z podstawowymi statystykami nukleotydów

import random


def generate_sequence(length: int) -> str:
    """Generuje losową sekwencję DNA złożoną z nukleotydów A, C, T, G

    Args: length (int): Długość generowanej sekwencji

    Returns: str: Losowa sekwencja DNA o podanej długości
    """
    codes = ['A', 'C', 'T', 'G']
    output = ""

    for _ in range(length):
        output += random.choice(codes)

    return output


def calculate_stats(sequence: str) -> dict:
    """Oblicza procentowy udział każdego nukleotydu oraz zawartość GC

    Wielkie litery to nukleotydy (A, C, G, T); małe litery to wstawione imię,
    które jest pomijane przy obliczeniach

    Args: sequence (str): Sekwencja DNA (może zawierać wstawione imię małymi literami)

    Returns: dict: Słownik z procentami A, C, G, T oraz kluczem 'gc' (GC-content)
    """
    bio_seq = ""
    for c in sequence:
        if c.isupper():
            bio_seq += c

    n = len(bio_seq)

    counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
    for nucleotide in bio_seq:
        if nucleotide in counts:
            counts[nucleotide] += 1

    stats = {base: (count / n * 100) for base, count in counts.items()}
    stats['gc'] = stats['G'] + stats['C']

    return stats


def insert_name(sequence: str, name: str) -> str:
    """Wstawia imię (małymi literami) w losowe miejsce sekwencji

    Małe litery pozwalają odróżnić imię od nukleotydów przy obliczaniu statystyk

    Args:
        sequence (str): Oryginalna sekwencja DNA
        name (str): Imię do wstawienia

    Returns: str: Sekwencja z wstawionym imieniem
    """
    position = random.randint(0, len(sequence))

    return sequence[:position] + name.lower() + sequence[position:]


def format_fasta(seq_id: str, description: str,
                 sequence: str, line_width: int = 80) -> str:
    """Formatuje sekwencję do standardowego formatu FASTA

    Args:
        seq_id (str): Identyfikator sekwencji
        description (str): Opis sekwencji (może być pusty)
        sequence (str): Sekwencja DNA do sformatowania
        line_width (int): Maksymalna długość wiersza (domyślnie 80)

    Returns: str: Sformatowany rekord FASTA zakończony znakiem nowej linii
    """
    header = f">{seq_id} {description}" if description else f">{seq_id}"
    # Zapewniamy łamanie sekwencji na linie o szerkośći dokłądnie 80 znaków zgodnie z wymaganiami
    lines = [sequence[i:i + line_width] for i in range(0, len(sequence), line_width)]

    return header + '\n' + '\n'.join(lines) + '\n'


def validate_positive_int(prompt: str,
                          min_val: int = 1,
                          max_val: int = 100_000) -> int:
    """Waliduje dane wejściowe użytkownika (długość sekwencji)

    Pętla działa dopóki użytkownik nie poda poprawnej wartości całkowitej
    z zakresu [1, 100000]

    Returns: int: Zwalidowana długość sekwencji
    """
    not_validate = True

    while not_validate:
        sequence = input(prompt)
        if sequence.isdigit() and min_val <= int(sequence) <= max_val:
            not_validate = False
        else:
            print("Błąd: wartość musi być liczbą całkowitą z zakresu [1, 100000]")

    return int(sequence)


def main():
    # Dane wejściowe z walidacją
    length = validate_positive_int("Podaj długość sekwencji: ")

    # ID nie może być puste ani zawierać białych znaków (wymóg formatu FASTA)
    while True:
        seq_id = input("Podaj ID sekwencji: ")
        if seq_id and not any(c.isspace() for c in seq_id):
            break
        print("Błąd: ID nie może zawierać białych znaków ani być puste.")

    description = input("Podaj opis sekwencji: ")
    name = input("Podaj imię: ")

    # Generowanie i przetwarzanie sekwencji
    sequence = generate_sequence(length)
    stats = calculate_stats(sequence)
    sequence_with_name = insert_name(sequence, name)

    # Zapis do pliku FASTA
    fasta_content = format_fasta(seq_id, description, sequence_with_name)
    filename = f"{seq_id}.fasta"

    with open(filename, 'w') as f:
        f.write(fasta_content)

    # Wyświetlenie wyników
    print(f"Sekwencja zapisana do pliku: {filename}")
    print(f"Statystyki sekwencji (n={length}):")
    print(f"  A: {stats['A']:.2f}%")
    print(f"  C: {stats['C']:.2f}%")
    print(f"  G: {stats['G']:.2f}%")
    print(f"  T: {stats['T']:.2f}%")
    print(f"  GC-content: {stats['gc']:.2f}%")


if __name__ == '__main__':
    main()
