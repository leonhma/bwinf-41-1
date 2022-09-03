from os import path
from re import findall
from time import time
from typing import List


def r_path(path_: str) -> str:
    return path.join(
        path.dirname(path.abspath(__file__)),
        path_
    )


# laden des buchs als wörter-array
words_in_book: List[str]

with open(r_path('beispieldaten/Alice_im_Wunderland.txt'), 'r') as f:
    words_in_book = list(map(lambda x: x[0].lower(), findall('(\\w+?)(\\W|$)', f.read())))


# hauptprogramm; worstcase O(n*k)
def main():
    print()
    bsp_nr = int(input('Bitte die Nummer des Beispiels eingeben [0; 5]: '))

    print()

    start_time = time()  # variable für die zeitmessung

    # laden des beispielsatzes
    sentence: List[str]
    with open(r_path(f'beispieldaten/stoerung{bsp_nr}.txt'), 'r') as f:
        text = f.read()
        print(text)
        sentence = text.split()
    print()

    # iterieren über das wörterarray und vergleichen mit dem beispielsatz
    results: List[str] = []
    for left in range(len(words_in_book) - len(sentence)):
        right = left
        for next_word in sentence:
            if (words_in_book[right] == next_word) or next_word == '_':
                right += 1
            else:
                break
        else:
            results.append(' '.join(words_in_book[left:right]))

    # ergebnisse ausgeben
    if len(results) == 0:
        print(f"Kein Ergebnis gefunden! ({format((time()-start_time)*1000, '.2f')}ms)")
    else:
        print(f"{len(results)} Ergebnis{'se' if len(results) > 1 else ''} gefunden: ({format((time()-start_time)*1000, '.2f')}ms)")
        print()
        for result in results:
            print(f'> {result}')


# programmschleife
print('Lieblingsbuchzitatfinder')
print('(Drücke ^C um das Programm zu beenden)')
print()
print('Buch: Alice im Wunderland')

while True:
    try:
        main()
    except Exception as e:
        print(e)
