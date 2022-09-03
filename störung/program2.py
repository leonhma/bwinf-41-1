from os import path
from re import findall
from time import time
from typing import Generator, List


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


# rolling window O(n*k)
def rolling_window(lines_words: List[List[str]], size: int) -> Generator:
    for il, line in enumerate(lines_words):
        for iw in range(len(line)):
            arr = []
            current_iline, current_line_len, current_iword = il, len(line), iw
            while len(arr) < size:
                arr.append(lines_words[current_iline]
                           [current_iword])
                if current_iword == current_line_len - 1 and len(arr) < size:
                    currentword = ''
                    while not currentword:
                        current_iline += 1
                        if current_iline == len(lines_words):
                            return
                        current_line_len = len(lines_words[current_iline])
                        current_iword = 0
                        try:
                            currentword = lines_words[current_iline][current_iword]
                        except IndexError:
                            continue
                else:
                    current_iword += 1
            line_ref = f'll. {il+1}-{current_iline+1}' if il != current_iline else f'l. {il+1}'
            yield (tuple(arr), line_ref)


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

    for words, line_ref in rolling_window(lines_words, len(sentence)):
        arr = []
        for i, word in enumerate(words):
            if word == sentence[i] or sentence[i] == '_':
                arr.append(word)
            else:
                break
        else:
            results.append((' '.join(arr), line_ref))

    # ergebnisse ausgeben
    if len(results) == 0:
        print(f"Kein Ergebnis gefunden! ({format((time() - start_time)*1000, '.2f')}ms)")
    else:
        print(f"{len(results)} Ergebnis{'se' if len(results) > 1 else ''} gefunden: ({format((time() - start_time)*1000, '.2f')}ms)")
        print()
        for result, line_ref in results:
            print(f'> {result} ({line_ref})')


# programmschleife
print('Lieblingsbuchzitatfinder')
print('(Drücke ^C um das Programm zu beenden)')
print()
print('Buch: Alice im Wunderland')

while True:
    main()
