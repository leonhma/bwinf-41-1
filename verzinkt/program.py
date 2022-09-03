from fire import Fire


def crystal(
        dt: float = 0.1, dtr: float = 0.1, st: float = 0.2, str: float = 0.05, sr: float = 0.2, srr:
        float = 0.05, sd: float = 0.23, sdr: float = 0.03, sl: float = 0.2, slr: float = 0.05, r: float = 102,
        rr: float = 10, g: float = 102, gr: float = 10, b: float = 153, br: float = 10):
    """
    Kristallmuster mit den folgenden Parametern generieren:

    Parameters
    ----------
    dt : float, optional
        Delta-T zwischen dem Auftreten von Kristallisationskernen, by default 0.1
    dtr : float, optional
        Delta-T-random, Bereich für die Veränderung von `dt`, by default 0.1
    st : float, optional
        Speed-Top, Geschwindigkeit für das Wachstum nach oben, by default 0.2
    str : float, optional
        Speed-Top-random, Bereich für die Veränderung von `st`, by default 0.05
    sr : float, optional
        Speed-Right, wie `st`, by default 0.2
    srr : float, optional
        Speed-Right-random, wie `str`, by default 0.05
    sd : float, optional
        Speed-Down, wie `st`, by default 0.23
    sdr : float, optional
        Speed-Down-random, wie `stt`, by default 0.03
    sl : float, optional
        Speed-Left, wie `st`, by default 0.2
    slr : float, optional
        Speed-Left-random, wie `st`, by default 0.05
    r : float, optional
        Red, Rote Komponente der Farbe (0-255), by default 102
    rr : float, optional
        Red-random, Bereich für die zufällige Veränderung von `r`, by default 10
    g : float, optional
        Green, Grüne Komponente der Farbe (0-255), by default 102
    gr : float, optional
        Green-random, Bereich für die Veränderung von `g`, by default 10
    b : float, optional
        Blue, Blaue Farbkomponente, by default 153
    br : float, optional
        Blue-random, Bereich für die veränderung von `b`, by default 10
    """


if __name__ == '__main__':
    Fire(crystal)
