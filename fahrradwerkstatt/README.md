# Fahrradwerkstatt

❔ A4 👥 00122 🧑 Leonhard Masche 📆 9.09.2022

## Lösungsidee

Die Idee zur Lösung ist, den Zeitpunkt der Aufgabe des Auftrags und dessen Dauer in einer Liste zu speichern. Nun werden die Aufträge mit den gegebenen Methoden (nach Zeitpunkt oder Dauer) bearbeitet und die Ergebnisse ausgegeben.

## Verbesserungen

Wie die Simulation zeigt ist auch die zweite Methode nicht optimal. Zwar wird die durchschnittliche Dauer der Aufträge gekürzt, meist steigt aber auch die maximale Wartezeit. Das liegt daran, dass kurze Aufträge den Langen vorgezogen werden, und es so passieren kann, dass längere Aufträge durch die wiederholte Aufgabe von kürzeren Aufträgen immer wieder in der Warteschlange nach hinten verschoben werden. So wird die Kundenzufriedenheit und die Verbindlichkeit der Prognosen zur Auftragsdauer verschlechtert. Um dieses Geschehnis zu berücksichtigen, wird zusätzlich zur maximalen- und durchschnittlichen Wartezeit auch die prozentuale Anzahl der Aufträge, die hinter kürzere Aufträge verschoben wurden gezählt. Der Kehrwert dieser Metrik kann auch als 'Fairness' oder 'Verbindlichkeit der Zeitprognosen' betrachtet werden.

## Umsetzung

Das Programm ist in Python umgesetzt und mit einer Umgebung ab der Version `3.6` ausführbar. Das Programm befindet sich in der Datei `program.py` in diesem Ordner.

Zuerst werden die Aufträge aus dem Beispiel in eine Liste geladen. Die Aufträge werden dabei als Tuple gespeichert. Das erste Element ist der Zeitpunkt der Aufgabe des Auftrags, das zweite Element ist die Dauer des Auftrags. Zur Sicherheit wird die Liste noch einmal nach Eingangszeitpunkt sortiert.

Nun werden die Aufträge mit den gegebenen Methoden bearbeitet. Hier gibt zusätzlich zu den vorgeschlagenen Methoden `process_by_submit` (Die Aufträge werden in der Reihenfolge ihrer Aufgabe bearbeitet) und `process_by_duration` (Unter den verfügbaren Aufträgen wird immer der Kürzeste ausgewählt). Die Ergebnisse werden in einem DataFrame aus der Bibliothek `pandas` gespeichert, um eine formatierte Ausgabe zu erleichtern.

Letztendlich werden die Ergebnisse formatiert ausgegeben.

### Big O

Die Laufzeit des Programms ergibt sich als die Summe der einzelnen Verarbeitungsmethoden. Die Laufzeit der einzelnen Methoden muss also einzeln betrachtet werden:

#### `process_by_submit`

Die Laufzeit der Methode `process_by_submit` ist `O(n)`, da die Liste der Aufträge einmal durchlaufen wird.

#### `process_by_duration`

Die Laufzeit der Methode `process_by_duration` ist schwerer zu ermitteln. Zuerst wird die Liste der Aufträge durchlaufen (`O(n)`). Dann wird der jetzige Eintrag in die PriorityQueue hinzugefügt. Die PriorityQueue ist eine Binomial-Heap-Struktur, die in der Regel `O(log n)` Zeit benötigt, um ein Element hinzuzufügen. Solange die PriorityQueue nicht leer ist, werden solange anstehende Anträge aus der PriorityQueue bearbeitet, bis der nächste Auftrag eingeht. Da es maximal `n` Einträge gibt, wird durchschnittlich `n/n`, also `1` mal iteriert. So ergibt sich hier eine Laufzeit von `O(n log n)`.

Insgesamt ergibt sich eine vereinfachte Laufzeit von `O(n log n)`

## Beispiele

Hier wird das Programm auf die fünf Beispiele von der Website angewendet:

`fahrradwerkstatt0.txt`

```text

Warteschlange simuliert in 0.004ms:

|                                   |   process_by_submit |   process_by_duration |
|:----------------------------------|--------------------:|----------------------:|
| Maximale Wartezeit (min)          |             8500    |               8500    |
| Durchschnittliche Wartezeit (min) |             2098.87 |               2048.46 |

```

---

`fahrradwerkstatt1.txt`

```text

Warteschlange simuliert in 0.010ms:

|                                   |   process_by_submit |   process_by_duration |
|:----------------------------------|--------------------:|----------------------:|
| Maximale Wartezeit (min)          |             2638    |                2927   |
| Durchschnittliche Wartezeit (min) |              484.82 |                 425.8 |

```

---

`fahrradwerkstatt2.txt`

```text

Warteschlange simuliert in 0.004ms:

|                                   |   process_by_submit |   process_by_duration |
|:----------------------------------|--------------------:|----------------------:|
| Maximale Wartezeit (min)          |             9755    |              10295    |
| Durchschnittliche Wartezeit (min) |             1660.39 |               1433.26 |

```

---

`fahrradwerkstatt3.txt`

```text

Warteschlange simuliert in 0.006ms:

|                                   |   process_by_submit |   process_by_duration |
|:----------------------------------|--------------------:|----------------------:|
| Maximale Wartezeit (min)          |             5319    |               5831    |
| Durchschnittliche Wartezeit (min) |             1099.88 |               1075.27 |

```

---

`fahrradwerkstatt4.txt`

```text

Warteschlange simuliert in 0.004ms:

|                                   |   process_by_submit |   process_by_duration |
|:----------------------------------|--------------------:|----------------------:|
| Maximale Wartezeit (min)          |             11803   |              18885    |
| Durchschnittliche Wartezeit (min) |              3284.3 |               2896.11 |

```

## Quellcode

`program.py`

```python
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

```
