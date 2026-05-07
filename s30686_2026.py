# Numer albumu: s30686
# Data: 2026-05-07
# Opis: Wersja podstawowa - Generator losowych sekwencji w formacie FASTA.

import random


def validate_positive_int(prompt: str, min_val: int = 1, max_val: int = 100_000) -> int:
    while True:
        odpowiedz = input(prompt)
        try:
            liczba = int(odpowiedz)
            if liczba >= min_val and liczba <= max_val:
                return liczba
            else:
                print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")
        except:
            print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")


def generate_sequence(length: int) -> str:
    nukleotydy = ['A', 'C', 'G', 'T']
    wynik = ""
    for i in range(length):
        wynik += random.choice(nukleotydy)
    return wynik


def calculate_stats(sequence: str) -> dict:
    dlugosc = len(sequence)
    if dlugosc == 0:
        return {"A": 0.0, "C": 0.0, "G": 0.0, "T": 0.0, "GC": 0.0}

    ile_a = sequence.count('A')
    ile_c = sequence.count('C')
    ile_g = sequence.count('G')
    ile_t = sequence.count('T')

    a_proc = (ile_a / dlugosc) * 100
    c_proc = (ile_c / dlugosc) * 100
    g_proc = (ile_g / dlugosc) * 100
    t_proc = (ile_t / dlugosc) * 100
    gc_proc = g_proc + c_proc

    return {"A": a_proc, "C": c_proc, "G": g_proc, "T": t_proc, "GC": gc_proc}


def insert_name(sequence: str, name: str) -> str:
    if len(sequence) == 0:
        return name.lower()
    losowa_pozycja = random.randint(0, len(sequence))
    lewa_strona = sequence[:losowa_pozycja]
    prawa_strona = sequence[losowa_pozycja:]
    return lewa_strona + name.lower() + prawa_strona


def format_fasta(seq_id: str, description: str, sequence: str, line_width: int = 80) -> str:
    if description != "":
        naglowek = f">{seq_id} {description}\n"
    else:
        naglowek = f">{seq_id}\n"

    sformatowana_sekwencja = ""
    for i in range(0, len(sequence), line_width):
        kawalek = sequence[i:i + line_width]
        sformatowana_sekwencja += kawalek + "\n"

    return naglowek + sformatowana_sekwencja


def pobierz_id():
    while True:
        seq_id = input("Podaj ID sekwencji: ")
        if " " in seq_id or "\t" in seq_id or seq_id == "":
            print("Błąd: ID nie może zawierać białych znaków i nie może być puste.")
        else:
            return seq_id


def main():
    dlugosc = validate_positive_int("Podaj długość sekwencji: ")
    seq_id = pobierz_id()
    opis = input("Podaj opis sekwencji: ")
    imie = input("Podaj imię: ")

    czysta_sekwencja = generate_sequence(dlugosc)

    statystyki = calculate_stats(czysta_sekwencja)
    print(f"\nStatystyki sekwencji (n={dlugosc}):")
    print(f"A: {statystyki['A']:.2f}%")
    print(f"C: {statystyki['C']:.2f}%")
    print(f"G: {statystyki['G']:.2f}%")
    print(f"T: {statystyki['T']:.2f}%")
    print(f"GC-content: {statystyki['GC']:.2f}%\n")

    sekwencja_z_imieniem = insert_name(czysta_sekwencja, imie)

    nazwa_pliku = f"{seq_id}.fasta"
    plik = open(nazwa_pliku, 'w')

    tekst_fasta = format_fasta(seq_id, opis, sekwencja_z_imieniem)
    plik.write(tekst_fasta)
    plik.close()

    print(f"Zapisano plik: {nazwa_pliku}")


if __name__ == "__main__":
    main()