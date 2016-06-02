import wx
 
MAIN_WINDOW_DEFAULT_SIZE = (300,200)
 
class Frame(wx.Frame):
     
    def __init__(self, parent, id, title):
        style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER) # XOR to remove the resizeable border       
        wx.Frame.__init__(self, parent, id, title=title, size=MAIN_WINDOW_DEFAULT_SIZE, style=style)
        self.Center() # open in the centre of the screen
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('White') # make the background of the window white
 
        self.CreateMenuBar()
         
        # create a StatusBar and give it 2 columns
        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetFieldsCount(2)
        self.statusBar.SetStatusText('No image specified', 1)
         
 
    def CreateMenuBar(self):
        "Create a menu bar with Open, Exit items"
        menuBar = wx.MenuBar()
        # Tell our Frame about this MenuBar
        self.SetMenuBar(menuBar)
        menuFile = wx.Menu()
        menuBar.Append(menuFile, '&File')
        # NOTE on wx ids - they're used everywhere, we don't care about them
        # Used to handle events and other things
        # An id can be -1 or wx.ID_ANY, wx.NewId(), your own id
        # Get the id using object.GetId()
        fileOpenMenuItem = menuFile.Append(-1, '&Open Image', 'Open a picture')
        #print "fileOpenMenuItem.GetId()", fileOpenMenuItem.GetId()
        #self.Bind(wx.EVT_MENU, self.OnOpen, fileOpenMenuItem)
 
        # add a 'mirror' option, disable it for now
        # we add mirrorMenuItem to self so that we can reference it later
        #self.mirrorMenuItem = menuFile.Append(-1, '&Mirror Image', 'Mirror the image horizontally')
        #self.mirrorMenuItem.Enable(False) # we can't mirror an image until we've loaded one in, so start with 'mirror' disabled
        #self.Bind(wx.EVT_MENU, self.OnMirrorImage, self.mirrorMenuItem)
         
        # create a menu item for Exit and bind it to the OnExit function      
        exitMenuItem = menuFile.Append(-1, 'E&xit', 'Exit the viewer')       
        self.Bind(wx.EVT_MENU, self.OnExit, exitMenuItem)
         
        # add a Help menu with an About item
        #menuHelp = wx.Menu()
        #menuBar.Append(menuHelp, '&Help')
        #helpMenuItem = menuHelp.Append(-1, '&About', 'About screen')
        #self.Bind(wx.EVT_MENU, self.OnAbout, helpMenuItem)

    def OnExit(self, event):
        "Close the application by Destroying the object"
        self.Destroy()


class Piece:
    Pawn, Knight, Bishop, Rook, Queen, King = range(6)

class App(wx.App):
    def uploadImage(self):
        self.image = wx.Image("board.png", wx.BITMAP_TYPE_ANY, -1).Rescale(20, 20) # auto-detect file type
        self.bitmap = wx.StaticBitmap(self.frame.panel, -1, wx.BitmapFromImage(self.image))

    def OnInit(self):
        self.frame = Frame(parent=None, id=-1, title='Image Viewer')
        self.frame.Show()

        self.SetTopWindow(self.frame)

        self.uploadImage()
        return True
     
if __name__ == "__main__":      
    # make an App object, set stdout to the console so we can see errors
    app = App(redirect=False)
    app.MainLoop()