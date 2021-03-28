import wx

class AlphaComboBox(wx.ComboBox):
    def __init__(self, parent,width, height):

        position = [(width* 53)/100, (height*4.5)/100]
        size = [(width*8)/100, (height*5)/100]
        choices = ['--Seleccione--','0.20', '0.10', '0.05', '0.02', '0.01', '0.005', '0.002', '0.001']

        wx.ComboBox.__init__(self, parent , choices = choices, size = size, pos = position)

        self.SetSelection(0)
        self.SetEditable(False)