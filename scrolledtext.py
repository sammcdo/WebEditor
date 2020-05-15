from tkinter import *

class ScrolledText():
    def __init__(self, parent=None, text='', file=None):
        self.frm = parent
        self.makewidgets()
        self.settext(text, file)

    def makewidgets(self):
        sbar = Scrollbar(self.frm)
        hbar  = Scrollbar(self.frm, orient='horizontal')
        text = Text(self.frm, relief=SUNKEN, undo=1, wrap='none')
        hbar.config(command=text.xview)
        sbar.config(command=text.yview)                  # xlink sbar and text
        text.config(yscrollcommand=sbar.set)             # call vbar.set on text move
        text.config(xscrollcommand=hbar.set)        
        sbar.pack(side=RIGHT, fill=Y)                    # pack first=clip last
        hbar.pack(side=BOTTOM, fill=X)                   # pack text last
        text.pack(side=LEFT, expand=YES, fill=BOTH)      # text clipped first
        self.text = text

    def settext(self, text='', file=None):
        if file:
            text = open(file, 'r').read()
        self.text.delete('1.0', END)                     # delete current text
        self.text.insert('1.0', text)                    # add at line 1, col 0
        self.text.mark_set(INSERT, '1.0')                # set insert cursor
        self.text.focus()                                # save user a click

    def gettext(self):                                   # returns a string
        return self.text.get('1.0', END+'-1c')           # first through last
