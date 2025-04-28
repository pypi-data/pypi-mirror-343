import os

# Find package directory
_package_dir = os.path.dirname(__file__)

def _load_text_file(filename):
    """Helper function to load a text file."""
    with open(os.path.join(_package_dir, filename), 'r', encoding='utf-8') as f:
        return f.read()

# Expose text files as variables
Emotion = _load_text_file('Emotion.txt')
Housing = _load_text_file('Housing.txt')
Plant = _load_text_file('Plant.txt')
BUBBLEMERGE = _load_text_file('BUBBLEMERGE.txt')
PARALLELREDUCTION = _load_text_file('PARALLELREDUCTION.txt')
VECTORMATRIX = _load_text_file('VECTORMATRIX.txt')
BFSDFS = _load_text_file('BFSDFS.txt')
