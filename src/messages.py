from typing import List
import random


class Messages:
    _good: List[str] = [
        "Still alive?",
        "Good but...",
        "Mmmmm ok",
        "Let's try with...",
        "Easy right?",
        "All set?",
        "Well...",
        "That was nice...",
        "Surprised already?",
    ]

    _bad: List[str] = [
        "Nope",
        "No amigo",
        "Not happening",
        "Negative",
        "I don't think so...",
        "Not here pal",
        "Not on my watch",
        "Wrong side",
        " =(",
    ]

    _die: List[str] = [
        "FAIL",
        "DIE",
        "FLOP",
        "Fiasco",
        "RUIN",
        "Suffer",
        "DOOM",
        "VOID",
        "Empty",
        "HARM",
    ]

    def good() -> str:
        return random.choice(Messages._good)

    def bad() -> str:
        return random.choice(Messages._bad)

    def die() -> str:
        return random.choice(Messages._die)
