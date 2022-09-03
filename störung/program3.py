from os import path
from re import findall
from time import time
from typing import List


def r_path(path_: str) -> str:
    return path.join(
        path.dirname(path.abspath(__file__)),
        path_
    )


# laden des buchs als zeilen-wörter-array O(1)
lines_words: List[List[str]]

with open(r_path('beispieldaten/Alice_im_Wunderland.txt'), 'r') as f:
    lines_words = list(map(
        lambda x: list(map(lambda y: y.lower(),
                           findall('(\\w+?)(?:\\W|$)', x))),
        f.read().split('\n')))


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

    # iterieren über das wörterarray und vergleichen mit dem beispielsatz O(n*k)
    results: List[str] = []

    match = []
    match_start = 0

    for il, line in enumerate(lines_words):
        for word in line:
            if len(match) == 0:
                match_start = il
            if sentence[len(match)] in [word, '_']:
                match.append(word)
            else:
                match.clear()
            if len(match) == len(sentence):
                results.append((' '.join(match),
                                f'll. {match_start+1}-{il+1}'
                                if match_start != il else f'l. {il+1}'))
                match.clear()

    # ergebnisse ausgeben
    if len(results) == 0:
        print(f"Kein Ergebnis gefunden! ({format((time() - start_time)*1000, '.2f')}ms)")
    else:
        print(f"{len(results)} Ergebnis{'se' if len(results) > 1 else ''}gefunden:"
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
