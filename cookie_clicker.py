"""Cookie Clicker - entry point.

Run with: python cookie_clicker.py
"""

import os
from tkinter import Tk

from config import ASSETS_DIR
from game import Cookies


def main():
    root = Tk()
    root.title("Cookie Clicker")
    root.iconbitmap(os.path.join(ASSETS_DIR, "cookieicon.ico"))
    root.resizable(0, 0)
    Cookies(root)
    root.mainloop()


if __name__ == "__main__":
    main()
