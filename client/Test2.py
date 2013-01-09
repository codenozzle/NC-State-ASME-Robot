#!/usr/bin/python

# borders.py

import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):

        wx.Frame.__init__(self, parent, id, title)
        hrzbox = wx.BoxSizer(wx.VERTICAL)
        leftPanel = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        rightPanel = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)

        hrzbox.Add(leftPanel, 1, wx.EXPAND | wx.ALL, 3)
        hrzbox.Add(rightPanel, 1, wx.EXPAND | wx.ALL, 3)

        self.SetSize((800, 600))
        self.SetSizer(hrzbox)
        self.Centre()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'borders.py')
        frame.Show(True)
        return True

app = MyApp(0)
app.MainLoop()