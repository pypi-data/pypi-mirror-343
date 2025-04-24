def parse_english_number(text: str) -> int:
    """Parse an English‑word number in lowercase with underscores"""
    # 0–19 and tens
    units = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
        "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
        "fourteen": 14, "fifteen": 15, "sixteen": 16,
        "seventeen": 17, "eighteen": 18, "nineteen": 19,
    }
    tens = {
        "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
        "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
    }

    # Extendable list of -illion names
    SCALE_NAMES = [
        "thousand", "million", "billion", "trillion", "quadrillion", "quintillion",
        "sextillion", "septillion", "octillion", "nonillion", "decillion",
        "undecillion", "duodecillion", "tredecillion", "quattuordecillion",
        "quindecillion", "sexdecillion", "septendecillion", "octodecillion",
        "novemdecillion", "vigintillion", "centillion",
    ]
    scales = {
        name: 10 ** (i * 3)
        for i, name in enumerate(SCALE_NAMES, start=1)
    }

    numwords = {**units, **tens, **scales, "hundred": 100}

    tokens = text.split("_")
    if not tokens:
        raise ValueError("Empty input")

    negative = False
    if tokens[0] == "minus":
        negative = True
        tokens = tokens[1:]
        if not tokens:
            raise ValueError("Nothing after 'minus'")

    current = total = 0

    for tok in tokens:
        if tok not in numwords:
            raise ValueError(f"Invalid token: {tok!r}")
        val = numwords[tok]

        if val < 100:
            current += val
        elif val == 100:
            current = (current or 1) * 100
        else:
            current = (current or 1) * val
            total += current
            current = 0

    result = total + current
    return -result if negative else result

