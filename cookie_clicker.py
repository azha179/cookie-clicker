from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
import time
import threading
import math
from functools import partial
import random
import pickle
import os


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
        
        # Save
        self.savebutton = Button(self.buttonframe, text='Save', bg='#051a4d', fg='white', padx=10, pady=10,
                                  command=self.save, font='arial 12 bold', activebackground='#123794', activeforeground='white')
        self.savebutton.grid(row=0, column=1)
        self.savebutton.bind("<Enter>", self.hoversave)
        self.savebutton.bind("<Leave>", self.unhoversave)        
        
        # Load
        self.loadbutton = Button(self.buttonframe, text='Load', bg='#051a4d', fg='white', padx=10, pady=10,
                                  command=self.load, font='arial 12 bold', activebackground='#123794', activeforeground='white')
        self.loadbutton.grid(row=0, column=2)
        self.loadbutton.bind("<Enter>", self.hoverload)
        self.loadbutton.bind("<Leave>", self.unhoverload)                

        # Quit
        self.quit_button = Button(self.buttonframe, text='Quit', bg='#8a1b0f', fg='white', padx=10, pady=10,
                                  command=self.quit, font='arial 12 bold', activebackground='#c42818', activeforeground='white')
        self.quit_button.grid(row=0, column=3)
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
        
        # Page arrows
        self.bupgradepagearrowframe = Frame(self.buildingupgradeframe, bg=bupgradebg, padx=200)
        self.upgradespreviouspagebutton = Button(self.bupgradepagearrowframe, text='<', font='arial 22 bold', bg=bupgradebg,
                                         padx=10, highlightthickness=0, bd=0, activebackground=bupgradebg, fg='#3d220f', state=DISABLED, command=self.upgradespreviouspage)
        self.upgradesnextpagebutton = Button(self.bupgradepagearrowframe, text='>', font='arial 22 bold', bg=bupgradebg,
                                         padx=10, highlightthickness=0, bd=0, activebackground=bupgradebg, fg='#3d220f', command=self.upgradesnextpage) 
        self.bupgradepagearrowframe.grid_columnconfigure(0, minsize=100, weight=1)
        
        self.upgradepagenumber = 1
        

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
        self.grandmaupgrade7 = GrandmaUpgrades(
            self, 'Xtreme walkers', 50000000000000, 200, 7, 2, 'Grandmas are twice as efficient.')
        self.grandmaupgrade8 = GrandmaUpgrades(
            self, 'The Unbridling', 50000000000000000, 250, 8, 2, 'Grandmas are twice as efficient.')
        self.grandmaupgrade9 = GrandmaUpgrades(
            self, 'Reverse dementia', 50000000000000000000, 300, 9, 2, 'Grandmas are twice as efficient.')
        self.grandmaupgrade10 = GrandmaUpgrades(
            self, 'Timeproof hair dyes', 50000000000000000000000, 350, 10, 2, 'Grandmas are twice as efficient.')
        self.grandmaupgrade11 = GrandmaUpgrades(
            self, 'Good manners', 500000000000000000000000000, 400, 11, 2, 'Grandmas are twice as efficient.')
        self.grandmaupgrade12 = GrandmaUpgrades(
            self, 'Generation degeneration', 5000000000000000000000000000000, 450, 12, 2, 'Grandmas are twice as efficient.')
        self.grandmaupgrade13 = GrandmaUpgrades(
            self, 'Visits', 50000000000000000000000000000000000, 500, 13, 2, 'Grandmas are twice as efficient.')        

        self.grandmaupgradelabel = Label(self.buildingupgradeframe, text='Forwards from grandma:\n1000 Cookies',
                                         font='arial 14', padx=20, pady=10, bg=bupgradebg, justify=LEFT, wraplength=200)

        self.grandmaupgradetext = Label(self.buildingupgradeframe, text=self.grandmaupgrade1.descriptiontext,
                                        font='arial 10', padx=20, pady=10, bg=bupgradebg, justify=CENTER, wraplength=150)

        self.grandmaupgradebutton = Button(self.buildingupgradeframe, padx=20, pady=10, command=self.grandmaupgrade,
                                           image=self.redbuybutton, highlightthickness=0, bd=0, bg=bupgradebg, activebackground=bupgradebg, cursor="hand2")

        # Farm Upgrade
        self.farmorder = 1
        self.farmupgradeprice = 11000
        
        self.farmupgrade1 = FarmUpgrades(
                self, 'Cheap hoes', 11000, 1, 1, 2, 'Farms are twice as efficient.')
        self.farmupgrade2 = FarmUpgrades(
                self, 'Fertilizer', 55000, 5, 2, 2, 'Farms are twice as efficient.')
        self.farmupgrade3 = FarmUpgrades(
                self, 'Cookie trees', 550000, 25, 3, 2, 'Farms are twice as efficient.')
        self.farmupgrade4 = FarmUpgrades(
                self, 'Genetically-modified cookies', 55000000, 50, 4, 2, 'Farms are twice as efficient.')
        self.farmupgrade5 = FarmUpgrades(
                self, 'Gingerbread scarecrows', 5500000000, 100, 5, 2, 'Farms are twice as efficient.')
        self.farmupgrade6 = FarmUpgrades(
                self, 'Pulsar sprinklers', 550000000000, 150, 6, 2, 'Farms are twice as efficient.')
        self.farmupgrade7 = FarmUpgrades(
                self, 'Fudge fungus', 550000000000000, 200, 7, 2, 'Farms are twice as efficient.')
        self.farmupgrade8 = FarmUpgrades(
                self, 'Wheat triffids', 550000000000000000, 250, 8, 2, 'Farms are twice as efficient.')
        self.farmupgrade9 = FarmUpgrades(
                self, 'Humane pesticides', 550000000000000000000, 300, 9, 2, 'Farms are twice as efficient.')
        self.farmupgrade10 = FarmUpgrades(
                self, 'Barnstars', 550000000000000000000000, 350, 10, 2, 'Farms are twice as efficient.')
        self.farmupgrade11 = FarmUpgrades(
                self, 'Lindworms', 5500000000000000000000000000, 400, 11, 2, 'Farms are twice as efficient.')
        self.farmupgrade12 = FarmUpgrades(
                self, 'Global seed vault', 55000000000000000000000000000000, 450, 12, 2, 'Farms are twice as efficient.')
        self.farmupgrade13 = FarmUpgrades(
                self, 'Reverse-veganism', 550000000000000000000000000000000000, 500, 13, 2, 'Farms are twice as efficient.')        
        
        self.farmupgradelabel = Label(self.buildingupgradeframe, text='Cheap hoes:\n11000 Cookies',
                                             font='arial 14', padx=20, pady=10, bg=bupgradebg, justify=LEFT, wraplength=200)
        
        self.farmupgradetext = Label(self.buildingupgradeframe, text=self.farmupgrade1.descriptiontext,
                                            font='arial 10', padx=20, pady=10, bg=bupgradebg, justify=CENTER, wraplength=150)
        
        self.farmupgradebutton = Button(self.buildingupgradeframe, padx=20, pady=10, command=self.farmupgrade,
                                               image=self.redbuybutton, highlightthickness=0, bd=0, bg=bupgradebg, activebackground=bupgradebg, cursor="hand2")

        # Mine Upgrade
        self.mineorder = 1
        self.mineupgradeprice = 120000
        
        self.mineupgrade1 = MineUpgrades(
                self, 'Sugar gas', 120000, 1, 1, 2, 'Mines are twice as efficient.')
        self.mineupgrade2 = MineUpgrades(
                self, 'Megadrill', 600000, 5, 2, 2, 'Mines are twice as efficient.')
        self.mineupgrade3 = MineUpgrades(
                self, 'Ultradrill', 6000000, 25, 3, 2, 'Mines are twice as efficient.')
        self.mineupgrade4 = MineUpgrades(
                self, 'Ultimadrill', 600000000, 50, 4, 2, 'Mines are twice as efficient.')
        self.mineupgrade5 = MineUpgrades(
                self, 'H-bomb mining', 60000000000, 100, 5, 2, 'Mines are twice as efficient.')
        self.mineupgrade6 = MineUpgrades(
                self, 'Coreforge', 6000000000000, 150, 6, 2, 'Mines are twice as efficient.')
        self.mineupgrade7 = MineUpgrades(
                self, 'Planetsplitters', 6000000000000000, 200, 7, 2, 'Mines are twice as efficient.')
        self.mineupgrade8 = MineUpgrades(
                self, 'Canola oil wells', 6000000000000000000, 250, 8, 2, 'Mines are twice as efficient.')
        self.mineupgrade9 = MineUpgrades(
                self, 'Mole people', 6000000000000000000000, 300, 9, 2, 'Mines are twice as efficient.')
        self.mineupgrade10 = MineUpgrades(
                self, 'Mine canaries', 6000000000000000000000000, 350, 10, 2, 'Mines are twice as efficient.')
        self.mineupgrade11 = MineUpgrades(
                self, 'Bore again', 60000000000000000000000000000, 400, 11, 2, 'Mines are twice as efficient.')
        self.mineupgrade12 = MineUpgrades(
                self, 'Air mining', 600000000000000000000000000000000, 450, 12, 2, 'Mines are twice as efficient.')
        self.mineupgrade13 = MineUpgrades(
                self, 'Caramel alloys', 6000000000000000000000000000000000000, 500, 13, 2, 'Mines are twice as efficient.')        
        
        self.mineupgradelabel = Label(self.buildingupgradeframe, text='Sugar gas:\n120000 Cookies',
                                             font='arial 14', padx=20, pady=10, bg=bupgradebg, justify=LEFT, wraplength=200)
        
        self.mineupgradetext = Label(self.buildingupgradeframe, text=self.mineupgrade1.descriptiontext,
                                            font='arial 10', padx=20, pady=10, bg=bupgradebg, justify=CENTER, wraplength=150)
        
        self.mineupgradebutton = Button(self.buildingupgradeframe, padx=20, pady=10, command=self.mineupgrade,
                                               image=self.redbuybutton, highlightthickness=0, bd=0, bg=bupgradebg, activebackground=bupgradebg, cursor="hand2")

        # Factory Upgrade
        self.factoryorder = 1
        self.factoryupgradeprice = 1300000
        
        self.factoryupgrade1 = FactoryUpgrades(
                self, 'Sturdier conveyor belts', 1300000, 1, 1, 2, 'Factories are twice as efficient.')
        self.factoryupgrade2 = FactoryUpgrades(
                self, 'Child labor', 6500000, 5, 2, 2, 'Factories are twice as efficient.')
        self.factoryupgrade3 = FactoryUpgrades(
                self, 'Sweatshop', 65000000, 25, 3, 2, 'Factories are twice as efficient.')
        self.factoryupgrade4 = FactoryUpgrades(
                self, 'Radium reactors', 6500000000, 50, 4, 2, 'Factories are twice as efficient.')
        self.factoryupgrade5 = FactoryUpgrades(
                self, 'Recombobulators', 650000000000, 100, 5, 2, 'Factories are twice as efficient.')
        self.factoryupgrade6 = FactoryUpgrades(
                self, 'Deep-bake process', 65000000000000, 150, 6, 2, 'Factories are twice as efficient.')
        self.factoryupgrade7 = FactoryUpgrades(
                self, 'Cyborg workforce', 65000000000000000, 200, 7, 2, 'Factories are twice as efficient.')
        self.factoryupgrade8 = FactoryUpgrades(
                self, '78-hour days', 65000000000000000000, 250, 8, 2, 'Factories are twice as efficient.')
        self.factoryupgrade9 = FactoryUpgrades(
                self, 'Machine learning', 65000000000000000000000, 300, 9, 2, 'Factories are twice as efficient.')
        self.factoryupgrade10 = FactoryUpgrades(
                self, 'Brownie point system', 65000000000000000000000000, 350, 10, 2, 'Factories are twice as efficient.')
        self.factoryupgrade11 = FactoryUpgrades(
                self, '"Volunteer" interns', 650000000000000000000000000000, 400, 11, 2, 'Factories are twice as efficient.')
        self.factoryupgrade12 = FactoryUpgrades(
                self, 'Behavioral reframing', 6500000000000000000000000000000000, 450, 12, 2, 'Factories are twice as efficient.')
        self.factoryupgrade13 = FactoryUpgrades(
                self, 'The infinity engine', 6000000000000000000000000000000000000, 500, 13, 2, 'Factories are twice as efficient.')        
        
        self.factoryupgradelabel = Label(self.buildingupgradeframe, text='Sturdier conveyor belts:\n1.30000 million Cookies',
                                             font='arial 14', padx=20, pady=10, bg=bupgradebg, justify=LEFT, wraplength=200)
        
        self.factoryupgradetext = Label(self.buildingupgradeframe, text=self.factoryupgrade1.descriptiontext,
                                            font='arial 10', padx=20, pady=10, bg=bupgradebg, justify=CENTER, wraplength=150)
        
        self.factoryupgradebutton = Button(self.buildingupgradeframe, padx=20, pady=10, command=self.factoryupgrade,
                                               image=self.redbuybutton, highlightthickness=0, bd=0, bg=bupgradebg, activebackground=bupgradebg, cursor="hand2")
        
        # Bank Upgrade
        self.bankorder = 1
        self.bankupgradeprice = 14000000
        
        self.bankupgrade1 = BankUpgrades(
                self, 'Taller tellers', 14000000, 1, 1, 2, 'Banks are twice as efficient.')
        self.bankupgrade2 = BankUpgrades(
                self, 'Scissor-resistant credit cards', 70000000, 5, 2, 2, 'Banks are twice as efficient.')
        self.bankupgrade3 = BankUpgrades(
                self, 'Acid-proof vaults', 700000000, 25, 3, 2, 'Banks are twice as efficient.')
        self.bankupgrade4 = BankUpgrades(
                self, 'Chocolate coins', 70000000000, 50, 4, 2, 'Banks are twice as efficient.')
        self.bankupgrade5 = BankUpgrades(
                self, 'Exponential interest rates', 7000000000000, 100, 5, 2, 'Banks are twice as efficient.')
        self.bankupgrade6 = BankUpgrades(
                self, 'Financial zen', 700000000000000, 150, 6, 2, 'Banks are twice as efficient.')
        self.bankupgrade7 = BankUpgrades(
                self, 'Way of the wallet', 700000000000000000, 200, 7, 2, 'Banks are twice as efficient.')
        self.bankupgrade8 = BankUpgrades(
                self, 'The stuff rationale', 700000000000000000000, 250, 8, 2, 'Banks are twice as efficient.')
        self.bankupgrade9 = BankUpgrades(
                self, 'Edible money', 700000000000000000000000, 300, 9, 2, 'Banks are twice as efficient.')
        self.bankupgrade10 = BankUpgrades(
                self, 'Grand supercycle', 700000000000000000000000000, 350, 10, 2, 'Banks are twice as efficient.')
        self.bankupgrade11 = BankUpgrades(
                self, 'Rules of acquisition', 7000000000000000000000000000000, 400, 11, 2, 'Banks are twice as efficient.')
        self.bankupgrade12 = BankUpgrades(
                self, 'Altruistic loop', 70000000000000000000000000000000000, 450, 12, 2, 'Banks are twice as efficient.')
        self.bankupgrade13 = BankUpgrades(
                self, 'Diminishing tax returns', 700000000000000000000000000000000000000, 500, 13, 2, 'Banks are twice as efficient.')        
        
        self.bankupgradelabel = Label(self.buildingupgradeframe, text='Taller tellers:\n14.0000 million Cookies',
                                             font='arial 14', padx=20, pady=10, bg=bupgradebg, justify=LEFT, wraplength=200)
        
        self.bankupgradetext = Label(self.buildingupgradeframe, text=self.bankupgrade1.descriptiontext,
                                            font='arial 10', padx=20, pady=10, bg=bupgradebg, justify=CENTER, wraplength=150)
        
        self.bankupgradebutton = Button(self.buildingupgradeframe, padx=20, pady=10, command=self.bankupgrade,
                                               image=self.redbuybutton, highlightthickness=0, bd=0, bg=bupgradebg, activebackground=bupgradebg, cursor="hand2")        
        
        # Temple Upgrade
        self.templeorder = 1
        self.templeupgradeprice = 200000000
        
        self.templeupgrade1 = TempleUpgrades(
                self, 'Golden idols', 200000000, 1, 1, 2, 'Temples are twice as efficient.')
        self.templeupgrade2 = TempleUpgrades(
                self, 'Sacrifices', 1000000000, 5, 2, 2, 'Temples are twice as efficient.')
        self.templeupgrade3 = TempleUpgrades(
                self, 'Delicious blessing', 10000000000, 25, 3, 2, 'Temples are twice as efficient.')
        self.templeupgrade4 = TempleUpgrades(
                self, 'Sun festival', 1000000000000, 50, 4, 2, 'Temples are twice as efficient.')
        self.templeupgrade5 = TempleUpgrades(
                self, 'Enlarged pantheon', 100000000000000, 100, 5, 2, 'Temples are twice as efficient.')
        self.templeupgrade6 = TempleUpgrades(
                self, 'Great Baker in the sky', 10000000000000000, 150, 6, 2, 'Temples are twice as efficient.')
        self.templeupgrade7 = TempleUpgrades(
                self, 'Creation myth', 10000000000000000000, 200, 7, 2, 'Temples are twice as efficient.')
        self.templeupgrade8 = TempleUpgrades(
                self, 'Theocracy', 10000000000000000000000, 250, 8, 2, 'Temples are twice as efficient.')
        self.templeupgrade9 = TempleUpgrades(
                self, 'Sick rap prayers', 10000000000000000000000000, 300, 9, 2, 'Temples are twice as efficient.')
        self.templeupgrade10 = TempleUpgrades(
                self, 'Psalm-reading', 10000000000000000000000000000, 350, 10, 2, 'Temples are twice as efficient.')
        self.templeupgrade11 = TempleUpgrades(
                self, 'War of the gods', 100000000000000000000000000000000, 400, 11, 2, 'Temples are twice as efficient.')
        self.templeupgrade12 = TempleUpgrades(
                self, 'A novel idea', 1000000000000000000000000000000000000, 450, 12, 2, 'Temples are twice as efficient.')
        self.templeupgrade13 = TempleUpgrades(
                self, 'Apparitions', 10000000000000000000000000000000000000000, 500, 13, 2, 'Temples are twice as efficient.')        
        
        self.templeupgradelabel = Label(self.buildingupgradeframe, text='Golden idols:\n200.000 million Cookies',
                                             font='arial 14', padx=20, pady=10, bg=bupgradebg, justify=LEFT, wraplength=200)
        
        self.templeupgradetext = Label(self.buildingupgradeframe, text=self.templeupgrade1.descriptiontext,
                                            font='arial 10', padx=20, pady=10, bg=bupgradebg, justify=CENTER, wraplength=150)
        
        self.templeupgradebutton = Button(self.buildingupgradeframe, padx=20, pady=10, command=self.templeupgrade,
                                               image=self.redbuybutton, highlightthickness=0, bd=0, bg=bupgradebg, activebackground=bupgradebg, cursor="hand2")
        
        # Wizard Tower Upgrade
        self.wizardtowerorder = 1
        self.wizardtowerupgradeprice = 3300000000
        
        self.wizardtowerupgrade1 = WizardTowerUpgrades(
                self, 'Pointier hats', 3300000000, 1, 1, 2, 'Wizard Towers are twice as efficient.')
        self.wizardtowerupgrade2 = WizardTowerUpgrades(
                self, 'Beardlier beards', 16500000000, 5, 2, 2, 'Wizard Towers are twice as efficient.')
        self.wizardtowerupgrade3 = WizardTowerUpgrades(
                self, 'Ancient grimoires', 165000000000, 25, 3, 2, 'Wizard Towers are twice as efficient.')
        self.wizardtowerupgrade4 = WizardTowerUpgrades(
                self, 'Kitchen curses', 16500000000000, 50, 4, 2, 'Wizard Towers are twice as efficient.')
        self.wizardtowerupgrade5 = WizardTowerUpgrades(
                self, 'School of sorcery', 1650000000000000, 100, 5, 2, 'Wizard Towers are twice as efficient.')
        self.wizardtowerupgrade6 = WizardTowerUpgrades(
                self, 'Dark formulas', 165000000000000000, 150, 6, 2, 'Wizard Towers are twice as efficient.')
        self.wizardtowerupgrade7 = WizardTowerUpgrades(
                self, 'Cookiemancy', 165000000000000000000, 200, 7, 2, 'Wizard Towers are twice as efficient.')
        self.wizardtowerupgrade8 = WizardTowerUpgrades(
                self, 'Rabbit trick', 165000000000000000000000, 250, 8, 2, 'Wizard Towers are twice as efficient.')
        self.wizardtowerupgrade9 = WizardTowerUpgrades(
                self, 'Deluxe tailored wands', 165000000000000000000000000, 300, 9, 2, 'Wizard Towers are twice as efficient.')
        self.wizardtowerupgrade10 = WizardTowerUpgrades(
                self, 'Immobile spellcasting', 165000000000000000000000000000, 350, 10, 2, 'Wizard Towers are twice as efficient.')
        self.wizardtowerupgrade11 = WizardTowerUpgrades(
                self, 'Electricity', 1650000000000000000000000000000000, 400, 11, 2, 'Wizard Towers are twice as efficient.')
        self.wizardtowerupgrade12 = WizardTowerUpgrades(
                self, 'Spelling bees', 16500000000000000000000000000000000000, 450, 12, 2, 'Wizard Towers are twice as efficient.')
        self.wizardtowerupgrade13 = WizardTowerUpgrades(
                self, 'Wizard basements', 165000000000000000000000000000000000000000, 500, 13, 2, 'Wizard Towers are twice as efficient.')        
        
        self.wizardtowerupgradelabel = Label(self.buildingupgradeframe, text='Pointier hats:\n3.30000 billion Cookies',
                                             font='arial 14', padx=20, pady=10, bg=bupgradebg, justify=LEFT, wraplength=200)
        
        self.wizardtowerupgradetext = Label(self.buildingupgradeframe, text=self.wizardtowerupgrade1.descriptiontext,
                                            font='arial 10', padx=20, pady=10, bg=bupgradebg, justify=CENTER, wraplength=150)
        
        self.wizardtowerupgradebutton = Button(self.buildingupgradeframe, padx=20, pady=10, command=self.wizardtowerupgrade,
                                               image=self.redbuybutton, highlightthickness=0, bd=0, bg=bupgradebg, activebackground=bupgradebg, cursor="hand2")
        
        # Shipment Upgrade
        self.shipmentorder = 1
        self.shipmentupgradeprice = 51000000000
        
        self.shipmentupgrade1 = ShipmentUpgrades(
                self, 'Vanilla nebulae', 51000000000, 1, 1, 2, 'Shipments are twice as efficient.')
        self.shipmentupgrade2 = ShipmentUpgrades(
                self, 'Wormholes', 255000000000, 5, 2, 2, 'Shipments are twice as efficient.')
        self.shipmentupgrade3 = ShipmentUpgrades(
                self, 'Frequent flyer', 2550000000000, 25, 3, 2, 'Shipments are twice as efficient.')
        self.shipmentupgrade4 = ShipmentUpgrades(
                self, 'Warp drive', 255000000000000, 50, 4, 2, 'Shipments are twice as efficient.')
        self.shipmentupgrade5 = ShipmentUpgrades(
                self, 'Chocolate monoliths', 25500000000000000, 100, 5, 2, 'Shipments are twice as efficient.')
        self.shipmentupgrade6 = ShipmentUpgrades(
                self, 'Generation ship', 2550000000000000000, 150, 6, 2, 'Shipments are twice as efficient.')
        self.shipmentupgrade7 = ShipmentUpgrades(
                self, 'Dyson sphere', 2550000000000000000000, 200, 7, 2, 'Shipments are twice as efficient.')
        self.shipmentupgrade8 = ShipmentUpgrades(
                self, 'The final frontier', 2550000000000000000000000, 250, 8, 2, 'Shipments are twice as efficient.')
        self.shipmentupgrade9 = ShipmentUpgrades(
                self, 'Autopilot', 2550000000000000000000000000, 300, 9, 2, 'Shipments are twice as efficient.')
        self.shipmentupgrade10 = ShipmentUpgrades(
                self, 'Restaurants at the end of the universe', 2550000000000000000000000000000, 350, 10, 2, 'Shipments are twice as efficient.')
        self.shipmentupgrade11 = ShipmentUpgrades(
                self, 'Universal alphabet', 25500000000000000000000000000000000, 400, 11, 2, 'Shipments are twice as efficient.')
        self.shipmentupgrade12 = ShipmentUpgrades(
                self, 'Toroid universe', 255000000000000000000000000000000000000, 450, 12, 2, 'Shipments are twice as efficient.')
        self.shipmentupgrade13 = ShipmentUpgrades(
                self, 'Prime directive', 2550000000000000000000000000000000000000000, 500, 13, 2, 'Shipments are twice as efficient.')        
        
        self.shipmentupgradelabel = Label(self.buildingupgradeframe, text='Vanilla nebulae:\n51.0000 billion Cookies',
                                             font='arial 14', padx=20, pady=10, bg=bupgradebg, justify=LEFT, wraplength=200)
        
        self.shipmentupgradetext = Label(self.buildingupgradeframe, text=self.shipmentupgrade1.descriptiontext,
                                            font='arial 10', padx=20, pady=10, bg=bupgradebg, justify=CENTER, wraplength=150)
        
        self.shipmentupgradebutton = Button(self.buildingupgradeframe, padx=20, pady=10, command=self.shipmentupgrade,
                                               image=self.redbuybutton, highlightthickness=0, bd=0, bg=bupgradebg, activebackground=bupgradebg, cursor="hand2")
        
        # AlchemyLab Upgrade
        self.alchemylaborder = 1
        self.alchemylabupgradeprice = 750000000000
        
        self.alchemylabupgrade1 = AlchemyLabUpgrades(
                self, 'Antimony', 750000000000, 1, 1, 2, 'Alchemy Labs are twice as efficient.')
        self.alchemylabupgrade2 = AlchemyLabUpgrades(
                self, 'Essence of dough', 3750000000000, 5, 2, 2, 'Alchemy Labs are twice as efficient.')
        self.alchemylabupgrade3 = AlchemyLabUpgrades(
                self, 'True chocolate', 37500000000000, 25, 3, 2, 'Alchemy Labs are twice as efficient.')
        self.alchemylabupgrade4 = AlchemyLabUpgrades(
                self, 'Ambrosia', 3750000000000000, 50, 4, 2, 'Alchemy Labs are twice as efficient.')
        self.alchemylabupgrade5 = AlchemyLabUpgrades(
                self, 'Aqua crustulae', 375000000000000000, 100, 5, 2, 'Alchemy Labs are twice as efficient.')
        self.alchemylabupgrade6 = AlchemyLabUpgrades(
                self, 'Origin crucible', 37500000000000000000, 150, 6, 2, 'Alchemy Labs are twice as efficient.')
        self.alchemylabupgrade7 = AlchemyLabUpgrades(
                self, 'Theory of atomic fluidity', 37500000000000000000000, 200, 7, 2, 'Alchemy Labs are twice as efficient.')
        self.alchemylabupgrade8 = AlchemyLabUpgrades(
                self, 'Beige goo', 37500000000000000000000000, 250, 8, 2, 'Alchemy Labs are twice as efficient.')
        self.alchemylabupgrade9 = AlchemyLabUpgrades(
                self, 'The advent of chemistry', 37500000000000000000000000000, 300, 9, 2, 'Alchemy Labs are twice as efficient.')
        self.alchemylabupgrade10 = AlchemyLabUpgrades(
                self, 'On second thought', 37500000000000000000000000000000, 350, 10, 2, 'Alchemy Labs are twice as efficient.')
        self.alchemylabupgrade11 = AlchemyLabUpgrades(
                self, 'Public betterment', 375000000000000000000000000000000000, 400, 11, 2, 'Alchemy Labs are twice as efficient.')
        self.alchemylabupgrade12 = AlchemyLabUpgrades(
                self, 'Hermetic reconciliation', 3750000000000000000000000000000000000000, 450, 12, 2, 'Alchemy Labs are twice as efficient.')
        self.alchemylabupgrade13 = AlchemyLabUpgrades(
                self, 'Chromatic cycling', 37500000000000000000000000000000000000000000, 500, 13, 2, 'Alchemy Labs are twice as efficient.')        
        
        self.alchemylabupgradelabel = Label(self.buildingupgradeframe, text='Antimony:\n750.000 billion Cookies',
                                             font='arial 14', padx=20, pady=10, bg=bupgradebg, justify=LEFT, wraplength=200)
        
        self.alchemylabupgradetext = Label(self.buildingupgradeframe, text=self.alchemylabupgrade1.descriptiontext,
                                            font='arial 10', padx=20, pady=10, bg=bupgradebg, justify=CENTER, wraplength=150)
        
        self.alchemylabupgradebutton = Button(self.buildingupgradeframe, padx=20, pady=10, command=self.alchemylabupgrade,
                                               image=self.redbuybutton, highlightthickness=0, bd=0, bg=bupgradebg, activebackground=bupgradebg, cursor="hand2")
        
        # Portal Upgrade
        self.portalorder = 1
        self.portalupgradeprice = 10000000000000
        
        self.portalupgrade1 = PortalUpgrades(
                self, 'Ancient tablet', 10000000000000, 1, 1, 2, 'Portals are twice as efficient.')
        self.portalupgrade2 = PortalUpgrades(
                self, 'Insane oatling workers', 50000000000000, 5, 2, 2, 'Portals are twice as efficient.')
        self.portalupgrade3 = PortalUpgrades(
                self, 'Soul bond', 500000000000000, 25, 3, 2, 'Portals are twice as efficient.')
        self.portalupgrade4 = PortalUpgrades(
                self, 'Sanity dance', 50000000000000000, 50, 4, 2, 'Portals are twice as efficient.')
        self.portalupgrade5 = PortalUpgrades(
                self, 'Brane transplant', 5000000000000000000, 100, 5, 2, 'Portals are twice as efficient.')
        self.portalupgrade6 = PortalUpgrades(
                self, 'Deity-sized portals', 500000000000000000000, 150, 6, 2, 'Portals are twice as efficient.')
        self.portalupgrade7 = PortalUpgrades(
                self, 'End of times back-up plan', 500000000000000000000000, 200, 7, 2, 'Portals are twice as efficient.')
        self.portalupgrade8 = PortalUpgrades(
                self, 'Maddening chants', 500000000000000000000000000, 250, 8, 2, 'Portals are twice as efficient.')
        self.portalupgrade9 = PortalUpgrades(
                self, 'The real world', 500000000000000000000000000000, 300, 9, 2, 'Portals are twice as efficient.')
        self.portalupgrade10 = PortalUpgrades(
                self, 'Dimensional garbage gulper', 500000000000000000000000000000000, 350, 10, 2, 'Portals are twice as efficient.')
        self.portalupgrade11 = PortalUpgrades(
                self, 'Embedded microportals', 5000000000000000000000000000000000000, 400, 11, 2, 'Portals are twice as efficient.')
        self.portalupgrade12 = PortalUpgrades(
                self, 'His advent', 50000000000000000000000000000000000000000, 450, 12, 2, 'Portals are twice as efficient.')
        self.portalupgrade13 = PortalUpgrades(
                self, 'Domestic rifts', 500000000000000000000000000000000000000000000, 500, 13, 2, 'Portals are twice as efficient.')        
        
        self.portalupgradelabel = Label(self.buildingupgradeframe, text='Ancient tablet:\n10.0000 trillion Cookies',
                                             font='arial 14', padx=20, pady=10, bg=bupgradebg, justify=LEFT, wraplength=200)
        
        self.portalupgradetext = Label(self.buildingupgradeframe, text=self.portalupgrade1.descriptiontext,
                                            font='arial 10', padx=20, pady=10, bg=bupgradebg, justify=CENTER, wraplength=150)
        
        self.portalupgradebutton = Button(self.buildingupgradeframe, padx=20, pady=10, command=self.portalupgrade,
                                               image=self.redbuybutton, highlightthickness=0, bd=0, bg=bupgradebg, activebackground=bupgradebg, cursor="hand2")
        
        # TimeMachine Upgrade
        self.timemachineorder = 1
        self.timemachineupgradeprice = 140000000000000
        
        self.timemachineupgrade1 = TimeMachineUpgrades(
                self, 'Flux capacitors', 140000000000000, 1, 1, 2, 'Time Machines are twice as efficient.')
        self.timemachineupgrade2 = TimeMachineUpgrades(
                self, 'Time paradox resolver', 700000000000000, 5, 2, 2, 'Time Machines are twice as efficient.')
        self.timemachineupgrade3 = TimeMachineUpgrades(
                self, 'Quantum conundrum', 7000000000000000, 25, 3, 2, 'Time Machines are twice as efficient.')
        self.timemachineupgrade4 = TimeMachineUpgrades(
                self, 'Causality enforcer', 700000000000000000, 50, 4, 2, 'Time Machines are twice as efficient.')
        self.timemachineupgrade5 = TimeMachineUpgrades(
                self, 'Yestermorrow comparators', 70000000000000000000, 100, 5, 2, 'Time Machines are twice as efficient.')
        self.timemachineupgrade6 = TimeMachineUpgrades(
                self, 'Far future enactment', 7000000000000000000000, 150, 6, 2, 'Time Machines are twice as efficient.')
        self.timemachineupgrade7 = TimeMachineUpgrades(
                self, 'Great loop hypothesis', 7000000000000000000000000, 200, 7, 2, 'Time Machines are twice as efficient.')
        self.timemachineupgrade8 = TimeMachineUpgrades(
                self, 'Cookietopian moments of maybe', 7000000000000000000000000000, 250, 8, 2, 'Time Machines are twice as efficient.')
        self.timemachineupgrade9 = TimeMachineUpgrades(
                self, 'Second seconds', 7000000000000000000000000000000, 300, 9, 2, 'Time Machines are twice as efficient.')
        self.timemachineupgrade10 = TimeMachineUpgrades(
                self, 'Additional clock hands', 7000000000000000000000000000000000, 350, 10, 2, 'Time Machines are twice as efficient.')
        self.timemachineupgrade11 = TimeMachineUpgrades(
                self, 'Nostalgia', 70000000000000000000000000000000000000, 400, 11, 2, 'Time Machines are twice as efficient.')
        self.timemachineupgrade12 = TimeMachineUpgrades(
                self, 'Split seconds', 700000000000000000000000000000000000000000, 450, 12, 2, 'Time Machines are twice as efficient.')
        self.timemachineupgrade13 = TimeMachineUpgrades(
                self, 'Patience abolished', 7000000000000000000000000000000000000000000000, 500, 13, 2, 'Time Machines are twice as efficient.')        
        
        self.timemachineupgradelabel = Label(self.buildingupgradeframe, text='Flux capacitors:\n140.000 trillion Cookies',
                                             font='arial 14', padx=20, pady=10, bg=bupgradebg, justify=LEFT, wraplength=200)
        
        self.timemachineupgradetext = Label(self.buildingupgradeframe, text=self.timemachineupgrade1.descriptiontext,
                                            font='arial 10', padx=20, pady=10, bg=bupgradebg, justify=CENTER, wraplength=150)
        
        self.timemachineupgradebutton = Button(self.buildingupgradeframe, padx=20, pady=10, command=self.timemachineupgrade,
                                               image=self.redbuybutton, highlightthickness=0, bd=0, bg=bupgradebg, activebackground=bupgradebg, cursor="hand2")        

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
            
        if self.cookies >= self.farmupgradeprice:
            self.farmupgradebutton.config(image=self.buybuttonimage)
            self.farmupgradebuyable = True
        else:
            self.farmupgradebutton.config(image=self.redbuybutton)
            self.farmupgradebuyable = False        
            
        if self.cookies >= self.mineupgradeprice:
            self.mineupgradebutton.config(image=self.buybuttonimage)
            self.mineupgradebuyable = True
        else:
            self.mineupgradebutton.config(image=self.redbuybutton)
            self.mineupgradebuyable = False               
            
        if self.cookies >= self.factoryupgradeprice:
            self.factoryupgradebutton.config(image=self.buybuttonimage)
            self.factoryupgradebuyable = True
        else:
            self.factoryupgradebutton.config(image=self.redbuybutton)
            self.factoryupgradebuyable = False    
            
        if self.cookies >= self.bankupgradeprice:
            self.bankupgradebutton.config(image=self.buybuttonimage)
            self.bankupgradebuyable = True
        else:
            self.bankupgradebutton.config(image=self.redbuybutton)
            self.bankupgradebuyable = False           
            
        if self.cookies >= self.templeupgradeprice:
            self.templeupgradebutton.config(image=self.buybuttonimage)
            self.templeupgradebuyable = True
        else:
            self.templeupgradebutton.config(image=self.redbuybutton)
            self.templeupgradebuyable = False           
            
        if self.cookies >= self.wizardtowerupgradeprice:
            self.wizardtowerupgradebutton.config(image=self.buybuttonimage)
            self.wizardtowerupgradebuyable = True
        else:
            self.wizardtowerupgradebutton.config(image=self.redbuybutton)
            self.wizardtowerupgradebuyable = False       
            
        if self.cookies >= self.shipmentupgradeprice:
            self.shipmentupgradebutton.config(image=self.buybuttonimage)
            self.shipmentupgradebuyable = True
        else:
            self.shipmentupgradebutton.config(image=self.redbuybutton)
            self.shipmentupgradebuyable = False           
            
        if self.cookies >= self.alchemylabupgradeprice:
            self.alchemylabupgradebutton.config(image=self.buybuttonimage)
            self.alchemylabupgradebuyable = True
        else:
            self.alchemylabupgradebutton.config(image=self.redbuybutton)
            self.alchemylabupgradebuyable = False           
            
        if self.cookies >= self.portalupgradeprice:
            self.portalupgradebutton.config(image=self.buybuttonimage)
            self.portalupgradebuyable = True
        else:
            self.portalupgradebutton.config(image=self.redbuybutton)
            self.portalupgradebuyable = False           
            
        if self.cookies >= self.timemachineupgradeprice:
            self.timemachineupgradebutton.config(image=self.buybuttonimage)
            self.timemachineupgradebuyable = True
        else:
            self.timemachineupgradebutton.config(image=self.redbuybutton)
            self.timemachineupgradebuyable = False           

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
                self.grandmaupgrade2.updateinfo(self)
                self.grandmaupgrade1.buy(self)
            elif self.grandmaorder == 2:
                self.grandmaupgrade3.updateinfo(self)
                self.grandmaupgrade2.buy(self)
            elif self.grandmaorder == 3:
                self.grandmaupgrade4.updateinfo(self)
                self.grandmaupgrade3.buy(self)
            elif self.grandmaorder == 4:
                self.grandmaupgrade5.updateinfo(self)
                self.grandmaupgrade4.buy(self)
            elif self.grandmaorder == 5:
                self.grandmaupgrade6.updateinfo(self)
                self.grandmaupgrade5.buy(self)
            elif self.grandmaorder == 6:
                self.grandmaupgrade7.updateinfo(self)
                self.grandmaupgrade6.buy(self)
            elif self.grandmaorder == 7:
                self.grandmaupgrade8.updateinfo(self)
                self.grandmaupgrade7.buy(self)
            elif self.grandmaorder == 8:
                self.grandmaupgrade9.updateinfo(self)
                self.grandmaupgrade8.buy(self)
            elif self.grandmaorder == 9:
                self.grandmaupgrade10.updateinfo(self)
                self.grandmaupgrade9.buy(self)
            elif self.grandmaorder == 10:
                self.grandmaupgrade11.updateinfo(self)
                self.grandmaupgrade10.buy(self)
            elif self.grandmaorder == 11:
                self.grandmaupgrade12.updateinfo(self)
                self.grandmaupgrade11.buy(self)
            elif self.grandmaorder == 12:
                self.grandmaupgrade13.updateinfo(self)
                self.grandmaupgrade12.buy(self)
            elif self.grandmaorder == 13:
                self.grandmaupgradeprice = math.inf
                self.grandmaupgradelabel.configure(
                    text='Grandma Upgrades Maxed')
                self.grandmaupgradetext.configure(
                    text='')
                self.grandmaupgrade13.buy(self)

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
    
    def farmupgrade(self):
        if self.farmupgradebuyable == True:
            if self.farmorder == 1:
                self.farmupgrade2.updateinfo(self)
                self.farmupgrade1.buy(self)
            elif self.farmorder == 2:
                self.farmupgrade3.updateinfo(self)
                self.farmupgrade2.buy(self)
            elif self.farmorder == 3:
                self.farmupgrade4.updateinfo(self)
                self.farmupgrade3.buy(self)
            elif self.farmorder == 4:
                self.farmupgrade5.updateinfo(self)
                self.farmupgrade4.buy(self)
            elif self.farmorder == 5:
                self.farmupgrade6.updateinfo(self)
                self.farmupgrade5.buy(self)
            elif self.farmorder == 6:
                self.farmupgrade7.updateinfo(self)
                self.farmupgrade6.buy(self)
            elif self.farmorder == 7:
                self.farmupgrade8.updateinfo(self)
                self.farmupgrade7.buy(self)
            elif self.farmorder == 8:
                self.farmupgrade9.updateinfo(self)
                self.farmupgrade8.buy(self)
            elif self.farmorder == 9:
                self.farmupgrade10.updateinfo(self)
                self.farmupgrade9.buy(self)
            elif self.farmorder == 10:
                self.farmupgrade11.updateinfo(self)
                self.farmupgrade10.buy(self)
            elif self.farmorder == 11:
                self.farmupgrade12.updateinfo(self)
                self.farmupgrade11.buy(self)
            elif self.farmorder == 12:
                self.farmupgrade13.updateinfo(self)
                self.farmupgrade12.buy(self)
            elif self.farmorder == 13:
                self.farmupgradeprice = math.inf
                self.farmupgradelabel.configure(
                    text='Farm Upgrades Maxed')
                self.farmupgradetext.configure(
                    text='')
                self.farmupgrade13.buy(self)    

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
        
    def mineupgrade(self):
        if self.mineupgradebuyable == True:
            if self.mineorder == 1:
                self.mineupgrade2.updateinfo(self)
                self.mineupgrade1.buy(self)
            elif self.mineorder == 2:
                self.mineupgrade3.updateinfo(self)
                self.mineupgrade2.buy(self)
            elif self.mineorder == 3:
                self.mineupgrade4.updateinfo(self)
                self.mineupgrade3.buy(self)
            elif self.mineorder == 4:
                self.mineupgrade5.updateinfo(self)
                self.mineupgrade4.buy(self)
            elif self.mineorder == 5:
                self.mineupgrade6.updateinfo(self)
                self.mineupgrade5.buy(self)
            elif self.mineorder == 6:
                self.mineupgrade7.updateinfo(self)
                self.mineupgrade6.buy(self)
            elif self.mineorder == 7:
                self.mineupgrade8.updateinfo(self)
                self.mineupgrade7.buy(self)
            elif self.mineorder == 8:
                self.mineupgrade9.updateinfo(self)
                self.mineupgrade8.buy(self)
            elif self.mineorder == 9:
                self.mineupgrade10.updateinfo(self)
                self.mineupgrade9.buy(self)
            elif self.mineorder == 10:
                self.mineupgrade11.updateinfo(self)
                self.mineupgrade10.buy(self)
            elif self.mineorder == 11:
                self.mineupgrade12.updateinfo(self)
                self.mineupgrade11.buy(self)
            elif self.mineorder == 12:
                self.mineupgrade13.updateinfo(self)
                self.mineupgrade12.buy(self)
            elif self.mineorder == 13:
                self.mineupgradeprice = math.inf
                self.mineupgradelabel.configure(
                    text='Mine Upgrades Maxed')
                self.mineupgradetext.configure(
                    text='')
                self.mineupgrade13.buy(self)       

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
        
    def factoryupgrade(self):
        if self.factoryupgradebuyable == True:
            if self.factoryorder == 1:
                self.factoryupgrade2.updateinfo(self)
                self.factoryupgrade1.buy(self)
            elif self.factoryorder == 2:
                self.factoryupgrade3.updateinfo(self)
                self.factoryupgrade2.buy(self)
            elif self.factoryorder == 3:
                self.factoryupgrade4.updateinfo(self)
                self.factoryupgrade3.buy(self)
            elif self.factoryorder == 4:
                self.factoryupgrade5.updateinfo(self)
                self.factoryupgrade4.buy(self)
            elif self.factoryorder == 5:
                self.factoryupgrade6.updateinfo(self)
                self.factoryupgrade5.buy(self)
            elif self.factoryorder == 6:
                self.factoryupgrade7.updateinfo(self)
                self.factoryupgrade6.buy(self)
            elif self.factoryorder == 7:
                self.factoryupgrade8.updateinfo(self)
                self.factoryupgrade7.buy(self)
            elif self.factoryorder == 8:
                self.factoryupgrade9.updateinfo(self)
                self.factoryupgrade8.buy(self)
            elif self.factoryorder == 9:
                self.factoryupgrade10.updateinfo(self)
                self.factoryupgrade9.buy(self)
            elif self.factoryorder == 10:
                self.factoryupgrade11.updateinfo(self)
                self.factoryupgrade10.buy(self)
            elif self.factoryorder == 11:
                self.factoryupgrade12.updateinfo(self)
                self.factoryupgrade11.buy(self)
            elif self.factoryorder == 12:
                self.factoryupgrade13.updateinfo(self)
                self.factoryupgrade12.buy(self)
            elif self.factoryorder == 13:
                self.factoryupgradeprice = math.inf
                self.factoryupgradelabel.configure(
                    text='Factory Upgrades Maxed')
                self.factoryupgradetext.configure(
                    text='')
                self.factoryupgrade13.buy(self)       

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
        
    def bankupgrade(self):
        if self.bankupgradebuyable == True:
            if self.bankorder == 1:
                self.bankupgrade2.updateinfo(self)
                self.bankupgrade1.buy(self)
            elif self.bankorder == 2:
                self.bankupgrade3.updateinfo(self)
                self.bankupgrade2.buy(self)
            elif self.bankorder == 3:
                self.bankupgrade4.updateinfo(self)
                self.bankupgrade3.buy(self)
            elif self.bankorder == 4:
                self.bankupgrade5.updateinfo(self)
                self.bankupgrade4.buy(self)
            elif self.bankorder == 5:
                self.bankupgrade6.updateinfo(self)
                self.bankupgrade5.buy(self)
            elif self.bankorder == 6:
                self.bankupgrade7.updateinfo(self)
                self.bankupgrade6.buy(self)
            elif self.bankorder == 7:
                self.bankupgrade8.updateinfo(self)
                self.bankupgrade7.buy(self)
            elif self.bankorder == 8:
                self.bankupgrade9.updateinfo(self)
                self.bankupgrade8.buy(self)
            elif self.bankorder == 9:
                self.bankupgrade10.updateinfo(self)
                self.bankupgrade9.buy(self)
            elif self.bankorder == 10:
                self.bankupgrade11.updateinfo(self)
                self.bankupgrade10.buy(self)
            elif self.bankorder == 11:
                self.bankupgrade12.updateinfo(self)
                self.bankupgrade11.buy(self)
            elif self.bankorder == 12:
                self.bankupgrade13.updateinfo(self)
                self.bankupgrade12.buy(self)
            elif self.bankorder == 13:
                self.bankupgradeprice = math.inf
                self.bankupgradelabel.configure(
                    text='Bank Upgrades Maxed')
                self.bankupgradetext.configure(
                    text='')
                self.bankupgrade13.buy(self)       

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
        
    def templeupgrade(self):
        if self.templeupgradebuyable == True:
            if self.templeorder == 1:
                self.templeupgrade2.updateinfo(self)
                self.templeupgrade1.buy(self)
            elif self.templeorder == 2:
                self.templeupgrade3.updateinfo(self)
                self.templeupgrade2.buy(self)
            elif self.templeorder == 3:
                self.templeupgrade4.updateinfo(self)
                self.templeupgrade3.buy(self)
            elif self.templeorder == 4:
                self.templeupgrade5.updateinfo(self)
                self.templeupgrade4.buy(self)
            elif self.templeorder == 5:
                self.templeupgrade6.updateinfo(self)
                self.templeupgrade5.buy(self)
            elif self.templeorder == 6:
                self.templeupgrade7.updateinfo(self)
                self.templeupgrade6.buy(self)
            elif self.templeorder == 7:
                self.templeupgrade8.updateinfo(self)
                self.templeupgrade7.buy(self)
            elif self.templeorder == 8:
                self.templeupgrade9.updateinfo(self)
                self.templeupgrade8.buy(self)
            elif self.templeorder == 9:
                self.templeupgrade10.updateinfo(self)
                self.templeupgrade9.buy(self)
            elif self.templeorder == 10:
                self.templeupgrade11.updateinfo(self)
                self.templeupgrade10.buy(self)
            elif self.templeorder == 11:
                self.templeupgrade12.updateinfo(self)
                self.templeupgrade11.buy(self)
            elif self.templeorder == 12:
                self.templeupgrade13.updateinfo(self)
                self.templeupgrade12.buy(self)
            elif self.templeorder == 13:
                self.templeupgradeprice = math.inf
                self.templeupgradelabel.configure(
                    text='Temple Upgrades Maxed')
                self.templeupgradetext.configure(
                    text='')
                self.templeupgrade13.buy(self)       

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
        
    def wizardtowerupgrade(self):
        if self.wizardtowerupgradebuyable == True:
            if self.wizardtowerorder == 1:
                self.wizardtowerupgrade2.updateinfo(self)
                self.wizardtowerupgrade1.buy(self)
            elif self.wizardtowerorder == 2:
                self.wizardtowerupgrade3.updateinfo(self)
                self.wizardtowerupgrade2.buy(self)
            elif self.wizardtowerorder == 3:
                self.wizardtowerupgrade4.updateinfo(self)
                self.wizardtowerupgrade3.buy(self)
            elif self.wizardtowerorder == 4:
                self.wizardtowerupgrade5.updateinfo(self)
                self.wizardtowerupgrade4.buy(self)
            elif self.wizardtowerorder == 5:
                self.wizardtowerupgrade6.updateinfo(self)
                self.wizardtowerupgrade5.buy(self)
            elif self.wizardtowerorder == 6:
                self.wizardtowerupgrade7.updateinfo(self)
                self.wizardtowerupgrade6.buy(self)
            elif self.wizardtowerorder == 7:
                self.wizardtowerupgrade8.updateinfo(self)
                self.wizardtowerupgrade7.buy(self)
            elif self.wizardtowerorder == 8:
                self.wizardtowerupgrade9.updateinfo(self)
                self.wizardtowerupgrade8.buy(self)
            elif self.wizardtowerorder == 9:
                self.wizardtowerupgrade10.updateinfo(self)
                self.wizardtowerupgrade9.buy(self)
            elif self.wizardtowerorder == 10:
                self.wizardtowerupgrade11.updateinfo(self)
                self.wizardtowerupgrade10.buy(self)
            elif self.wizardtowerorder == 11:
                self.wizardtowerupgrade12.updateinfo(self)
                self.wizardtowerupgrade11.buy(self)
            elif self.wizardtowerorder == 12:
                self.wizardtowerupgrade13.updateinfo(self)
                self.wizardtowerupgrade12.buy(self)
            elif self.wizardtowerorder == 13:
                self.wizardtowerupgradeprice = math.inf
                self.wizardtowerupgradelabel.configure(
                    text='Wizard Tower Upgrades Maxed')
                self.wizardtowerupgradetext.configure(
                    text='')
                self.wizardtowerupgrade13.buy(self)       

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
        
    def shipmentupgrade(self):
        if self.shipmentupgradebuyable == True:
            if self.shipmentorder == 1:
                self.shipmentupgrade2.updateinfo(self)
                self.shipmentupgrade1.buy(self)
            elif self.shipmentorder == 2:
                self.shipmentupgrade3.updateinfo(self)
                self.shipmentupgrade2.buy(self)
            elif self.shipmentorder == 3:
                self.shipmentupgrade4.updateinfo(self)
                self.shipmentupgrade3.buy(self)
            elif self.shipmentorder == 4:
                self.shipmentupgrade5.updateinfo(self)
                self.shipmentupgrade4.buy(self)
            elif self.shipmentorder == 5:
                self.shipmentupgrade6.updateinfo(self)
                self.shipmentupgrade5.buy(self)
            elif self.shipmentorder == 6:
                self.shipmentupgrade7.updateinfo(self)
                self.shipmentupgrade6.buy(self)
            elif self.shipmentorder == 7:
                self.shipmentupgrade8.updateinfo(self)
                self.shipmentupgrade7.buy(self)
            elif self.shipmentorder == 8:
                self.shipmentupgrade9.updateinfo(self)
                self.shipmentupgrade8.buy(self)
            elif self.shipmentorder == 9:
                self.shipmentupgrade10.updateinfo(self)
                self.shipmentupgrade9.buy(self)
            elif self.shipmentorder == 10:
                self.shipmentupgrade11.updateinfo(self)
                self.shipmentupgrade10.buy(self)
            elif self.shipmentorder == 11:
                self.shipmentupgrade12.updateinfo(self)
                self.shipmentupgrade11.buy(self)
            elif self.shipmentorder == 12:
                self.shipmentupgrade13.updateinfo(self)
                self.shipmentupgrade12.buy(self)
            elif self.shipmentorder == 13:
                self.shipmentupgradeprice = math.inf
                self.shipmentupgradelabel.configure(
                    text='Shipment Upgrades Maxed')
                self.shipmentupgradetext.configure(
                    text='')
                self.shipmentupgrade13.buy(self)       

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
        
    def alchemylabupgrade(self):
        if self.alchemylabupgradebuyable == True:
            if self.alchemylaborder == 1:
                self.alchemylabupgrade2.updateinfo(self)
                self.alchemylabupgrade1.buy(self)
            elif self.alchemylaborder == 2:
                self.alchemylabupgrade3.updateinfo(self)
                self.alchemylabupgrade2.buy(self)
            elif self.alchemylaborder == 3:
                self.alchemylabupgrade4.updateinfo(self)
                self.alchemylabupgrade3.buy(self)
            elif self.alchemylaborder == 4:
                self.alchemylabupgrade5.updateinfo(self)
                self.alchemylabupgrade4.buy(self)
            elif self.alchemylaborder == 5:
                self.alchemylabupgrade6.updateinfo(self)
                self.alchemylabupgrade5.buy(self)
            elif self.alchemylaborder == 6:
                self.alchemylabupgrade7.updateinfo(self)
                self.alchemylabupgrade6.buy(self)
            elif self.alchemylaborder == 7:
                self.alchemylabupgrade8.updateinfo(self)
                self.alchemylabupgrade7.buy(self)
            elif self.alchemylaborder == 8:
                self.alchemylabupgrade9.updateinfo(self)
                self.alchemylabupgrade8.buy(self)
            elif self.alchemylaborder == 9:
                self.alchemylabupgrade10.updateinfo(self)
                self.alchemylabupgrade9.buy(self)
            elif self.alchemylaborder == 10:
                self.alchemylabupgrade11.updateinfo(self)
                self.alchemylabupgrade10.buy(self)
            elif self.alchemylaborder == 11:
                self.alchemylabupgrade12.updateinfo(self)
                self.alchemylabupgrade11.buy(self)
            elif self.alchemylaborder == 12:
                self.alchemylabupgrade13.updateinfo(self)
                self.alchemylabupgrade12.buy(self)
            elif self.alchemylaborder == 13:
                self.alchemylabupgradeprice = math.inf
                self.alchemylabupgradelabel.configure(
                    text='Alchemy Lab Upgrades Maxed')
                self.alchemylabupgradetext.configure(
                    text='')
                self.alchemylabupgrade13.buy(self)       

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
        
    def portalupgrade(self):
        if self.portalupgradebuyable == True:
            if self.portalorder == 1:
                self.portalupgrade2.updateinfo(self)
                self.portalupgrade1.buy(self)
            elif self.portalorder == 2:
                self.portalupgrade3.updateinfo(self)
                self.portalupgrade2.buy(self)
            elif self.portalorder == 3:
                self.portalupgrade4.updateinfo(self)
                self.portalupgrade3.buy(self)
            elif self.portalorder == 4:
                self.portalupgrade5.updateinfo(self)
                self.portalupgrade4.buy(self)
            elif self.portalorder == 5:
                self.portalupgrade6.updateinfo(self)
                self.portalupgrade5.buy(self)
            elif self.portalorder == 6:
                self.portalupgrade7.updateinfo(self)
                self.portalupgrade6.buy(self)
            elif self.portalorder == 7:
                self.portalupgrade8.updateinfo(self)
                self.portalupgrade7.buy(self)
            elif self.portalorder == 8:
                self.portalupgrade9.updateinfo(self)
                self.portalupgrade8.buy(self)
            elif self.portalorder == 9:
                self.portalupgrade10.updateinfo(self)
                self.portalupgrade9.buy(self)
            elif self.portalorder == 10:
                self.portalupgrade11.updateinfo(self)
                self.portalupgrade10.buy(self)
            elif self.portalorder == 11:
                self.portalupgrade12.updateinfo(self)
                self.portalupgrade11.buy(self)
            elif self.portalorder == 12:
                self.portalupgrade13.updateinfo(self)
                self.portalupgrade12.buy(self)
            elif self.portalorder == 13:
                self.portalupgradeprice = math.inf
                self.portalupgradelabel.configure(
                    text='Portal Upgrades Maxed')
                self.portalupgradetext.configure(
                    text='')
                self.portalupgrade13.buy(self)       

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
        
    def timemachineupgrade(self):
        if self.timemachineupgradebuyable == True:
            if self.timemachineorder == 1:
                self.timemachineupgrade2.updateinfo(self)
                self.timemachineupgrade1.buy(self)
            elif self.timemachineorder == 2:
                self.timemachineupgrade3.updateinfo(self)
                self.timemachineupgrade2.buy(self)
            elif self.timemachineorder == 3:
                self.timemachineupgrade4.updateinfo(self)
                self.timemachineupgrade3.buy(self)
            elif self.timemachineorder == 4:
                self.timemachineupgrade5.updateinfo(self)
                self.timemachineupgrade4.buy(self)
            elif self.timemachineorder == 5:
                self.timemachineupgrade6.updateinfo(self)
                self.timemachineupgrade5.buy(self)
            elif self.timemachineorder == 6:
                self.timemachineupgrade7.updateinfo(self)
                self.timemachineupgrade6.buy(self)
            elif self.timemachineorder == 7:
                self.timemachineupgrade8.updateinfo(self)
                self.timemachineupgrade7.buy(self)
            elif self.timemachineorder == 8:
                self.timemachineupgrade9.updateinfo(self)
                self.timemachineupgrade8.buy(self)
            elif self.timemachineorder == 9:
                self.timemachineupgrade10.updateinfo(self)
                self.timemachineupgrade9.buy(self)
            elif self.timemachineorder == 10:
                self.timemachineupgrade11.updateinfo(self)
                self.timemachineupgrade10.buy(self)
            elif self.timemachineorder == 11:
                self.timemachineupgrade12.updateinfo(self)
                self.timemachineupgrade11.buy(self)
            elif self.timemachineorder == 12:
                self.timemachineupgrade13.updateinfo(self)
                self.timemachineupgrade12.buy(self)
            elif self.timemachineorder == 13:
                self.timemachineupgradeprice = math.inf
                self.timemachineupgradelabel.configure(
                    text='Time Machine Upgrades Maxed')
                self.timemachineupgradetext.configure(
                    text='')
                self.timemachineupgrade13.buy(self)       

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
        self.bupgradepagearrowframe.grid_forget()
        self.upgradespreviouspagebutton.grid_forget()
        self.upgradesnextpagebutton.grid_forget()
        
        if self.upgradepagenumber == 1:
            self.cursorupgradelabel.grid_forget()
            self.cursorupgradetext.grid_forget()
            self.cursorupgradebutton.grid_forget()
            self.grandmaupgradelabel.grid_forget()
            self.grandmaupgradetext.grid_forget()
            self.grandmaupgradebutton.grid_forget()
            self.farmupgradelabel.grid_forget()
            self.farmupgradetext.grid_forget()
            self.farmupgradebutton.grid_forget()
            self.mineupgradelabel.grid_forget()
            self.mineupgradetext.grid_forget()
            self.mineupgradebutton.grid_forget()
            self.factoryupgradelabel.grid_forget()
            self.factoryupgradetext.grid_forget()
            self.factoryupgradebutton.grid_forget()
            self.bankupgradelabel.grid_forget()
            self.bankupgradetext.grid_forget()
            self.bankupgradebutton.grid_forget()
            
        elif self.upgradepagenumber == 2:
            self.templeupgradelabel.grid_forget()
            self.templeupgradetext.grid_forget()
            self.templeupgradebutton.grid_forget()
            self.wizardtowerupgradelabel.grid_forget()
            self.wizardtowerupgradetext.grid_forget()
            self.wizardtowerupgradebutton.grid_forget()
            self.shipmentupgradelabel.grid_forget()
            self.shipmentupgradetext.grid_forget()
            self.shipmentupgradebutton.grid_forget()
            self.alchemylabupgradelabel.grid_forget()
            self.alchemylabupgradetext.grid_forget()
            self.alchemylabupgradebutton.grid_forget()
            self.portalupgradelabel.grid_forget()
            self.portalupgradetext.grid_forget()
            self.portalupgradebutton.grid_forget()
            self.timemachineupgradelabel.grid_forget()
            self.timemachineupgradetext.grid_forget()
            self.timemachineupgradebutton.grid_forget()                
        
        self.bupgradeexpandbutton.configure(
            command=self.expandupgrade, text='+')

    def expandupgrade(self):
        self.bupgradeexpandbutton.configure(
            command=self.collapseupgrade, text='-')
        self.bupgradelabel.grid_forget()
        self.bupgradelabel.grid(row=0, columnspan=3,
                                pady=10, padx=10, sticky=N)

        self.bupgradepagearrowframe.grid(row=1, columnspan=3)
        self.upgradespreviouspagebutton.grid(row=0, column=0, sticky=W)
        self.upgradesnextpagebutton.grid(row=0, column=1, sticky=E)
        
        if self.upgradepagenumber == 1:
            self.cursorupgradelabel.grid(row=2, column=0, sticky=W)
            self.cursorupgradetext.grid(row=2, column=1)
            self.cursorupgradebutton.grid(
                row=2, column=2, sticky=E, padx=20, pady=10)
            self.grandmaupgradelabel.grid(row=3, column=0, sticky=W)
            self.grandmaupgradetext.grid(row=3, column=1)
            self.grandmaupgradebutton.grid(
                row=3, column=2, sticky=E, padx=20, pady=10)
            self.farmupgradelabel.grid(row=4, column=0, sticky=W)
            self.farmupgradetext.grid(row=4, column=1)
            self.farmupgradebutton.grid(
                row=4, column=2, sticky=E, padx=20, pady=10)
            self.mineupgradelabel.grid(row=5, column=0, sticky=W)
            self.mineupgradetext.grid(row=5, column=1)
            self.mineupgradebutton.grid(
                row=5, column=2, sticky=E, padx=20, pady=10)
            self.factoryupgradelabel.grid(row=6, column=0, sticky=W)
            self.factoryupgradetext.grid(row=6, column=1)
            self.factoryupgradebutton.grid(
                row=6, column=2, sticky=E, padx=20, pady=10)
            self.bankupgradelabel.grid(row=7, column=0, sticky=W)
            self.bankupgradetext.grid(row=7, column=1)
            self.bankupgradebutton.grid(
                row=7, column=2, sticky=E, padx=20, pady=10)        
            
        elif self.upgradepagenumber == 2:
            self.templeupgradelabel.grid(row=2, column=0, sticky=W)
            self.templeupgradetext.grid(row=2, column=1)
            self.templeupgradebutton.grid(
                row=2, column=2, sticky=E, padx=20, pady=10)
            self.wizardtowerupgradelabel.grid(row=3, column=0, sticky=W)
            self.wizardtowerupgradetext.grid(row=3, column=1)
            self.wizardtowerupgradebutton.grid(
                row=3, column=2, sticky=E, padx=20, pady=10)
            self.shipmentupgradelabel.grid(row=4, column=0, sticky=W)
            self.shipmentupgradetext.grid(row=4, column=1)
            self.shipmentupgradebutton.grid(
                row=4, column=2, sticky=E, padx=20, pady=10)
            self.alchemylabupgradelabel.grid(row=5, column=0, sticky=W)
            self.alchemylabupgradetext.grid(row=5, column=1)
            self.alchemylabupgradebutton.grid(
                row=5, column=2, sticky=E, padx=20, pady=10)
            self.portalupgradelabel.grid(row=6, column=0, sticky=W)
            self.portalupgradetext.grid(row=6, column=1)
            self.portalupgradebutton.grid(
                row=6, column=2, sticky=E, padx=20, pady=10)
            self.timemachineupgradelabel.grid(row=7, column=0, sticky=W)
            self.timemachineupgradetext.grid(row=7, column=1)
            self.timemachineupgradebutton.grid(
                row=7, column=2, sticky=E, padx=20, pady=10)                    

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
            
    def upgradespreviouspage(self):
        if self.upgradepagenumber == 2:
            self.templeupgradelabel.grid_forget()
            self.templeupgradetext.grid_forget()
            self.templeupgradebutton.grid_forget()
            self.wizardtowerupgradelabel.grid_forget()
            self.wizardtowerupgradetext.grid_forget()
            self.wizardtowerupgradebutton.grid_forget()
            self.shipmentupgradelabel.grid_forget()
            self.shipmentupgradetext.grid_forget()
            self.shipmentupgradebutton.grid_forget()
            self.alchemylabupgradelabel.grid_forget()
            self.alchemylabupgradetext.grid_forget()
            self.alchemylabupgradebutton.grid_forget()
            self.portalupgradelabel.grid_forget()
            self.portalupgradetext.grid_forget()
            self.portalupgradebutton.grid_forget()
            self.timemachineupgradelabel.grid_forget()
            self.timemachineupgradetext.grid_forget()
            self.timemachineupgradebutton.grid_forget()            
            
            self.cursorupgradelabel.grid(row=2, column=0, sticky=W)
            self.cursorupgradetext.grid(row=2, column=1)
            self.cursorupgradebutton.grid(
                row=2, column=2, sticky=E, padx=20, pady=10)
            self.grandmaupgradelabel.grid(row=3, column=0, sticky=W)
            self.grandmaupgradetext.grid(row=3, column=1)
            self.grandmaupgradebutton.grid(
                row=3, column=2, sticky=E, padx=20, pady=10)
            self.farmupgradelabel.grid(row=4, column=0, sticky=W)
            self.farmupgradetext.grid(row=4, column=1)
            self.farmupgradebutton.grid(
                row=4, column=2, sticky=E, padx=20, pady=10)
            self.mineupgradelabel.grid(row=5, column=0, sticky=W)
            self.mineupgradetext.grid(row=5, column=1)
            self.mineupgradebutton.grid(
                row=5, column=2, sticky=E, padx=20, pady=10)
            self.factoryupgradelabel.grid(row=6, column=0, sticky=W)
            self.factoryupgradetext.grid(row=6, column=1)
            self.factoryupgradebutton.grid(
                row=6, column=2, sticky=E, padx=20, pady=10)
            self.bankupgradelabel.grid(row=7, column=0, sticky=W)
            self.bankupgradetext.grid(row=7, column=1)
            self.bankupgradebutton.grid(
                row=7, column=2, sticky=E, padx=20, pady=10)                    

            self.upgradespreviouspagebutton.configure(state=DISABLED)
            self.upgradesnextpagebutton.configure(state=NORMAL)
            self.upgradepagenumber = 1
        else:
            self.previouspagebutton.configure(state=DISABLED)

    def upgradesnextpage(self):
        if self.upgradepagenumber == 1:
            self.cursorupgradelabel.grid_forget()
            self.cursorupgradetext.grid_forget()
            self.cursorupgradebutton.grid_forget()
            self.grandmaupgradelabel.grid_forget()
            self.grandmaupgradetext.grid_forget()
            self.grandmaupgradebutton.grid_forget()
            self.farmupgradelabel.grid_forget()
            self.farmupgradetext.grid_forget()
            self.farmupgradebutton.grid_forget()
            self.mineupgradelabel.grid_forget()
            self.mineupgradetext.grid_forget()
            self.mineupgradebutton.grid_forget()
            self.factoryupgradelabel.grid_forget()
            self.factoryupgradetext.grid_forget()
            self.factoryupgradebutton.grid_forget()
            self.bankupgradelabel.grid_forget()
            self.bankupgradetext.grid_forget()
            self.bankupgradebutton.grid_forget()            
            
            self.templeupgradelabel.grid(row=2, column=0, sticky=W)
            self.templeupgradetext.grid(row=2, column=1)
            self.templeupgradebutton.grid(
                row=2, column=2, sticky=E, padx=20, pady=10)
            self.wizardtowerupgradelabel.grid(row=3, column=0, sticky=W)
            self.wizardtowerupgradetext.grid(row=3, column=1)
            self.wizardtowerupgradebutton.grid(
                row=3, column=2, sticky=E, padx=20, pady=10)
            self.shipmentupgradelabel.grid(row=4, column=0, sticky=W)
            self.shipmentupgradetext.grid(row=4, column=1)
            self.shipmentupgradebutton.grid(
                row=4, column=2, sticky=E, padx=20, pady=10)
            self.alchemylabupgradelabel.grid(row=5, column=0, sticky=W)
            self.alchemylabupgradetext.grid(row=5, column=1)
            self.alchemylabupgradebutton.grid(
                row=5, column=2, sticky=E, padx=20, pady=10)
            self.portalupgradelabel.grid(row=6, column=0, sticky=W)
            self.portalupgradetext.grid(row=6, column=1)
            self.portalupgradebutton.grid(
                row=6, column=2, sticky=E, padx=20, pady=10)
            self.timemachineupgradelabel.grid(row=7, column=0, sticky=W)
            self.timemachineupgradetext.grid(row=7, column=1)
            self.timemachineupgradebutton.grid(
                row=7, column=2, sticky=E, padx=20, pady=10)              

            self.upgradesnextpagebutton.configure(state=DISABLED)
            self.upgradespreviouspagebutton.configure(state=NORMAL)
            self.upgradepagenumber = 2
        else:
            self.upgradesnextpagebutton.configure(state=DISABLED)    

    def hoverhelp(self, parent):
        parent.widget['background'] = '#21c716'

    def unhoverhelp(self, parent):
        parent.widget['background'] = '#188f10'
        
    def hoversave(self, parent):
        parent.widget['background'] = '#123794'
    
    def unhoversave(self, parent):
        parent.widget['background'] = '#051a4d'
        
    def hoverload(self, parent):
        parent.widget['background'] = '#123794'
    
    def unhoverload(self, parent):
        parent.widget['background'] = '#051a4d'    

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
        
    def save(self):
        variables = [self.cookies, self.perclick, self.cursors, self.grandmas, self.farms, self.mines, self.factories, self.banks, self.temples, self.wizardtowers, self.shipments, self.alchemylabs, self.portals, self.timemachines, self.cursororder, self.grandmaorder, self.farmorder, self.mineorder, self.factoryorder, self.bankorder, self.templeorder, self.wizardtowerorder, self.shipmentorder, self.alchemylaborder, self.portalorder, self.timemachineorder, self.firstgoldencookie, self.thousandfingersbought, self.basecursor_price, self.basegrandma_price, self.basefarm_price, self.basemine_price, self.basefactory_price, self.basebank_price, self.basetemple_price, self.basewizardtower_price, self.baseshipment_price, self.basealchemylab_price, self.baseportal_price, self.basetimemachine_price, self.cursorupgradeprice, self.grandmaupgradeprice, self.farmupgradeprice, self.mineupgradeprice, self.factoryupgradeprice, self.bankupgradeprice, self.templeupgradeprice, self.wizardtowerupgradeprice, self.shipmentupgradeprice, self.alchemylabupgradeprice, self.portalupgradeprice, self.timemachineupgradeprice, self.upgradeinfolist]
        files = [('Cookie Clicker Save File', '*.save')]
        try:
            file = asksaveasfile(filetypes = files, defaultextension = files, title='Save Cookie Clicker Game')
            path = os.path.realpath(file.name)
            file.close()
            
            with open(path, 'wb') as f:
                pickle.dump(variables, f)
    
            opensave = Save(self)
            
        except AttributeError:
            pass
          
    def load(self):
        files = [('Cookie Clicker Save File', '*.save')]
        
        try:
            path = askopenfilename(filetypes = files, defaultextension = files, title = 'Load Cookie Clicker Game')
            
            with open(path, 'rb') as f:
                variables = pickle.load(f)
                
            self.cookies=variables[0]
            self.perclick=variables[1]
            self.cursors=variables[2]
            self.grandmas=variables[3]
            self.farms=variables[4]
            self.mines=variables[5]
            self.factories=variables[6]
            self.banks=variables[7]
            self.temples=variables[8]
            self.wizardtowers=variables[9]
            self.shipments=variables[10]
            self.alchemylabs=variables[11]
            self.portals=variables[12]
            self.timemachines=variables[13]
            self.cursororder=variables[14]
            self.grandmaorder=variables[15]
            self.farmorder=variables[16]
            self.mineorder=variables[17]
            self.factoryorder=variables[18]
            self.bankorder=variables[19]
            self.templeorder=variables[20]
            self.wizardtowerorder=variables[21]
            self.shipmentorder=variables[22]
            self.alchemylaborder=variables[23]
            self.portalorder=variables[24]
            self.timemachineorder=variables[25]
            self.firstgoldencookie=variables[26]
            self.thousandfingersbought=variables[27]
            self.basecursor_price=variables[28]
            self.basegrandma_price=variables[29]
            self.basefarm_price=variables[30]
            self.basemine_price=variables[31]
            self.basefactory_price=variables[32]
            self.basebank_price=variables[33]
            self.basetemple_price=variables[34]
            self.basewizardtower_price=variables[35]
            self.baseshipment_price=variables[36]
            self.basealchemylab_price=variables[37]
            self.baseportal_price=variables[38]
            self.basetimemachine_price=variables[39]
            self.cursorupgradeprice=variables[40]
            self.grandmaupgradeprice=variables[41]
            self.farmupgradeprice=variables[42]
            self.mineupgradeprice=variables[43]
            self.factoryupgradeprice=variables[44]
            self.bankupgradeprice=variables[45]
            self.templeupgradeprice=variables[46]
            self.wizardtowerupgradeprice=variables[47]
            self.shipmentupgradeprice=variables[48]
            self.alchemylabupgradeprice=variables[49]
            self.portalupgradeprice=variables[50]
            self.timemachineupgradeprice=variables[51]
            self.upgradeinfolist=variables[52]
            
            # Change amount text
            cursors_text = ('Amount: {}'.format(self.cursors))
            self.cursor_amount.configure(text=cursors_text)
            grandmas_text = ('Amount: {}'.format(self.grandmas))
            self.grandma_amount.configure(text=grandmas_text)
            farms_text = ('Amount: {}'.format(self.farms))
            self.farm_amount.configure(text=farms_text)
            mines_text = ('Amount: {}'.format(self.mines))
            self.mine_amount.configure(text=mines_text)
            factories_text = ('Amount: {}'.format(self.factories))
            self.factory_amount.configure(text=factories_text)
            banks_text = ('Amount: {}'.format(self.banks))
            self.bank_amount.configure(text=banks_text)
            temples_text = ('Amount: {}'.format(self.temples))
            self.temple_amount.configure(text=temples_text)
            wizardtowers_text = ('Amount: {}'.format(self.wizardtowers))
            self.wizardtower_amount.configure(text=wizardtowers_text)
            shipments_text = ('Amount: {}'.format(self.shipments))
            self.shipment_amount.configure(text=shipments_text)
            alchemylabs_text = ('Amount: {}'.format(self.alchemylabs))
            self.alchemylab_amount.configure(text=alchemylabs_text)
            portals_text = ('Amount: {}'.format(self.portals))
            self.portal_amount.configure(text=portals_text)
            timemachines_text = ('Amount: {}'.format(self.timemachines))
            self.timemachine_amount.configure(text=timemachines_text)
            
            if self.cursororder == 1:
                self.cursorupgrade1.updateinfo(self)
            elif self.cursororder == 2:
                self.cursorupgrade2.updateinfo(self)
            elif self.cursororder == 3:
                self.cursorupgrade3.updateinfo(self)
            elif self.cursororder == 4:
                self.cursorupgrade4.updateinfo(self)
            elif self.cursororder == 5:
                self.cursorupgrade5.updateinfo(self)
            elif self.cursororder == 6:
                self.cursorupgrade6.updateinfo(self)
            elif self.cursororder == 7:
                self.cursorupgrade7.updateinfo(self)
            elif self.cursororder == 8:
                self.cursorupgrade8.updateinfo(self)
            elif self.cursororder == 9:
                self.cursorupgrade9.updateinfo(self)
            elif self.cursororder == 10:
                self.cursorupgrade10.updateinfo(self)
            elif self.cursororder == 13:
                self.cursorupgrade11.updateinfo(self)
            elif self.cursororder == 12:
                self.cursorupgrade12.updateinfo(self)
            elif self.cursororder == 13:
                self.cursorupgrade13.updateinfo(self)
            elif self.cursororder == 14:
                self.cursorupgradeprice = math.inf
                self.cursorupgradelabel.configure(
                        text='Cursor Upgrades Maxed')
                self.cursorupgradetext.configure(
                        text='')     
                
            if self.grandmaorder == 1:
                self.grandmaupgrade1.updateinfo(self)
            elif self.grandmaorder == 2:
                self.grandmaupgrade2.updateinfo(self)
            elif self.grandmaorder == 3:
                self.grandmaupgrade3.updateinfo(self)
            elif self.grandmaorder == 4:
                self.grandmaupgrade4.updateinfo(self)
            elif self.grandmaorder == 5:
                self.grandmaupgrade5.updateinfo(self)
            elif self.grandmaorder == 6:
                self.grandmaupgrade6.updateinfo(self)
            elif self.grandmaorder == 7:
                self.grandmaupgrade7.updateinfo(self)
            elif self.grandmaorder == 8:
                self.grandmaupgrade8.updateinfo(self)
            elif self.grandmaorder == 9:
                self.grandmaupgrade9.updateinfo(self)
            elif self.grandmaorder == 10:
                self.grandmaupgrade10.updateinfo(self)
            elif self.grandmaorder == 13:
                self.grandmaupgrade11.updateinfo(self)
            elif self.grandmaorder == 12:
                self.grandmaupgrade12.updateinfo(self)
            elif self.grandmaorder == 13:
                self.grandmaupgrade13.updateinfo(self)
            elif self.grandmaorder == 14:
                self.grandmaupgradeprice = math.inf
                self.grandmaupgradelabel.configure(
                        text='Grandma Upgrades Maxed')
                self.grandmaupgradetext.configure(
                        text='')        
                
            if self.farmorder == 1:
                self.farmupgrade1.updateinfo(self)
            elif self.farmorder == 2:
                self.farmupgrade2.updateinfo(self)
            elif self.farmorder == 3:
                self.farmupgrade3.updateinfo(self)
            elif self.farmorder == 4:
                self.farmupgrade4.updateinfo(self)
            elif self.farmorder == 5:
                self.farmupgrade5.updateinfo(self)
            elif self.farmorder == 6:
                self.farmupgrade6.updateinfo(self)
            elif self.farmorder == 7:
                self.farmupgrade7.updateinfo(self)
            elif self.farmorder == 8:
                self.farmupgrade8.updateinfo(self)
            elif self.farmorder == 9:
                self.farmupgrade9.updateinfo(self)
            elif self.farmorder == 10:
                self.farmupgrade10.updateinfo(self)
            elif self.farmorder == 13:
                self.farmupgrade11.updateinfo(self)
            elif self.farmorder == 12:
                self.farmupgrade12.updateinfo(self)
            elif self.farmorder == 13:
                self.farmupgrade13.updateinfo(self)
            elif self.farmorder == 14:
                self.farmupgradeprice = math.inf
                self.farmupgradelabel.configure(
                        text='Farm Upgrades Maxed')
                self.farmupgradetext.configure(
                        text='')        
                
            if self.mineorder == 1:
                self.mineupgrade1.updateinfo(self)
            elif self.mineorder == 2:
                self.mineupgrade2.updateinfo(self)
            elif self.mineorder == 3:
                self.mineupgrade3.updateinfo(self)
            elif self.mineorder == 4:
                self.mineupgrade4.updateinfo(self)
            elif self.mineorder == 5:
                self.mineupgrade5.updateinfo(self)
            elif self.mineorder == 6:
                self.mineupgrade6.updateinfo(self)
            elif self.mineorder == 7:
                self.mineupgrade7.updateinfo(self)
            elif self.mineorder == 8:
                self.mineupgrade8.updateinfo(self)
            elif self.mineorder == 9:
                self.mineupgrade9.updateinfo(self)
            elif self.mineorder == 10:
                self.mineupgrade10.updateinfo(self)
            elif self.mineorder == 13:
                self.mineupgrade11.updateinfo(self)
            elif self.mineorder == 12:
                self.mineupgrade12.updateinfo(self)
            elif self.mineorder == 13:
                self.mineupgrade13.updateinfo(self)
            elif self.mineorder == 14:
                self.mineupgradeprice = math.inf
                self.mineupgradelabel.configure(
                        text='Mine Upgrades Maxed')
                self.mineupgradetext.configure(
                        text='')        
                
            if self.factoryorder == 1:
                self.factoryupgrade1.updateinfo(self)
            elif self.factoryorder == 2:
                self.factoryupgrade2.updateinfo(self)
            elif self.factoryorder == 3:
                self.factoryupgrade3.updateinfo(self)
            elif self.factoryorder == 4:
                self.factoryupgrade4.updateinfo(self)
            elif self.factoryorder == 5:
                self.factoryupgrade5.updateinfo(self)
            elif self.factoryorder == 6:
                self.factoryupgrade6.updateinfo(self)
            elif self.factoryorder == 7:
                self.factoryupgrade7.updateinfo(self)
            elif self.factoryorder == 8:
                self.factoryupgrade8.updateinfo(self)
            elif self.factoryorder == 9:
                self.factoryupgrade9.updateinfo(self)
            elif self.factoryorder == 10:
                self.factoryupgrade10.updateinfo(self)
            elif self.factoryorder == 13:
                self.factoryupgrade11.updateinfo(self)
            elif self.factoryorder == 12:
                self.factoryupgrade12.updateinfo(self)
            elif self.factoryorder == 13:
                self.factoryupgrade13.updateinfo(self)
            elif self.factoryorder == 14:
                self.factoryupgradeprice = math.inf
                self.factoryupgradelabel.configure(
                        text='Factory Upgrades Maxed')
                self.factoryupgradetext.configure(
                        text='')
                    
            if self.bankorder == 1:
                self.bankupgrade1.updateinfo(self)
            elif self.bankorder == 2:
                self.bankupgrade2.updateinfo(self)
            elif self.bankorder == 3:
                self.bankupgrade3.updateinfo(self)
            elif self.bankorder == 4:
                self.bankupgrade4.updateinfo(self)
            elif self.bankorder == 5:
                self.bankupgrade5.updateinfo(self)
            elif self.bankorder == 6:
                self.bankupgrade6.updateinfo(self)
            elif self.bankorder == 7:
                self.bankupgrade7.updateinfo(self)
            elif self.bankorder == 8:
                self.bankupgrade8.updateinfo(self)
            elif self.bankorder == 9:
                self.bankupgrade9.updateinfo(self)
            elif self.bankorder == 10:
                self.bankupgrade10.updateinfo(self)
            elif self.bankorder == 13:
                self.bankupgrade11.updateinfo(self)
            elif self.bankorder == 12:
                self.bankupgrade12.updateinfo(self)
            elif self.bankorder == 13:
                self.bankupgrade13.updateinfo(self)
            elif self.bankorder == 14:
                self.bankupgradeprice = math.inf
                self.bankupgradelabel.configure(
                        text='Cursor Upgrades Maxed')
                self.bankupgradetext.configure(
                        text='')        
                
            if self.templeorder == 1:
                self.templeupgrade1.updateinfo(self)
            elif self.templeorder == 2:
                self.templeupgrade2.updateinfo(self)
            elif self.templeorder == 3:
                self.templeupgrade3.updateinfo(self)
            elif self.templeorder == 4:
                self.templeupgrade4.updateinfo(self)
            elif self.templeorder == 5:
                self.templeupgrade5.updateinfo(self)
            elif self.templeorder == 6:
                self.templeupgrade6.updateinfo(self)
            elif self.templeorder == 7:
                self.templeupgrade7.updateinfo(self)
            elif self.templeorder == 8:
                self.templeupgrade8.updateinfo(self)
            elif self.templeorder == 9:
                self.templeupgrade9.updateinfo(self)
            elif self.templeorder == 10:
                self.templeupgrade10.updateinfo(self)
            elif self.templeorder == 13:
                self.templeupgrade11.updateinfo(self)
            elif self.templeorder == 12:
                self.templeupgrade12.updateinfo(self)
            elif self.templeorder == 13:
                self.templeupgrade13.updateinfo(self)
            elif self.templeorder == 14:
                self.templeupgradeprice = math.inf
                self.templeupgradelabel.configure(
                        text='Temple Upgrades Maxed')
                self.templeupgradetext.configure(
                        text='')        
                
            if self.wizardtowerorder == 1:
                self.wizardtowerupgrade1.updateinfo(self)
            elif self.wizardtowerorder == 2:
                self.wizardtowerupgrade2.updateinfo(self)
            elif self.wizardtowerorder == 3:
                self.wizardtowerupgrade3.updateinfo(self)
            elif self.wizardtowerorder == 4:
                self.wizardtowerupgrade4.updateinfo(self)
            elif self.wizardtowerorder == 5:
                self.wizardtowerupgrade5.updateinfo(self)
            elif self.wizardtowerorder == 6:
                self.wizardtowerupgrade6.updateinfo(self)
            elif self.wizardtowerorder == 7:
                self.wizardtowerupgrade7.updateinfo(self)
            elif self.wizardtowerorder == 8:
                self.wizardtowerupgrade8.updateinfo(self)
            elif self.wizardtowerorder == 9:
                self.wizardtowerupgrade9.updateinfo(self)
            elif self.wizardtowerorder == 10:
                self.wizardtowerupgrade10.updateinfo(self)
            elif self.wizardtowerorder == 13:
                self.wizardtowerupgrade11.updateinfo(self)
            elif self.wizardtowerorder == 12:
                self.wizardtowerupgrade12.updateinfo(self)
            elif self.wizardtowerorder == 13:
                self.wizardtowerupgrade13.updateinfo(self)
            elif self.wizardtowerorder == 14:
                self.wizardtowerupgradeprice = math.inf
                self.wizardtowerupgradelabel.configure(
                        text='Wizard Tower Upgrades Maxed')
                self.wizardtowerupgradetext.configure(
                        text='')        
                
            if self.shipmentorder == 1:
                self.shipmentupgrade1.updateinfo(self)
            elif self.shipmentorder == 2:
                self.shipmentupgrade2.updateinfo(self)
            elif self.shipmentorder == 3:
                self.shipmentupgrade3.updateinfo(self)
            elif self.shipmentorder == 4:
                self.shipmentupgrade4.updateinfo(self)
            elif self.shipmentorder == 5:
                self.shipmentupgrade5.updateinfo(self)
            elif self.shipmentorder == 6:
                self.shipmentupgrade6.updateinfo(self)
            elif self.shipmentorder == 7:
                self.shipmentupgrade7.updateinfo(self)
            elif self.shipmentorder == 8:
                self.shipmentupgrade8.updateinfo(self)
            elif self.shipmentorder == 9:
                self.shipmentupgrade9.updateinfo(self)
            elif self.shipmentorder == 10:
                self.shipmentupgrade10.updateinfo(self)
            elif self.shipmentorder == 13:
                self.shipmentupgrade11.updateinfo(self)
            elif self.shipmentorder == 12:
                self.shipmentupgrade12.updateinfo(self)
            elif self.shipmentorder == 13:
                self.shipmentupgrade13.updateinfo(self)
            elif self.shipmentorder == 14:
                self.shipmentupgradeprice = math.inf
                self.shipmentupgradelabel.configure(
                        text='Wizard Tower Upgrades Maxed')
                self.shipmentupgradetext.configure(
                        text='')        
                
            if self.alchemylaborder == 1:
                self.alchemylabupgrade1.updateinfo(self)
            elif self.alchemylaborder == 2:
                self.alchemylabupgrade2.updateinfo(self)
            elif self.alchemylaborder == 3:
                self.alchemylabupgrade3.updateinfo(self)
            elif self.alchemylaborder == 4:
                self.alchemylabupgrade4.updateinfo(self)
            elif self.alchemylaborder == 5:
                self.alchemylabupgrade5.updateinfo(self)
            elif self.alchemylaborder == 6:
                self.alchemylabupgrade6.updateinfo(self)
            elif self.alchemylaborder == 7:
                self.alchemylabupgrade7.updateinfo(self)
            elif self.alchemylaborder == 8:
                self.alchemylabupgrade8.updateinfo(self)
            elif self.alchemylaborder == 9:
                self.alchemylabupgrade9.updateinfo(self)
            elif self.alchemylaborder == 10:
                self.alchemylabupgrade10.updateinfo(self)
            elif self.alchemylaborder == 13:
                self.alchemylabupgrade11.updateinfo(self)
            elif self.alchemylaborder == 12:
                self.alchemylabupgrade12.updateinfo(self)
            elif self.alchemylaborder == 13:
                self.alchemylabupgrade13.updateinfo(self)
            elif self.alchemylaborder == 14:
                self.alchemylabupgradeprice = math.inf
                self.alchemylabupgradelabel.configure(
                        text='Alchemy Lab Upgrades Maxed')
                self.alchemylabupgradetext.configure(
                        text='')        
                
            if self.portalorder == 1:
                self.portalupgrade1.updateinfo(self)
            elif self.portalorder == 2:
                self.portalupgrade2.updateinfo(self)
            elif self.portalorder == 3:
                self.portalupgrade3.updateinfo(self)
            elif self.portalorder == 4:
                self.portalupgrade4.updateinfo(self)
            elif self.portalorder == 5:
                self.portalupgrade5.updateinfo(self)
            elif self.portalorder == 6:
                self.portalupgrade6.updateinfo(self)
            elif self.portalorder == 7:
                self.portalupgrade7.updateinfo(self)
            elif self.portalorder == 8:
                self.portalupgrade8.updateinfo(self)
            elif self.portalorder == 9:
                self.portalupgrade9.updateinfo(self)
            elif self.portalorder == 10:
                self.portalupgrade10.updateinfo(self)
            elif self.portalorder == 13:
                self.portalupgrade11.updateinfo(self)
            elif self.portalorder == 12:
                self.portalupgrade12.updateinfo(self)
            elif self.portalorder == 13:
                self.portalupgrade13.updateinfo(self)
            elif self.portalorder == 14:
                self.portalupgradeprice = math.inf
                self.portalupgradelabel.configure(
                        text='Portal Upgrades Maxed')
                self.portalupgradetext.configure(
                        text='')        
                
            if self.timemachineorder == 1:
                self.timemachineupgrade1.updateinfo(self)
            elif self.timemachineorder == 2:
                self.timemachineupgrade2.updateinfo(self)
            elif self.timemachineorder == 3:
                self.timemachineupgrade3.updateinfo(self)
            elif self.timemachineorder == 4:
                self.timemachineupgrade4.updateinfo(self)
            elif self.timemachineorder == 5:
                self.timemachineupgrade5.updateinfo(self)
            elif self.timemachineorder == 6:
                self.timemachineupgrade6.updateinfo(self)
            elif self.timemachineorder == 7:
                self.timemachineupgrade7.updateinfo(self)
            elif self.timemachineorder == 8:
                self.timemachineupgrade8.updateinfo(self)
            elif self.timemachineorder == 9:
                self.timemachineupgrade9.updateinfo(self)
            elif self.timemachineorder == 10:
                self.timemachineupgrade10.updateinfo(self)
            elif self.timemachineorder == 13:
                self.timemachineupgrade11.updateinfo(self)
            elif self.timemachineorder == 12:
                self.timemachineupgrade12.updateinfo(self)
            elif self.timemachineorder == 13:
                self.timemachineupgrade13.updateinfo(self)
            elif self.timemachineorder == 14:
                self.timemachineupgradeprice = math.inf
                self.timemachineupgradelabel.configure(
                        text='Time Machine Upgrades Maxed')
                self.timemachineupgradetext.configure(
                        text='')        
            
            self.pricecalc()
            self.pricecheck()
            self.thousandfingerscalc()
            self.updateperclick()
            self.cpscalc()
            self.changecookietext()
            
            totalbuildingsexceptcursors = self.grandmas + \
                    self.farms + self.mines + self.factories + self.banks + self.temples + \
                    self.wizardtowers + self.shipments + \
                    self.alchemylabs + self.portals + self.timemachines
            if totalbuildingsexceptcursors > 0:
                self.startidletimer()
                
        except FileNotFoundError:
            pass
                
        

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
        
class Save:

    def __init__(self, parent):
        parent.savebutton.configure(state=DISABLED)
        self.box = Toplevel()
        self.box.iconbitmap(r'cookieicon.ico')
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
            parent.thousandfingersamount = self.effectnumber
            parent.thousandfingerscalc()
        if self.effectfunction == 'timesthousand':
            parent.thousandfingersamount = parent.thousandfingersamount * self.effectnumber
            parent.thousandfingerscalc()

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
        parent.updateupgradesinfo(
            self.name, self.descriptiontext)        

        parent.grandmacps = parent.grandmacps * self.effectnumber
        parent.cpscalc()
        
    def updateinfo(self, parent):
        parent.grandmaupgradeprice = self.price
        upgrade_text = ('{}:\n{} Cookies'.format(
            self.name, parent.numbercheck(self.price)))
        parent.grandmaupgradelabel.configure(text=upgrade_text)
        parent.grandmaupgradetext.configure(
            text=self.descriptiontext)
    
class FarmUpgrades:
    def __init__(self, parent, name, price, unlock, order, effectnumber, description):
        self.name = str(name)
        self.price = price
        self.unlockcondition = unlock
        self.order = order
        self.effectnumber = effectnumber
        self.descriptiontext = description

    def buy(self, parent):
        parent.farmorder += 1
        parent.cookies = parent.cookies - self.price
        parent.pricecheck()
        parent.changecookietext()
        parent.updateupgradesinfo(
            self.name, self.descriptiontext)        

        parent.farmcps = parent.farmcps * self.effectnumber
        parent.cpscalc()
        
    def updateinfo(self, parent):
        parent.farmupgradeprice = self.price
        upgrade_text = ('{}:\n{} Cookies'.format(
            self.name, parent.numbercheck(self.price)))
        parent.farmupgradelabel.configure(text=upgrade_text)
        parent.farmupgradetext.configure(
            text=self.descriptiontext)
        
class MineUpgrades:
    def __init__(self, parent, name, price, unlock, order, effectnumber, description):
        self.name = str(name)
        self.price = price
        self.unlockcondition = unlock
        self.order = order
        self.effectnumber = effectnumber
        self.descriptiontext = description

    def buy(self, parent):
        parent.mineorder += 1
        parent.cookies = parent.cookies - self.price
        parent.pricecheck()
        parent.changecookietext()
        parent.updateupgradesinfo(
            self.name, self.descriptiontext)        

        parent.minecps = parent.minecps * self.effectnumber
        parent.cpscalc()
        
    def updateinfo(self, parent):
        parent.mineupgradeprice = self.price
        upgrade_text = ('{}:\n{} Cookies'.format(
            self.name, parent.numbercheck(self.price)))
        parent.mineupgradelabel.configure(text=upgrade_text)
        parent.mineupgradetext.configure(
            text=self.descriptiontext)
        
class FactoryUpgrades:
    def __init__(self, parent, name, price, unlock, order, effectnumber, description):
        self.name = str(name)
        self.price = price
        self.unlockcondition = unlock
        self.order = order
        self.effectnumber = effectnumber
        self.descriptiontext = description

    def buy(self, parent):
        parent.factoryorder += 1
        parent.cookies = parent.cookies - self.price
        parent.pricecheck()
        parent.changecookietext()
        parent.updateupgradesinfo(
            self.name, self.descriptiontext)        

        parent.factorycps = parent.factorycps * self.effectnumber
        parent.cpscalc()
        
    def updateinfo(self, parent):
        parent.factoryupgradeprice = self.price
        upgrade_text = ('{}:\n{} Cookies'.format(
            self.name, parent.numbercheck(self.price)))
        parent.factoryupgradelabel.configure(text=upgrade_text)
        parent.factoryupgradetext.configure(
            text=self.descriptiontext)
        
class BankUpgrades:
    def __init__(self, parent, name, price, unlock, order, effectnumber, description):
        self.name = str(name)
        self.price = price
        self.unlockcondition = unlock
        self.order = order
        self.effectnumber = effectnumber
        self.descriptiontext = description

    def buy(self, parent):
        parent.bankorder += 1
        parent.cookies = parent.cookies - self.price
        parent.pricecheck()
        parent.changecookietext()
        parent.updateupgradesinfo(
            self.name, self.descriptiontext)        

        parent.bankcps = parent.bankcps * self.effectnumber
        parent.cpscalc()
        
    def updateinfo(self, parent):
        parent.bankupgradeprice = self.price
        upgrade_text = ('{}:\n{} Cookies'.format(
            self.name, parent.numbercheck(self.price)))
        parent.bankupgradelabel.configure(text=upgrade_text)
        parent.bankupgradetext.configure(
            text=self.descriptiontext)
        
class TempleUpgrades:
    def __init__(self, parent, name, price, unlock, order, effectnumber, description):
        self.name = str(name)
        self.price = price
        self.unlockcondition = unlock
        self.order = order
        self.effectnumber = effectnumber
        self.descriptiontext = description

    def buy(self, parent):
        parent.templeorder += 1
        parent.cookies = parent.cookies - self.price
        parent.pricecheck()
        parent.changecookietext()
        parent.updateupgradesinfo(
            self.name, self.descriptiontext)        

        parent.templecps = parent.templecps * self.effectnumber
        parent.cpscalc()
        
    def updateinfo(self, parent):
        parent.templeupgradeprice = self.price
        upgrade_text = ('{}:\n{} Cookies'.format(
            self.name, parent.numbercheck(self.price)))
        parent.templeupgradelabel.configure(text=upgrade_text)
        parent.templeupgradetext.configure(
            text=self.descriptiontext)
        
class WizardTowerUpgrades:
    def __init__(self, parent, name, price, unlock, order, effectnumber, description):
        self.name = str(name)
        self.price = price
        self.unlockcondition = unlock
        self.order = order
        self.effectnumber = effectnumber
        self.descriptiontext = description

    def buy(self, parent):
        parent.wizardtowerorder += 1
        parent.cookies = parent.cookies - self.price
        parent.pricecheck()
        parent.changecookietext()
        parent.updateupgradesinfo(
            self.name, self.descriptiontext)        

        parent.wizardtowercps = parent.wizardtowercps * self.effectnumber
        parent.cpscalc()
        
    def updateinfo(self, parent):
        parent.wizardtowerupgradeprice = self.price
        upgrade_text = ('{}:\n{} Cookies'.format(
            self.name, parent.numbercheck(self.price)))
        parent.wizardtowerupgradelabel.configure(text=upgrade_text)
        parent.wizardtowerupgradetext.configure(
            text=self.descriptiontext)
        
class ShipmentUpgrades:
    def __init__(self, parent, name, price, unlock, order, effectnumber, description):
        self.name = str(name)
        self.price = price
        self.unlockcondition = unlock
        self.order = order
        self.effectnumber = effectnumber
        self.descriptiontext = description

    def buy(self, parent):
        parent.shipmentorder += 1
        parent.cookies = parent.cookies - self.price
        parent.pricecheck()
        parent.changecookietext()
        parent.updateupgradesinfo(
            self.name, self.descriptiontext)        

        parent.shipmentcps = parent.shipmentcps * self.effectnumber
        parent.cpscalc()
        
    def updateinfo(self, parent):
        parent.shipmentupgradeprice = self.price
        upgrade_text = ('{}:\n{} Cookies'.format(
            self.name, parent.numbercheck(self.price)))
        parent.shipmentupgradelabel.configure(text=upgrade_text)
        parent.shipmentupgradetext.configure(
            text=self.descriptiontext)
        
class AlchemyLabUpgrades:
    def __init__(self, parent, name, price, unlock, order, effectnumber, description):
        self.name = str(name)
        self.price = price
        self.unlockcondition = unlock
        self.order = order
        self.effectnumber = effectnumber
        self.descriptiontext = description

    def buy(self, parent):
        parent.alchemylaborder += 1
        parent.cookies = parent.cookies - self.price
        parent.pricecheck()
        parent.changecookietext()
        parent.updateupgradesinfo(
            self.name, self.descriptiontext)        

        parent.alchemylabcps = parent.alchemylabcps * self.effectnumber
        parent.cpscalc()
        
    def updateinfo(self, parent):
        parent.alchemylabupgradeprice = self.price
        upgrade_text = ('{}:\n{} Cookies'.format(
            self.name, parent.numbercheck(self.price)))
        parent.alchemylabupgradelabel.configure(text=upgrade_text)
        parent.alchemylabupgradetext.configure(
            text=self.descriptiontext)
        
class PortalUpgrades:
    def __init__(self, parent, name, price, unlock, order, effectnumber, description):
        self.name = str(name)
        self.price = price
        self.unlockcondition = unlock
        self.order = order
        self.effectnumber = effectnumber
        self.descriptiontext = description

    def buy(self, parent):
        parent.portalorder += 1
        parent.cookies = parent.cookies - self.price
        parent.pricecheck()
        parent.changecookietext()
        parent.updateupgradesinfo(
            self.name, self.descriptiontext)        

        parent.portalcps = parent.portalcps * self.effectnumber
        parent.cpscalc()
        
    def updateinfo(self, parent):
        parent.portalupgradeprice = self.price
        upgrade_text = ('{}:\n{} Cookies'.format(
            self.name, parent.numbercheck(self.price)))
        parent.portalupgradelabel.configure(text=upgrade_text)
        parent.portalupgradetext.configure(
            text=self.descriptiontext)
        
class TimeMachineUpgrades:
    def __init__(self, parent, name, price, unlock, order, effectnumber, description):
        self.name = str(name)
        self.price = price
        self.unlockcondition = unlock
        self.order = order
        self.effectnumber = effectnumber
        self.descriptiontext = description

    def buy(self, parent):
        parent.timemachineorder += 1
        parent.cookies = parent.cookies - self.price
        parent.pricecheck()
        parent.changecookietext()
        parent.updateupgradesinfo(
            self.name, self.descriptiontext)        

        parent.timemachinecps = parent.timemachinecps * self.effectnumber
        parent.cpscalc()
        
    def updateinfo(self, parent):
        parent.timemachineupgradeprice = self.price
        upgrade_text = ('{}:\n{} Cookies'.format(
            self.name, parent.numbercheck(self.price)))
        parent.timemachineupgradelabel.configure(text=upgrade_text)
        parent.timemachineupgradetext.configure(
            text=self.descriptiontext)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Cookie Clicker")
    root.iconbitmap(r'cookieicon.ico')
    root.resizable(0, 0)
    Generate = Cookies(root)
    root.mainloop()
