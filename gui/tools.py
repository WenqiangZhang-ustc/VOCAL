"""
    tools.py
    @author: Grant Mercer
    6/3/2015

"""
from Tkinter import TclError, Label, LEFT, SOLID, CENTER, Toplevel, Button, \
    StringVar
from matplotlib.backends.backend_tkagg import NavigationToolbar2

toggleContainer = []

# Allows for tool tips to be displayed just below buttons
class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipWindow = None
        self.x = self.y = 0

    # Parameter: text to display as tooltip
    def showTip(self, text):
        self.text = text
        if self.tipWindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipWindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except TclError:
            pass
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hideTip(self):
        tw = self.tipWindow
        self.tipWindow = None
        if tw:
            tw.destroy()

def createToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showTip(text)
    def leave(event):
        toolTip.hideTip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
    
# Button wrapper which simulates the toggled button as you see in the draw, magnify, etc. 
#    buttons. Interally keeps a bind map which on toggle binds the keys in the map, and 
#    unbinds them on untoggle or forced untoggle.
class ToggleableButton(Button):

    # static class container to keep track of all active and unactive buttons
    # currently living
    
    # Parameters:
    #    root        -> the root of the program, which handles the cursor
    #    master      -> the parent of the actual button 
    #    cnf         -> button forward args
    #    kw          -> button forward args
    def __init__(self, root, master=None, cnf={}, **kw):
        self.__bindMap = []         # bind map to be bound once toggled
        self.isToggled = False      # internal var to keep track of toggling
        self.__root = root          # root variable for setting the cursor
        self.__cursor = ""          # cursor private var
        self.__destructor = None    # destructor var called when untoggled
        self.__master = master
        
        Button.__init__(self, master, cnf, **kw)    # call button constructor
        self.configure(command=self.toggle)         # button command is always bound internally to toggle
        toggleContainer.append(self)         # push button to static container
        
    # Parameters: 
    #    key         -> a string which accepts a valid Tkinter key
    #    command     -> the command to be bound to string
    #    cursor      -> the cursor to be set when toggled
    #    destructor  -> a function called when untoggled
    def latch(self, key="", command=None, cursor="", destructor=None):
        # only set these variables if the user entered one
        if cursor != "" : self.__cursor = cursor
        if key != "" and command != None : self.__bindMap.append((self.__root, key, command))
        if destructor != None : self.__destructor = destructor

    # Clone to toggle, except the only functionality of unToggle is to forceably
    #    untoggle the button and set the state accordingly
    def unToggle(self):
        self.isToggled = False
        self.config(relief='raised')
        for pair in self.__bindMap:
            pair[0].unbind(pair[1])
        if self.__destructor : self.__destructor()

    # The toggle function ensures that the button is either correctly toggled, or not. The
    #    button command is bound here and additionally any functions 'latched' to a command
    #    will be binded here when toggled. Also internally ensures no two toggled buttons can
    #    exist at any one time
    def toggle(self):
        # first flip the toggle switch
        self.isToggled = not self.isToggled
        # if any buttons are currently active, untoggle them
        for s in [x for x in toggleContainer if x.isToggled == True and x is not self]:  
            s.unToggle()
            
        # else if next state it false
        if self.isToggled == False:
            self.config(relief='raised')                # raise the button, e.g. deactivated
            for pair in self.__bindMap:                 # unbind using the bindmap
                pair[0].unbind(pair[1])
            if self.__destructor : self.__destructor()  # call the pseudo 'destructor'
        # else if next state is true
        else:
            self.config(relief='sunken')                # sink the button, e.g. activate
            for pair in self.__bindMap:                 # bind using the bindmap
                pair[0].bind(pair[1], pair[2])


# Wrapper of a wrapper of a button, it's a mouthful but it useful for having 
#    additional functionality the matplotlib buttons would require. Instead
#    of placing more overhead in the ToggleableButton another class is created 
#    since the number of matplotlib functions will remain constant, while we
#    may continue creating new tools that use ToggleableButton
class ToolbarToggleableButton(Button):
    # Parameters: 
    #    root, master, cnf, kw    -> forwarded args to the ToggleableButton class
    #    func                     -> function to be called along with the invocation of Toggle
    def __init__(self, root, master=None, func=None, cnf={}, **kw):
        self.isToggled = False      # internal var to keep track of toggling
        self.__root = root          # root variable for setting the cursor
        self.__cursor = ""          # cursor private var
        self.__master = master
        self.__func = func
        
        Button.__init__(self, master, cnf, **kw)    # call button constructor
        self.configure(command=self.toggle)         # button command is always bound internally to toggle
        toggleContainer.append(self)         # push button to static container
        
    def latch(self, cursor=""):
        # only set these variables if the user entered one
        if cursor != "" : self.__cursor = cursor
        
    # Clone to toggle, except the only functionality of unToggle is to forceably
    #    untoggle the button and set the state accordingly
    def unToggle(self):
        self.isToggled = False
        self.config(relief='raised')
        if self.__func : self.__func()
        
    # Call the super classes Toggle, and execute our function as well
    def toggle(self):
        self.isToggled = not self.isToggled
        # if any buttons are currently active, untoggle them
        for s in [x for x in toggleContainer if x.isToggled == True and x is not self]:  
            s.unToggle()
        
        # first flip the toggle switch
        if self.__func : self.__func()
        # else if next state it false
        if self.isToggled == False:
            self.config(relief='raised')                # raise the button, e.g. deactivated
            self.__root.config(cursor="")
        # else if next state is true
        else:
            self.__root.config(cursor=self.__cursor)
            self.config(relief='sunken')                # sink the button, e.g. activate
# Custom toolbar derived from matplotlib.backend, since we won't be specifically displaying
#    any of their provided TkGUI, we will be creating our own GUI outside of the toolbar and
#    simply using the functions provided by NavigationToolbar2. Thus we strip the toolbar of
#    anything GUI related 
class NavigationToolbar2CALIPSO(NavigationToolbar2):
    def __init__(self, canvas, master):
        self.canvas = canvas
        self.master = master
        NavigationToolbar2.__init__(self, canvas)
        
    def _init_toolbar(self):
        self.message = StringVar(master=self.master)
        self._message_label = Label(master=self.master, textvariable=self.message)
        self._message_label.grid(row=3, column=1)

    def draw_rubberband(self, event, x0, y0, x1, y1):
        height = self.canvas.figure.bbox.height
        y0 =  height-y0
        y1 =  height-y1
        try: self.lastrect
        except AttributeError: pass
        else: self.canvas._tkcanvas.delete(self.lastrect)
        self.lastrect = self.canvas._tkcanvas.create_rectangle(x0, y0, x1, y1)
        
    def release(self, event):
        try: self.lastrect
        except AttributeError: pass
        else:
            self.canvas._tkcanvas.delete(self.lastrect)
            del self.lastrect
        
    def set_message(self, s):
        self.message.set(s)
        
    def set_cursor(self, event):
        pass
    
    def save_figure(self, *args):
        pass
    
    def configure_subplots(self):
        pass
    
    def set_active(self, ind):
        pass
    
    def update(self):
        NavigationToolbar2.update(self)

    def dynamic_update(self):
        pass
    
def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))
