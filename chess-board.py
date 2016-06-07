import wx
 
MAIN_WINDOW_DEFAULT_SIZE = (600,600)
 
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
    exitMenuItem = menuFile.Append(-1, 'E&xit', 'Exit')       
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
  def __init__(self, k, c, (x, y)):
    self.kind = k
    self.color = c
    self.x = x
    self.y = y

  def show(self, app):
    route = "images/" + self.color + "_" + self.kind + ".png"
    self.image = wx.Image(route, wx.BITMAP_TYPE_ANY, -1).Rescale(60, 60) # auto-detect file type
    self.bitmap = wx.StaticBitmap(app.frame.panel, -1, wx.BitmapFromImage(self.image), (self.x*60+8, self.y*60+10))

    #app.uploadImage(route, (self.x*60+8, self.y*60+10))

#algToPosition converts from the algebraic notation to the matrix position
def algToPosition(pos):
  return (ord(pos[0])-97, 8-(ord(pos[1])-48))

#positionToAlg converts from the matrix position to the algebraic notation
def positionToAlg((x,y)):
  return chr(x+97) + chr(y+48)

class Board:
  def __init__(self):
    self.m = [[None for x in range(8)] for y in range(8)]

  #sets the standard starting position
  def setStandard(self, app):
    # pawns
    for x in range(0, 8):
      self.setPiece("pawn", "white", chr(x+97)+'2', app)
    for x in range(0, 8):
      self.setPiece("pawn", "black", chr(x+97)+'7', app)

    # other pieces white
    self.setPiece("rook", "white", 'a1', app)
    self.setPiece("knight", "white", 'b1', app)
    self.setPiece("bishop", "white", 'c1', app)
    self.setPiece("queen", "white", 'd1', app)
    self.setPiece("king", "white", 'e1', app)
    self.setPiece("bishop", "white", 'f1', app)
    self.setPiece("knight", "white", 'g1', app)
    self.setPiece("rook", "white", 'h1', app)

    # other pieces black
    self.setPiece("rook", "black", 'a8', app)
    self.setPiece("knight", "black", 'b8', app)
    self.setPiece("bishop", "black", 'c8', app)
    self.setPiece("queen", "black", 'd8', app)
    self.setPiece("king", "black", 'e8', app)
    self.setPiece("bishop", "black", 'f8', app)
    self.setPiece("knight", "black", 'g8', app)
    self.setPiece("rook", "black", 'h8', app)

  def setPiece(self, kind, color, alg, app):
    (x,y) = algToPosition(alg)
    p = Piece(kind, color, (x,y))
    p.show(app)
    self.m[x][y] = p

  def movePiece(self, algFrom, algTo, app):
    (fromX, fromY) = algToPosition(algFrom)
    (toX, toY) = algToPosition(algTo)

    if self.m[toX][toY] is not None:
      self.m[toX][toY].bitmap.Destroy() # delete eaten piece
      print "Eating piece"

    self.m[toX][toY] = self.m[fromX][fromY]


    self.m[fromX][fromY].bitmap.Destroy() # delete moving piece
    self.m[toX][toY].x = toX
    self.m[toX][toY].y = toY

    self.m[toX][toY].show(app)

    self.m[fromX][fromY] = None

class App(wx.App):
  def uploadImage(self, route, position=(0,0), size=60):
    self.image = wx.Image(route, wx.BITMAP_TYPE_ANY, -1).Rescale(size, size) # auto-detect file type
    self.bitmap = wx.StaticBitmap(self.frame.panel, -1, wx.BitmapFromImage(self.image), position)

  def OnEnter(self, event):
    move = self.tcMoves.GetValue()
    ### For now, only accepting the moves "AXBY" where AX is the initial position and BY is the final position
    fromPosition, toPosition = move[:2], move[2:]
    self.board.movePiece(fromPosition, toPosition, self)


    self.tcMoves.SetValue("")
    print "Moving from " + fromPosition + " to " + toPosition

  def OnInit(self):
    self.frame = Frame(parent=None, id=-1, title='Dynamic chess board')
    self.frame.Show()


    self.SetTopWindow(self.frame)

    # uploads board
    self.uploadImage("images/board.png", (0,0), 500)

    # sets the standard starting position
    self.board = Board()
    self.board.setStandard(self)

    #self.board.movePiece(('e', 2), ('e', 4), self)

    self.tcMoves = wx.TextCtrl(self.frame.panel, style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(200, 510), size=(140, 30))

    self.tcMoves.Bind(wx.EVT_TEXT_ENTER, self.OnEnter, self.tcMoves)
    self.tcMoves.SetFocus()



    

    return True
     
if __name__ == "__main__":      
  # make an App object, set stdout to the console so we can see errors
  app = App(redirect=False)
  app.MainLoop()

##################
  