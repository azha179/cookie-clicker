import os

# Absolute path to the bundled assets, resolved relative to this file so the
# game runs correctly regardless of the current working directory.
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
