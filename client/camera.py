import httplib
import base64
import StringIO
import datetime

class Camera():

	def __init__(self, ip, username, password):
		self.IP = ip
		self.Username = username
		self.Password = password
		self.Connected = False
		
	def Connect(self):
		pass
		
	def Disconnect(self):
		pass
		
	def Update(self):
		pass

class DLink(Camera):

	def __init__(self, ip, username, password):
		Camera.__init__(self, ip, username, password)
		
	def Connect(self):
		if self.Connected == False:
			
			try:
				print "Acquiring connection: " + self.Username + "@" + self.IP
				h = httplib.HTTP(self.IP)
				h.putrequest("GET", "/video/mjpg.cgi")
				h.putheader("Authorization", "Basic %s" % base64.encodestring("%s:%s" % (self.Username, self.Password))[:-1])
				h.endheaders()
				#errcode, ermsg, headers = h.getreply()
				h.getreply()
				self.File = h.getfile()
				self.Connected = True
				print "Connection established:", datetime.datetime.now()
				print "Starting live stream...\n"
				
			except:
				print "Unable to connect"
				self.Connected = False
		
	def Disconnect(self):
		self.Connected = False
		print "Connection closed\n"
		
	def Update(self):
		if self.Connected:
			s = self.File.readline()  # "--video boundary--'
			s = self.File.readline()  # "Content-Length: #####"
			framesize = int(s[16:])
			s = self.File.readline()  # "Date: ##-##-#### ##:##:## AM IO_00000000_PT_000_000"
			s = self.File.readline()  # "Content-type: image/jpeg"
			s = self.File.read(framesize)  # jpeg data
			while s[0] != chr(0xff):
				s = s[1:]
			return StringIO.StringIO(s)

	

