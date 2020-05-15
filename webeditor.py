from tkinter import *
# python3


# pyinstaller
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
from tkinter.messagebox import askokcancel
from tkinter.filedialog   import asksaveasfilename
from tkinter.filedialog   import askopenfilename
#from scrolledtext import ScrolledText
from tkinter.messagebox import showwarning

import webbrowser
import json
import html
import sys
import pyperclip


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


# dont forget to metion to download pbcopy, pbpaste for MAC and xclip or xsel for Linux

class SimpleEditor():
    def __init__(self, file=None):
        """Set it all up."""
        self.root = Tk()
        self.root.title("Web Editor")
        #self.root.iconify()
        if sys.platform.startswith("win"):
            self.root.iconbitmap('web.ico')
        self.root.protocol('WM_DELETE_WINDOW', self.onQuit)
        self.root.minsize(500, 500)
        self.img = PhotoImage(file="run.gif")
        frm = Frame(self.root, relief=SUNKEN, bd=4, bg="#00cbff")
        frm.pack(side=BOTTOM, fill=X)
        # #00cbff #00f8b8
        #self.newbutton = Button(frm, text='New',  command=self.onNew).pack(side=LEFT)
        #self.savebutton = Button(frm, text='Save',  command=self.onSave).pack(side=LEFT)
        self.filelabel = Label(frm, text="", bg="#000000", fg="#ffffff")
        self.filelabel.pack(fill=X, side=TOP)
        self.cutbutton = Button(frm, text='Copy',   command=self.onCopy).pack(side=LEFT)
        self.pastebutton = Button(frm, text='Paste', command=self.onPaste).pack(side=LEFT)
        self.findbutton = Button(frm, text='Find',  command=self.onFind).pack(side=LEFT)
        #self.openbutton = Button(frm, text='Open', command=self.onOpen).pack(side=LEFT)
        self.undobutton = Button(frm, text='Undo', command=self.onUndo).pack(side=LEFT)
        self.redobutton = Button(frm, text='Redo', command=self.onRedo).pack(side=LEFT)
        self.quitbutton = Button(frm, text="Quit", command=self.onQuit).pack(side=RIGHT)
        self.helpbutton = Button(frm, text="Help", command=self.onHelp).pack(side=RIGHT)
        self.parsebutton= Button(frm, text="Parse", command=self.onParse).pack(side=LEFT)
        #self.tempbutton = Button(frm, text='Templates', command=self.onTemp).pack(side=LEFT)
        self.runbutton = Button(frm, image=self.img, command=self.onRun).pack(side=LEFT)
        self.st = ScrolledText(parent=self.root, file=file)
        # fam=0 size=1, weight=2, bg=3
        with open("prefs.json", 'r') as obj:
            pref = json.load(obj)
            self.fontfam   = pref[0]
            self.fontsize  = pref[1]
            self.fontweight= pref[2]
            self.bg = pref[3]
        self.st.text.config(font=(self.fontfam, self.fontsize, self.fontweight), bg=self.bg)
        
        self.typesoffiles = [("All Files", "*"),
                             ("Text Files", ".txt"),
                             ("HTML Document (.html)", ".html"),
                             ("HTML Document (.htm)", ".htm"),
                             ("Cascading Style Sheet", ".css"),
                             ("JavaScript Program", ".js"),
                             ("Java Applet", ".java"),
                             ("CSV", ".csv"),
                             ("JSON", ".json"),
                             ("PHP", ".php"),
                             ("XML", ".xml")]
        
        self.filenameused = ""
        with open("templates.json") as fobj:
            self.templates = json.load(fobj)
        self.makemenu()
        with open("codebits.json") as fobj:
                self.codebits = json.load(fobj)      
        self.filenameused = ""
        if file != None:
            self.filenameused = file
        with open("help.json") as fobj2:
            self.helpdict = json.load(fobj2)
        self.st.text.edit_modified(False)



    def onSaveAs(self, sequence=None):
        try:
            self.filenameused = asksaveasfilename(title='Save', filetypes=self.typesoffiles)
            if self.filenameused:
                alltext = self.st.gettext()                      # first through last
                open(self.filenameused, 'w').write(alltext)
                self.filelabel.config(text=self.filenameused)
                self.st.text.edit_modified(False)
        except:
            showwarning("Editor", "Saving Error")



    def onSave(self, sequence=None):
        try:
            if self.filenameused == "":
                self.filenameused = asksaveasfilename(title='Save', filetypes=self.typesoffiles)
                if self.filenameused:
                    alltext = self.st.gettext()                      # first through last
                    open(self.filenameused, 'w').write(alltext)
                    self.filelabel.config(text=self.filenameused)
            else:
                alltext = self.st.gettext()                      # first through last
                open(self.filenameused, 'w').write(alltext)
                self.filelabel.config(text=self.filenameused)
            self.st.text.edit_modified(False)
        except:
            showwarning("Editor", "Saving Error")



    def onHelp(self, sequence=None):
        try:
            helpthing = askstring("Editor", "Help object?")
            if helpthing:
                for key, value in self.helpdict.items():
                    if helpthing.title() == key:
                        showinfo("Editor - "+key, value)
            else:
                pass
        except:
            showwarning("Editor", "Help Error")



    def onCP(self, sequence=None):
        try:
            window = Toplevel()
            window.wm_title("Color Picker")
            
            
            def doColor(something):
                red = redSlider.get()
                green = greenSlider.get()
                blue = blueSlider.get()
            
                colour = "#%02x%02x%02x" % (red, green, blue)
                canvas.config(bg=colour)
                hexText.delete(0, END)
                hexText.insert(0, colour)
            
            colorslabel = Label(window, text="Red\n\n\n\n\nGreen\n\n\n\n\nBlue")
            
            redSlider = Scale(window, from_=0, to=255, command=doColor, orient="horizontal")
            greenSlider = Scale(window, from_=0, to=255, command=doColor, orient="horizontal")
            blueSlider = Scale(window, from_=0, to=255, command=doColor, orient="horizontal")
            
            canvas = Canvas(window, width=200, height=200)
            
            hexText = Entry(window)
            
            colorslabel.grid(row=1, column=2, rowspan=3)
            redSlider.grid(row=2, column=2)
            greenSlider.grid(row=3, column=2)
            blueSlider.grid(row=4, column=2)
            canvas.grid(row=2, column=3, columnspan=3, rowspan=3)
            hexText.grid(row=5, column=2, columnspan=3)
            
            window.mainloop()
        except:
            showwarning("Editor", "Color Picker Error")
    
    def onParse(self, sequence=None):
        try:
            text = self.st.text.get(SEL_FIRST, SEL_LAST)
            text = html.escape(text)
            self.st.text.delete(SEL_FIRST, SEL_LAST)
            self.st.text.insert(INSERT, text)
        except:
            showwarning('Editor', 'Parse error!')


    def onUnparse(self, sequence=None):
        try:
            text = self.st.text.get(SEL_FIRST, SEL_LAST)
            text = html.unescape(text)
            self.st.text.delete(SEL_FIRST, SEL_LAST)
            self.st.text.insert(INSERT, text)
        except:
            showwarning('Editor', 'Parse error!')


            
    def onNew(self, sequence=None):
        try:
            if self.st.text.edit_modified():
                self.onSave()
            self.st.text.delete(1.0, END)
            self.st.text.insert(1.0, "")
            self.st.text.mark_set(INSERT, '1.0')
            self.st.text.focus()
            self.filenameused=""
        except:
            showwarning("Editor", "Error making new page")



    def onBHTML(self):
        if self.st.text.edit_modified():
            self.onSave()
        self.st.text.delete(1.0, END)
        self.st.text.insert(1.0, self.templates[0][1])
        self.st.text.mark_set(INSERT, '1.0')
        self.st.text.focus()
        
    def onBPAGE(self):
        if self.st.text.edit_modified():
            self.onSave()
        self.st.text.delete(1.0, END)
        self.st.text.insert(1.0, self.templates[1][1])
        self.st.text.mark_set(INSERT, '1.0')
        self.st.text.focus()



    def onQuit(self, sequence=None):
        with open("prefs.json", 'w') as obj:
            #print(self.fontfam)
            json.dump([self.fontfam, self.fontsize, self.fontweight, self.bg], obj)
        if self.st.text.edit_modified():
            ans = askokcancel('Verify exit', "Web Editor has unsaved changes.\nQuit with out saving?")
            if ans:
                self.root.destroy()
        else:
            self.root.destroy()



    def onTemp(self):
        pop = Toplevel()
        self.onNew()
        for temp in self.templates:
            Button(pop, text=temp[0]).pack()



    def onUndo(self, sequence=None):                           # 2.0
        try:                                    # tk8.4 keeps undo/redo stacks
            self.st.text.edit_undo()               # exception if stacks empty
        except TclError:
            showwarning('Editor', 'Nothing to undo')
            
            
    
    def onRedo(self, sequence=None):
        try:
            self.st.text.edit_redo()
        except TclError:
            showwarning('Editor', 'Nothing to redo')    




    def onCut(self, sequence=None):
        try:
            text = self.st.text.get(SEL_FIRST, SEL_LAST)         # error if no select
            self.st.text.delete(SEL_FIRST, SEL_LAST)             # should wrap in try
            pyperclip.copy(text)
            #self.root.clipboard_clear()
            #self.root.clipboard_append(text)
        except:
            showwarning("Editor", "Cutting Error!")
    
    
    def onCopy(self, sequence=None):
        try:
            text = self.st.text.get(SEL_FIRST, SEL_LAST)
            pyperclip.copy(text)
        except:
            showwarning("Editor", "Copying Error!")



    def onPaste(self, sequence=None):
        try:
            #text = self.root.selection_get(selection='CLIPBOARD')
            text = pyperclip.paste()
            self.st.text.insert(INSERT, text)
        except:
            showwarning(title="Editor", message="Nothing to paste!")



    def onOpen(self, sequence=None):
        self.filenameused=askopenfilename(filetypes=self.typesoffiles)
        self.filelabel.config(text=self.filenameused)
        try:
            self.st.settext(file=self.filenameused)
            self.filelabel.config(text=self.filenameused)
        except:
            showwarning(title="Editor", message="Could not open File: ")



    def onFind(self, sequence=None):
        try:
            target = askstring('Editor', 'Search String?')
            if target:
                where = self.st.text.search(target, INSERT, END)  # from insert cursor
                if where:                                      # returns an index
                    pastit = where + ('+%dc' % len(target))    # index past target
                   #self.st.text.tag_remove(SEL, '1.0', END)      # remove selection
                    self.st.text.tag_add(SEL, where, pastit)      # select found target
                    self.st.text.mark_set(INSERT, pastit)         # set insert mark
                    self.st.text.see(INSERT)                      # scroll display
                    self.st.text.focus()                          # select text widget
        except:
            showwarning("Editor", "Finding Error")
                


    def onRun(self, sequence=None):
        try:
            if self.filenameused == "":
                filename = asksaveasfilename(title='Save Before Running', filetypes=self.typesoffiles)
                if filename:
                    alltext = self.st.gettext()                      # first through last
                    open(filename, 'w').write(alltext)
                    self.filenameused = filename
            else:
                alltext = self.st.gettext()                      # first through last
                open(self.filenameused, 'w').write(alltext)            
            
            webbrowser.open_new_tab(self.filenameused)
        except:
            showwarning("Editor", "Running Error")
            


    def quit2(self):
        self.fontsize = self.sizevar.get()
        self.fontweight= self.weightvar.get()
        self.st.text.config(font=(self.fontfam, self.fontsize, self.fontweight))
        self.win.destroy()
    
    def getfontprefs(self, event=None):
        index = self.fontlist.curselection()                    # on list double-click
        label = self.fontlist.get(index)                    # fetch selection text
        self.fontfam = label
        print()
    
    
    
    def onPrefs(self):
        self.win = Toplevel()
        fontspot = Frame(self.win)
        fontlabel = Label(fontspot, text="Font Preferences").pack()
        fontfrm = Frame(fontspot)
        fontelse = Frame(fontspot)
        
        
        tk = getattr(self.root, 'tk', self.root)
        fonts = tk.splitlist(tk.call("font", "families"))
                                                               # or get(ACTIVE)
        self.testfontfam = StringVar()
        sbar = Scrollbar(fontfrm)
        self.fontlist = Listbox(fontfrm, relief=SUNKEN, listvariable=self.testfontfam)
        sbar.config(command=self.fontlist.yview)                    # xlink sbar and list
        self.fontlist.config(yscrollcommand=sbar.set)               # move one moves other
        sbar.pack(side=RIGHT, fill=Y)                          # pack first=clip last
        self.fontlist.pack(side=LEFT, expand=YES, fill=BOTH)        # list clipped first
        pos = 0
        for label in fonts:                              # add to listbox
            self.fontlist.insert(pos, label)
            pos += 1
        #self.fontlist.select(self.fontfam)
       #list.config(selectmode=SINGLE, setgrid=1)
        #print(self.testfontfam)
        #self.fontlist.activate(self.testfontfam.get().index(self.fontfam))
        self.fontlist.bind('<Double-1>', self.getfontprefs)
        self.win.protocol('WM_DELETE_WINDOW', self.quit2)
        fontfrm.pack(side=LEFT)
        
        self.weightvar = StringVar()
        weight = OptionMenu(fontelse, self.weightvar, 'normal', 'bold',  'italic', 'roman')
        self.weightvar.set(self.fontweight)
        weight.pack(side=TOP)
        
        self.sizevar = IntVar()
        size = OptionMenu(fontelse, self.sizevar, 7, 8, 10, 12, 14, 16, 18, 20, 22)
        self.sizevar.set(self.fontsize)
        size.pack(side=TOP)
        
        fontelse.pack(side=RIGHT)
        
        fontspot.pack()
        
        window = Frame(self.win)
        top = Frame(window)
        slide = Frame(top)
        
        def doColor(something):
            red = redSlider.get()
            green = greenSlider.get()
            blue = blueSlider.get()
        
            colour = "#%02x%02x%02x" % (red, green, blue)
            canvas.config(bg=colour)
            hexText.delete(0, END)
            hexText.insert(0, colour)
        
        colorlabel = Label(window, text="Color Preferences")
        redSlider = Scale(slide, from_=0, to=255, command=doColor, orient="horizontal", label="Red")
        greenSlider = Scale(slide, from_=0, to=255, command=doColor, orient="horizontal", label="Green")
        blueSlider = Scale(slide, from_=0, to=255, command=doColor, orient="horizontal", label="Blue")
        
        canvas = Canvas(top, width=200, height=200)
        
        hexText = Entry(window)
        
        colorlabel.pack()
        redSlider.pack(side=TOP)
        greenSlider.pack(side=TOP)
        blueSlider.pack(side=TOP)
        slide.pack(side=LEFT)
        canvas.pack(side=RIGHT)
        top.pack(side=TOP)
        hexText.pack(side=BOTTOM)  
        
        window.pack()
    


    def onRunOpen(self):
        try:
            filename = askopenfilename(filetypes=self.typesoffiles)
            webbrowser.open_new_tab(filename)
        except:
            showwarning("Editor", "Running Error")
    
    
    def onCodebit(self, name):
        for code in self.codebits:
            #print(code)
            if code[0] == name:
                pyperclip.copy(code[1])
                #print("found")
                break
        #print("codebits", name)

    
    def makemenu(self):        
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        pulldown1 = Menu(menubar)
        pulldown1.add_command(label='New      Ctlr-n', command=self.onNew)
        self.root.bind("<Control-n>", self.onNew, add=True)
        
        pulldown1.add_command(label='Open     Ctlr-o', command=self.onOpen)
        self.root.bind("<Control-o>", self.onOpen, add=True)
        
        pulldown1.add_separator()
        
        pulldown1.add_command(label='Save      Ctlr-s',    command=self.onSave)
        self.root.bind("<Control-s>", self.onSave, add=True)
        
        pulldown1.add_command(label='Save As  Ctlr-Shift-s',    command=self.onSaveAs)
        self.root.bind("<Control-Shift-s>", self.onSaveAs, add=True)
        
        pulldown1.add_separator()
        
        pulldown1.add_command(label='Quit       Ctlr-Q',    command=self.onQuit)
        self.root.bind("<Control-q>", self.onQuit, add=True)
        
        menubar.add_cascade(label='File', underline=0, menu=pulldown1)
        
        pulldown2 = Menu(menubar)
        
        pulldown2.add_command(label='Cut     Ctlr-x', command=self.onCut)
        #self.root.bind("<Control-x>", self.onCut, add=True)
        
        pulldown2.add_command(label='Copy   Ctlr-c', command=self.onCopy)
        #self.root.bind("<Control-c>", self.onCopy, add=True)
        
        pulldown2.add_command(label='Paste  Ctlr-v', command=self.onPaste)
        #self.root.bind("<Control-v>", self.onPaste, add=True)
        
        pulldown2.add_separator()
        
        pulldown2.add_command(label='Undo   Ctlr-z', command=self.onUndo)
        self.root.bind("<Control-z>", self.onUndo, add=True)
        
        pulldown2.add_command(label='Redo   Ctrl-y', command=self.onRedo)
        self.root.bind("<Control-y>", self.onRedo, add=True)
        
        pulldown2.add_separator()
        
        pulldown2.add_command(label='Preferences', command=self.onPrefs)
        
        menubar.add_cascade(label="Edit", menu=pulldown2)
        
        pulldown3 = Menu(menubar)
        
        pulldown3.add_command(label='Color Picker    Ctlr-a', command=self.onCP)
        self.root.bind("<Control-a>", self.onCP, add=True)
        
        pulldown3.add_separator()
        
        pulldown3.add_command(label='Parse      Ctlr-o', command=self.onParse)
        self.root.bind("<Control-o>", self.onParse, add=True)
        
        pulldown3.add_command(label='Unparse      Ctlr-p', command=self.onUnparse)
        self.root.bind("<Control-p>", self.onUnparse, add=True)
        
        pulldown3.add_separator()
        
        interpull1 = Menu(pulldown3)
        interpull1.add_command(label='Basic HTML', command=self.onBHTML)
        interpull1.add_command(label='Basic Page', command=self.onBPAGE)
        pulldown3.add_cascade(label="Templates", menu=interpull1)
        
        interpull2 = Menu(pulldown3)
        interpull2.add_command(label='Unordered List', command=lambda: self.onCodebit("unordered list"))
        interpull2.add_command(label='Ordered List', command=lambda:self.onCodebit("ordered list"))
        interpull2.add_command(label='HTML5 Video', command=lambda:self.onCodebit("html5 vid"))
        interpull2.add_command(label='Image', command=lambda:self.onCodebit("image"))
        interpull2.add_command(label='Stylesheet Link', command=lambda:self.onCodebit("style link"))
        interpull2.add_command(label='Javascript', command=lambda:self.onCodebit("javascript"))
        interpull2.add_command(label='Table', command=lambda:self.onCodebit("table"))
        pulldown3.add_cascade(label="Codebits", menu=interpull2)
        
        menubar.add_cascade(label="Tools", menu=pulldown3)
        
        pulldown4 = Menu(menubar)
        
        pulldown4.add_command(label='Run    Ctlr-r', command=self.onRun)
        self.root.bind("<Control-r>", self.onRun, add=True)
        
        pulldown4.add_command(label='Run from File    Ctlr-Shift-r', command=self.onRunOpen)
        self.root.bind("<Control-Shift-r>", self.onRunOpen, add=True)
        
        menubar.add_cascade(label="Run", menu=pulldown4)
        
        menubar.add_command(label="Help", command=self.onHelp)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        file = "".join(sys.argv[1:])
    else:
        file=None
    editor = SimpleEditor(file=file)
    #editor.onCodebit("unordered list")
    #editor.onPrefs()
    #editor.onTemp()
    #editor.makemenu()
    editor.root.mainloop()
