"""Pop-up Toplevel windows: help, save confirmation, upgrade info, golden cookie."""

from tkinter import *
from functools import partial
import os

from config import ASSETS_DIR


class Help:

    def __init__(self, parent):
        parent.help_button.configure(state=DISABLED)
        self.box = Toplevel()
        self.box.iconbitmap(os.path.join(ASSETS_DIR, "cookieicon.ico"))
        self.box.protocol("WM_DELETE_WINDOW", partial(self.close, parent))
        self.frame = Frame(self.box, bg='#fab875', width=600, height=600)
        self.frame.pack(side=TOP, expand=TRUE, fill=BOTH)
        self.title = Label(self.frame, font='Arial 16 bold',
                           text='How to play Cookie Clicker', justify=CENTER, pady=10, bg='#fab875')
        self.title.pack(side=TOP, expand=TRUE, fill=BOTH)
        self.text = Label(self.frame, font='Arial 12', text='Click the cookie to get a cookie! Use your cookies to purchase buildings which can generate you even more cookies! Upgrade your buildings too boost their cookie production even more!',
                          pady=10, padx=20, wraplength=500, bg='#fab875')
        self.text.pack(side=TOP, expand=TRUE, fill=BOTH)
        self.button = Button(self.frame, text="Dismiss", width=10,
                             bg="white", font="arial 10 bold", command=partial(self.close, parent), pady=5, cursor="hand2")
        self.button.pack(side=BOTTOM, pady=10, expand=TRUE)

    def close(self, parent):
        self.box.destroy()
        parent.help_button.configure(state=NORMAL)
        
class Save:

    def __init__(self, parent):
        parent.savebutton.configure(state=DISABLED)
        self.box = Toplevel()
        self.box.iconbitmap(os.path.join(ASSETS_DIR, "cookieicon.ico"))
        self.box.protocol("WM_DELETE_WINDOW", partial(self.close, parent))
        self.frame = Frame(self.box, bg='#fab875', width=600, height=600)
        self.frame.pack(side=TOP, expand=TRUE, fill=BOTH)
        self.title = Label(self.frame, font='Arial 16 bold',
                           text='Game Saved', justify=CENTER, pady=10, bg='#fab875')
        self.title.pack(side=TOP, expand=TRUE, fill=BOTH)
        self.text = Label(self.frame, font='Arial 12', text='Your game has been saved as a .save file. Use this file to load the game from your current progress by clicking the Load button',
                          pady=10, padx=20, wraplength=500, bg='#fab875')
        self.text.pack(side=TOP, expand=TRUE, fill=BOTH)
        self.button = Button(self.frame, text="Dismiss", width=10,
                             bg="white", font="arial 10 bold", command=partial(self.close, parent), pady=5, cursor="hand2")
        self.button.pack(side=BOTTOM, pady=10, expand=TRUE)

    def close(self, parent):
        self.box.destroy()
        parent.savebutton.configure(state=NORMAL)


class UpgradeInfo:
    def __init__(self, parent):
        parent.bupgradeinfobutton.configure(state=DISABLED)
        self.box = Toplevel()
        self.box.iconbitmap(os.path.join(ASSETS_DIR, "cookieicon.ico"))
        self.box.protocol("WM_DELETE_WINDOW", partial(self.close, parent))
        self.frame = Frame(self.box, bg='#fab875')
        self.frame.pack(side=TOP, expand=TRUE, fill=BOTH)
        self.title = Label(self.frame, font='Arial 16 bold',
                           text='Upgrades Acquired', justify=CENTER, pady=10, bg='#fab875')
        self.title.pack(side=TOP, expand=TRUE, fill=BOTH)
        self.childframe = Frame(self.frame, bg='#fab875')
        self.childframe.pack(side=TOP, expand=TRUE, fill=BOTH, padx=10)

        upgradeinfotext = ''
        if parent.upgradeinfolist != []:
            scrollbar = Scrollbar(self.childframe)
            scrollbar.pack(side=RIGHT, fill=Y)
            self.text = Text(self.childframe, font='Arial 12',
                             bg='#fab875', wrap=WORD, yscrollcommand=scrollbar.set)

            for i in parent.upgradeinfolist:
                self.text.insert(END, i + '\n' * 2)

            self.text.pack(side=TOP, expand=TRUE, fill=BOTH)
            scrollbar.config(command=self.text.yview)
            self.text.config(state=DISABLED)

        else:
            self.text = Label(self.frame, font='Arial 12', text='You currently have no upgrades.',
                              pady=10, padx=20, wraplength=500, bg='#fab875')
            self.text.pack(side=TOP, expand=TRUE, fill=BOTH)

        self.button = Button(self.frame, text="Dismiss", width=10,
                             bg="white", font="arial 10 bold", command=partial(self.close, parent), pady=5, wraplength=500, cursor="hand2")
        self.button.pack(side=BOTTOM, pady=10, expand=TRUE)

    def close(self, parent):
        self.box.destroy()
        parent.bupgradeinfobutton.configure(state=NORMAL)


class FirstGold:
    def __init__(self, parent):
        self.box = Toplevel()
        self.box.iconbitmap(os.path.join(ASSETS_DIR, "cookieicon.ico"))
        self.frame = Frame(self.box, bg='#ffe76d', width=600, height=600)
        self.frame.pack(side=TOP, expand=TRUE, fill=BOTH)
        self.title = Label(self.frame, font='Arial 16 bold',
                           text='Congratulations! You found a golden cookie!', justify=CENTER, pady=10, bg='#ffe76d')
        self.title.pack(side=TOP, expand=TRUE, fill=BOTH)
        self.text = Label(self.frame, font='Arial 12', text='A random golden cookie will appear every 30 - 180 seconds. Click on it within 13 seconds to receive 100x your current per click amount.',
                          pady=10, padx=20, wraplength=500, bg='#ffe76d')
        self.text.pack(side=TOP, expand=TRUE, fill=BOTH)
        self.button = Button(self.frame, text="Dismiss", width=10,
                             bg="white", font="arial 10 bold", command=self.close, pady=5, cursor="hand2")
        self.button.pack(side=BOTTOM, pady=10, expand=TRUE)

    def close(self):
        self.box.destroy()

