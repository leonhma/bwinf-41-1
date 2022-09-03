# Störung

❔ A1 👥 00122 🧑 Leonhard Masche 📆 3.09.2022

## Lösungsidee

Die Idee zur Lösung ist das Buch (Alice im Wunderland) in ein Array zu laden. Dann kann man über die Wörter iterieren, und in einem seperaten Array von Länge des zu findenden Satzes einen Treffer während dem iterieren 'aufbauen'. Wenn dieser Treffer voll ist (Volltreffer), wird der Text und die Zeilenreferenz in einer dritten Liste gespeichert, und am Ende ausgegeben.

## Umsetzung

Das Programm ist in Python umgesetzt und mit einer Umgebung ab der Version `3.6` ausführbar. Das Programm befindet sich in der Datei `program.py` in diesem Ordner.

Zuerst wird das Buch mithilfe eines RegEx (`(\\w+?)(?:\\W|$)`) in eine zweidimensionale Liste (Zeilen-Wörter) geladen und normalisiert.
Die Dimensionalität der Liste ist wichtig, um die Verbindung zwischen den Wörtern und den dazugehörigen Zeilennummern nicht zu verlieren.
Der zu findende Satz wird auch in eine Liste geladen.
Zusätzlich werden zwei weitere Listen erstellt: Eine, um alle bisher gefundenen Ergebnisse zu speichern, und eine Zweite, die den Treffer, der gerade aufgebaut wird hält.

Nun wird mit zwei verschachtelten `for`-Schleifen über die Buch-Matrix iteriert. Findet sich ein Wort das auf den Satz an der Stelle des bisherigen Fortschritts des Treffers passt, wird es dem Treffer angehängt und es wird weiter iteriert. Passt das Wort nicht, wird der bisherige Treffer gelöscht. Wenn der Treffer die Länge des zu findenden Satzes erreicht, wird er, zusammen mit seiner Zeilennummer zum Array der gefundenen Ergebnisse hinzugefügt.

Letztendlich werden die Ergebnisse formatiert ausgegeben.

### Big O

Die Zeit-Komplexität lässt sich hier sehr einfach ermitteln.

Da nur einmal über die Wörter im Buch iteriert wird, während der Treffer mitlaufend aufgebaut wird, ergibt sich eine Komplexität von `O(n)`, mit `n` als der Anzahl von Wörtern im Buch.

## Beispiele

Hier wird das Programm auf die fünf Beispiele von der Website angewendet:

`stoerung0.txt`

```text

das _ mir _ _ _ vor

1 Ergebnis gefunden: (15.40ms)

> das kommt mir gar nicht richtig vor (l. 440)

```

---

`stoerung1.txt`

```text

ich muß _ clara _

2 Ergebnisse gefunden: (15.99ms)

> ich muß in clara verwandelt (l. 425)
> ich muß doch clara sein (l. 441)

```

---

`stoerung2.txt`

```text

fressen _ gern _

3 Ergebnisse gefunden: (17.19ms)

> fressen katzen gern spatzen (ll. 213-214)
> fressen katzen gern spatzen (l. 214)
> fressen spatzen gern katzen (l. 214)

```

---

`stoerung3.txt`

```text

das _ fing _

2 Ergebnisse gefunden: (15.93ms)

> das spiel fing an (l. 2319)
> das publikum fing an (l. 3301)

```

---

`stoerung4.txt`

```text

ein _ _ tag

1 Ergebnis gefunden: (15.80ms)

> ein sehr schöner tag (l. 2293)

```

---

`stoerung5.txt`

```text

wollen _ so _ sein

1 Ergebnis gefunden: (17.64ms)

> wollen sie so gut sein (l. 2185)

```

## Quellcode

`program.py`

```python
from os import path
from re import findall
from time import time
from typing import List


def r_path(path_: str) -> str:
    return path.join(
        path.dirname(path.abspath(__file__)),
        path_
    )


# die zeilen-wörter matrix
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

    # iterieren über das wörterarray und aufbauen eines treffers
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
                if sentence[len(match)] in [word, '_']:
                    match.append(word)
            if len(match) == len(sentence):
                results.append((' '.join(match),
                                f'll. {match_start+1}-{il+1}'
                                if match_start != il else f'l. {il+1}'))
                match.clear()

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

```
