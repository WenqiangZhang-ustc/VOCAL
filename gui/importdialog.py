'''
Created on Jun 15, 2015

@author: Grant Mercer

'''
from Tkinter import Toplevel, Entry, Button, Listbox, BOTH, Frame, \
    RIGHT, Label, RAISED, Menubutton, IntVar, Menu, END, Scrollbar, \
    VERTICAL, EXTENDED, BOTTOM, TOP, X, RIDGE
    
from gui import Constants
from gui.db import db, dbPolygon
from gui.tools import center
#import db

class dbDialog(Toplevel):
    '''
    Dialog window which prompts user for a selection of objects to import as well as
    showing a customizable list for displaying the data
    '''
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        
        self.title("Import from existing database")
        center(self, (Constants.IMPORTWIDTH,Constants.IMPORTHEIGH))
        
        self.container = Frame(self)
        self.container.pack(side=TOP, fill=BOTH, expand=True)
        
        self.createTopFrame()
        self.createBottomFrame()
        
    def createTopFrame(self):
        # create top frame, do not expand out
        self.topFrame = Frame(self.container)
        self.topFrame.pack(side=TOP, fill=X, expand=False)
        
        # search label and entry
        self.label = Label(self.topFrame, text="Search ")
        self.label.grid(row=0, column=0, padx=5, pady=10)
        self.e = Entry(self.topFrame)
        self.e.grid(row=0, column=1, padx=5, pady=10)
        
        self.orderSelectionButton = Menubutton(self.topFrame, text="Order by", 
                                               relief=RAISED, width=10)
        self.orderSelectionButton.grid(row=0, column=2, padx=5, pady=10)
        self.orderSelectionButton.menu = Menu(self.orderSelectionButton, tearoff=0)
        self.orderSelectionButton["menu"] = self.orderSelectionButton.menu
        self.selection = IntVar()
        
        labels = [("File name",Constants.FILE_NAME), ("Color",Constants.COLOR), 
                  ("Attributes",Constants.ATTRIBUTES), ("Custom",Constants.CUSTOM)]
        
        for tx in labels:
            self.orderSelectionButton.menu.add_radiobutton(label=tx[0],
                                                           variable=self.selection,
                                                           value=tx[1],
                                                           command=self.order)
            
        self.filterButton = Button(self.topFrame, text="Filter", command=self.filterDialog,
                                   width=10)
        self.filterButton.grid(row=0, column=3, padx=5, pady=10)
        
    def createBottomFrame(self):
        self.bottomFrame = Frame(self.container)
        self.bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=True)
        self.separator = Frame(self.bottomFrame, relief=RIDGE, height=2, bg="gray")
        self.separator.pack(side=TOP, fill=X, expand=False)
        self.bottomButtonFrame = Frame(self.bottomFrame)
        self.bottomButtonFrame.pack(side=BOTTOM, fill=X, expand=False)
        
        self.listbox = Listbox(self.bottomFrame, selectmode=EXTENDED)
        self.listbox.pack(fill=BOTH, expand=True)
        
        self.scrollbar = Scrollbar(self.listbox, orient=VERTICAL)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill="y")
        
        session = db.getSession()
        for obj in session.query(dbPolygon).all():
            self.listbox.insert(END, obj)
        session.close()
            
        self.button = Button(self.bottomButtonFrame, text="Import", width=30,
                             command=self.importSelection)
        self.button.pack(side=BOTTOM, pady=10)
        
    def order(self):
        pass
    
    def importSelection(self):
        items = self.listbox.curselection()
        print items
    
    def filterDialog(self):
        pass
    
    def free(self):
        self.destroy()
        
