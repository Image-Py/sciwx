import wx

def make_logo(cont, obj):
    if isinstance(obj, str) and len(obj)>1:
        bmp = wx.Bitmap(obj)
    if isinstance(obj, str) and len(obj)==1:
        bmp = wx.Bitmap.FromRGBA(16, 16)
        dc = wx.BufferedDC(wx.ClientDC(cont), bmp)
        dc.SetBackground(wx.Brush((255,255,255)))
        dc.Clear()
        dc.SetTextForeground((0,0,150))
        font = dc.GetFont()
        font.SetPointSize(12)
        dc.SetFont(font)
        w, h = dc.GetTextExtent(obj)
        dc.DrawText(obj, 8-w//2, 8-h//2)
        rgb = bytes(768)
        bmp.CopyToBuffer(rgb)
        a = memoryview(rgb[::3]).tolist()
        a = bytes([255-i for i in a])
        bmp = wx.Bitmap.FromBufferAndAlpha(16, 16, rgb, a)
    img = bmp.ConvertToImage()
    img.Resize((20, 20), (2, 2))
    return img.ConvertToBitmap()

class ToolBar(wx.Panel):
    def __init__(self, parent, vertical=False):
        wx.Panel.__init__( self, parent, wx.ID_ANY,  wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sizer = wx.BoxSizer( (wx.HORIZONTAL, wx.VERTICAL)[vertical] )
        self.SetSizer( sizer )
        self.toolset = []

    def bind(self, btn, tol):
        btn.Bind( wx.EVT_LEFT_DOWN, lambda x, obj=tol: obj().start())
            
    def add_tool(self, tool, logo):
        btn = wx.BitmapButton(self, wx.ID_ANY, make_logo(self, logo), 
            wx.DefaultPosition, (32,32), wx.BU_AUTODRAW|wx.RAISED_BORDER )
        self.bind(btn, tool)
        self.GetSizer().Add(btn, 0, wx.ALL, 1)

    def add_tools(self, name, tools, fixed=True):
        if not fixed: self.toolset.append((name, []))
        for tool, logo in tools:
            btn = wx.BitmapButton(self, wx.ID_ANY, make_logo(self, logo), 
                wx.DefaultPosition, (32,32), wx.BU_AUTODRAW|wx.RAISED_BORDER )
            self.bind(btn, tool)
            self.GetSizer().Add(btn, 0, wx.ALL, 1)
            if not fixed: self.toolset[-1][1].append(btn)
        if fixed:
            line = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
            self.GetSizer().Add( line, 0, wx.ALL|wx.EXPAND, 2 )

    def active_set(self, name):
        for n, tools in self.toolset:
            print('select', name, n)
            for btn in tools:
                if n==name: btn.Show()
                if n!=name: btn.Hide()
        self.Layout()
        
    def add_pop(self, logo, default):
        self.GetSizer().AddStretchSpacer(1)
        btn = wx.BitmapButton(self, wx.ID_ANY, make_logo(self, logo), 
                wx.DefaultPosition, (32,32), wx.BU_AUTODRAW|wx.RAISED_BORDER )
        btn.Bind(wx.EVT_LEFT_DOWN, self.menu_drop)
        self.GetSizer().Add(btn, 0, wx.ALL, 1)
        self.active_set(default)

    def menu_drop(self, event):
        menu = wx.Menu()
        for name, item in self.toolset:
            item = wx.MenuItem(menu, wx.ID_ANY, name, wx.EmptyString, wx.ITEM_NORMAL )
            menu.Append(item)
            f = lambda e, name=name:self.active_set(name)
            menu.Bind(wx.EVT_MENU, f, id=item.GetId())
        self.PopupMenu( menu )
        menu.Destroy()
        
if __name__ == '__main__':
    path = 'C:/Users/54631/Documents/projects/imagepy/imagepy/tools/drop.gif'
    app = wx.App()
    frame = wx.Frame(None)
    tool = ToolBar(frame)
    tool.add_tools('A', [(None, 'A')] * 3)
    tool.add_tools('B', [(None, 'B')] * 3, False)
    tool.add_tools('C', [(None, 'C')] * 3, False)
    tool.add_pop('P', 'B')
    tool.Layout()
    frame.Fit()
    frame.Show()
    app.MainLoop()
