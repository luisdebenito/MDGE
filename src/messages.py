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

    _score: List[str] = [
        "luisbq(8)",
        "lenaagal(3)",
        "ladebepa(4)",
        "luisbq(1)",
    ]

    def good() -> str:
        return random.choice(Messages._good)

    def bad() -> str:
        return random.choice(Messages._bad)

    def score() -> List[str]:
        return Messages._score
