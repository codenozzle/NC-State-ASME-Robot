import wx
from Constants import Constants
from Camera import DLink

class GUI(wx.Frame):

    ID_FRAME_REFRESH = wx.NewId()

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, Constants.APP_TITLE, style=wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER)
        
        # Add a panel so it looks the correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)

        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()

        exitMenuItem = fileMenu.Append(wx.NewId(), "Quit", "Quit")
        self.Bind(wx.EVT_MENU, self.onExit, exitMenuItem)

        menuBar.Append(fileMenu, "&Robot")
        self.SetMenuBar(menuBar)
        
        # IP Camera
        self.Camera = DLink(Constants.CAMERA_IP, Constants.CAMERA_USERNAME, Constants.CAMERA_PASSWORD)
        self.Camera.Connect()
        
        # Camera Panel
        self.CameraPanel = CameraPanel(self, self.Camera)
        
        # Frame timer
        self.Timer = wx.Timer(self, self.ID_FRAME_REFRESH)
        self.Timer.Start(1)
        wx.EVT_TIMER(self, self.ID_FRAME_REFRESH, self.Refresh)
        
        # Frame Sizer
        self.Sizer = None
        self.Size()
        
        # Show frame
        self.Show(True)
        
    def Size(self):
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.CameraPanel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.Sizer)
        self.Fit()
        
    def Refresh(self, event):
        self.CameraPanel.Refresh()
        
    def onExit(self, event):
        self.Camera.Disconnect()
        self.Close()

class CameraPanel(wx.Panel):

    # Global Variables #
    CAMERA_SIZE_WIDTH = 640
    CAMERA_SIZE_HEIGHT = 480
    
    def __init__(self, parent, camera):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, style=wx.SIMPLE_BORDER)
        
        self.Camera = camera
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        
        self.SetSize((self.CAMERA_SIZE_WIDTH, self.CAMERA_SIZE_HEIGHT))
        
    def OnEraseBackground(self, event):
        pass
        
    def OnPaint(self, event):
        
        dc = wx.BufferedPaintDC(self)
        
        # Draw the camera image
        if self.Camera.Connected:
            try:
                stream = self.Camera.Update()
                if stream != None:
                    img = wx.ImageFromStream(stream)
                    bmp = wx.BitmapFromImage(img)
                    dc.DrawBitmap(bmp, 0, 0, True)
            except:
                pass
        
        # If camera is not connected draw blank white screen
        else:
            dc.SetBrush(wx.RED_BRUSH)
            dc.DrawRectangle(-1, -1, self.CAMERA_SIZE_WIDTH, self.CAMERA_SIZE_HEIGHT)
            

def main():
    app = wx.App(redirect=False)
    GUI()
    app.MainLoop()

if __name__ == "__main__":
    main()
