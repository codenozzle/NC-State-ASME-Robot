#!/usr/bin/python

import httplib
import base64
import StringIO
import wx

"""

	CONFIG STUFFS

"""

# Socket Client
SOCKET_CLIENT_HOST = "localhost"
SOCKET_CLIENT_PORT = 2525

# IP Camaera
CAMERA_IP = "192.168.1.104"
CAMERA_USERNAME = "admin"
CAMERA_PASSWORD = "hvyw82500"
CAMERA_SIZE_WIDTH = 620
CAMERA_SIZE_HEIGHT = 480
CAMERA_SIZE = (CAMERA_SIZE_WIDTH, CAMERA_SIZE_HEIGHT)

# HUD stuff
HUD_COLOR = wx.Color(0,255,0)

class Camera():

	def __init__( self, ip, username, password ):
		self.IP = ip
		self.Username = username
		self.Password = password
		self.Connected = False
		
	def Connect( self ):
		pass
		
	def Disconnect( self ):
		pass
		
	def Update( self ):
		pass

class DLink( Camera ):

	def __init__( self, ip, username, password ):
		Camera.__init__( self, ip, username, password )
		
	def Connect( self ):
		if self.Connected == False:
			try:
				print "Attempting to connect to camera", self.IP, self.Username, self.Password
				h = httplib.HTTP( self.IP )
				h.putrequest( "GET", "/video/mjpg.cgi" )
				h.putheader( "Authorization", "Basic %s" % base64.encodestring( "%s:%s" % (self.Username, self.Password))[:-1] )
				h.endheaders()
				errcode, ermsg, headers = h.getreply()
				self.File = h.getfile()
				print "Connected!"
				self.Connected = True
			except:
				print "Unable to connect!"
				self.Connected = False
		
	def Disconnect( self ):
		self.Connected = False
		print "Camear Disconnected!"
		
	def Update( self ):
		if self.Connected:
			s = self.File.readline() # "--video boundry--'
			s = self.File.readline() # "Content-Length: #####"
			framesize = int(s[16:])
			s = self.File.readline() # "Date: ##-##-#### ##:##:## AM IO_00000000_PT_000_000"
			s = self.File.readline() # "Content-type: image/jpeg"
			s = self.File.read( framesize ) # jpeg data
			while s[0] != chr(0xff):
				s = s[1:]
			return StringIO.StringIO(s)

"""

	CameraPanel
	
"""

class CameraPanel( wx.Panel ):

	def __init__( self, parent, camera ):
		wx.Panel.__init__( self, parent, id=wx.ID_ANY, style=wx.SIMPLE_BORDER )
		
		self.Camera = camera
		
		self.Bind( wx.EVT_PAINT, self.OnPaint )
		self.Bind( wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground )
		
		self.SetSize( CAMERA_SIZE )
		
	def OnEraseBackground( self, event ):
		pass
		
	def OnPaint( self, event ):
		
		dc = wx.BufferedPaintDC( self )
		
		# Draw the camera image
		if self.Camera.Connected:
			try:
				stream = self.Camera.Update()
				if stream != None:
					img = wx.ImageFromStream( stream )
					bmp = wx.BitmapFromImage( img )
					dc.DrawBitmap( bmp, 0, 0, True )
			except:
				pass
		
		# If camera not connected draw blank white screen
		else:
			dc.SetBrush( wx.WHITE_BRUSH )
			dc.DrawRectangle( -1, -1, CAMERA_SIZE_WIDTH, CAMERA_SIZE_HEIGHT )

		
class MWCam( wx.Frame ):

	ID_FRAME_REFRESH = wx.NewId()

	def __init__( self ):
		wx.Frame.__init__( self, None, wx.ID_ANY, "Robot Cam", style=wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER )
		
		# IP Camera
		#self.Camera = Trendnet( CAMERA_IP, CAMERA_USERNAME, CAMERA_PASSWORD )
		self.Camera = DLink( CAMERA_IP, CAMERA_USERNAME, CAMERA_PASSWORD )
		self.Camera.Connect()
		
		# Camera Panel
		self.CameraPanel = CameraPanel(self, self.Camera)
		
		# Frame timer
		self.Timer = wx.Timer( self, self.ID_FRAME_REFRESH )
		self.Timer.Start(10)
		wx.EVT_TIMER( self, self.ID_FRAME_REFRESH, self.Refresh )
		
		# Frame Sizer
		self.Sizer = None
		self.Size()
		
		# Show frame
		self.Show( True )
		
	def Size( self ):
		self.Sizer = wx.BoxSizer( wx.VERTICAL )
		self.Sizer.Add( self.CameraPanel, 1, wx.EXPAND|wx.ALL, 5)
		self.SetSizer( self.Sizer )
		self.Fit()
		
	def Refresh( self, event ):
		self.CameraPanel.Refresh()

class GUI():
        def main(self):
                app = wx.App(0)
	
                # Supress crazy erorr boxes
                wx.Log_SetActiveTarget( wx.LogStderr() )
                
                frame = MWCam()
                app.MainLoop()

# allow use as a module or standalone script
if __name__ == "__main__":
        gui = GUI()
        gui.main()

	

