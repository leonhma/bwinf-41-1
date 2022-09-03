from itertools import chain
from os import path
from re import findall
from time import time
from typing import List, Tuple


def r_path(path_: str) -> str:
    return path.join(
        path.dirname(path.abspath(__file__)),
        path_
    )


# die wörter-liste
book: Tuple[Tuple[int, str]]

with open(r_path('beispieldaten/Alice_im_Wunderland.txt'), 'r') as f:
    book = tuple(chain(*map(
        lambda x: ((x[0], word.lower()) for word in findall(r'(\w+?)(?:\W|$)', x[1])),
                ((i, line) for i, line in enumerate(f.read().split('\n'))))))


# hauptprogramm
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
    for left in range(len(book) - len(sentence)):
        right = left
        for next_word in sentence:
            if (book[right][1] == next_word) or next_word == '_':
                right += 1
            else:
                break
        else:
            line_l, line_r = book[left][0] + 1, book[right - 1][0] + 1
            results.append((
                ' '.join(map(lambda x: x[1], book[left:right])),
                f'l. {line_l}' if line_l == line_r else f'll. {line_l}-{line_r}'))

    # ergebnisse ausgeben
    if len(results) == 0:
        print(f"Kein Ergebnis gefunden! ({format((time() - start_time)*1000, '.2f')}ms)")
    else:
        print(f"{len(results)} Ergebnis{'se' if len(results) > 1 else ''} gefunden:"
              f" ({format((time() - start_time)*1000, '.2f')}ms)")
        print()
        for result, line_ref in results:
            print(f'> {result} ({line_ref})')


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
    except KeyboardInterrupt:
        print('\n')
        exit()
