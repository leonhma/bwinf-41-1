# Sudokopie

- für jede reihe/spalte im block die zahl der gefüllten felder plus 1 malnehmen, und die ergebnisse von reihe und zeile addieren um 'fingerprint' zu erhalten
- go through all combinations of block shifts and rotations (6x6x4) and loosely match them by their 'square numbers'
- if theres a match, go through all combinations of single row/column shifts (6⁶) and check for a full match (while accounting for possible number changes)

- compute fingerprints
- go through rough combinations (6*6*4 = 144)
 -> if match
    - go through all full combinations (6⁶ = 46.656)
    - for each combination, check ignoring number shuffles
     -> if full match return output
