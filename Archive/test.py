from tkinter import *
import time
import threading
import math
from functools import partial
import random

class Minigame:
    def __init__(self,parent):
        
        self.mainframe = Frame(root)
        self.mainframe.grid()
        
        self.heading = Label(self.mainframe, text='Click the Cookies before they disappear!', font='arial 18 bold', justify = CENTER)
        self.heading.grid(row=0,padx=20,pady=20, sticky=N, columnspan=100)
        
               
           
            
        self.startbutton = Button(self.mainframe, text='Start', padx=20, pady=20, command=self.start)
        self.startbutton.grid(columnspan=100, padx=10, pady=10, sticky=S)

    def start(self):
        
        self.startbutton.config(state=DISABLED)
        
        def clicked():
            print('clicked')
            global clickedd
            clickedd+=1
            minigameframe.destroy()
            spawn()
        
            
       
        def missed():
            minigameframe.destroy()
            
            print('game over')   
            self.startbutton.config(state=NORMAL)
            
        def timer():
            a=0
            while True:
                time.sleep(0.1)
                
                if clickedd%2 == 0:
                    a+=1
                    if a==20:
                        missed()
                        break
                    else:
                        pass
                else:
                    print('yep')
                    break
                    
        timerthread = threading.Thread(name='timer',target=timer)
             
        def spawn():
            global clickbutton
            global clickedd
            global minigameframe
                       
            clickedd = 0
    
            minigameframe = Frame(self.mainframe)
            minigameframe.grid(row=1, column=0, rowspan=100,columnspan=100, sticky=E+W+N+S, padx=30, pady=10)              
            while True:
                for r in range(0,15):
                    for c in range (0,20):
                        Button(minigameframe, bg='black', padx=15, pady=10, highlightthickness = 0, bd = 0, command=missed).grid(row=r,column=c)
                break
            buttonrow = random.randint(0,14)
            print(buttonrow)
            buttoncolumn = random.randint(0,19)
            print(buttoncolumn)
        
            clickbutton = Button(minigameframe, padx=15, pady=10, bg='orange', command=clicked, highlightthickness = 0, bd = 0)
            clickbutton.grid(row=buttonrow, column=buttoncolumn)
            
            #minigameframe.after(1000, missed)
            
        
                            
        
        spawn()
    
        
        
        
        
# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Minigame")
    Generate = Minigame(root)
    root.mainloop()