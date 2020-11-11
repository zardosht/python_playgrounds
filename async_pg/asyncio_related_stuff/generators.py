

# From here: 
# https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/
# How the heck does async/await work in Python 3.5?


# not a generator

def eager_range(up_to):
    """Create a list of integers, from 0 to up_to, exclusive."""
    sequence = []
    index = 0
    while index < up_to:
        sequence.append(index)
        index += 1
    return sequence



# generator

def lazy_range(up_to):
    """Generator to return the sequence of integers from 0 to up_to, exclusive."""
    index = 0
    while index < up_to:
        yield index
        index += 1



