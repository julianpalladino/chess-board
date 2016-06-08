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
  def __init__(self, k, c, (x, y), app):
    self.app = app
    self.kind = k
    self.color = c
    self.x = x
    self.y = y

  def show(self):
    route = "images/" + self.color + "_" + self.kind + ".png"
    self.image = wx.Image(route, wx.BITMAP_TYPE_ANY, -1).Rescale(60, 60) # auto-detect file type
    self.bitmap = wx.StaticBitmap(self.app.frame.panel, -1, wx.BitmapFromImage(self.image), (self.x*60+8, self.y*60+10))

    #app.UploadImage(route, (self.x*60+8, self.y*60+10))

#algToPosition converts from the algebraic notation to the matrix position
def algToPosition(pos):
  return (ord(pos[0])-97, 8-(ord(pos[1])-48))

#positionToAlg converts from the matrix position to the algebraic notation
def positionToAlg((x,y)):
  return chr(x+97) + chr(y+48)

class Board:
  def __init__(self, app):
    self.m = [[None for x in range(8)] for y in range(8)]
    self.app = app

  def Turn(self):
    return app.turnLabel.GetLabel()[0] # W if White to move, B if Black to move

  def SwitchTurns(self):
    if (self.Turn() == 'w'):
      app.turnLabel.SetLabel("black to move")
    else:
      app.turnLabel.SetLabel("white to move")

  #sets the standard starting position
  def SetStandard(self):
    # pawns
    for x in range(0, 8):
      self.SetPiece("pawn", "w", chr(x+97)+'2')
    for x in range(0, 8):
      self.SetPiece("pawn", "b", chr(x+97)+'7')

    # other pieces white
    self.SetPiece("rook", "w", 'a1')
    self.SetPiece("knight", "w", 'b1')
    self.SetPiece("bishop", "w", 'c1')
    self.SetPiece("queen", "w", 'd1')
    self.SetPiece("king", "w", 'e1')
    self.SetPiece("bishop", "w", 'f1')
    self.SetPiece("knight", "w", 'g1')
    self.SetPiece("rook", "w", 'h1')

    # other pieces black
    self.SetPiece("rook", "b", 'a8')
    self.SetPiece("knight", "b", 'b8')
    self.SetPiece("bishop", "b", 'c8')
    self.SetPiece("queen", "b", 'd8')
    self.SetPiece("king", "b", 'e8')
    self.SetPiece("bishop", "b", 'f8')
    self.SetPiece("knight", "b", 'g8')
    self.SetPiece("rook", "b", 'h8')

  def SetPiece(self, kind, color, alg):
    (x,y) = algToPosition(alg)
    p = Piece(kind, color, (x,y), self.app)
    p.show()
    self.m[x][y] = p

  def MovePiece(self, algFrom, algTo):
    (fromX, fromY) = algToPosition(algFrom)
    (toX, toY) = algToPosition(algTo)

    if (self.m[fromX][fromY].color == self.Turn()): # if the piece matches the color to move

      if self.m[toX][toY] is not None:
        self.m[toX][toY].bitmap.Destroy() # delete eaten piece
        print "Eating piece"

      self.m[toX][toY] = self.m[fromX][fromY]


      self.m[fromX][fromY].bitmap.Destroy() # delete moving piece
      self.m[toX][toY].x = toX
      self.m[toX][toY].y = toY

      self.m[toX][toY].show()

      self.m[fromX][fromY] = None

      self.SwitchTurns()

      print "Moving from " + algFrom + " to " + algTo
    else:
      print "Not your turn!"

class App(wx.App):


  def UploadImage(self, route, position=(0,0), size=60):
    self.image = wx.Image(route, wx.BITMAP_TYPE_ANY, -1).Rescale(size, size) # auto-detect file type
    self.bitmap = wx.StaticBitmap(self.frame.panel, -1, wx.BitmapFromImage(self.image), position)

  def OnEnter(self, event):
    move = self.tcMoves.GetValue()
    ### For now, only accepting the moves "AXBY" where AX is the initial position and BY is the final position
    fromPosition, toPosition = move[:2], move[2:]
    self.board.MovePiece(fromPosition, toPosition)

    self.tcMoves.SetValue("")

  def OnInit(self):
    self.frame = Frame(parent=None, id=-1, title='Dynamic chess board')
    self.frame.Show()


    self.SetTopWindow(self.frame)

    # uploads board
    self.UploadImage("images/board.png", (0,0), 500)

    # sets the standard starting position
    self.board = Board(self)
    self.board.SetStandard()

    # textbox and label
    self.tcMoves = wx.TextCtrl(self.frame.panel, style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, pos=(200, 510), size=(140, 30))
    self.turnLabel = wx.StaticText(self.frame.panel, -1, "white to move", (50, 510), style=wx.ALIGN_CENTRE)
    
    #__init__(self, parent, id=-1, label=EmptyString, pos=DefaultPosition, size=DefaultSize, style=0, name=StaticTextNameStr) 


    self.tcMoves.Bind(wx.EVT_TEXT_ENTER, self.OnEnter, self.tcMoves)
    self.tcMoves.SetFocus()



    

    return True
     
if __name__ == "__main__":      
  # make an App object, set stdout to the console so we can see errors
  app = App(redirect=False)
  app.MainLoop()

##################
  