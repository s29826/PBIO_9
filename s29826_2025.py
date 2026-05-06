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


def generate_sequence_with_distribution(length: int, distribution: dict) -> str:
    """Generuje losową sekwencję DNA z konfigurowalnym rozkładem nukleotydów

    Args:
        length (int): Długość generowanej sekwencji
        distribution (dict): Słownik z procentowym udziałem każdego nukleotydu
                             np. {'A': 30, 'C': 20, 'G': 20, 'T': 30}

    Returns: str: Losowa sekwencja DNA o podanej długości i zadanym rozkładzie
    """
    bases = list(distribution.keys())
    weights = [distribution[b] for b in bases]
    output = ""

    for _ in range(length):
        output += random.choices(bases, weights=weights, k=1)[0]

    return output


def get_nucleotide_distribution() -> dict:
    """Pobiera od użytkownika procentowy udział każdego nukleotydu i waliduje dane

    Pętla działa dopóki suma procentów nie wynosi dokładnie 100

    Returns: dict: Słownik z procentowym udziałem A, C, G, T (wartości całkowite)
    """
    while True:
        distribution = {}
        print("Podaj procentowy udział każdego nukleotydu (liczby całkowite, suma = 100):")

        valid = True
        for base in ['A', 'C', 'G', 'T']:
            value = input(f"  {base} [%]: ")
            if value.isdigit():
                distribution[base] = int(value)
            else:
                print(f"Błąd: wartość dla {base} musi być nieujemną liczbą całkowitą.")
                valid = False
                break

        if not valid:
            continue

        total = sum(distribution.values())
        if total == 100:
            return distribution
        else:
            print(f"Błąd: suma procentów wynosi {total}%, a musi wynosić dokładnie 100%.")


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


def find_motifs(sequence: str, motif: str) -> list:
    """Wyszukuje wszystkie wystąpienia motywu w sekwencji DNA

    Przeszukuje sekwencję i zwraca pozycje zgodne z konwencją biologiczną
    (indeksowanie od 1). Przy przeszukiwaniu ignoruje małe litery (wstawione imię)

    Args:
        sequence (str): Sekwencja DNA (może zawierać wstawione imię małymi literami)
        motif (str): Szukany motyw (np. "ATG")

    Returns: list: Lista pozycji (int) wystąpień motywu, indeksowanych od 1;
                   pusta lista jeśli motyw nie został znaleziony
    """
    bio_seq = ""
    for c in sequence:
        if c.isupper():
            bio_seq += c

    motif = motif.upper()
    positions = []
    start = 0

    while True:
        pos = bio_seq.find(motif, start)
        if pos == -1:
            break
        positions.append(pos + 1)  # konwencja biologiczna: indeksowanie od 1
        start = pos + 1

    return positions


def transcribe_to_mrna(sequence: str) -> str:
    """Przeprowadza transkrypcję in silico: generuje sekwencję mRNA z sekwencji DNA

    Zamiana T na U zgodnie z zasadą transkrypcji (nić kodująca → mRNA)
    Małe litery (wstawione imię) są pomijane – mRNA zawiera wyłącznie nukleotydy

    Args: sequence (str): Sekwencja DNA (może zawierać wstawione imię małymi literami)

    Returns: str: Sekwencja mRNA złożona z nukleotydów A, C, G, U
    """
    mrna = ""
    for c in sequence:
        if c.isupper():
            if c == 'T':
                mrna += 'U'
            else:
                mrna += c

    return mrna


def get_complementary_strands(sequence: str) -> tuple:
    """Generuje nić komplementarną oraz nić odwrotnie komplementarną sekwencji DNA

    Komplementarność zasad: A ↔ T, C ↔ G
    Nić odwrotnie komplementarna (reverse complement) to nić komplementarna
    odczytana w kierunku 3' → 5', co odpowiada nici antysensowej odczytanej 5' →3'
    Małe litery (wstawione imię) są pomijane – obie nici zawierają wyłącznie nukleotydy

    Args: sequence (str): Sekwencja DNA (może zawierać wstawione imię małymi literami)

    Returns: tuple: Para (nić_komplementarna, nić_odwrotnie_komplementarna) jako str
    """
    complement_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

    bio_seq = ""
    for c in sequence:
        if c.isupper():
            bio_seq += c

    complementary = ""
    for base in bio_seq:
        complementary += complement_map.get(base, base)

    reverse_complement = complementary[::-1]

    return complementary, reverse_complement


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

    # Wybór trybu generowania sekwencji
    print("\nCzy chcesz użyć własnego rozkładu nukleotydów? (t/n): ", end="")
    use_custom = input().strip().lower()

    if use_custom == 't':
        distribution = get_nucleotide_distribution()
        sequence = generate_sequence_with_distribution(length, distribution)
    else:
        sequence = generate_sequence(length)

    # Statystyki i sekwencja z imieniem
    stats = calculate_stats(sequence)
    sequence_with_name = insert_name(sequence, name)

    # Wyszukiwanie motywu
    motif = input("\nPodaj motyw do wyszukania (np. ATG), lub Enter aby pominąć: ").strip()
    if motif:
        positions = find_motifs(sequence_with_name, motif)
        if positions:
            print(f"Motyw '{motif.upper()}' znaleziono na pozycjach (1-based): {positions}")
        else:
            print(f"Motyw '{motif.upper()}' nie został znaleziony w sekwencji.")

    # Transkrypcja in silico
    mrna_sequence = transcribe_to_mrna(sequence_with_name)

    # Sekwencja komplementarna i odwrotnie komplementarna
    complementary, reverse_complement = get_complementary_strands(sequence_with_name)

    # Zapis do pliku FASTA (sekwencja oryginalna + mRNA + komplementarna + odwrotnie komplementarna)
    fasta_content = format_fasta(seq_id, description, sequence_with_name)
    fasta_content += format_fasta(f"{seq_id}_mRNA", f"transkrypt mRNA | {description}", mrna_sequence)
    fasta_content += format_fasta(f"{seq_id}_COMP", f"nic komplementarna | {description}", complementary)
    fasta_content += format_fasta(f"{seq_id}_REVCOMP", f"nic odwrotnie komplementarna | {description}", reverse_complement)

    filename = f"{seq_id}.fasta"
    with open(filename, 'w') as f:
        f.write(fasta_content)

    # Wyświetlenie wyników
    print(f"\nSekwencja zapisana do pliku: {filename}")
    print(f"Statystyki sekwencji (n={length}):")
    print(f"  A: {stats['A']:.2f}%")
    print(f"  C: {stats['C']:.2f}%")
    print(f"  G: {stats['G']:.2f}%")
    print(f"  T: {stats['T']:.2f}%")
    print(f"  GC-content: {stats['gc']:.2f}%")
    print(f"\nDo pliku dopisano rekordy: mRNA, nić komplementarna, nić odwrotnie komplementarna.")


if __name__ == '__main__':
    main()