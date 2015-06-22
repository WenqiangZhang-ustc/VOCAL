'''
Created on Jun 15, 2015

@author: Grant Mercer

'''

from Tkinter import Toplevel, Entry, Button, Listbox, BOTH, Frame, \
    RIGHT, Label, RAISED, Menubutton, IntVar, Menu, END, Scrollbar, \
    VERTICAL, EXTENDED, BOTTOM, TOP, X, RIDGE, HORIZONTAL, Y, YES

from gui import Constants
from gui.db import db, dbPolygon
from gui.tools import TreeListBox, center
from statsmodels.regression.tests.test_quantile_regression import idx
#import TkTreectrl as treectrl
#import db

class dbDialog(Toplevel):
    '''
    Dialog window which prompts user for a selection of objects to import as well as
    showing a customizable list for displaying the data
    '''
    def __init__(self, root, master):
        '''
        root -> root tk widget, often Tk()
        master -> the main window, for access of polygonList
        '''
        Toplevel.__init__(self, root)

        self.__itList = list()
        self.__master = master        
        self.title("Import from existing database")
        center(self, (Constants.IMPORTWIDTH,Constants.IMPORTHEIGH)) # simple function to center window and set size
        
        self.container = Frame(self)                                # create center frame, for use of splitting window horizontally later
        self.container.pack(side=TOP, fill=BOTH, expand=True)       # place
        
        self.createTopFrame()                                       # create the top frame and pack buttons / etc. on it
        self.createBottomFrame()                                    # create the bottom frame and pack
        
    def createTopFrame(self):
        '''
        Initialize the upper frame of the window in charge of buttons
        '''
        self.topFrame = Frame(self.container)                       # create top frame
        self.topFrame.pack(side=TOP, fill=X, expand=False)
        
        self.label = Label(self.topFrame, text="Search ")           # search label 
        self.e = Entry(self.topFrame)                               # input box for searching specific attributes
        self.label.grid(row=0, column=0, padx=5, pady=10)
        self.e.grid(row=0, column=1, padx=5, pady=10)
        
        # Create our 'order by' radio button drop down menu, iterates over a list
        # of tuples and create the dropdown menu via the for loop
        self.orderSelectionButton = Menubutton(self.topFrame, text="Order by", 
                                               relief=RAISED, width=10)
        self.orderSelectionButton.menu = Menu(self.orderSelectionButton, tearoff=0)
        self.orderSelectionButton["menu"] = self.orderSelectionButton.menu
        self.orderSelectionButton.grid(row=0, column=2, padx=5, pady=10)
        self.selection = IntVar()
        labels = [("File name",Constants.FILE_NAME), ("Color",Constants.COLOR), 
                  ("Attributes",Constants.ATTRIBUTES), ("Custom",Constants.CUSTOM)]
        
        for tx in labels:
            self.orderSelectionButton.menu.add_radiobutton(label=tx[0],
                                                           variable=self.selection,
                                                           value=tx[1],
                                                           command=self.order)
            
        # custom command for filtering objects by properties
        self.filterButton = Button(self.topFrame, text="Filter", command=self.filterDialog,
                                   width=10)
        self.filterButton.grid(row=0, column=3, padx=5, pady=10)
        
        
    def createBottomFrame(self):
        '''
        Create and display database in listbox, also add lower button frame for import
        button
        '''
        self.bottomFrame = Frame(self.container)                                            # create bottom frame
        self.bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=True)          
        self.separator = Frame(self.bottomFrame, relief=RIDGE, height=2, bg="gray")         # tiny separator splitting the top and bottom frame
        self.separator.pack(side=TOP, fill=X, expand=False)
        self.bottomButtonFrame = Frame(self.bottomFrame)                                    # bottom frame for import button
        self.bottomButtonFrame.pack(side=BOTTOM, fill=X, expand=False)
        
        self.tree = TreeListBox(self.bottomFrame,
            ['name', 'attributes', 'plot', 'date', 'file'])
        self.tree.list = list()
        #self.listbox.column('#0', stretch=True)
        #self.listbox = McListBox(self.bottomFrame, ['name', 'date', 'color', 'attributes'])
        session = db.getSession()                                                           # insert the entire database
        for obj in session.query(dbPolygon).all():
            self.__itList.append(obj)
            self.tree.list.append(
                (obj.tag, obj.attributes, obj.plot, obj.time_, obj.hdf)
            )
        session.close()
        
            
        self.button = Button(self.bottomButtonFrame, text="Import", width=30,
                             command=self.importSelection)
        self.button.pack(side=BOTTOM, pady=10)
        self.tree.update()
        
    @staticmethod
    def p_selected(selected):
        print 'Selected items:', selected
        
    def order(self):
        pass
    
    def importSelection(self):
        '''
        Import selected objects from libox into program
        '''
        items = self.tree.tree.selection()
        for tag in items:
            # the tag represents the selected item, but must be converted to an index
            idx = int(tag[1:])
            print self.tree.list[idx]
            self.__master.getPolygonList().readPlot(
                readFromString=str(self.__itList[idx]))
        self.free()
            
    def filterDialog(self):
        pass
    
    def free(self):
        '''
        Free window
        '''
        self.destroy()
        
