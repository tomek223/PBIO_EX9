# Numer albumu: s30686
# Data: 2026-05-07
# Opis: Generator losowych sekwencji w formacie FASTA.
# Program wylicza GC-content i statystyki.
# Dodatkowe 4 funkcje: szukanie motywu, komplementarnosc, mRNA, translacja.

import random


def validate_positive_int(prompt: str, min_val: int = 1, max_val: int = 100_000) -> int:
    """Pobiera od użytkownika liczbę całkowitą z zakresu.
    W przypadku błędu powtarza pytanie."""
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
    """Zwraca losową sekwencję DNA o zadanej długości."""
    nukleotydy = ['A', 'C', 'G', 'T']
    wynik = ""
    # Prosta pętla budująca sekwencję znak po znaku
    for i in range(length):
        wynik += random.choice(nukleotydy)
    return wynik


def calculate_stats(sequence: str) -> dict:
    """Zwraca słownik ze statystykami sekwencji.
    Klucze: "A", "C", "G", "T" (wartości float, %),
    "GC" (wartość float, %)."""
    dlugosc = len(sequence)
    if dlugosc == 0:
        return {"A": 0.0, "C": 0.0, "G": 0.0, "T": 0.0, "GC": 0.0}

    # Ręczne liczenie nukleotydów - typowe dla początkujących
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
    """Wstawia imię w losową pozycję sekwencji.
    Imię zapisane małymi literami."""
    if len(sequence) == 0:
        return name.lower()

    losowa_pozycja = random.randint(0, len(sequence))
    lewa_strona = sequence[:losowa_pozycja]
    prawa_strona = sequence[losowa_pozycja:]

    return lewa_strona + name.lower() + prawa_strona


def format_fasta(seq_id: str, description: str, sequence: str, line_width: int = 80) -> str:
    """Zwraca sformatowany rekord FASTA jako string."""
    if description != "":
        naglowek = f">{seq_id} {description}\n"
    else:
        naglowek = f">{seq_id}\n"

    sformatowana_sekwencja = ""
    # Krokowe łamanie linii w prostej pętli
    for i in range(0, len(sequence), line_width):
        kawalek = sequence[i:i + line_width]
        sformatowana_sekwencja += kawalek + "\n"

    return naglowek + sformatowana_sekwencja



# FUNKCJONALNOŚCI DODATKOWE


def znajdz_motyw(sekwencja, motyw):
    """Wyszukuje podany motyw i zwraca listę jego pozycji."""
    pozycje = []
    motyw = motyw.upper()
    dlugosc_motywu = len(motyw)

    for i in range(len(sekwencja) - dlugosc_motywu + 1):
        # Wycinamy fragment z sekwencji i przyrównujemy
        fragment = sekwencja[i:i + dlugosc_motywu]
        if fragment == motyw:
            pozycje.append(i + 1)
    return pozycje


def komplementarna_i_odwrotna(sekwencja):
    """Zamienia nukleotydy na komplementarne i odwraca nić."""
    nic_komp = ""
    for znak in sekwencja:
        if znak == 'A':
            nic_komp += 'T'
        elif znak == 'T':
            nic_komp += 'A'
        elif znak == 'C':
            nic_komp += 'G'
        elif znak == 'G':
            nic_komp += 'C'
        else:
            nic_komp += znak

    # Odwrócenie stringa
    odwrotna_komp = nic_komp[::-1]
    return nic_komp, odwrotna_komp


def transkrypcja_rna(sekwencja):
    """Prosta zamiana T na U dla sekwencji mRNA."""
    mrna = sekwencja.replace('T', 'U')
    return mrna


def translacja_bialka(sekwencja):
    """Tłumaczy DNA na kodony i przypisuje aminokwasy."""
    # Podstawowa tabela kodonów
    kodony = {
        'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
        'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
        'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K',
        'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
        'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
        'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
        'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
        'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
        'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
        'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E',
        'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
        'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
        'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
        'TAC': 'Y', 'TAT': 'Y', 'TAA': '*', 'TAG': '*', 'TGA': '*',
        'TGC': 'C', 'TGT': 'C', 'TGG': 'W',
    }
    bialko = ""
    # Pętla po 3 nukleotydy
    for i in range(0, len(sekwencja), 3):
        kawalek = sekwencja[i:i + 3]
        if len(kawalek) == 3:
            if kawalek in kodony:
                bialko += kodony[kawalek]
            else:
                bialko += "?"
    return bialko


def pobierz_id():
    """Pobiera ID bez spacji i tabulatorów."""
    while True:
        seq_id = input("Podaj ID sekwencji: ")
        if " " in seq_id or "\t" in seq_id or seq_id == "":
            print("Błąd: ID nie może zawierać białych znaków i nie może być puste.")
        else:
            return seq_id


def main():
    """Wiadomo."""
    # Pobieranie danych
    dlugosc = validate_positive_int("Podaj długość sekwencji: ")
    seq_id = pobierz_id()
    opis = input("Podaj opis sekwencji: ")
    imie = input("Podaj imię: ")

    # Wygenerowanie czystej biologicznej sekwencji
    czysta_sekwencja = generate_sequence(dlugosc)

    # Obliczenie i wypisanie statystyk
    statystyki = calculate_stats(czysta_sekwencja)
    print(f"\nStatystyki sekwencji (n={dlugosc}):")
    print(f"A: {statystyki['A']:.2f}%")
    print(f"C: {statystyki['C']:.2f}%")
    print(f"G: {statystyki['G']:.2f}%")
    print(f"T: {statystyki['T']:.2f}%")
    print(f"GC-content: {statystyki['GC']:.2f}%\n")

    # Wstawienie imienia (wyłącznie do zapisu pierwszej sekwencji)
    sekwencja_z_imieniem = insert_name(czysta_sekwencja, imie)

    # Przygotowanie do zapisu multi-FASTA
    nazwa_pliku = f"{seq_id}.fasta"
    plik = open(nazwa_pliku, 'w')

    # Zapis bazowej sekwencji z imieniem
    tekst_fasta = format_fasta(seq_id, opis, sekwencja_z_imieniem)
    plik.write(tekst_fasta)

    # 1. Transkrypcja (korzysta z czystej_sekwencji bez imienia)
    mrna = transkrypcja_rna(czysta_sekwencja)
    plik.write(format_fasta(f"{seq_id}_mRNA", "Transkrypcja", mrna))

    # 2. Komplementarność
    nic_komp, odwrotna_komp = komplementarna_i_odwrotna(czysta_sekwencja)
    plik.write(format_fasta(f"{seq_id}_komp", "Nic komplementarna", nic_komp))
    plik.write(format_fasta(f"{seq_id}_odwrotna", "Nic odwrotnie komplementarna", odwrotna_komp))

    # 3. Translacja
    bialko = translacja_bialka(czysta_sekwencja)
    plik.write(format_fasta(f"{seq_id}_bialko", "Translacja", bialko))

    plik.close()
    print(f"Zapisano plik: {nazwa_pliku}")

    # 4. Wyszukiwanie motywu
    motyw = input("\nPodaj motyw do wyszukania (np. ATG): ")
    if motyw != "":
        pozycje = znajdz_motyw(czysta_sekwencja, motyw)
        if len(pozycje) > 0:
            print(f"Znaleziono motyw '{motyw.upper()}' na pozycjach: {pozycje}")
        else:
            print(f"Nie znaleziono motywu '{motyw.upper()}'.")


if __name__ == "__main__":
    main()