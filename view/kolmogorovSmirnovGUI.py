import wx, math
import wx.grid as grid
import pygame
from controller.main import Control

pygame.display.init()
resolution = pygame.display.Info()

width = resolution.current_w
height = resolution.current_h - 50

class Table(grid.Grid):
    def __init__(self, parent, rows, cols, rowsOrCols):
        grid.Grid.__init__(self, parent, size=wx.Size( (cols) * 82, (resolution.current_h * 29) / 100), pos=wx.Point(0, 0))

        self.CreateGrid(rows, cols)

        for i in range(0, cols):
            self.SetColSize(i, 70)

        self.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        if(rowsOrCols == 'rows'):
            self.HideRowLabels()  # Ocula el panel de labels de las filas
        else:
            for i in range(0, rows):
                self.SetRowLabelValue(i, "Ri")
            self.HideColLabels()  # Ocula el panel de labels de las filas

        # self.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_DEFAULT)

        # self.SetColLabelValue(0, 'Rango o intervalo')
        # self.SetColLabelValue(1, 'Significa')

        # self.SetCellValue(0,0, '[0 a 0.1)')
        # self.SetCellValue(1,0, '[0.1 a 0.2)')
        # self.SetCellValue(2,0, '[0.2 a 0.3)')
        # self.SetCellValue(3,0, '[0.3 a 0.4)')
        # self.SetCellValue(4,0, '[0.4 a 0.5)')
        # self.SetCellValue(5,0, '[0.5 a 0.6)')
        # self.SetCellValue(6,0, '[0.6 a 0.7)')
        # self.SetCellValue(7,0, '[0.7 a 0.8)')
        # self.SetCellValue(8,0, '[0.8 a 0.9)')
        # self.SetCellValue(9,0, '[0.9 a 1.0)')

        # self.SetRowSize(0, 20)
        # self.SetColSize(0, 120)

        # And set grid cell contents as strings
        # self.SetCellValue(0, 0, 'wxGrid is good')

        # We can specify that some cells are read.only
        # self.SetCellValue(0, 3, 'This is read.only')
        # self.SetReadOnly(0, 3)

        # Colours can be specified for grid cell contents
        # self.SetCellValue(3, 3, 'green on grey')
        # self.SetCellTextColour(3, 3, wx.GREEN)
        # self.SetCellBackgroundColour(3, 3, wx.LIGHT_GREY)

        # We can specify the some cells will store numeric
        # values rather than strings. Here we set grid column 5
        # to hold floating point values displayed with width of 6
        # and precision of 2
        # self.SetColFormatFloat(5, 6, 2)
        # self.SetCellValue(0, 6, '3.1415')


class MyForm(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='Congruential Mixed Method | Kolmogorov-Smirnov Test', name = "riTable",
                          pos=wx.Point(0, 0), size=wx.Size(width, height), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        mainPanel = wx.Panel(self)
        mainPanel.SetBackgroundColour((102, 255, 255))

        size = [(resolution.current_w * 67)/100, (resolution.current_h * 25) / 100]
        position = [(resolution.current_w * 30)/100, (resolution.current_h * 5) / 100]

        self.riPanel = wx.Panel(mainPanel, pos = position, size = size)
        self.riPanel.Hide()

        size = [(resolution.current_w * 25)/100, (resolution.current_h * 15) / 100]
        position = [(resolution.current_w * 3)/100, (resolution.current_h * 5) / 100]

        dataPanel = wx.Panel(mainPanel, size=size, pos=position)
        dataPanel.SetBackgroundColour((255, 255, 0))

        dataPanelTitle = wx.StaticText(dataPanel, -1, "Valores iniciales")
        dataPanelTitle.SetForegroundColour((0, 0, 0))

        labels = ["X0", "a", "c", "m"]
        xPos, yPos = 35, 52

        x0Label = wx.StaticText(dataPanel, -1, labels[0], pos=[xPos, yPos])
        x0Label.SetForegroundColour((0, 0, 0))

        xPos += 75
        aLabel = wx.StaticText(dataPanel, -1, labels[1], pos=[xPos, yPos])
        aLabel.SetForegroundColour((0, 0, 0))

        xPos += 70
        cLabel = wx.StaticText(dataPanel, -1, labels[2], pos=[xPos, yPos])
        cLabel.SetForegroundColour((0, 0, 0))

        xPos += 65
        mLabel = wx.StaticText(dataPanel, -1, labels[3], pos=[xPos, yPos])
        mLabel.SetForegroundColour((0, 0, 0))

        size = [50, 20]

        xPos, yPos = 50, 50

        self.x0Input = wx.TextCtrl(dataPanel, size=size, style=wx.TE_CENTER, pos=[xPos, yPos])
        xPos += 70
        self.aInput = wx.TextCtrl(dataPanel, size=size, style=wx.TE_CENTER, pos=[xPos, yPos])
        xPos += 70
        self.cInput = wx.TextCtrl(dataPanel, size=size, style=wx.TE_CENTER, pos=[xPos, yPos])
        xPos += 70
        self.mInput = wx.TextCtrl(dataPanel, size=size, style=wx.TE_CENTER, pos=[xPos, yPos])

        xPos, yPos = 50, 80

        btnSend = wx.Button(dataPanel, -1, label="Generar números aleatorios", pos = [xPos, yPos])
        btnSend.Bind(wx.EVT_BUTTON, self.onClick)

    def onClick(self,e):
        if(len(self.riPanel.GetChildren()) > 0):
            table = self.riPanel.GetChildren()[0]
            table.Destroy()
    
        x0 = int(self.x0Input.GetLineText(0))
        a = int(self.aInput.GetLineText(0))
        c = int(self.cInput.GetLineText(0))
        m = int(self.mInput.GetLineText(0))
        control = Control()
        values = control.getRandomNumbers(x0,a,c,m)   ## Números aleatorios ##
       ################################################
        rows = math.ceil(len(values) / 8)
        table = Table(self.riPanel, rows , 8, "columns")
        row, col = 0 , 0
        for i in range(0,len(values)):
            table.SetCellValue(row,col, str(values[i]))
            if(col == 7):
                row +=1
                col = 0
            else:
                col+=1
        btnSend = wx.Button(self.riPanel, -1, label="Aplicar prueba de Kolmogorov-Smirnov", pos = [(8 * 82) + 4, 0])
        self.riPanel.Update()
        if(not(self.riPanel.IsShown())):
            self.riPanel.Show()
        

def runProgram():
    app = wx.App()
    frame = MyForm().Show()
    app.MainLoop()
