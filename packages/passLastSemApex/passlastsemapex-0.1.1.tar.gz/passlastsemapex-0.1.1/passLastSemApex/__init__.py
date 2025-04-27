import os

# Find package directory
_package_dir = os.path.dirname(__file__)

def _load_text_file(filename):
    """Helper function to load a text file."""
    with open(os.path.join(_package_dir, filename), 'r', encoding='utf-8') as f:
        return f.read()

# Expose text files as variables
ass1 = _load_text_file('ass1.txt')
ass2 = _load_text_file('ass2.txt')
# Add more assignments here as needed
