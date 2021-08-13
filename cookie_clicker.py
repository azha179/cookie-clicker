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
        self.buildingandupgradeframe = Frame(self.cookie_frame, bg=upgradebg)
        self.buildingandupgradeframe.grid(
            row=0, column=1, rowspan=10, padx=20, pady=10)

        # Cookie Amount (row1, column0)
        self.cookie_counter = Label(
            self.cookie_frame, text=' ', font='arial 18', pady=10, bg=bgcolour, fg='white')
        self.changecookietext()
        self.cookie_counter.grid(row=1)

        # Cookie button frame (row2, column0)
        self.cookie_frame = Frame(self.cookie_frame, bg=bgcolour)
        self.cookie_frame.grid(row=2)

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
        self.buttonframe.grid(row=3, pady=20)

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
            self.buildingandupgradeframe, highlightbackground='#01365e', highlightthickness=3, bg=upgradebg)
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
        self.cookiespersecond.grid(row=0, columnspan=3, pady=10)

        # Expand
        self.buildingexpandbutton = Button(self.upgradesframe, text='-', font='arial 22 bold', bg=upgradebg,
                                           padx=10, command=self.collapsebuilding, highlightthickness=0, bd=0, activebackground=upgradebg, fg='dark grey')
        self.buildingexpandbutton.grid(row=0, column=3, sticky=NE)

        # Cookies per second count
        self.cpslabel = Label(self.upgradesframe, text='0.0 cps',
                              font='arial 12', pady=5, justify=CENTER, bg=upgradebg)
        self.cpslabel.grid(row=1, columnspan=3)

        # Multiplier buy
        self.buymultiplierframe = Frame(self.upgradesframe, bg='#465d70')
        self.buymultiplierframe.grid(row=2, columnspan=3, pady=10)

        self.multiplierlabel = Label(self.buymultiplierframe, text='Buy',
                                     font='arial 14 bold', bg='#465d70', padx=10, pady=5, fg='white')
        self.multiplierlabel.grid(row=0, column=0, padx=20)

        self.multiplierone = Button(self.buymultiplierframe, text='x1', font='arial 12 bold', bg='#465d70', highlightthickness=0,
                                    bd=0, padx=10, fg='white', activebackground='#465d70', activeforeground='white', command=self.timesone)
        self.multiplierone.grid(row=0, column=1, padx=20)

        self.multiplierten = Button(self.buymultiplierframe, text='x10', font='arial 12 ', bg='#465d70', highlightthickness=0,
                                    bd=0, padx=10, fg='white', activebackground='#465d70', activeforeground='white', command=self.timesten)
        self.multiplierten.grid(row=0, column=2, padx=20)

        self.multiplierhundred = Button(self.buymultiplierframe, text='x100', font='arial 12 ', bg='#465d70', highlightthickness=0,
                                        bd=0, padx=10, fg='white', activebackground='#465d70', activeforeground='white', command=self.timeshundred)
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
        )], image=self.buybuttonimage, highlightthickness=0, bd=0, bg=upgradebg, activebackground=upgradebg, pady=10)
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
        )], image=self.buybuttonimage, highlightthickness=0, bd=0, bg=upgradebg, activebackground=upgradebg, pady=10)
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
        )], image=self.buybuttonimage, highlightthickness=0, bd=0, bg=upgradebg, activebackground=upgradebg, pady=10)
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
        )], image=self.buybuttonimage, highlightthickness=0, bd=0, bg=upgradebg, activebackground=upgradebg, pady=10)
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
        )], image=self.buybuttonimage, highlightthickness=0, bd=0, bg=upgradebg, activebackground=upgradebg, pady=10)
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
        )], image=self.buybuttonimage, highlightthickness=0, bd=0, bg=upgradebg, activebackground=upgradebg, pady=10)
        self.bank_buy.grid(row=8, column=2, sticky=E, padx=20, pady=10)

        # Building Upgrades

        # Info Button
        self.bupgradeinfobutton = Button(self.buildingupgradeframe, text='Info', font='arial 14 bold', bg='#ffce8f',
                                         padx=10, highlightthickness=0, bd=0, activebackground='#ffce8f', fg='dark grey', command=self.upgradeinfo)
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

        self.cursorupgradelabel = Label(self.buildingupgradeframe, text='Upgrade Cursor:\n100 Cookies',
                                        font='arial 14', padx=20, pady=10, bg=bupgradebg, justify=LEFT)

        self.cursorupgradetext = Label(self.buildingupgradeframe, text=self.cursorupgrade1.descriptiontext,
                                       font='arial 10', padx=20, pady=10, bg=bupgradebg, justify=CENTER, wraplength=150)

        self.cursorupgradebutton = Button(self.buildingupgradeframe, padx=20, pady=10, command=self.cursorupgrade,
                                          image=self.redbuybutton, highlightthickness=0, bd=0, bg=bupgradebg, activebackground=bupgradebg)

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

        self.grandmaupgradelabel = Label(self.buildingupgradeframe, text='Upgrade Grandma:\n1000 Cookies',
                                         font='arial 14', padx=20, pady=10, bg=bupgradebg, justify=LEFT)

        self.grandmaupgradetext = Label(self.buildingupgradeframe, text=self.grandmaupgrade1.descriptiontext,
                                        font='arial 10', padx=20, pady=10, bg=bupgradebg, justify=CENTER, wraplength=150)

        self.grandmaupgradebutton = Button(self.buildingupgradeframe, padx=20, pady=10, command=self.grandmaupgrade,
                                           image=self.redbuybutton, highlightthickness=0, bd=0, bg=bupgradebg, activebackground=bupgradebg)

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
        else:
            pass

    def cursorupgrade(self):
        if self.cursorupgradebuyable == True:
            if self.cursororder == 1:
                self.cursorupgradeprice = self.cursorupgrade2.price
                cursorsupgrade_text = ('Upgrade Cursor:\n{} Cookies'.format(
                    self.numbercheck(self.cursorupgrade2.price)))
                self.cursorupgradelabel.configure(text=cursorsupgrade_text)
                self.cursorupgradetext.configure(
                    text=self.cursorupgrade2.descriptiontext)
                self.cursorupgrade1.buy(self)

            elif self.cursororder == 2:
                self.cursorupgradeprice = self.cursorupgrade3.price
                cursorsupgrade_text = ('Upgrade Cursor:\n{} Cookies'.format(
                    self.numbercheck(self.cursorupgrade3.price)))
                self.cursorupgradelabel.configure(text=cursorsupgrade_text)
                self.cursorupgradetext.configure(
                    text=self.cursorupgrade3.descriptiontext)
                self.cursorupgrade2.buy(self)
            elif self.cursororder == 3:
                self.cursorupgradeprice = self.cursorupgrade4.price
                cursorsupgrade_text = ('Upgrade Cursor:\n{} Cookies'.format(
                    self.numbercheck(self.cursorupgrade4.price)))
                self.cursorupgradelabel.configure(text=cursorsupgrade_text)
                self.cursorupgradetext.configure(
                    text=self.cursorupgrade4.descriptiontext)
                self.cursorupgrade3.buy(self)
            elif self.cursororder == 4:
                self.cursorupgradeprice = self.cursorupgrade5.price
                cursorsupgrade_text = ('Upgrade Cursor:\n{} Cookies'.format(
                    self.numbercheck(self.cursorupgrade5.price)))
                self.cursorupgradelabel.configure(text=cursorsupgrade_text)
                self.cursorupgradetext.configure(
                    text=self.cursorupgrade5.descriptiontext)
                self.cursorupgrade4.buy(self)
            elif self.cursororder == 5:
                self.cursorupgradeprice = self.cursorupgrade6.price
                cursorsupgrade_text = ('Upgrade Cursor:\n{} Cookies'.format(
                    self.numbercheck(self.cursorupgrade6.price)))
                self.cursorupgradelabel.configure(text=cursorsupgrade_text)
                self.cursorupgradetext.configure(
                    text=self.cursorupgrade6.descriptiontext)
                self.cursorupgrade5.buy(self)
            elif self.cursororder == 6:
                self.cursorupgrade6.buy(self)
            # if self.cursororder == 7:
                # self.cursorupgrade7.buy(self)
            # if self.cursororder == 8:
                # self.cursorupgrade8.buy(self)

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
        else:
            pass

    def grandmaupgrade(self):
        if self.grandmaupgradebuyable == True:
            if self.grandmaorder == 1:
                self.grandmaupgradeprice = self.grandmaupgrade2.price
                grandmasupgrade_text = ('Upgrade Grandma:\n{} Cookies'.format(
                    self.numbercheck(self.grandmaupgrade2.price)))
                self.grandmaupgradelabel.configure(text=grandmasupgrade_text)
                self.grandmaupgradetext.configure(
                    text=self.grandmaupgrade2.descriptiontext)
                self.grandmaupgrade1.buy(self)

            elif self.grandmaorder == 2:
                self.grandmaupgradeprice = self.grandmaupgrade3.price
                grandmasupgrade_text = ('Upgrade Grandma:\n{} Cookies'.format(
                    self.numbercheck(self.grandmaupgrade3.price)))
                self.grandmaupgradelabel.configure(text=grandmasupgrade_text)
                self.grandmaupgradetext.configure(
                    text=self.grandmaupgrade3.descriptiontext)
                self.grandmaupgrade2.buy(self)
            elif self.grandmaorder == 3:
                self.grandmaupgradeprice = self.grandmaupgrade4.price
                grandmasupgrade_text = ('Upgrade Grandma:\n{} Cookies'.format(
                    self.numbercheck(self.grandmaupgrade4.price)))
                self.grandmaupgradelabel.configure(text=grandmasupgrade_text)
                self.grandmaupgradetext.configure(
                    text=self.grandmaupgrade4.descriptiontext)
                self.grandmaupgrade3.buy(self)
            elif self.grandmaorder == 4:
                self.grandmaupgradeprice = self.grandmaupgrade5.price
                grandmasupgrade_text = ('Upgrade Grandma:\n{} Cookies'.format(
                    self.numbercheck(self.grandmaupgrade5.price)))
                self.grandmaupgradelabel.configure(text=grandmasupgrade_text)
                self.grandmaupgradetext.configure(
                    text=self.grandmaupgrade5.descriptiontext)
                self.grandmaupgrade4.buy(self)
            elif self.grandmaorder == 5:
                self.grandmaupgradeprice = self.grandmaupgrade6.price
                grandmasupgrade_text = ('Upgrade Grandma:\n{} Cookies'.format(
                    self.numbercheck(self.grandmaupgrade6.price)))
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
            self.factories + self.bankcps * self.banks
        try:
            cps_text = ('{:.1f} cps'.format(self.numbercheck(self.cps)))
        except ValueError:
            cps_text = ('{} cps'.format(self.numbercheck(self.cps)))
        self.cpslabel.configure(text=cps_text)

    def collapsebuilding(self):
        self.cookiespersecond.grid_forget()

        self.cpslabel.grid_forget()
        self.buymultiplierframe.grid_forget()

        self.multiplierlabel.grid_forget()

        self.multiplierone.grid_forget()

        self.multiplierten.grid_forget()

        self.multiplierhundred.grid_forget()

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

    def expandbuilding(self):
        self.cookiespersecond.grid(row=0, columnspan=3, pady=10)

        self.cpslabel.grid(row=1, columnspan=3)

        self.buymultiplierframe.grid(row=2, columnspan=3, pady=10)

        self.multiplierlabel.grid(row=0, column=0, padx=20)

        self.multiplierone.grid(row=0, column=1, padx=20)

        self.multiplierten.grid(row=0, column=2, padx=20)

        self.multiplierhundred.grid(row=0, column=3, padx=20)

        self.cursor_label.grid(row=3, column=0, sticky=W)

        self.cursor_amount.grid(row=3, column=1)

        self.cursor_buy.grid(row=3, column=2, padx=20, pady=10)

        self.grandma_label.grid(row=4, column=0, sticky=W)

        self.grandma_amount.grid(row=4, column=1)

        self.grandma_buy.grid(row=4, column=2, sticky=E, padx=20, pady=10)

        self.farm_label.grid(row=5, column=0, sticky=W)

        self.farm_amount.grid(row=5, column=1)

        self.farm_buy.grid(row=5, column=2, sticky=E, padx=20, pady=10)

        self.mine_label.grid(row=6, column=0, sticky=W)

        self.mine_amount.grid(row=6, column=1)

        self.mine_buy.grid(row=6, column=2, sticky=E, padx=20, pady=10)

        self.factory_label.grid(row=7, column=0, sticky=W)

        self.factory_amount.grid(row=7, column=1)

        self.factory_buy.grid(row=7, column=2, sticky=E, padx=20, pady=10)

        self.bank_label.grid(row=8, column=0, sticky=W)

        self.bank_amount.grid(row=8, column=1)

        self.bank_buy.grid(row=8, column=2, sticky=E, padx=20, pady=10)

    def collapseupgrade(self):
        self.bupgradelabel.grid_forget()
        self.bupgradelabel.grid(row=0, column=1, pady=10, padx=10, sticky=N)
        self.cursorupgradelabel.grid_forget()
        self.cursorupgradetext.grid_forget()
        self.cursorupgradebutton.grid_forget()

        # Grandma
        self.grandmaupgradelabel.grid_forget()

        self.grandmaupgradetext.grid_forget()

        self.grandmaupgradebutton.grid_forget()

        # Farm
        self.farmupgradelabel.grid_forget()

        self.farmtext.grid_forget()

        self.farmupgradebutton.grid_forget()

        # Mine
        self.mineupgradelabel.grid_forget()

        self.minetext.grid_forget()

        self.mineupgradebutton.grid_forget()

        # Factory
        self.factoryupgradelabel.grid_forget()

        self.factorytext.grid_forget()

        self.factoryupgradebutton.grid_forget()

        self.bupgradeexpandbutton.configure(
            command=self.expandupgrade, text='+')

    def expandupgrade(self):
        self.bupgradeexpandbutton.configure(
            command=self.collapseupgrade, text='-')

        # bg colours
        bgcolour = '#0d6bb8'
        upgradebg = '#99d1ff'
        bupgradebg = '#ffcf91'

        self.bupgradelabel.grid_forget()
        self.bupgradelabel.grid(row=0, columnspan=3,
                                pady=10, padx=10, sticky=N)

        # Cursor Upgrade

        self.cursorupgradelabel.grid(row=1, column=0, sticky=W)

        self.cursorupgradetext.grid(row=1, column=1)

        self.cursorupgradebutton.grid(
            row=1, column=2, sticky=E, padx=20, pady=10)

        # Grandma
        self.grandmaupgradelabel.grid(row=2, column=0, sticky=W)

        self.grandmaupgradetext.grid(row=2, column=1)

        self.grandmaupgradebutton.grid(
            row=2, column=2, sticky=E, padx=20, pady=10)

        # Farm
        self.farmupgradelabel.grid(row=3, column=0, sticky=W)

        self.farmtext.grid(row=3, column=1)

        self.farmupgradebutton.grid(
            row=3, column=2, sticky=E, padx=20, pady=10)

        # Mine
        self.mineupgradelabel.grid(row=4, column=0, sticky=W)

        self.minetext.grid(row=4, column=1)

        self.mineupgradebutton.grid(
            row=4, column=2, sticky=E, padx=20, pady=10)

        # Factory
        self.factoryupgradelabel.grid(row=5, column=0, sticky=W)

        self.factorytext.grid(row=5, column=1)

        self.factoryupgradebutton.grid(
            row=5, column=2, sticky=E, padx=20, pady=10)

        self.pricecheck()

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
        get_help.help_text.configure(
            text="Click on the Cookie to get a cookie! Use your cookies to buy upgrades which boost your cookie production.")

    def upgradeinfo(self):
        get_info = UpgradeInfo(self)


class Help:

    def __init__(self, partner):

        bg_colour = "#a1a8ff"

        # Disable button
        partner.help_button.config(state=DISABLED)

        # Set up child window
        self.help_box = Toplevel()

        # Press Cross
        self.help_box.protocol(
            "WM_DELETE_WINDOW", partial(self.close_help, partner))

        # Frame setup
        self.help_frame = Frame(
            self.help_box, width=300, height=200, bg=bg_colour)
        self.help_frame.grid()

        # Heading
        how_heading = Label(self.help_frame, text="Help / Info",
                            font="arial 16 bold", bg=bg_colour, pady=10)
        how_heading.grid(row=0)

        # Body Text
        self.help_text = Label(self.help_frame, text="", justify=CENTER,
                               width=40, bg=bg_colour, wrap=250, font="arial 12")
        self.help_text.grid(row=1, column=0)

        # Dismiss button
        dismiss_btn = Button(self.help_frame, text="Dismiss", width=10, bg="white", font="arial 10 bold",
                             command=partial(self.close_help, partner))
        dismiss_btn.grid(row=2, pady=10)

    def close_help(self, partner):
        partner.help_button.config(state=NORMAL)
        self.help_box.destroy()


class UpgradeInfo:
    def __init__(self, parent):
        self.info_box = Toplevel()


class FirstGold:
    def __init__(self, parent):
        self.box = Toplevel()
        self.frame = Frame(self.box, bg='#ffe76d', width=600, height=600)
        self.frame.pack(side=TOP, expand=TRUE, fill=BOTH)
        self.title = Label(self.frame, font='Arial 16 bold',
                           text='Congratulations! You found a golden cookie!', justify=CENTER, pady=10, bg='#ffe76d')
        self.title.pack(side=TOP, expand=TRUE, fill=BOTH)
        self.text = Label(self.frame, font='Arial 12', text='A random golden cookie will appear every 30 - 180 seconds. Click on it within 13 seconds to receive 100x your current per click amount.',
                          pady=10, padx=20, wraplength=500, bg='#ffe76d')
        self.text.pack(side=TOP, expand=TRUE, fill=BOTH)
        self.button = Button(self.frame, text="Dismiss", width=10,
                             bg="white", font="arial 10 bold", command=self.close, pady=5)
        self.button.pack(side=BOTTOM, pady=10, expand=TRUE)

    def close(self):
        self.box.destroy()


class CursorUpgrades:
    def __init__(self, parent, name, price, unlock, order, effectfunction, effectnumber, description):
        self.name = name
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
        if self.effectfunction == 'times':
            parent.perclick = parent.perclick * self.effectnumber
            parent.cursorcps = parent.cursorcps * self.effectnumber
            parent.cpscalc()
        if self.effectfunction == 'plus':
            self.totalbuildingsexceptcursors = parent.grandmas + \
                parent.farms + parent.mines + parent.factories + parent.banks
            parent.thousandfingersamount = self.effectnumber
            parent.perclick = parent.perclick + \
                self.totalbuildingsexceptcursors * parent.thousandfingersamount
            parent.cursorcps = parent.cursorcps + \
                self.totalbuildingsexceptcursors * parent.thousandfingersamount
            parent.cpscalc()
        if self.effectfunction == 'timesthousand':
            self.totalbuildingsexceptcursors = parent.grandmas + \
                parent.farms + parent.mines + parent.factories + parent.banks
            self.thousandfingersamount = parent.thousandfingersamount * self.effectnumber
            parent.perclick = parent.perclick + \
                self.totalbuildingsexceptcursors * parent.thousandfingersamount
            parent.cursorcps = parent.cursorcps + \
                self.totalbuildingsexceptcursors * parent.thousandfingersamount
            parent.cpscalc()


class GrandmaUpgrades:
    def __init__(self, parent, name, price, unlock, order, effectnumber, description):
        self.name = name
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
