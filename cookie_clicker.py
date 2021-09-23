from tkinter import *
import time
import threading
import math
from functools import partial
import random
import csv


class Cookies:
    def __init__(self, parent):

        # Default Variables
        self.closeprogram = False
        self.cookies = 0
        self.perclick = 1
        self.upgrademultiplieramount = 1
        self.upgrademultiplier = 1
        self.cps = 0

        # Background colours
        bgcolour = '#0d6bb8'
        upgradebg = '#99d1ff'
        bupgradebg = '#ffcf91'

        # assigns the X button for window to the quit command
        root.protocol("WM_DELETE_WINDOW", self.quit)

        # Frame
        self.cookie_frame = Frame(parent, bg=bgcolour)
        self.cookie_frame.grid()

        # Click Heading (row0, column0)
        self.cookie_heading = Label(self.cookie_frame, text='Click the Cookie',
                                    font='arial 24 bold', padx=20, pady=20, bg=bgcolour, fg='white')
        self.cookie_heading.grid(row=0)

        # upgrade frame (column1)
        self.buildingandupgradeframe = Frame(self.cookie_frame, bg=bgcolour)
        self.buildingandupgradeframe.grid(
            row=0, column=1, rowspan=10, padx=20, pady=10)

        # Cookie Amount (row1, column0)
        self.cookie_counter = Label(
            self.cookie_frame, text=' ', font='arial 18', pady=10, bg=bgcolour, fg='white')
        self.changecookietext()
        self.cookie_counter.grid(row=1)

        # Per click
        self.perclicklabel = Label(
            self.cookie_frame, text='', font='arial 11', pady=5, bg=bgcolour, fg='white')
        self.updateperclick()
        self.perclicklabel.grid(row=2)

        # Cookie button frame (row2, column0)
        self.cookie_frame = Frame(self.cookie_frame, bg=bgcolour)
        self.cookie_frame.grid(row=3)

        # Cookie button
        self.cookieimage = PhotoImage(file=r"cookie.png")
        self.hovercookieimage = PhotoImage(file=r"hovercookie.png")
        self.goldcookieimage = PhotoImage(file=r"goldcookie.png")
        self.hovergoldcookieimage = PhotoImage(file=r"hovergoldcookie.png")
        self.cookie_button = Button(self.cookie_frame, image=self.cookieimage, command=self.cookie_click,
                                    highlightthickness=0, bd=0, bg=bgcolour, activebackground=bgcolour)
        self.cookie_button.grid(row=0, column=0)
        self.cookie_button.bind("<Enter>", self.hovercookie)
        self.cookie_button.bind("<Leave>", self.unhovercookie)

        # Row 3 buttons frame
        self.buttonframe = Frame(self.cookie_frame, bg=bgcolour)
        self.buttonframe.grid(row=4, pady=20)

        # Help
        self.help_button = Button(self.buttonframe, text='Help', bg='#188f10', fg='white', padx=10, pady=10,
                                  command=self.help, font='arial 12 bold', activebackground='#21c716', activeforeground='white')
        self.help_button.grid(row=0, column=0)
        self.help_button.bind("<Enter>", self.hoverhelp)
        self.help_button.bind("<Leave>", self.unhoverhelp)

        # Quit
        self.quit_button = Button(self.buttonframe, text='Quit', bg='#8a1b0f', fg='white', padx=10, pady=10,
                                  command=self.quit, font='arial 12 bold', activebackground='#c42818', activeforeground='white')
        self.quit_button.grid(row=0, column=1)
        self.quit_button.bind("<Enter>", self.hoverquit)
        self.quit_button.bind("<Leave>", self.unhoverquit)

        # Buildings

        # Building Frame
        self.upgradesframe = Frame(
            self.buildingandupgradeframe, highlightbackground='#7098b8', highlightthickness=3, bg=upgradebg)
        self.upgradesframe.grid(
            row=0, column=0, rowspan=10, padx=20, pady=10)

        # Building Upgrades Frame
        self.buildingupgradeframe = Frame(
            self.buildingandupgradeframe, highlightthickness=3, highlightbackground='#a37340', bg=bupgradebg)
        self.buildingupgradeframe.grid(
            row=0, rowspan=10, column=1, padx=10, pady=10)

        # Cookies per second
        self.cookiespersecond = Label(
            self.upgradesframe, text='Buildings', font='arial 26 bold', justify=CENTER, bg=upgradebg)
        self.cookiespersecond.grid(row=0, columnspan=3, pady=10, padx=10)

        # Expand
        self.buildingexpandbutton = Button(self.upgradesframe, text='-', font='arial 22 bold', bg=upgradebg,
                                           padx=10, command=self.collapsebuilding, highlightthickness=0, bd=0, activebackground=upgradebg, fg='dark grey')
        self.buildingexpandbutton.grid(row=0, column=3, sticky=E)

        # Frame to fit arrows and cps label
        self.arrowsandcpsframe = Frame(self.upgradesframe, bg=upgradebg)
        self.arrowsandcpsframe.grid(row=1, columnspan=3)

        self.buildingpagenumber = 1

        # Left Arrow
        self.previouspagebutton = Button(self.arrowsandcpsframe, text='<', font='arial 22 bold', bg=upgradebg,
                                         padx=10, highlightthickness=0, bd=0, activebackground=upgradebg, fg='#0f1466', state=DISABLED, command=self.previouspage)
        self.previouspagebutton.grid(row=0, column=0, sticky=W)

        # Cookies per second count
        self.cpslabel = Label(self.arrowsandcpsframe, text='0.0 cps',
                              font='arial 12', pady=5, justify=CENTER, bg=upgradebg)
        self.cpslabel.grid(row=0, column=1, sticky='news', padx=100)

        # Right Arrow
        self.nextpagebutton = Button(self.arrowsandcpsframe, text='>', font='arial 22 bold', bg=upgradebg,
                                     padx=10, highlightthickness=0, bd=0, activebackground=upgradebg, fg='#0f1466', command=self.nextpage)
        self.nextpagebutton.grid(row=0, column=2, sticky=E)

        # Multiplier buy
        self.buymultiplierframe = Frame(self.upgradesframe, bg='#465d70')
        self.buymultiplierframe.grid(row=2, columnspan=3, pady=10)

        self.multiplierlabel = Label(self.buymultiplierframe, text='Buy',
                                     font='arial 14 bold', bg='#465d70', padx=10, pady=5, fg='white')
        self.multiplierlabel.grid(row=0, column=0, padx=20)

        self.multiplierone = Button(self.buymultiplierframe, text='x1', font='arial 12 bold', bg='#465d70', highlightthickness=0,
                                    bd=0, padx=10, fg='white', activebackground='#465d70', activeforeground='white', command=self.timesone, cursor="hand2")
        self.multiplierone.grid(row=0, column=1, padx=20)

        self.multiplierten = Button(self.buymultiplierframe, text='x10', font='arial 12 ', bg='#465d70', highlightthickness=0,
                                    bd=0, padx=10, fg='white', activebackground='#465d70', activeforeground='white', command=self.timesten, cursor="hand2")
        self.multiplierten.grid(row=0, column=2, padx=20)

        self.multiplierhundred = Button(self.buymultiplierframe, text='x100', font='arial 12 ', bg='#465d70', highlightthickness=0,
                                        bd=0, padx=10, fg='white', activebackground='#465d70', activeforeground='white', command=self.timeshundred, cursor="hand2")
        self.multiplierhundred.grid(row=0, column=3, padx=20)

        # Assigning Images
        self.buybuttonimage = PhotoImage(file=r"buy_button.png")
        self.redbuybutton = PhotoImage(file=r"buy_button_red.png")

        # Cursor
        self.cursors = 0
        self.cursor_price = 15
        self.basecursor_price = 15
        self.cursorcps = 0.1

        self.cursor_label = Label(self.upgradesframe, text='Cursor:\n15 Cookies',
                                  font='arial 14', padx=20, pady=10, bg=upgradebg, justify=LEFT)
        self.cursor_label.grid(row=3, column=0, sticky=W)

        self.cursor_amount = Label(
            self.upgradesframe, text='Amount: 0', font='arial 10', padx=20, pady=10, bg=upgradebg)
        self.cursor_amount.grid(row=3, column=1)

        self.cursor_buy = Button(self.upgradesframe, command=lambda: [self.cursor(), self.startidletimer(
        )], image=self.buybuttonimage, highlightthickness=0, bd=0, bg=upgradebg, activebackground=upgradebg, pady=10, cursor="hand2")
        self.cursor_buy.grid(row=3, column=2, padx=20, pady=10)

        # Grandma
        self.grandmas = 0
        self.grandma_price = 100
        self.basegrandma_price = 100
        self.grandmacps = 1

        self.grandma_label = Label(self.upgradesframe, text='Grandma:\n100 Cookies',
                                   font='arial 14', padx=20, pady=10, bg=upgradebg, justify=LEFT)
        self.grandma_label.grid(row=4, column=0, sticky=W)

        self.grandma_amount = Label(
            self.upgradesframe, text='Amount: 0', font='arial 10', padx=20, pady=10, bg=upgradebg)
        self.grandma_amount.grid(row=4, column=1)

        self.grandma_buy = Button(self.upgradesframe, command=lambda: [self.grandma(), self.startidletimer(
        )], image=self.buybuttonimage, highlightthickness=0, bd=0, bg=upgradebg, activebackground=upgradebg, pady=10, cursor="hand2")
        self.grandma_buy.grid(row=4, column=2, sticky=E, padx=20, pady=10)

        # Farm
        self.farms = 0
        self.farm_price = 1100
        self.basefarm_price = 1100
        self.farmcps = 8

        self.farm_label = Label(self.upgradesframe, text='Farm:\n1100 Cookies',
                                font='arial 14', padx=20, pady=10, bg=upgradebg, justify=LEFT)
        self.farm_label.grid(row=5, column=0, sticky=W)

        self.farm_amount = Label(
            self.upgradesframe, text='Amount: 0', font='arial 10', padx=20, pady=10, bg=upgradebg)
        self.farm_amount.grid(row=5, column=1)

        self.farm_buy = Button(self.upgradesframe, command=lambda: [self.farm(), self.startidletimer(
        )], image=self.buybuttonimage, highlightthickness=0, bd=0, bg=upgradebg, activebackground=upgradebg, pady=10, cursor="hand2")
        self.farm_buy.grid(row=5, column=2, sticky=E, padx=20, pady=10)

        # Mine
        self.mines = 0
        self.mine_price = 12000
        self.basemine_price = 12000
        self.minecps = 47

        self.mine_label = Label(self.upgradesframe, text='Mine:\n12000 Cookies',
                                font='arial 14', padx=20, pady=10, bg=upgradebg, justify=LEFT)
        self.mine_label.grid(row=6, column=0, sticky=W)

        self.mine_amount = Label(
            self.upgradesframe, text='Amount: 0', font='arial 10', padx=20, pady=10, bg=upgradebg)
        self.mine_amount.grid(row=6, column=1)

        self.mine_buy = Button(self.upgradesframe, command=lambda: [self.mine(), self.startidletimer(
        )], image=self.buybuttonimage, highlightthickness=0, bd=0, bg=upgradebg, activebackground=upgradebg, pady=10, cursor="hand2")
        self.mine_buy.grid(row=6, column=2, sticky=E, padx=20, pady=10)

        # Factory
        self.factories = 0
        self.factory_price = 130000
        self.basefactory_price = 130000
        self.factorycps = 260

        self.factory_label = Label(self.upgradesframe, text='Factory:\n130000 Cookies',
                                   font='arial 14', padx=20, pady=10, bg=upgradebg, justify=LEFT)
        self.factory_label.grid(row=7, column=0, sticky=W)

        self.factory_amount = Label(
            self.upgradesframe, text='Amount: 0', font='arial 10', padx=20, pady=10, bg=upgradebg)
        self.factory_amount.grid(row=7, column=1)

        self.factory_buy = Button(self.upgradesframe, command=lambda: [self.factory(), self.startidletimer(
        )], image=self.buybuttonimage, highlightthickness=0, bd=0, bg=upgradebg, activebackground=upgradebg, pady=10, cursor="hand2")
        self.factory_buy.grid(row=7, column=2, sticky=E, padx=20, pady=10)

        # Bank
        self.banks = 0
        self.bank_price = 1400000
        self.basebank_price = 1400000
        self.bankcps = 1400

        self.bank_label = Label(self.upgradesframe, text='Bank:\n1.40000 million Cookies',
                                font='arial 14', padx=20, pady=10, bg=upgradebg, justify=LEFT)
        self.bank_label.grid(row=8, column=0, sticky=W)

        self.bank_amount = Label(
            self.upgradesframe, text='Amount: 0', font='arial 10', padx=20, pady=10, bg=upgradebg)
        self.bank_amount.grid(row=8, column=1)

        self.bank_buy = Button(self.upgradesframe, command=lambda: [self.bank(), self.startidletimer(
        )], image=self.buybuttonimage, highlightthickness=0, bd=0, bg=upgradebg, activebackground=upgradebg, pady=10, cursor="hand2")
        self.bank_buy.grid(row=8, column=2, sticky=E, padx=20, pady=10)

        # Temple
        self.temples = 0
        self.temple_price = 20000000
        self.basetemple_price = 20000000
        self.templecps = 7800

        self.temple_label = Label(self.upgradesframe, text='Temple:\n20.0000 million Cookies',
                                  font='arial 14', padx=20, pady=10, bg=upgradebg, justify=LEFT)

        self.temple_amount = Label(
            self.upgradesframe, text='Amount: 0', font='arial 10', padx=20, pady=10, bg=upgradebg)

        self.temple_buy = Button(self.upgradesframe, command=lambda: [self.temple(), self.startidletimer(
        )], image=self.buybuttonimage, highlightthickness=0, bd=0, bg=upgradebg, activebackground=upgradebg, pady=10, cursor="hand2")

        # Wizard Tower
        self.wizardtowers = 0
        self.wizardtower_price = 330000000
        self.basewizardtower_price = 330000000
        self.wizardtowercps = 44000

        self.wizardtower_label = Label(self.upgradesframe, text='Wizard Tower:\n330.000 million Cookies',
                                       font='arial 14', padx=20, pady=10, bg=upgradebg, justify=LEFT)

        self.wizardtower_amount = Label(
            self.upgradesframe, text='Amount: 0', font='arial 10', padx=20, pady=10, bg=upgradebg)

        self.wizardtower_buy = Button(self.upgradesframe, command=lambda: [self.wizardtower(), self.startidletimer(
        )], image=self.buybuttonimage, highlightthickness=0, bd=0, bg=upgradebg, activebackground=upgradebg, pady=10, cursor="hand2")

        # Shipment
        self.shipments = 0
        self.shipment_price = 5100000000
        self.baseshipment_price = 5100000000
        self.shipmentcps = 260000

        self.shipment_label = Label(self.upgradesframe, text='Shipment:\n5.10000 billion Cookies',
                                    font='arial 14', padx=20, pady=10, bg=upgradebg, justify=LEFT)

        self.shipment_amount = Label(
            self.upgradesframe, text='Amount: 0', font='arial 10', padx=20, pady=10, bg=upgradebg)

        self.shipment_buy = Button(self.upgradesframe, command=lambda: [self.shipment(), self.startidletimer(
        )], image=self.buybuttonimage, highlightthickness=0, bd=0, bg=upgradebg, activebackground=upgradebg, pady=10, cursor="hand2")

        # Alchemy Lab
        self.alchemylabs = 0
        self.alchemylab_price = 75000000000
        self.basealchemylab_price = 75000000000
        self.alchemylabcps = 1600000

        self.alchemylab_label = Label(self.upgradesframe, text='Alchemy Lab:\n75.0000 billion Cookies',
                                      font='arial 14', padx=20, pady=10, bg=upgradebg, justify=LEFT)

        self.alchemylab_amount = Label(
            self.upgradesframe, text='Amount: 0', font='arial 10', padx=20, pady=10, bg=upgradebg)

        self.alchemylab_buy = Button(self.upgradesframe, command=lambda: [self.alchemylab(), self.startidletimer(
        )], image=self.buybuttonimage, highlightthickness=0, bd=0, bg=upgradebg, activebackground=upgradebg, pady=10, cursor="hand2")

        # Portal
        self.portals = 0
        self.portal_price = 1000000000000
        self.baseportal_price = 1000000000000
        self.portalcps = 10000000

        self.portal_label = Label(self.upgradesframe, text='Portal:\n1.00000 trillion Cookies',
                                  font='arial 14', padx=20, pady=10, bg=upgradebg, justify=LEFT)

        self.portal_amount = Label(
            self.upgradesframe, text='Amount: 0', font='arial 10', padx=20, pady=10, bg=upgradebg)

        self.portal_buy = Button(self.upgradesframe, command=lambda: [self.portal(), self.startidletimer(
        )], image=self.buybuttonimage, highlightthickness=0, bd=0, bg=upgradebg, activebackground=upgradebg, pady=10, cursor="hand2")

        # Time Machine
        self.timemachines = 0
        self.timemachine_price = 14000000000000
        self.basetimemachine_price = 14000000000000
        self.timemachinecps = 65000000

        self.timemachine_label = Label(self.upgradesframe, text='Time Machine:\n14.0000 trillion Cookies',
                                       font='arial 14', padx=20, pady=10, bg=upgradebg, justify=LEFT)

        self.timemachine_amount = Label(
            self.upgradesframe, text='Amount: 0', font='arial 10', padx=20, pady=10, bg=upgradebg)

        self.timemachine_buy = Button(self.upgradesframe, command=lambda: [self.timemachine(), self.startidletimer(
        )], image=self.buybuttonimage, highlightthickness=0, bd=0, bg=upgradebg, activebackground=upgradebg, pady=10, cursor="hand2")

        # Building Upgrades

        # Info Button
        self.upgradeinfolist = []
        self.bupgradeinfobutton = Button(self.buildingupgradeframe, text='Info', font='arial 14 bold', bg='#ffce8f',
                                         padx=10, highlightthickness=0, bd=0, activebackground='#ffce8f', fg='#2a7dbf', command=self.upgradeinfo, cursor="hand2")
        self.bupgradeinfobutton.grid(row=0, column=0, sticky=W)

        # Label
        self.bupgradelabel = Label(self.buildingupgradeframe, text='Upgrades',
                                   font='arial 18 bold', justify=CENTER, bg=bupgradebg)
        self.bupgradelabel.grid(row=0, column=1, pady=10, padx=10, sticky=N)

        # Expand
        self.bupgradeexpandbutton = Button(self.buildingupgradeframe, text='+', font='arial 22 bold', bg='#ffce8f',
                                           padx=10, command=self.expandupgrade, highlightthickness=0, bd=0, activebackground='#ffce8f', fg='dark grey')
        self.bupgradeexpandbutton.grid(row=0, column=2, sticky=NE)

        # Cursor Upgrade
        self.cursororder = 1
        self.thousandfingersamount = 0
        self.thousandfingersbought = False
        self.cursorupgradeprice = 100

        self.cursorupgrade1 = CursorUpgrades(
            self, 'Reinforced index finger', 100, 1, 1, 'times', 2, 'The mouse and cursors are twice as efficient.')
        self.cursorupgrade2 = CursorUpgrades(
            self, 'Carpal tunnel prevention cream', 500, 1, 2, 'times', 2, 'The mouse and cursors are twice as efficient.')
        self.cursorupgrade3 = CursorUpgrades(
            self, 'Ambidextrous', 10000, 10, 3, 'times', 2, 'The mouse and cursors are twice as efficient.')
        self.cursorupgrade4 = CursorUpgrades(self, 'Thousand fingers', 100000, 25, 4, 'plus',
                                             0.1, 'The mouse and cursors gain +0.1 cookies for each non-cursor object owned.')
        self.cursorupgrade5 = CursorUpgrades(
            self, 'Million fingers', 10000000, 50, 5, 'timesthousand', 5, 'Multiplies the gain from Thousand fingers by 5.')
        self.cursorupgrade6 = CursorUpgrades(self, 'Billion fingers', 100000000, 100,
                                             6, 'timesthousand', 10, 'Multiplies the gain from Thousand fingers by 10.')
        self.cursorupgrade7 = CursorUpgrades(self, 'Trillion fingers', 1000000000, 150,
                                             7, 'timesthousand', 20, 'Multiplies the gain from Thousand fingers by 20.')
        self.cursorupgrade8 = CursorUpgrades(self, 'Quadrillion fingers', 10000000000, 200,
                                             8, 'timesthousand', 20, 'Multiplies the gain from Thousand fingers by 20.')
        self.cursorupgrade9 = CursorUpgrades(self, 'Quintillion fingers', 10000000000000, 250,
                                             9, 'timesthousand', 20, 'Multiplies the gain from Thousand fingers by 20.')
        self.cursorupgrade10 = CursorUpgrades(self, 'Sextillion fingers', 10000000000000000, 300,
                                              10, 'timesthousand', 20, 'Multiplies the gain from Thousand fingers by 20.')
        self.cursorupgrade11 = CursorUpgrades(self, 'Septillion fingers', 10000000000000000000, 350,
                                              11, 'timesthousand', 20, 'Multiplies the gain from Thousand fingers by 20.')
        self.cursorupgrade12 = CursorUpgrades(self, 'Octillion fingers', 10000000000000000000000, 400,
                                              12, 'timesthousand', 20, 'Multiplies the gain from Thousand fingers by 20.')
        self.cursorupgrade13 = CursorUpgrades(self, 'Nonillion fingers', 10000000000000000000000000, 450,
                                              13, 'timesthousand', 20, 'Multiplies the gain from Thousand fingers by 20.')

        self.cursorupgradelabel = Label(self.buildingupgradeframe, text='Reinforced index finger:\n100 Cookies',
                                        font='arial 14', padx=20, pady=10, bg=bupgradebg, justify=LEFT, wraplength=200)

        self.cursorupgradetext = Label(self.buildingupgradeframe, text=self.cursorupgrade1.descriptiontext,
                                       font='arial 10', padx=20, pady=10, bg=bupgradebg, justify=CENTER, wraplength=150)

        self.cursorupgradebutton = Button(self.buildingupgradeframe, padx=20, pady=10, command=self.cursorupgrade,
                                          image=self.redbuybutton, highlightthickness=0, bd=0, bg=bupgradebg, activebackground=bupgradebg, cursor="hand2")

        # Grandma Upgrade
        self.grandmaorder = 1
        self.grandmaupgradeprice = 1000

        self.grandmaupgrade1 = GrandmaUpgrades(
            self, 'Forwards from grandma', 1000, 1, 1, 2, 'Grandmas are twice as efficient.')
        self.grandmaupgrade2 = GrandmaUpgrades(
            self, 'Steel-plated rolling pins', 5000, 5, 2, 2, 'Grandmas are twice as efficient.')
        self.grandmaupgrade3 = GrandmaUpgrades(
            self, 'Lubricated dentures', 50000, 25, 3, 2, 'Grandmas are twice as efficient.')
        self.grandmaupgrade4 = GrandmaUpgrades(
            self, 'Prune juice', 5000000, 50, 4, 2, 'Grandmas are twice as efficient.')
        self.grandmaupgrade5 = GrandmaUpgrades(
            self, 'Double-thick glasses', 500000000, 100, 5, 2, 'Grandmas are twice as efficient.')
        self.grandmaupgrade6 = GrandmaUpgrades(
            self, 'Aging agents', 50000000000, 150, 6, 2, 'Grandmas are twice as efficient.')

        self.grandmaupgradelabel = Label(self.buildingupgradeframe, text='Forwards from grandma:\n1000 Cookies',
                                         font='arial 14', padx=20, pady=10, bg=bupgradebg, justify=LEFT, wraplength=200)

        self.grandmaupgradetext = Label(self.buildingupgradeframe, text=self.grandmaupgrade1.descriptiontext,
                                        font='arial 10', padx=20, pady=10, bg=bupgradebg, justify=CENTER, wraplength=150)

        self.grandmaupgradebutton = Button(self.buildingupgradeframe, padx=20, pady=10, command=self.grandmaupgrade,
                                           image=self.redbuybutton, highlightthickness=0, bd=0, bg=bupgradebg, activebackground=bupgradebg, cursor="hand2")

        # Farm
        self.farmupgradelabel = Label(
            self.buildingupgradeframe, text='Upgrade Farm', font='arial 14', padx=20, pady=10, bg=bupgradebg)

        self.farmtext = Label(self.buildingupgradeframe, text='Multiplier: 1x',
                              font='arial 10', padx=20, pady=10, bg=bupgradebg)

        self.farmupgradebutton = Button(self.buildingupgradeframe, text='Buy', font='arial 14 bold',
                                        padx=20, pady=10, command=self.b, state=DISABLED, fg='green4')

        # Mine
        self.mineupgradelabel = Label(
            self.buildingupgradeframe, text='Upgrade Mine', font='arial 14', padx=20, pady=10, bg=bupgradebg)

        self.minetext = Label(self.buildingupgradeframe, text='Multiplier: 1x',
                              font='arial 10', padx=20, pady=10, bg=bupgradebg)

        self.mineupgradebutton = Button(self.buildingupgradeframe, text='Buy', font='arial 14 bold',
                                        padx=20, pady=10, command=self.b, state=DISABLED, fg='green4')

        # Factory
        self.factoryupgradelabel = Label(
            self.buildingupgradeframe, text='Upgrade Factory', font='arial 14', padx=20, pady=10, bg=bupgradebg)

        self.factorytext = Label(self.buildingupgradeframe, text='Multiplier: 1x',
                                 font='arial 10', padx=20, pady=10, bg=bupgradebg)

        self.factoryupgradebutton = Button(self.buildingupgradeframe, text='Buy',
                                           font='arial 14 bold', padx=20, pady=10, command=self.b, state=DISABLED, fg='green4')

        self.pricecheck()

        def spawngoldcookie():  # Function which creates an event every 30-180 seconds which spawns a gold cookie worth 1000% of cookies per click
            while True:
                if self.closeprogram == True:
                    break
                else:
                    # random number for seconds to before golden cookie occurs
                    randomtime = random.randint(30, 180)
                    for i in range(randomtime):
                        time.sleep(1)
                        if self.closeprogram == True:
                            break
                    if self.closeprogram == True:
                        break
                    else:
                        self.cookie_button.configure(
                            image=self.goldcookieimage, command=self.gold_cookie_click)
                        self.cookie_heading.configure(
                            fg='#ffe76d', text='Click the Golden Cookie')
                        self.cookie_button.unbind("<Enter>")
                        self.cookie_button.unbind("<Leave>")
                        self.cookie_button.bind(
                            "<Enter>", self.hovergoldcookie)
                        self.cookie_button.bind(
                            "<Leave>", self.unhovergoldcookie)
                        for i in range(13):
                            time.sleep(1)
                            if self.closeprogram == True:
                                break
                        if self.closeprogram == True:
                            break
                        else:
                            self.cookie_button.configure(
                                image=self.cookieimage, command=self.cookie_click)
                            self.cookie_heading.configure(
                                fg='white', text='Click the Cookie')
                            self.cookie_button.unbind("<Enter>")
                            self.cookie_button.unbind("<Leave>")
                            self.cookie_button.bind(
                                "<Enter>", self.hovercookie)
                            self.cookie_button.bind(
                                "<Leave>", self.unhovercookie)

        self.firstgoldencookie = False
        self.backgroundspawngoldcookie = threading.Thread(
            name='spawngoldcookietimer', target=spawngoldcookie)  # create threading variable
        self.backgroundspawngoldcookie.start()

        def idlecookies():  # Background loop for idle upgrades
            while True:
                if self.closeprogram == True:
                    break
                else:
                    try:
                        try:
                            sleeptime = 1 / self.cps  # calculate time for 1 cookie
                            if sleeptime < 0.15:  # prevent lag as min time.sleep is 10-12ms
                                time.sleep(0.15)
                                self.cookies += 0.15 * self.cps
                                self.changecookietext()
                                self.pricecheck()
                            elif sleeptime > 1:  # If cps < 1
                                remainder = sleeptime % 1
                                sleeptimeround = math.floor(sleeptime)
                                for i in range(sleeptimeround):
                                    time.sleep(1)
                                    if self.closeprogram == True:
                                        break
                                    elif 1 / self.cps <= 1:
                                        break
                                if self.closeprogram == True:
                                    break
                                else:
                                    time.sleep(remainder)
                                    self.cookies += 1
                                    self.changecookietext()
                                    self.pricecheck()
                            else:  # normal cookie idle
                                time.sleep(sleeptime)
                                self.cookies += 1
                                self.changecookietext()
                                self.pricecheck()
                        except ZeroDivisionError:  # in the case thread starts when cps = 0, ignores error.
                            pass
                    except RuntimeError:  # break loop when program is closed
                        break

        self.backgroundpersec = threading.Thread(
            name='idlecookies', target=idlecookies)  # create threading variable

    def b(self):
        pass

    def startidletimer(self):  # starts idle thread
        try:
            self.backgroundpersec.start()
        except RuntimeError:  # doesnt start if already started
            pass

    # function which takes in a number then shortens it if it is a large number e.g. 1,000,000,000 = 1 billion
    def numbercheck(self, inputed):
        num = math.floor(inputed)
        if 10 > len(str(num)) >= 7:
            numstr = str(num)
            if len(str(num)) == 7:
                decimal = numstr[:1] + '.' + numstr[1:6]
            if len(str(num)) == 8:
                decimal = numstr[:2] + '.' + numstr[2:6]
            if len(str(num)) == 9:
                decimal = numstr[:3] + '.' + numstr[3:6]
            number = ('{} million'.format(decimal))
            return number
        if 13 > len(str(num)) >= 10:
            numstr = str(num)
            if len(str(num)) == 10:
                decimal = numstr[:1] + '.' + numstr[1:6]
            if len(str(num)) == 11:
                decimal = numstr[:2] + '.' + numstr[2:6]
            if len(str(num)) == 12:
                decimal = numstr[:3] + '.' + numstr[3:6]
            number = ('{} billion'.format(decimal))
            return number
        if 16 > len(str(num)) >= 13:
            numstr = str(num)
            if len(str(num)) == 13:
                decimal = numstr[:1] + '.' + numstr[1:6]
            if len(str(num)) == 14:
                decimal = numstr[:2] + '.' + numstr[2:6]
            if len(str(num)) == 15:
                decimal = numstr[:3] + '.' + numstr[3:6]
            number = ('{} trillion'.format(decimal))
            return number
        if 19 > len(str(num)) >= 16:
            numstr = str(num)
            if len(str(num)) == 16:
                decimal = numstr[:1] + '.' + numstr[1:6]
            if len(str(num)) == 17:
                decimal = numstr[:2] + '.' + numstr[2:6]
            if len(str(num)) == 18:
                decimal = numstr[:3] + '.' + numstr[3:6]
            number = ('{} quadrillion'.format(decimal))
            return number
        if 22 > len(str(num)) >= 19:
            numstr = str(num)
            if len(str(num)) == 19:
                decimal = numstr[:1] + '.' + numstr[1:6]
            if len(str(num)) == 20:
                decimal = numstr[:2] + '.' + numstr[2:6]
            if len(str(num)) == 21:
                decimal = numstr[:3] + '.' + numstr[3:6]
            number = ('{} quintillion'.format(decimal))
            return number
        if 25 > len(str(num)) >= 22:
            numstr = str(num)
            if len(str(num)) == 22:
                decimal = numstr[:1] + '.' + numstr[1:6]
            if len(str(num)) == 23:
                decimal = numstr[:2] + '.' + numstr[2:6]
            if len(str(num)) == 24:
                decimal = numstr[:3] + '.' + numstr[3:6]
            number = ('{} sextillion'.format(decimal))
            return number
        if 28 > len(str(num)) >= 25:
            numstr = str(num)
            if len(str(num)) == 25:
                decimal = numstr[:1] + '.' + numstr[1:6]
            if len(str(num)) == 26:
                decimal = numstr[:2] + '.' + numstr[2:6]
            if len(str(num)) == 27:
                decimal = numstr[:3] + '.' + numstr[3:6]
            number = ('{} septillion'.format(decimal))
            return number
        if 31 > len(str(num)) >= 28:
            numstr = str(num)
            if len(str(num)) == 28:
                decimal = numstr[:1] + '.' + numstr[1:6]
            if len(str(num)) == 29:
                decimal = numstr[:2] + '.' + numstr[2:6]
            if len(str(num)) == 30:
                decimal = numstr[:3] + '.' + numstr[3:6]
            number = ('{} octillion'.format(decimal))
            return number
        if 34 > len(str(num)) >= 31:
            numstr = str(num)
            if len(str(num)) == 31:
                decimal = numstr[:1] + '.' + numstr[1:6]
            if len(str(num)) == 32:
                decimal = numstr[:2] + '.' + numstr[2:6]
            if len(str(num)) == 33:
                decimal = numstr[:3] + '.' + numstr[3:6]
            number = ('{} nonillion'.format(decimal))
            return number
        if 37 > len(str(num)) >= 34:
            numstr = str(num)
            if len(str(num)) == 34:
                decimal = numstr[:1] + '.' + numstr[1:6]
            if len(str(num)) == 35:
                decimal = numstr[:2] + '.' + numstr[2:6]
            if len(str(num)) == 36:
                decimal = numstr[:3] + '.' + numstr[3:6]
            number = ('{} decillion'.format(decimal))
            return number
        if len(str(num)) >= 37:
            numstr = str(num)
            decimal = numstr[:1] + '.' + numstr[1:6]
            exponent = len(str(num)) - 1
            number = ('{}e{}'.format(decimal, exponent))
            return number
        else:
            return inputed

    def pricecheck(self):  # Checks the cookie count and prices then enables/disables upgrade buy buttons accordingly
        if self.cookies >= self.cursor_price:
            self.cursor_buy.config(image=self.buybuttonimage)
            self.cursor_buyable = True
            pass
        else:
            self.cursor_buy.config(image=self.redbuybutton)
            self.cursor_buyable = False
            pass

        if self.cookies >= self.grandma_price:
            self.grandma_buy.config(image=self.buybuttonimage)
            self.grandma_buyable = True
            pass
        else:
            self.grandma_buy.config(image=self.redbuybutton)
            self.grandma_buyable = False
            pass

        if self.cookies >= self.farm_price:
            self.farm_buy.config(image=self.buybuttonimage)
            self.farm_buyable = True
            pass
        else:
            self.farm_buy.config(image=self.redbuybutton)
            self.farm_buyable = False
            pass
        if self.cookies >= self.mine_price:
            self.mine_buy.config(image=self.buybuttonimage)
            self.mine_buyable = True
            pass
        else:
            self.mine_buy.config(image=self.redbuybutton)
            self.mine_buyable = False
            pass
        if self.cookies >= self.factory_price:
            self.factory_buy.config(image=self.buybuttonimage)
            self.factory_buyable = True
            pass
        else:
            self.factory_buy.config(image=self.redbuybutton)
            self.factory_buyable = False
            pass
        if self.cookies >= self.bank_price:
            self.bank_buy.config(image=self.buybuttonimage)
            self.bank_buyable = True
            pass
        else:
            self.bank_buy.config(image=self.redbuybutton)
            self.bank_buyable = False
            pass
        if self.cookies >= self.temple_price:
            self.temple_buy.config(image=self.buybuttonimage)
            self.temple_buyable = True
            pass
        else:
            self.temple_buy.config(image=self.redbuybutton)
            self.temple_buyable = False
            pass
        if self.cookies >= self.wizardtower_price:
            self.wizardtower_buy.config(image=self.buybuttonimage)
            self.wizardtower_buyable = True
            pass
        else:
            self.wizardtower_buy.config(image=self.redbuybutton)
            self.wizardtower_buyable = False
            pass
        if self.cookies >= self.shipment_price:
            self.shipment_buy.config(image=self.buybuttonimage)
            self.shipment_buyable = True
            pass
        else:
            self.shipment_buy.config(image=self.redbuybutton)
            self.shipment_buyable = False
            pass
        if self.cookies >= self.alchemylab_price:
            self.alchemylab_buy.config(image=self.buybuttonimage)
            self.alchemylab_buyable = True
            pass
        else:
            self.alchemylab_buy.config(image=self.redbuybutton)
            self.alchemylab_buyable = False
            pass
        if self.cookies >= self.portal_price:
            self.portal_buy.config(image=self.buybuttonimage)
            self.portal_buyable = True
            pass
        else:
            self.portal_buy.config(image=self.redbuybutton)
            self.portal_buyable = False
            pass
        if self.cookies >= self.timemachine_price:
            self.timemachine_buy.config(image=self.buybuttonimage)
            self.timemachine_buyable = True
            pass
        else:
            self.timemachine_buy.config(image=self.redbuybutton)
            self.timemachine_buyable = False
            pass

        if self.cookies >= self.cursorupgradeprice:
            self.cursorupgradebutton.config(image=self.buybuttonimage)
            self.cursorupgradebuyable = True
        else:
            self.cursorupgradebutton.config(image=self.redbuybutton)
            self.cursorupgradebuyable = False

        if self.cookies >= self.grandmaupgradeprice:
            self.grandmaupgradebutton.config(image=self.buybuttonimage)
            self.grandmaupgradebuyable = True
        else:
            self.grandmaupgradebutton.config(image=self.redbuybutton)
            self.grandmaupgradebuyable = False

    def changecookietext(self):  # Change the cookie amount label
        # round down as actual amount can have decimals
        roundedcookies = math.floor(self.cookies)
        try:
            cookieamt = math.floor(self.numbercheck(self.cookies))
        except TypeError:
            cookieamt = self.numbercheck(self.cookies)
        cookies_text = ('{} Cookies'.format(cookieamt))
        self.cookie_counter.configure(text=cookies_text)

    def timesone(self):  # function for x1 button, sets multiplier to 1 and updates labels
        if self.upgrademultiplieramount == 1:
            pass
        else:
            self.upgrademultiplieramount = 1
            self.upgrademultiplier = 1.15
            self.multiplierone.configure(font='arial 12 bold')
            self.multiplierten.configure(font='arial 12')
            self.multiplierhundred.configure(font='arial 12')
            self.pricecalc()

    def timesten(self):  # function for x10 button, sets multiplier to 10 and updates labels
        if self.upgrademultiplieramount == 10:
            pass
        else:
            self.upgrademultiplieramount = 10
            self.upgrademultiplier = 20.303718238
            self.multiplierone.configure(font='arial 12')
            self.multiplierten.configure(font='arial 12 bold')
            self.multiplierhundred.configure(font='arial 12')
            self.pricecalc()

    # function for x100 button, sets multiplier to 100 and updates labels
    def timeshundred(self):
        if self.upgrademultiplieramount == 100:
            pass
        else:
            self.upgrademultiplieramount = 100
            self.upgrademultiplier = 7828749.671335256
            self.multiplierone.configure(font='arial 12')
            self.multiplierten.configure(font='arial 12')
            self.multiplierhundred.configure(font='arial 12 bold')
            self.pricecalc()

    def pricecalc(self):  # calculates the prices of upgrade purchases depending on the upgrade multiplier selected
        if self.upgrademultiplieramount == 1:
            self.cursor_price = self.basecursor_price
            cursorprice_text = ('Cursor:\n{} Cookies'.format(
                self.numbercheck(self.cursor_price)))
            self.cursor_label.configure(text=cursorprice_text)

            self.grandma_price = self.basegrandma_price
            grandmaprice_text = ('Grandma:\n{} Cookies'.format(
                self.numbercheck(self.grandma_price)))
            self.grandma_label.configure(text=grandmaprice_text)

            self.farm_price = self.basefarm_price
            farmprice_text = ('Farm:\n{} Cookies'.format(
                self.numbercheck(self.farm_price)))
            self.farm_label.configure(text=farmprice_text)

            self.mine_price = self.basemine_price
            mineprice_text = ('Mine:\n{} Cookies'.format(
                self.numbercheck(self.mine_price)))
            self.mine_label.configure(text=mineprice_text)

            self.factory_price = self.basefactory_price
            factoryprice_text = ('Factory:\n{} Cookies'.format(
                self.numbercheck(self.factory_price)))
            self.factory_label.configure(text=factoryprice_text)

            self.bank_price = self.basebank_price
            bankprice_text = ('Bank:\n{} Cookies'.format(
                self.numbercheck(self.bank_price)))
            self.bank_label.configure(text=bankprice_text)

            self.temple_price = self.basetemple_price
            templeprice_text = ('Temple:\n{} Cookies'.format(
                self.numbercheck(self.temple_price)))
            self.temple_label.configure(text=templeprice_text)

            self.wizardtower_price = self.basewizardtower_price
            wizardtowerprice_text = ('Wizard Tower:\n{} Cookies'.format(
                self.numbercheck(self.wizardtower_price)))
            self.wizardtower_label.configure(text=wizardtowerprice_text)

            self.shipment_price = self.baseshipment_price
            shipmentprice_text = ('Shipment:\n{} Cookies'.format(
                self.numbercheck(self.shipment_price)))
            self.shipment_label.configure(text=shipmentprice_text)

            self.alchemylab_price = self.basealchemylab_price
            alchemylabprice_text = ('Alchemy Lab:\n{} Cookies'.format(
                self.numbercheck(self.alchemylab_price)))
            self.alchemylab_label.configure(text=alchemylabprice_text)

            self.portal_price = self.baseportal_price
            portalprice_text = ('Portal:\n{} Cookies'.format(
                self.numbercheck(self.portal_price)))
            self.portal_label.configure(text=portalprice_text)

            self.timemachine_price = self.basetimemachine_price
            timemachineprice_text = ('Time Machine:\n{} Cookies'.format(
                self.numbercheck(self.timemachine_price)))
            self.timemachine_label.configure(text=timemachineprice_text)

        else:
            self.cursor_price = math.ceil(
                self.basecursor_price * self.upgrademultiplier)
            cursorprice_text = ('Cursor:\n{} Cookies'.format(
                self.numbercheck(self.cursor_price)))
            self.cursor_label.configure(text=cursorprice_text)

            self.grandma_price = math.ceil(
                self.basegrandma_price * self.upgrademultiplier)
            grandmaprice_text = ('Grandma:\n{} Cookies'.format(
                self.numbercheck(self.grandma_price)))
            self.grandma_label.configure(text=grandmaprice_text)

            self.farm_price = math.ceil(
                self.basefarm_price * self.upgrademultiplier)
            farmprice_text = ('Farm:\n{} Cookies'.format(
                self.numbercheck(self.farm_price)))
            self.farm_label.configure(text=farmprice_text)

            self.mine_price = math.ceil(
                self.basemine_price * self.upgrademultiplier)
            mineprice_text = ('Mine:\n{} Cookies'.format(
                self.numbercheck(self.mine_price)))
            self.mine_label.configure(text=mineprice_text)

            self.factory_price = math.ceil(
                self.basefactory_price * self.upgrademultiplier)
            factoryprice_text = ('Factory:\n{} Cookies'.format(
                self.numbercheck(self.factory_price)))
            self.factory_label.configure(text=factoryprice_text)

            self.bank_price = math.ceil(
                self.basebank_price * self.upgrademultiplier)
            bankprice_text = ('Bank:\n{} Cookies'.format(
                self.numbercheck(self.bank_price)))
            self.bank_label.configure(text=bankprice_text)

            self.temple_price = math.ceil(
                self.basetemple_price * self.upgrademultiplier)
            templeprice_text = ('Temple:\n{} Cookies'.format(
                self.numbercheck(self.temple_price)))
            self.temple_label.configure(text=templeprice_text)

            self.wizardtower_price = math.ceil(
                self.basewizardtower_price * self.upgrademultiplier)
            wizardtowerprice_text = ('Wizard Tower:\n{} Cookies'.format(
                self.numbercheck(self.wizardtower_price)))
            self.wizardtower_label.configure(text=wizardtowerprice_text)

            self.shipment_price = math.ceil(
                self.baseshipment_price * self.upgrademultiplier)
            shipmentprice_text = ('Shipment:\n{} Cookies'.format(
                self.numbercheck(self.shipment_price)))
            self.shipment_label.configure(text=shipmentprice_text)

            self.alchemylab_price = math.ceil(
                self.basealchemylab_price * self.upgrademultiplier)
            alchemylabprice_text = ('Alchemy Lab:\n{} Cookies'.format(
                self.numbercheck(self.alchemylab_price)))
            self.alchemylab_label.configure(text=alchemylabprice_text)

            self.portal_price = math.ceil(
                self.baseportal_price * self.upgrademultiplier)
            portalprice_text = ('Portal:\n{} Cookies'.format(
                self.numbercheck(self.portal_price)))
            self.portal_label.configure(text=portalprice_text)

            self.timemachine_price = math.ceil(
                self.basetimemachine_price * self.upgrademultiplier)
            timemachineprice_text = ('Time Machine:\n{} Cookies'.format(
                self.numbercheck(self.timemachine_price)))
            self.timemachine_label.configure(text=timemachineprice_text)

        # Change button state
        self.pricecheck()

    def cursor(self):  # function for buying a cursor
        if self.cursor_buyable == True:
            self.cursors += 1 * self.upgrademultiplieramount  # Add a cursor

            # Change amount text
            cursors_text = ('Amount: {}'.format(self.cursors))
            self.cursor_amount.configure(text=cursors_text)

            self.cookies = self.cookies - self.cursor_price  # Deduct cookies from price

            # change cookie amount text
            self.changecookietext()

            # Calculate new price
            self.basecursor_price = math.ceil(
                self.basecursor_price * 1.15 * self.upgrademultiplieramount)
            self.pricecalc()

            # Change button state
            self.pricecheck()

            # calculates cookies per second
            self.cpscalc()

            self.thousandfingerscalc()
        else:
            pass

    def cursorupgrade(self):
        if self.cursorupgradebuyable == True:
            if self.cursororder == 1:
                self.cursorupgrade2.updateinfo(self)
                self.cursorupgrade1.buy(self)
            elif self.cursororder == 2:
                self.cursorupgrade3.updateinfo(self)
                self.cursorupgrade2.buy(self)
            elif self.cursororder == 3:
                self.cursorupgrade4.updateinfo(self)
                self.cursorupgrade3.buy(self)
            elif self.cursororder == 4:
                self.cursorupgrade5.updateinfo(self)
                self.cursorupgrade4.buy(self)
            elif self.cursororder == 5:
                self.cursorupgrade6.updateinfo(self)
                self.cursorupgrade5.buy(self)
            elif self.cursororder == 6:
                self.cursorupgrade7.updateinfo(self)
                self.cursorupgrade6.buy(self)
            elif self.cursororder == 7:
                self.cursorupgrade8.updateinfo(self)
                self.cursorupgrade7.buy(self)
            elif self.cursororder == 8:
                self.cursorupgrade9.updateinfo(self)
                self.cursorupgrade8.buy(self)
            elif self.cursororder == 9:
                self.cursorupgrade10.updateinfo(self)
                self.cursorupgrade9.buy(self)
            elif self.cursororder == 10:
                self.cursorupgrade11.updateinfo(self)
                self.cursorupgrade10.buy(self)
            elif self.cursororder == 11:
                self.cursorupgrade12.updateinfo(self)
                self.cursorupgrade11.buy(self)
            elif self.cursororder == 12:
                self.cursorupgrade13.updateinfo(self)
                self.cursorupgrade12.buy(self)
            elif self.cursororder == 13:
                self.cursorupgradeprice = math.inf
                self.cursorupgradelabel.configure(
                    text='Cursor Upgrades Maxed')
                self.cursorupgradetext.configure(
                    text='')
                self.cursorupgrade13.buy(self)

    def thousandfingerscalc(self):
        if self.thousandfingersbought == True:
            totalbuildingsexceptcursors = self.grandmas + \
                self.farms + self.mines + self.factories + self.banks + self.temples + \
                self.wizardtowers + self.shipments + \
                self.alchemylabs + self.portals + self.timemachines
            self.perclick = self.perclick + \
                totalbuildingsexceptcursors * self.thousandfingersamount
            self.cursorcps = self.cursorcps + \
                totalbuildingsexceptcursors * self.thousandfingersamount
            self.cpscalc()
            self.updateperclick()
        else:
            pass

    def grandma(self):  # function for buying a grandma
        if self.grandma_buyable == True:
            self.grandmas += 1 * self.upgrademultiplieramount  # Add a grandma

            # Change amount text
            grandmas_text = ('Amount: {}'.format(self.grandmas))
            self.grandma_amount.configure(text=grandmas_text)

            self.cookies = self.cookies - self.grandma_price  # Deduct cookies from price

            # change cookie amount text
            self.changecookietext()

            # Calculate new price
            self.basegrandma_price = math.ceil(
                self.basegrandma_price * 1.15 * self.upgrademultiplieramount)
            self.pricecalc()

            # Change button state
            self.pricecheck()

            # calculates cookies per second
            self.cpscalc()
            self.thousandfingerscalc()
        else:
            pass

    def grandmaupgrade(self):
        if self.grandmaupgradebuyable == True:
            if self.grandmaorder == 1:
                self.grandmaupgradeprice = self.grandmaupgrade2.price
                grandmasupgrade_text = ('{}:\n{} Cookies'.format(
                    self.grandmaupgrade2.name, self.numbercheck(self.grandmaupgrade2.price)))
                self.grandmaupgradelabel.configure(text=grandmasupgrade_text)
                self.grandmaupgradetext.configure(
                    text=self.grandmaupgrade2.descriptiontext)
                self.grandmaupgrade1.buy(self)

            elif self.grandmaorder == 2:
                self.grandmaupgradeprice = self.grandmaupgrade3.price
                grandmasupgrade_text = ('{}:\n{} Cookies'.format(
                    self.grandmaupgrade3.name, self.numbercheck(self.grandmaupgrade3.price)))
                self.grandmaupgradelabel.configure(text=grandmasupgrade_text)
                self.grandmaupgradetext.configure(
                    text=self.grandmaupgrade3.descriptiontext)
                self.grandmaupgrade2.buy(self)
            elif self.grandmaorder == 3:
                self.grandmaupgradeprice = self.grandmaupgrade4.price
                grandmasupgrade_text = ('{}:\n{} Cookies'.format(
                    self.grandmaupgrade4.name, self.numbercheck(self.grandmaupgrade4.price)))
                self.grandmaupgradelabel.configure(text=grandmasupgrade_text)
                self.grandmaupgradetext.configure(
                    text=self.grandmaupgrade4.descriptiontext)
                self.grandmaupgrade3.buy(self)
            elif self.grandmaorder == 4:
                self.grandmaupgradeprice = self.grandmaupgrade5.price
                grandmasupgrade_text = ('{}:\n{} Cookies'.format(
                    self.grandmaupgrade5.name, self.numbercheck(self.grandmaupgrade5.price)))
                self.grandmaupgradelabel.configure(text=grandmasupgrade_text)
                self.grandmaupgradetext.configure(
                    text=self.grandmaupgrade5.descriptiontext)
                self.grandmaupgrade4.buy(self)
            elif self.grandmaorder == 5:
                self.grandmaupgradeprice = self.grandmaupgrade6.price
                grandmasupgrade_text = ('{}:\n{} Cookies'.format(
                    self.grandmaupgrade6.name, self.numbercheck(self.grandmaupgrade6.price)))
                self.grandmaupgradelabel.configure(text=grandmasupgrade_text)
                self.grandmaupgradetext.configure(
                    text=self.grandmaupgrade6.descriptiontext)
                self.grandmaupgrade5.buy(self)
            elif self.grandmaorder == 6:
                self.grandmaupgrade6.buy(self)

    def farm(self):  # function for buying a farm
        if self.farm_buyable == True:
            self.farms += 1 * self.upgrademultiplieramount  # Add a farm

            # Change amount text
            farms_text = ('Amount: {}'.format(self.farms))
            self.farm_amount.configure(text=farms_text)

            self.cookies = self.cookies - self.farm_price  # Deduct cookies from price

            # change cookie amount text
            self.changecookietext()

            # Calculate new price
            self.basefarm_price = math.ceil(
                self.basefarm_price * 1.15 * self.upgrademultiplieramount)
            self.pricecalc()

            # Change button state
            self.pricecheck()

            # calculates cookies per second
            self.cpscalc()
            self.thousandfingerscalc()
        else:
            pass

    def mine(self):  # function for buying a mine
        if self.mine_buyable == True:
            self.mines += 1 * self.upgrademultiplieramount  # Add a mine

            # Change amount text
            mines_text = ('Amount: {}'.format(self.mines))
            self.mine_amount.configure(text=mines_text)

            self.cookies = self.cookies - self.mine_price  # Deduct cookies from price

            # change cookie amount text
            self.changecookietext()

            # Calculate new price
            self.basemine_price = math.ceil(
                self.basemine_price * 1.15 * self.upgrademultiplieramount)
            self.pricecalc()

            # Change button state
            self.pricecheck()

            # calculates cookies per second
            self.cpscalc()
            self.thousandfingerscalc()
        else:
            pass

    def factory(self):  # function for buying a factory
        if self.factory_buyable == True:
            self.factories += 1 * self.upgrademultiplieramount  # Add a factory

            # Change amount text
            factories_text = ('Amount: {}'.format(self.factories))
            self.factory_amount.configure(text=factories_text)

            self.cookies = self.cookies - self.factory_price  # Deduct cookies from price

            # change cookie amount text
            self.changecookietext()

            # Calculate new price
            self.basefactory_price = math.ceil(
                self.basefactory_price * 1.15 * self.upgrademultiplieramount)
            self.pricecalc()

            # Change button state
            self.pricecheck()

            # calculates cookies per second
            self.cpscalc()
            self.thousandfingerscalc()
        else:
            pass

    def bank(self):  # function for buying a bank
        if self.bank_buyable == True:
            self.banks += 1 * self.upgrademultiplieramount  # Add a bank

            # Change amount text
            banks_text = ('Amount: {}'.format(self.banks))
            self.bank_amount.configure(text=banks_text)

            self.cookies = self.cookies - self.bank_price  # Deduct cookies from price

            # change cookie amount text
            self.changecookietext()

            # Calculate new price
            self.basebank_price = math.ceil(
                self.basebank_price * 1.15 * self.upgrademultiplieramount)
            self.pricecalc()

            # Change button state
            self.pricecheck()

            # calculates cookies per second
            self.cpscalc()
            self.thousandfingerscalc()
        else:
            pass

    def temple(self):  # function for buying a temple
        if self.temple_buyable == True:
            self.temples += 1 * self.upgrademultiplieramount  # Add a temple

            # Change amount text
            temples_text = ('Amount: {}'.format(self.temples))
            self.temple_amount.configure(text=temples_text)

            self.cookies = self.cookies - self.temple_price  # Deduct cookies from price

            # change cookie amount text
            self.changecookietext()

            # Calculate new price
            self.basetemple_price = math.ceil(
                self.basetemple_price * 1.15 * self.upgrademultiplieramount)
            self.pricecalc()

            # Change button state
            self.pricecheck()

            # calculates cookies per second
            self.cpscalc()

            self.thousandfingerscalc()
        else:
            pass

    def wizardtower(self):  # function for buying a wizardtower
        if self.wizardtower_buyable == True:
            self.wizardtowers += 1 * self.upgrademultiplieramount  # Add a wizardtower

            # Change amount text
            wizardtowers_text = ('Amount: {}'.format(self.wizardtowers))
            self.wizardtower_amount.configure(text=wizardtowers_text)

            self.cookies = self.cookies - self.wizardtower_price  # Deduct cookies from price

            # change cookie amount text
            self.changecookietext()

            # Calculate new price
            self.basewizardtower_price = math.ceil(
                self.basewizardtower_price * 1.15 * self.upgrademultiplieramount)
            self.pricecalc()

            # Change button state
            self.pricecheck()

            # calculates cookies per second
            self.cpscalc()

            self.thousandfingerscalc()
        else:
            pass

    def shipment(self):  # function for buying a shipment
        if self.shipment_buyable == True:
            self.shipments += 1 * self.upgrademultiplieramount  # Add a shipment

            # Change amount text
            shipments_text = ('Amount: {}'.format(self.shipments))
            self.shipment_amount.configure(text=shipments_text)

            self.cookies = self.cookies - self.shipment_price  # Deduct cookies from price

            # change cookie amount text
            self.changecookietext()

            # Calculate new price
            self.baseshipment_price = math.ceil(
                self.baseshipment_price * 1.15 * self.upgrademultiplieramount)
            self.pricecalc()

            # Change button state
            self.pricecheck()

            # calculates cookies per second
            self.cpscalc()

            self.thousandfingerscalc()
        else:
            pass

    def alchemylab(self):  # function for buying a alchemylab
        if self.alchemylab_buyable == True:
            self.alchemylabs += 1 * self.upgrademultiplieramount  # Add a alchemylab

            # Change amount text
            alchemylabs_text = ('Amount: {}'.format(self.alchemylabs))
            self.alchemylab_amount.configure(text=alchemylabs_text)

            self.cookies = self.cookies - self.alchemylab_price  # Deduct cookies from price

            # change cookie amount text
            self.changecookietext()

            # Calculate new price
            self.basealchemylab_price = math.ceil(
                self.basealchemylab_price * 1.15 * self.upgrademultiplieramount)
            self.pricecalc()

            # Change button state
            self.pricecheck()

            # calculates cookies per second
            self.cpscalc()

            self.thousandfingerscalc()
        else:
            pass

    def portal(self):  # function for buying a portal
        if self.portal_buyable == True:
            self.portals += 1 * self.upgrademultiplieramount  # Add a portal

            # Change amount text
            portals_text = ('Amount: {}'.format(self.portals))
            self.portal_amount.configure(text=portals_text)

            self.cookies = self.cookies - self.portal_price  # Deduct cookies from price

            # change cookie amount text
            self.changecookietext()

            # Calculate new price
            self.baseportal_price = math.ceil(
                self.baseportal_price * 1.15 * self.upgrademultiplieramount)
            self.pricecalc()

            # Change button state
            self.pricecheck()

            # calculates cookies per second
            self.cpscalc()

            self.thousandfingerscalc()
        else:
            pass

    def timemachine(self):  # function for buying a timemachine
        if self.timemachine_buyable == True:
            self.timemachines += 1 * self.upgrademultiplieramount  # Add a timemachine

            # Change amount text
            timemachines_text = ('Amount: {}'.format(self.timemachines))
            self.timemachine_amount.configure(text=timemachines_text)

            self.cookies = self.cookies - self.timemachine_price  # Deduct cookies from price

            # change cookie amount text
            self.changecookietext()

            # Calculate new price
            self.basetimemachine_price = math.ceil(
                self.basetimemachine_price * 1.15 * self.upgrademultiplieramount)
            self.pricecalc()

            # Change button state
            self.pricecheck()

            # calculates cookies per second
            self.cpscalc()

            self.thousandfingerscalc()
        else:
            pass

    def cookie_click(self):  # function for clicking on cookie
        self.cookies += self.perclick  # adds cookie by perclick multiplier
        self.changecookietext()  # updates cookie amount label
        self.pricecheck()  # checks if any purchases are available

    def gold_cookie_click(self):
        if self.firstgoldencookie == False:
            firstgoldencookiewindow = FirstGold(self)
            self.firstgoldencookie = True
        self.cookies += self.perclick * 100
        self.changecookietext()
        self.pricecheck()
        self.cookie_button.configure(
            image=self.cookieimage, command=self.cookie_click)
        self.cookie_heading.configure(fg='white', text='Click the Cookie')
        self.cookie_button.unbind("<Enter>")
        self.cookie_button.unbind("<Leave>")
        self.cookie_button.bind("<Enter>", self.hovercookie)
        self.cookie_button.bind("<Leave>", self.unhovercookie)

    def cpscalc(self):  # calculates cps from number of upgrades owned
        self.cps = self.cursorcps * self.cursors + self.grandmacps * self.grandmas + self.farmcps * \
            self.farms + self.minecps * self.mines + self.factorycps * \
            self.factories + self.bankcps * self.banks + self.templecps * self.temples + self.wizardtowercps * self.wizardtowers + self.shipmentcps * \
            self.shipments + self.alchemylabcps * self.alchemylabs + \
            self.portalcps * self.portals + self.timemachinecps * self.timemachines
        try:
            cps_text = ('{:.1f} cps'.format(self.numbercheck(self.cps)))
        except ValueError:
            cps_text = ('{} cps'.format(self.numbercheck(self.cps)))
        self.cpslabel.configure(text=cps_text)

    def updateperclick(self):  # updates the label displaying cookies/click value
        if self.perclick > 1:
            text = ('{} Cookies/click'.format(self.numbercheck(self.perclick)))
            self.perclicklabel.configure(text=text)
        else:
            text = ('{} Cookie/click'.format(self.numbercheck(self.perclick)))
            self.perclicklabel.configure(text=text)

    def collapsebuilding(self):
        self.buildingexpandbutton.configure(
            text='+', command=self.expandbuilding)
        self.arrowsandcpsframe.grid_forget()
        self.previouspagebutton.grid_forget()
        self.cpslabel.grid_forget()
        self.nextpagebutton.grid_forget()
        self.buymultiplierframe.grid_forget()
        self.multiplierlabel.grid_forget()
        self.multiplierone.grid_forget()
        self.multiplierten.grid_forget()
        self.multiplierhundred.grid_forget()

        if self.buildingpagenumber == 1:
            self.cursor_label.grid_forget()
            self.cursor_amount.grid_forget()
            self.cursor_buy.grid_forget()
            self.grandma_label.grid_forget()
            self.grandma_amount.grid_forget()
            self.grandma_buy.grid_forget()
            self.farm_label.grid_forget()
            self.farm_amount.grid_forget()
            self.farm_buy.grid_forget()
            self.mine_label.grid_forget()
            self.mine_amount.grid_forget()
            self.mine_buy.grid_forget()
            self.factory_label.grid_forget()
            self.factory_amount.grid_forget()
            self.factory_buy.grid_forget()
            self.bank_label.grid_forget()
            self.bank_amount.grid_forget()
            self.bank_buy.grid_forget()

        elif self.buildingpagenumber == 2:
            self.temple_label.grid_forget()
            self.temple_amount.grid_forget()
            self.temple_buy.grid_forget()
            self.wizardtower_label.grid_forget()
            self.wizardtower_amount.grid_forget()
            self.wizardtower_buy.grid_forget()
            self.shipment_label.grid_forget()
            self.shipment_amount.grid_forget()
            self.shipment_buy.grid_forget()
            self.alchemylab_label.grid_forget()
            self.alchemylab_amount.grid_forget()
            self.alchemylab_buy.grid_forget()
            self.portal_label.grid_forget()
            self.portal_amount.grid_forget()
            self.portal_buy.grid_forget()
            self.timemachine_label.grid_forget()
            self.timemachine_amount.grid_forget()
            self.timemachine_buy.grid_forget()

    def expandbuilding(self):
        self.buildingexpandbutton.configure(
            text='-', command=self.collapsebuilding)
        self.arrowsandcpsframe.grid(row=1, columnspan=3)
        self.previouspagebutton.grid(row=0, column=0, sticky=W)
        self.cpslabel.grid(row=0, column=1, sticky='news', padx=100)
        self.nextpagebutton.grid(row=0, column=2, sticky=E)
        self.buymultiplierframe.grid(row=2, columnspan=3, pady=10)
        self.multiplierlabel.grid(row=0, column=0, padx=20)
        self.multiplierone.grid(row=0, column=1, padx=20)
        self.multiplierten.grid(row=0, column=2, padx=20)
        self.multiplierhundred.grid(row=0, column=3, padx=20)

        if self.buildingpagenumber == 1:
            self.cursor_label.grid(row=3, column=0, sticky=W)
            self.cursor_amount.grid(row=3, column=1)
            self.cursor_buy.grid(row=3, column=2, padx=20, pady=10)
            self.grandma_label.grid(row=4, column=0, sticky=W)
            self.grandma_amount.grid(row=4, column=1)
            self.grandma_buy.grid(
                row=4, column=2, sticky=E, padx=20, pady=10)
            self.farm_label.grid(row=5, column=0, sticky=W)
            self.farm_amount.grid(row=5, column=1)
            self.farm_buy.grid(row=5, column=2, sticky=E, padx=20, pady=10)
            self.mine_label.grid(row=6, column=0, sticky=W)
            self.mine_amount.grid(row=6, column=1)
            self.mine_buy.grid(row=6, column=2, sticky=E, padx=20, pady=10)
            self.factory_label.grid(row=7, column=0, sticky=W)
            self.factory_amount.grid(row=7, column=1)
            self.factory_buy.grid(
                row=7, column=2, sticky=E, padx=20, pady=10)
            self.bank_label.grid(row=8, column=0, sticky=W)
            self.bank_amount.grid(row=8, column=1)
            self.bank_buy.grid(row=8, column=2, sticky=E, padx=20, pady=10)

        elif self.buildingpagenumber == 2:
            self.temple_label.grid(row=3, column=0, sticky=W)
            self.temple_amount.grid(row=3, column=1)
            self.temple_buy.grid(row=3, column=2, padx=20, pady=10)
            self.wizardtower_label.grid(row=4, column=0, sticky=W)
            self.wizardtower_amount.grid(row=4, column=1)
            self.wizardtower_buy.grid(
                row=4, column=2, sticky=E, padx=20, pady=10)
            self.shipment_label.grid(row=5, column=0, sticky=W)
            self.shipment_amount.grid(row=5, column=1)
            self.shipment_buy.grid(
                row=5, column=2, sticky=E, padx=20, pady=10)
            self.alchemylab_label.grid(row=6, column=0, sticky=W)
            self.alchemylab_amount.grid(row=6, column=1)
            self.alchemylab_buy.grid(
                row=6, column=2, sticky=E, padx=20, pady=10)
            self.portal_label.grid(row=7, column=0, sticky=W)
            self.portal_amount.grid(row=7, column=1)
            self.portal_buy.grid(row=7, column=2, sticky=E, padx=20, pady=10)
            self.timemachine_label.grid(row=8, column=0, sticky=W)
            self.timemachine_amount.grid(row=8, column=1)
            self.timemachine_buy.grid(
                row=8, column=2, sticky=E, padx=20, pady=10)

    def collapseupgrade(self):
        self.bupgradelabel.grid_forget()
        self.bupgradelabel.grid(row=0, column=1, pady=10, padx=10, sticky=N)
        self.cursorupgradelabel.grid_forget()
        self.cursorupgradetext.grid_forget()
        self.cursorupgradebutton.grid_forget()
        self.grandmaupgradelabel.grid_forget()
        self.grandmaupgradetext.grid_forget()
        self.grandmaupgradebutton.grid_forget()
        self.farmupgradelabel.grid_forget()
        self.farmtext.grid_forget()
        self.farmupgradebutton.grid_forget()
        self.mineupgradelabel.grid_forget()
        self.minetext.grid_forget()
        self.mineupgradebutton.grid_forget()
        self.factoryupgradelabel.grid_forget()
        self.factorytext.grid_forget()
        self.factoryupgradebutton.grid_forget()

        self.bupgradeexpandbutton.configure(
            command=self.expandupgrade, text='+')

    def expandupgrade(self):
        self.bupgradeexpandbutton.configure(
            command=self.collapseupgrade, text='-')
        self.bupgradelabel.grid_forget()
        self.bupgradelabel.grid(row=0, columnspan=3,
                                pady=10, padx=10, sticky=N)
        self.cursorupgradelabel.grid(row=1, column=0, sticky=W)
        self.cursorupgradetext.grid(row=1, column=1)
        self.cursorupgradebutton.grid(
            row=1, column=2, sticky=E, padx=20, pady=10)
        self.grandmaupgradelabel.grid(row=2, column=0, sticky=W)
        self.grandmaupgradetext.grid(row=2, column=1)
        self.grandmaupgradebutton.grid(
            row=2, column=2, sticky=E, padx=20, pady=10)
        self.farmupgradelabel.grid(row=3, column=0, sticky=W)
        self.farmtext.grid(row=3, column=1)
        self.farmupgradebutton.grid(
            row=3, column=2, sticky=E, padx=20, pady=10)
        self.mineupgradelabel.grid(row=4, column=0, sticky=W)
        self.minetext.grid(row=4, column=1)
        self.mineupgradebutton.grid(
            row=4, column=2, sticky=E, padx=20, pady=10)
        self.factoryupgradelabel.grid(row=5, column=0, sticky=W)
        self.factorytext.grid(row=5, column=1)
        self.factoryupgradebutton.grid(
            row=5, column=2, sticky=E, padx=20, pady=10)

        self.pricecheck()

    def previouspage(self):
        if self.buildingpagenumber == 2:
            self.temple_label.grid_forget()
            self.temple_amount.grid_forget()
            self.temple_buy.grid_forget()
            self.wizardtower_label.grid_forget()
            self.wizardtower_amount.grid_forget()
            self.wizardtower_buy.grid_forget()
            self.shipment_label.grid_forget()
            self.shipment_amount.grid_forget()
            self.shipment_buy.grid_forget()
            self.alchemylab_label.grid_forget()
            self.alchemylab_amount.grid_forget()
            self.alchemylab_buy.grid_forget()
            self.portal_label.grid_forget()
            self.portal_amount.grid_forget()
            self.portal_buy.grid_forget()
            self.timemachine_label.grid_forget()
            self.timemachine_amount.grid_forget()
            self.timemachine_buy.grid_forget()

            self.cursor_label.grid(row=3, column=0, sticky=W)
            self.cursor_amount.grid(row=3, column=1)
            self.cursor_buy.grid(row=3, column=2, padx=20, pady=10)
            self.grandma_label.grid(row=4, column=0, sticky=W)
            self.grandma_amount.grid(row=4, column=1)
            self.grandma_buy.grid(
                row=4, column=2, sticky=E, padx=20, pady=10)
            self.farm_label.grid(row=5, column=0, sticky=W)
            self.farm_amount.grid(row=5, column=1)
            self.farm_buy.grid(row=5, column=2, sticky=E, padx=20, pady=10)
            self.mine_label.grid(row=6, column=0, sticky=W)
            self.mine_amount.grid(row=6, column=1)
            self.mine_buy.grid(row=6, column=2, sticky=E, padx=20, pady=10)
            self.factory_label.grid(row=7, column=0, sticky=W)
            self.factory_amount.grid(row=7, column=1)
            self.factory_buy.grid(
                row=7, column=2, sticky=E, padx=20, pady=10)
            self.bank_label.grid(row=8, column=0, sticky=W)
            self.bank_amount.grid(row=8, column=1)
            self.bank_buy.grid(row=8, column=2, sticky=E, padx=20, pady=10)

            self.previouspagebutton.configure(state=DISABLED)
            self.nextpagebutton.configure(state=NORMAL)
            self.buildingpagenumber = 1
        else:
            self.previouspagebutton.configure(state=DISABLED)

    def nextpage(self):
        if self.buildingpagenumber == 1:
            self.cursor_label.grid_forget()
            self.cursor_amount.grid_forget()
            self.cursor_buy.grid_forget()
            self.grandma_label.grid_forget()
            self.grandma_amount.grid_forget()
            self.grandma_buy.grid_forget()
            self.farm_label.grid_forget()
            self.farm_amount.grid_forget()
            self.farm_buy.grid_forget()
            self.mine_label.grid_forget()
            self.mine_amount.grid_forget()
            self.mine_buy.grid_forget()
            self.factory_label.grid_forget()
            self.factory_amount.grid_forget()
            self.factory_buy.grid_forget()
            self.bank_label.grid_forget()
            self.bank_amount.grid_forget()
            self.bank_buy.grid_forget()

            self.temple_label.grid(row=3, column=0, sticky=W)
            self.temple_amount.grid(row=3, column=1)
            self.temple_buy.grid(row=3, column=2, padx=20, pady=10)
            self.wizardtower_label.grid(row=4, column=0, sticky=W)
            self.wizardtower_amount.grid(row=4, column=1)
            self.wizardtower_buy.grid(
                row=4, column=2, sticky=E, padx=20, pady=10)
            self.shipment_label.grid(row=5, column=0, sticky=W)
            self.shipment_amount.grid(row=5, column=1)
            self.shipment_buy.grid(
                row=5, column=2, sticky=E, padx=20, pady=10)
            self.alchemylab_label.grid(row=6, column=0, sticky=W)
            self.alchemylab_amount.grid(row=6, column=1)
            self.alchemylab_buy.grid(
                row=6, column=2, sticky=E, padx=20, pady=10)
            self.portal_label.grid(row=7, column=0, sticky=W)
            self.portal_amount.grid(row=7, column=1)
            self.portal_buy.grid(row=7, column=2, sticky=E, padx=20, pady=10)
            self.timemachine_label.grid(row=8, column=0, sticky=W)
            self.timemachine_amount.grid(row=8, column=1)
            self.timemachine_buy.grid(
                row=8, column=2, sticky=E, padx=20, pady=10)

            self.nextpagebutton.configure(state=DISABLED)
            self.previouspagebutton.configure(state=NORMAL)
            self.buildingpagenumber = 2
        else:
            self.nextpagebutton.configure(state=DISABLED)

    def hoverhelp(self, parent):
        parent.widget['background'] = '#21c716'

    def unhoverhelp(self, parent):
        parent.widget['background'] = '#188f10'

    def hoverquit(self, parent):
        parent.widget['background'] = '#c42818'

    def unhoverquit(self, parent):
        parent.widget['background'] = '#8a1b0f'

    def hovercookie(self, parent):
        parent.widget['image'] = self.hovercookieimage

    def unhovercookie(self, parent):
        parent.widget['image'] = self.cookieimage

    def hovergoldcookie(self, parent):
        parent.widget['image'] = self.hovergoldcookieimage

    def unhovergoldcookie(self, parent):
        parent.widget['image'] = self.goldcookieimage

    def quit(self):  # quit button function

        self.cps = 10  # sets cps to 10 so thread sleeps for less time and therefore can kill itself
        self.closeprogram = True
        root.destroy()

    def help(self):  # help button function
        get_help = Help(self)

    def upgradeinfo(self):
        get_info = UpgradeInfo(self)

    def updateupgradesinfo(self, name, description):
        text = str(name) + ': ' + str(description)
        self.upgradeinfolist.append(text)


class Help:

    def __init__(self, parent):
        parent.help_button.configure(state=DISABLED)
        self.box = Toplevel()
        self.box.iconbitmap(r'cookieicon.ico')
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


class UpgradeInfo:
    def __init__(self, parent):
        parent.bupgradeinfobutton.configure(state=DISABLED)
        self.box = Toplevel()
        self.box.iconbitmap(r'cookieicon.ico')
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
        self.box.iconbitmap(r'cookieicon.ico')
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


class CursorUpgrades:
    def __init__(self, parent, name, price, unlock, order, effectfunction, effectnumber, description):
        self.name = str(name)
        self.price = price
        self.unlockcondition = unlock
        self.order = order
        self.effectfunction = effectfunction
        self.effectnumber = effectnumber
        self.descriptiontext = description

    def buy(self, parent):
        parent.cursororder += 1
        parent.cookies = parent.cookies - self.price
        parent.pricecheck()
        parent.changecookietext()
        parent.updateupgradesinfo(
            self.name, self.descriptiontext)
        if self.effectfunction == 'times':
            parent.perclick = parent.perclick * self.effectnumber
            parent.cursorcps = parent.cursorcps * self.effectnumber
            parent.cpscalc()
            parent.updateperclick()
        if self.effectfunction == 'plus':
            parent.thousandfingersbought = True
            self.totalbuildingsexceptcursors = parent.grandmas + \
                parent.farms + parent.mines + parent.factories + parent.banks
            parent.thousandfingersamount = self.effectnumber
            parent.perclick = parent.perclick + \
                self.totalbuildingsexceptcursors * parent.thousandfingersamount
            parent.cursorcps = parent.cursorcps + \
                self.totalbuildingsexceptcursors * parent.thousandfingersamount
            parent.cpscalc()
            parent.updateperclick()
        if self.effectfunction == 'timesthousand':
            self.totalbuildingsexceptcursors = parent.grandmas + \
                parent.farms + parent.mines + parent.factories + parent.banks
            parent.thousandfingersamount = parent.thousandfingersamount * self.effectnumber
            parent.perclick = parent.perclick + \
                self.totalbuildingsexceptcursors * parent.thousandfingersamount
            parent.cursorcps = parent.cursorcps + \
                self.totalbuildingsexceptcursors * parent.thousandfingersamount
            parent.cpscalc()
            parent.updateperclick()

    def updateinfo(self, parent):
        parent.cursorupgradeprice = self.price
        cursorsupgrade_text = ('{}:\n{} Cookies'.format(
            self.name, parent.numbercheck(self.price)))
        parent.cursorupgradelabel.configure(text=cursorsupgrade_text)
        parent.cursorupgradetext.configure(
            text=self.descriptiontext)


class GrandmaUpgrades:
    def __init__(self, parent, name, price, unlock, order, effectnumber, description):
        self.name = str(name)
        self.price = price
        self.unlockcondition = unlock
        self.order = order
        self.effectnumber = effectnumber
        self.descriptiontext = description

    def buy(self, parent):
        parent.grandmaorder += 1
        parent.cookies = parent.cookies - self.price
        parent.pricecheck()
        parent.changecookietext()

        parent.grandmacps = parent.grandmacps * self.effectnumber
        parent.cpscalc()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Cookie Clicker")
    root.iconbitmap(r'cookieicon.ico')
    root.resizable(0, 0)
    Generate = Cookies(root)
    root.mainloop()
