import wx
import math
import wx.grid as grid
import wx.lib
import numpy as np
import pygame
from controller.main import Control

pygame.display.init()
resolution = pygame.display.Info()

width = resolution.current_w
height = resolution.current_h - 50

class AlphaComboBox(wx.ComboBox):
    def __init__(self, parent):

        position = [(width* 54)/100, (height*2.5)/100]
        size = [(width*8)/100, (height*5)/100]
        choices = ['--Seleccione--','0.20', '0.10', '0.05', '0.02', '0.01', '0.005', '0.002', '0.001']

        wx.ComboBox.__init__(self, parent , choices = choices, size = size, pos = position)

        self.SetSelection(0)

class Table(grid.Grid):
    def __init__(self, parent, rows, cols, rowsOrCols, tableHeigth):

        colSize = ((width*5)/100) if(rowsOrCols == 'rows' or rowsOrCols == 'columns') else ((width*9.5)/100)

        grid.Grid.__init__(self, parent, name='riData', size=wx.Size(
            (cols) * (colSize + 12), (height * tableHeigth) / 100), pos=wx.Point(0, 0))

        self.CreateGrid(rows, cols)
        self.SetBackgroundColour((255, 0, 0))

        self.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_NEVER)

        if(rowsOrCols == 'rows'):
            self.HideRowLabels()
        elif(rowsOrCols == 'columns'):
            for i in range(0, rows):
                self.SetRowLabelValue(i, "Ri")
            self.HideColLabels()

        for i in range(0, cols):
            self.SetColSize(i, colSize)


class MainView(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='Congruential Mixed Method | Kolmogorov-Smirnov Test', name="riTable",
                          pos=wx.Point(0, 0), size=wx.Size(width, height))

        self.mainPanel = wx.Panel(self)
        self.mainPanel.SetBackgroundColour((126,12,45))

        size = [(width * 67)/100, (height * 25) / 100]
        position = [(width * 30)/100, (height * 5) / 100]

        ##############################################################
        self.riPanel = wx.Panel(self.mainPanel, pos=position, size=size)
        self.riPanel.Hide()
        ##########################
        self.btnSend = wx.Button(self.riPanel, -1, label="Aplicar prueba de Kolmogorov-Smirnov", pos=[(8 * 82) + 4, (height* 12) / 100])
        ##########################
        self.alpha = AlphaComboBox(self.riPanel)
        ##########################
        position = [(width * 50)/100, (height * 3) / 100]
        self.alphaLabel = wx.StaticText(self.riPanel, -1, "ALPHA: ", pos = position)
        self.alphaLabel.SetForegroundColour((255, 255, 255))
        ##########################
        position = [(width * 50)/100, 0]
        self.comboSelectionAlert = wx.StaticText(self.riPanel, -1, "Seleccione un valor para alpha", pos = position)
        self.comboSelectionAlert.SetForegroundColour((255, 0, 0))
        self.comboSelectionAlert.Hide()
        ##########################
        ##############################################################
        size = [(width * 91)/100, (height * 35) / 100]
        position = [(width * 3.5)/100, (height * 35) / 100]

        self.kolmogorovPanel = wx.Panel(self.mainPanel, pos=position, size=size)
        self.kolmogorovPanel.Hide()

        size = [(width * 91)/100, (height * 15) / 100]
        position = [(width * 3.5)/100, (height * 75) / 100]

        ###############################################################################
        self.conclusionPanel = wx.Panel(self.mainPanel, pos=position, size=size)
        self.conclusionPanel.Hide()
        ###############################
        position = [(width * 0.5)/100, (height * 0.5) / 100]
        self.conclusionLabel = wx.StaticText(self.conclusionPanel, -1, "CONCLUSIÓN: ", pos = position)
        self.conclusionLabel.SetForegroundColour((255, 255, 255))
        ###############################
        size = [(width * 55)/100, (height * 14) / 100]
        position = [(width * 6.5)/100, (height * 0.5) / 100]
        self.conclusionText = wx.TextCtrl(self.conclusionPanel, size=size, pos=position)
        ###############################
        position = [(width * 63)/100, (height * 0.5) / 100]
        self.kologorovLabel = wx.StaticText(self.conclusionPanel, -1, "VALOR CRÍTICO: ", pos = position)
        self.kologorovLabel.SetForegroundColour((255, 255, 255))
        ###############################
        size = [(width * 10)/100, (height * 7) / 100]
        position = [(width * 70)/100, (height * 0.5) / 100]
        self.kolmogorovVal = wx.TextCtrl(self.conclusionPanel, size=size, pos=position)
        ###############################################################################

        size = [(width * 25)/100, (height * 15) / 100]
        position = [(width * 3)/100, (height * 5) / 100]

        dataPanel = wx.Panel(self.mainPanel, size=size, pos=position, style = wx.BORDER_DOUBLE)
        dataPanel.SetBackgroundColour((255, 255, 0))

        dataPanelTitle = wx.StaticText(dataPanel, -1, "Valores iniciales")
        dataPanelTitle.SetForegroundColour((0, 0, 0))

        labels = ["X0", "a", "c", "m", "Periodo (T)"]
        xPos, yPos = 35, 22

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

        xPos = 35
        yPos += 30

        tLabel = wx.StaticText(dataPanel, -1, labels[4], pos=[xPos, yPos])
        mLabel.SetForegroundColour((0, 0, 0))

        size = [50, 20]

        xPos, yPos = 50, 22

        self.x0Input = wx.TextCtrl(dataPanel, size=size, style=wx.TE_CENTER, pos=[xPos, yPos])
        xPos += 70
        self.aInput = wx.TextCtrl(dataPanel, size=size, style=wx.TE_CENTER, pos=[xPos, yPos])
        xPos += 70
        self.cInput = wx.TextCtrl(dataPanel, size=size, style=wx.TE_CENTER, pos=[xPos, yPos])
        xPos += 70
        self.mInput = wx.TextCtrl(dataPanel, size=size, style=wx.TE_CENTER, pos=[xPos, yPos])
        xPos = 100
        yPos = 52
        self.tInput = wx.TextCtrl(dataPanel, size=size, style=wx.TE_CENTER, pos=[xPos, yPos])

        xPos, yPos = 88, 80

        btnSend = wx.Button(dataPanel, -1, label="Generar números aleatorios", pos=[xPos, yPos])
        btnSend.Bind(wx.EVT_BUTTON, self.generateRandomNumbers)

        xPos, yPos = 0, 80
        btnSend = wx.Button(dataPanel, -1, label="Nuevo", pos=[xPos, yPos])
        btnSend.Bind(wx.EVT_BUTTON, self.__deleteWidgets)


    def generateRandomNumbers(self, e):
        x0 = int(self.x0Input.GetLineText(0))
        a = int(self.aInput.GetLineText(0))
        c = int(self.cInput.GetLineText(0))
        m = int(self.mInput.GetLineText(0))

        control = Control()
        result = control.getRandomNumbers(x0, a, c, m)
        values = result.doubleValues  # Números aleatorios ##
        period = result.period  # Periodo
        self.tInput.SetValue(str(period[1] - period[0]))
        ################################################
        rows = math.ceil(len(values) / 8)
        table = Table(self.riPanel, rows, 8, "columns", 29)
        self.__setCellsReadonly(table, rows)

        row, col = 0, 0
        for i in range(0, len(values)):
            if(i >= period[0] and i < period[1]):
                table.SetCellBackgroundColour(row, col, (125, 65, 255))
        
            table.SetCellValue(row, col, "{:.4f}".format(values[i]))
            if(col == 7):
                row += 1
                col = 0
            else:
                col += 1

        self.btnSend.Bind(wx.EVT_BUTTON, lambda event: self.applyKolmogorovSmirnov(e, values))

        self.riPanel.Validate()
        self.riPanel.Update()
        self.riPanel.Show()

    def __deleteWidgets(self, e):
        self.riPanel.Hide()
        self.kolmogorovPanel.Hide()
        self.conclusionPanel.Hide()
        self.alpha.SetSelection(0)

    def applyKolmogorovSmirnov(self, e, values):
        if(self.alpha.GetSelection()> 0):
            self.comboSelectionAlert.Hide()

            control = Control()
            matrix = control.getKolmogorovSmirnovRes(values)  # Tabla solución

            table = Table(self.kolmogorovPanel, 10, 9, "", 33.5)
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
            table.SetColLabelValue(8, 'Diferencia (D)')
            ##########################################################
            #################### INTERVALS ####################
            table.SetCellValue(0, 0, '[0 a 0.1)')
            table.SetCellValue(1, 0, '[0.1 a 0.2)')
            table.SetCellValue(2, 0, '[0.2 a 0.3)')
            table.SetCellValue(3, 0, '[0.3 a 0.4)')
            table.SetCellValue(4, 0, '[0.4 a 0.5)')
            table.SetCellValue(5, 0, '[0.5 a 0.6)')
            table.SetCellValue(6, 0, '[0.6 a 0.7)')
            table.SetCellValue(7, 0, '[0.7 a 0.8)')
            table.SetCellValue(8, 0, '[0.8 a 0.9)')
            table.SetCellValue(9, 0, '[0.9 a 1.0)')
            ####################################################
            ############### MEANINGS COLUMN DATA ###############
            table.SetCellValue(0, 1, '0 <= n < 0.1')
            table.SetCellValue(1, 1, '0.1 <= n < 0.2')
            table.SetCellValue(2, 1, '0.2 <= n < 0.3')
            table.SetCellValue(3, 1, '0.3 <= n < 0.4')
            table.SetCellValue(4, 1, '0.4 <= n < 0.5')
            table.SetCellValue(5, 1, '0.5 <= n < 0.6')
            table.SetCellValue(6, 1, '0.6 <= n < 0.7')
            table.SetCellValue(7, 1, '0.7 <= n < 0.8')
            table.SetCellValue(8, 1, '0.8 <= n < 0.9')
            table.SetCellValue(9, 1, '0.9 <= n < 1.0')
            ####################################################
            ############# SETTING DATA ############
            for i in range(0, np.shape(matrix)[0]):
                for j in range(0, np.shape(matrix)[1]):
                    table.SetCellValue(i, j + 2, "{:.3f}".format(round(matrix[i][j],3)))
            ####################################################
            maxValue = control.getDifferenceMaxValue(matrix)

            for i in range(0,np.shape(matrix)[0]):
                if(matrix[i][np.shape(matrix)[1] - 1] == maxValue):
                    table.SetCellBackgroundColour(i,np.shape(matrix)[1] + 1, (125,65,22))

            ####################################################
            alphaValue = float(self.alpha.GetValue())

            kolmogorovValue = control.getKolmogorovTableValue(alphaValue, len(values))
            self.kolmogorovVal.SetValue(str(kolmogorovValue))

            conclusion = 'Como el valor crítico es menor que el valor de D, se concluye que los' 
            conclusion += ' números del conjunto ri no siguen una distribución uniforme'
            if(maxValue < kolmogorovValue):
                conclusion = 'Como el valor crítico es mayor que el valor de D, se concluye que los' 
                conclusion += ' números del conjunto ri siguen una distribución uniforme'

            self.conclusionText.SetValue(conclusion)
            self.conclusionPanel.Show()
            ####################################################

            self.kolmogorovPanel.Validate()
            self.kolmogorovPanel.Update()
            self.kolmogorovPanel.Show()
    
        else:
            self.comboSelectionAlert.Show()
        

    def __setCellsReadonly(self, table, rowsLength):
        attr = wx.grid.GridCellAttr()
        attr.SetReadOnly(True)
        for i in range(0, rowsLength):
            table.SetRowAttr(i, attr)


def runProgram():
    app = wx.App()
    frame = MainView().Show()
    app.MainLoop()
