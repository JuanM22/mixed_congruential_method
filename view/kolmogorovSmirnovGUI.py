import wx, math
import wx.grid as grid
import numpy as np
import pygame
from controller.main import Control

pygame.display.init()
resolution = pygame.display.Info()

width = resolution.current_w
height = resolution.current_h - 50

class Table(grid.Grid):
    def __init__(self, parent, rows, cols, rowsOrCols, tableHeigth):

        colSize = ((width*5)/100)  if(rowsOrCols == 'rows' or rowsOrCols == 'columns') else ((width*9.5)/100)

        grid.Grid.__init__(self, parent, size=wx.Size((cols) * (colSize + 12), (height * tableHeigth) / 100), pos=wx.Point(0, 0))

        self.CreateGrid(rows, cols)
        self.SetBackgroundColour((255,0,0))

        self.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        if(rowsOrCols == 'rows'):
            self.HideRowLabels() 
        elif(rowsOrCols == 'columns'):
            for i in range(0, rows):
                self.SetRowLabelValue(i, "Ri")
            self.HideColLabels()

        for i in range(0, cols):
            self.SetColSize(i, colSize)

class MyForm(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='Congruential Mixed Method | Kolmogorov-Smirnov Test', name = "riTable",
                          pos=wx.Point(0, 0), size = wx.Size(width, height))

        self.values = []

        mainPanel = wx.Panel(self)
        mainPanel.SetBackgroundColour((102, 255, 255))

        size = [(width * 67)/100, (height * 25) / 100]
        position = [(width * 30)/100, (height * 5) / 100]

        self.riPanel = wx.Panel(mainPanel, pos = position, size = size)
        self.riPanel.Hide()

        size = [(width * 91)/100, (height * 35) / 100]
        position = [(width * 3.5)/100, (height * 35) / 100]

        self.kolmogorovPanel = wx.Panel(mainPanel, pos = position, size = size)
        self.kolmogorovPanel.Hide()

        size = [(width * 25)/100, (height * 15) / 100]
        position = [(width * 3)/100, (height * 5) / 100]

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
        btnSend.Bind(wx.EVT_BUTTON, self.generateRandomNumbers)

    def generateRandomNumbers(self,e):
        if(len(self.riPanel.GetChildren()) > 0):
            table = self.riPanel.GetChildren()[0]
            table.Destroy()
    
        x0 = int(self.x0Input.GetLineText(0))
        a = int(self.aInput.GetLineText(0))
        c = int(self.cInput.GetLineText(0))
        m = int(self.mInput.GetLineText(0))
        control = Control()
        self.values = control.getRandomNumbers(x0,a,c,m)   ## Números aleatorios ##
        ################################################
        rows = math.ceil(len(self.values) / 8)
        table = Table(self.riPanel, rows , 8, "columns", 29)
        self.__setCellsReadonly(table, rows)

        row, col = 0 , 0
        for i in range(0,len(self.values)):
            table.SetCellValue(row,col, "{:.4f}".format(self.values[i]))
            if(col == 7):
                row +=1
                col = 0
            else:
                col+=1

        btnSend = wx.Button(self.riPanel, -1, label="Aplicar prueba de Kolmogorov-Smirnov", pos = [(8 * 82) + 4, 0])
        btnSend.Bind(wx.EVT_BUTTON, self.applyKolmogorovSmirnov)

        self.riPanel.Update()
        if(not(self.riPanel.IsShown())):
            self.riPanel.Show()
        
    
    def applyKolmogorovSmirnov(self, e):
        if(len(self.kolmogorovPanel.GetChildren()) > 0):
            table = self.kolmogorovPanel.GetChildren()[0]
            table.Destroy()

        control = Control()
        matrix = control.getKolmogorovSmirnovRes(self.values) ## Tabla solución

        table = Table(self.kolmogorovPanel, 10 , 9, "", 33.5)
        table.SetColLabelSize(50)
        self.__setCellsReadonly(table, np.shape(matrix)[0])
        ####################### HEADER ###########################
        table.SetColLabelValue(0, 'Rango o intervalo')
        table.SetColLabelValue(1, 'Significa')
        table.SetColLabelValue(2, 'Frecuencia obtenida')
        table.SetColLabelValue(3, 'Frecuencia obtenida \nacumulada')
        table.SetColLabelValue(4, 'Probabilidad obtenida \nacumulada')
        table.SetColLabelValue(5, 'Frecuencia esperada \n(n/m)')
        table.SetColLabelValue(6, 'Frecuencia esperada \nacumulada')
        table.SetColLabelValue(7, 'Probabilidad esperada \nacumulada')
        table.SetColLabelValue(8, 'Diferencia')
        ##########################################################
        #################### INTERVALS ####################
        table.SetCellValue(0,0, '[0 a 0.1)')
        table.SetCellValue(1,0, '[0.1 a 0.2)')
        table.SetCellValue(2,0, '[0.2 a 0.3)')
        table.SetCellValue(3,0, '[0.3 a 0.4)')
        table.SetCellValue(4,0, '[0.4 a 0.5)')
        table.SetCellValue(5,0, '[0.5 a 0.6)')
        table.SetCellValue(6,0, '[0.6 a 0.7)')
        table.SetCellValue(7,0, '[0.7 a 0.8)')
        table.SetCellValue(8,0, '[0.8 a 0.9)')
        table.SetCellValue(9,0, '[0.9 a 1.0)')
        ####################################################
        ############### MEANINGS COLUMN DATA ###############
        table.SetCellValue(0,1, '0 <= n < 0.1')
        table.SetCellValue(1,1, '0.1 <= n < 0.2')
        table.SetCellValue(2,1, '0.2 <= n < 0.3')
        table.SetCellValue(3,1, '0.3 <= n < 0.4')
        table.SetCellValue(4,1, '0.4 <= n < 0.5')
        table.SetCellValue(5,1, '0.5 <= n < 0.6')
        table.SetCellValue(6,1, '0.6 <= n < 0.7')
        table.SetCellValue(7,1, '0.7 <= n < 0.8')
        table.SetCellValue(8,1, '0.8 <= n < 0.9')
        table.SetCellValue(9,1, '0.9 <= n < 1.0')
        ####################################################
        ############# SETTING DATA ############
        for i in range(0, np.shape(matrix)[0]):
            for j in range(0, np.shape(matrix)[1]):
                table.SetCellValue(i,j + 2, "{:.3f}".format(matrix[i][j]))
        ####################################################
        self.kolmogorovPanel.Update()
        if(not(self.kolmogorovPanel.IsShown())):
            self.kolmogorovPanel.Show()

    def __setCellsReadonly(self, table, rowsLength):
        attr = wx.grid.GridCellAttr()
        attr.SetReadOnly(True)
        for i in range(0, rowsLength):
            table.SetRowAttr(i,attr)

def runProgram():
    app = wx.App()
    frame = MyForm().Show()
    app.MainLoop()
