"""Per-building upgrade definitions.

Each class describes one building's upgrades. Instances receive the running
``Cookies`` game instance as ``parent`` and read/update its state directly.
"""


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

