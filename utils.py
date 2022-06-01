import random

def is_in(elt, seq):
    """Similar to (elt in seq), but compares with 'is', not '=='."""
    return any(x is elt for x in seq)
def count(seq):
    """Count the number of items in sequence that are interpreted as true."""
    return sum(bool(x) for x in seq)
def first(iterable, default=None):
    "Return the first element of an iterable or the next element of a generator; or default."
    try:
        return iterable[0]
    except IndexError:
        return default
    except TypeError:
        return next(iterable, default)

def shuffled(iterable):
    "Randomly shuffle a copy of iterable."
    items = list(iterable)
    random.shuffle(items)
    return items

