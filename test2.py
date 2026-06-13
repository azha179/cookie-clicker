list = ['cursor', 'grandma', 'farm', 'mine', 'factorie', 'bank', 'temple', 'wizardtower', 'shipment', 'alchemylab', 'portal', 'timemachine']

for i in list:
    text = ("{}s_text = ('Amount: {}'.format(self.{}s))".format(i, '{}', i))
    print(text)
    a = ("self.{}_amount.configure(text={}s_text)".format(i, i))
    print(a)
    

