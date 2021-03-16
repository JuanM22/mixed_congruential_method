import wx, math, pygame, sys
import wx.grid as grid
import wx.lib
import numpy as np
from controller.main import Control

pygame.display.init()
resolution = pygame.display.Info()

width = resolution.current_w
height = resolution.current_h - 50

mainBG = [255,178,102]
panelBackGround = [139, 148, 154]
tableLabelsBG = [0,0,204]
white = [255,255,255]
red = [255,0,0]
darkGray = [64,64,64]
black = [0,0,0]
tCellBG = [51,153,255]

class AlphaComboBox(wx.ComboBox):
    def __init__(self, parent):

        position = [(width* 53)/100, (height*4.5)/100]
        size = [(width*8)/100, (height*5)/100]
        choices = ['--Seleccione--','0.20', '0.10', '0.05', '0.02', '0.01', '0.005', '0.002', '0.001']

        wx.ComboBox.__init__(self, parent , choices = choices, size = size, pos = position)

        self.SetSelection(0)
        self.SetEditable(False)

class Table(grid.Grid):
    def __init__(self, parent, rows, cols, rowsOrCols, tableHeigth):

        colSize = ((width*5)/100) if(rowsOrCols == 'rows' or rowsOrCols == 'columns') else ((width*9.5)/100)

        grid.Grid.__init__(self, parent, name='riData', size=wx.Size((cols) * (colSize + 12), (height * tableHeigth) / 100), pos=wx.Point(0, 0))

        self.CreateGrid(rows, cols)

        self.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_DEFAULT)
        self.SetLabelBackgroundColour(tableLabelsBG)
        self.SetLabelTextColour(white)
        self.SetDefaultCellBackgroundColour(darkGray)
        self.SetDefaultCellTextColour(white)

        if(rowsOrCols == 'rows'):
            self.HideRowLabels()
        elif(rowsOrCols == 'columns'):
            for i in range(0, rows):
                self.SetRowLabelValue(i, "Ri")
            self.HideColLabels()

        for i in range(0, cols):
            self.SetColSize(i, colSize)

        self.DisableDragColSize()
        self.DisableDragRowSize()

class MainView(wx.Frame):

    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, title = title, name="riTable", pos=wx.Point(0, 0), size=wx.Size(width, height), style = wx.CAPTION)

        self.mainPanel = wx.Panel(self)
        self.mainPanel.SetBackgroundColour(mainBG)

        #### Data Panel ####
        self.size = [(width * 25)/100, (height * 28) / 100]
        self.position = [(width * 3)/100, (height * 5) / 100]
        self.__createDataPanel()
        ###############################################################################

        #### Ri Panel ####
        self.size = [(width * 67)/100, (height * 28) / 100]
        self.position = [(width * 28.5)/100, (height * 5) / 100]
        self.__createRiPanel()
        ###############################################################################
        
        #### Kolmogorov Panel ####
        self.size = [(width * 91)/100, (height * 34) / 100]
        self.position = [(width * 3.8)/100, (height * 35) / 100]
        self.__createKolmogorovPanel()
        self.__createKolmogorovTable()
        ###############################################################################

        ##### Alpha ComboBox ####
        self.alpha = AlphaComboBox(self.riPanel)
        self.position = [(width * 48.5)/100, (height * 5) / 100]
        self.alphaLabel = wx.StaticText(self.riPanel, -1, "ALPHA: ", pos = self.position)
        self.alphaLabel.SetForegroundColour(white)
        self.position = [(width * 53)/100, (height*1.5)/100]
        self.comboSelectionAlert = wx.StaticText(self.riPanel, -1, "Seleccione un valor para alpha", pos = self.position)
        self.comboSelectionAlert.SetForegroundColour(red)
        self.comboSelectionAlert.Hide()
        ###############################################################################

        #### Conclusion Panel ####
        self.size = [(width * 91)/100, (height * 10) / 100]
        self.position = [(width * 3.8)/100, (height * 70) / 100]
        self.__createConclusionPanel()
        ###############################################################################

        #### Exit Button ####
        self.position = [(width * 92)/100, (height * 1) / 100]
        self.exitBtn = wx.Button(self.mainPanel, -1, label="Salir", pos= self.position)
        self.exitBtn.Bind(wx.EVT_BUTTON, self.__exit)

        self.__inputsEditable('disabled')        

    def __createDataPanel(self):
        self.dataPanel = wx.Panel(self.mainPanel, size= self.size, pos= self.position, style = wx.BORDER_DOUBLE)
        self.dataPanel.SetBackgroundColour(panelBackGround)
        ###########################################################
        self.position = [(width * 3)/100, (height * 17.2) / 100]
        self.constraintsBox = wx.StaticText(self.dataPanel,-1, pos = self.position)
        self.constraintsBox.SetForegroundColour(red)
        self.constraintsBox.Hide()
        ###########################################################
        self.size = [(width * 25)/100, (height * 3) / 100]
        self.position = [0 ,0]
        titlePanel = wx.Panel(self.dataPanel, size= self.size, pos= self.position)
        titlePanel.SetBackgroundColour((tableLabelsBG))

        self.position = [(width * 8.5)/100, (height * 0.5) / 100]
        dataPanelTitle = wx.StaticText(titlePanel, -1, "VALORES INICIALES", pos = self.position)
        dataPanelTitle.SetForegroundColour(white)

        labels = ["X0", "a", "c", "m", "Periodo (T)"]

        self.position = [(width * 2)/100, (height * 5) / 100]

        x0Label = wx.StaticText(self.dataPanel, -1, labels[0], pos= self.position)
        x0Label.SetForegroundColour(black)

        self.position = [(width * 8.5)/100, (height * 5) / 100]

        aLabel = wx.StaticText(self.dataPanel, -1, labels[1], pos= self.position)
        aLabel.SetForegroundColour(black)

        self.position = [(width * 2.5)/100, (height * 9) / 100]

        cLabel = wx.StaticText(self.dataPanel, -1, labels[2], pos= self.position)
        cLabel.SetForegroundColour(black)

        self.position = [(width * 8)/100, (height * 9) / 100]

        mLabel = wx.StaticText(self.dataPanel, -1, labels[3], pos= self.position)
        mLabel.SetForegroundColour(black)

        self.position = [(width * 15)/100, (height * 5) / 100]

        tLabel = wx.StaticText(self.dataPanel, -1, labels[4], pos = self.position)
        mLabel.SetForegroundColour(black)
        #################################################################################

        self.position = [(width * 3.5)/100, (height * 4.5) / 100]
        size = [(width * 4)/100, (height * 3) / 100]

        self.x0Input = wx.TextCtrl(self.dataPanel, size=size, style=wx.TE_CENTER, pos= self.position)
        self.x0Input.Bind(wx.EVT_CHAR, self.__onlyNumbers)

        self.position = [(width * 9.5)/100, (height * 4.5) / 100]

        self.aInput = wx.TextCtrl(self.dataPanel, size=size, style=wx.TE_CENTER, pos = self.position)
        self.aInput.Bind(wx.EVT_CHAR, self.__onlyNumbers)

        self.position = [(width * 3.5)/100, (height * 8.5) / 100]

        self.cInput = wx.TextCtrl(self.dataPanel, size=size, style=wx.TE_CENTER,pos = self.position)
        self.cInput.Bind(wx.EVT_CHAR, self.__onlyNumbers)

        self.position = [(width * 9.5)/100, (height * 8.5) / 100]

        self.mInput = wx.TextCtrl(self.dataPanel, size=size, style=wx.TE_CENTER,pos = self.position)
        self.mInput.Bind(wx.EVT_CHAR, self.__onlyNumbers)

        self.position = [(width * 19.5)/100, (height * 4.5) / 100]

        self.tInput = wx.TextCtrl(self.dataPanel, size=size, style=wx.TE_CENTER, pos= self.position)
        self.tInput.SetEditable(False)


        ##################################################################################
        self.position = [(width * 3)/100, (height * 13) / 100]

        self.newBtn = wx.Button(self.dataPanel, -1, label="Nuevo", pos= self.position)
        self.newBtn.Bind(wx.EVT_BUTTON, self.__deleteWidgets)

        self.position = [(width * 10)/100, (height * 13) / 100]

        self.numberGeneratorBtn = wx.Button(self.dataPanel, -1, label="Generar números aleatorios", pos= self.position)
        self.numberGeneratorBtn.Bind(wx.EVT_BUTTON, self.generateRandomNumbers)
        self.numberGeneratorBtn.Disable()

    def __onlyNumbers(self, e):
        key_code = e.GetKeyCode()
        if (ord('0') <= key_code <= ord('9') or key_code == 8):
            e.Skip()
            return

    def __createRiPanel(self):
        self.riPanel = wx.Panel(self.mainPanel, pos= self.position, size= self.size, style = wx.BORDER_DOUBLE)
        self.riPanel.SetBackgroundColour(panelBackGround)
        self.riPanel.Hide()

    def __createKolmogorovPanel(self):
        self.kolmogorovPanel = wx.Panel(self.mainPanel, pos= self.position, size= self.size, style = wx.BORDER_DOUBLE)
        self.kolmogorovPanel.SetBackgroundColour(darkGray)
        self.kolmogorovPanel.Hide()
        self.kolmogorovBtn = wx.Button(self.riPanel, -1, label="Aplicar prueba de Kolmogorov-Smirnov", pos=[(width* 48.5)/100, (height* 12) / 100])

    def __createKolmogorovTable(self):
        self.kolmogorovTable = Table(self.kolmogorovPanel, 10, 9, "", 33.5)
        self.kolmogorovTable.SetColLabelSize(50)
        ####################### HEADER ###########################
        colLabels = ['Rango o intervalo','Significa','Frecuencia obtenida','Frecuencia obtenida \nacumulada', 'Probabilidad obtenida \nacumulada',
                     'Frecuencia esperada \n(n/m)','Frecuencia esperada \nacumulada','Probabilidad esperada \nacumulada', 'Diferencia (D)']

        for i in range(0, len(colLabels)):
            self.kolmogorovTable.SetColLabelValue(i, colLabels[i])

        #################### INTERVALS ####################
        rowLabels = ['[0 a 0.1)','[0.1 a 0.2)','[0.2 a 0.3)','[0.3 a 0.4)','[0.4 a 0.5)','[0.5 a 0.6)','[0.6 a 0.7)','[0.7 a 0.8)','[0.8 a 0.9)','[0.9 a 1.0)']

        for i in range(0, len(rowLabels)):
            self.kolmogorovTable.SetCellValue(i,0, rowLabels[i])

        ############### MEANINGS COLUMN DATA ###############
        meaningsColumn = ['0 <= n < 0.1','0.1 <= n < 0.2', '0.2 <= n < 0.3','0.3 <= n < 0.4','0.4 <= n < 0.5','0.5 <= n < 0.6','0.6 <= n < 0.7',
                          '0.7 <= n < 0.8','0.8 <= n < 0.9','0.9 <= n < 1.0']
        
        for i in range(0, len(meaningsColumn)):
                self.kolmogorovTable.SetCellValue(i,1, meaningsColumn[i])    

        self.__setCellsReadonly(self.kolmogorovTable, self.kolmogorovTable.GetNumberRows(), self.kolmogorovTable.GetNumberCols())

    def __createConclusionPanel(self):
        self.conclusionPanel = wx.Panel(self.mainPanel, pos= self.position, size= self.size, style = wx.BORDER_DOUBLE)
        self.conclusionPanel.SetBackgroundColour(darkGray)
        self.conclusionPanel.Hide()
        ###############################
        self.position = [(width * 0.5)/100, (height * 0.5) / 100]
        self.conclusionLabel = wx.StaticText(self.conclusionPanel, -1, "CONCLUSIÓN: ", pos = self.position)
        self.conclusionLabel.SetForegroundColour(white)
        ###############################
        self.size = [(width * 55)/100, (height * 7) / 100]
        self.position = [(width * 6.5)/100, (height * 0.5) / 100]
        self.conclusionText = wx.TextCtrl(self.conclusionPanel, size= self.size, pos= self.position)
        self.conclusionText.SetEditable(False)
        ###############################
        self.position = [(width * 63)/100, (height * 0.5) / 100]
        self.kologorovLabel = wx.StaticText(self.conclusionPanel, -1, "VALOR CRÍTICO: ", pos = self.position)
        self.kologorovLabel.SetForegroundColour(white)
        ###############################
        self.size = [(width * 10)/100, (height * 7) / 100]
        self.position = [(width * 70)/100, (height * 0.5) / 100]
        self.kolmogorovVal = wx.TextCtrl(self.conclusionPanel, size= self.size, pos= self.position)
        self.kolmogorovVal.SetEditable(False)

    def generateRandomNumbers(self, e):
        empty = ['',' ']
        
        if(not(self.x0Input.GetValue() in empty) and not(self.aInput.GetValue() in empty) and not(self.cInput.GetValue() in empty) and not(self.mInput.GetValue() in empty)):
            self.constraintsBox.Hide()

            x0 = int(self.x0Input.GetValue())
            a = int(self.aInput.GetValue())
            c = int(self.cInput.GetValue())
            m = int(self.mInput.GetValue())

            control = Control()
            constraintMessages = []
            constraintMessages = control.validateData(x0, a, c, m)
            if(len(constraintMessages) > 0):
                self.constraintsBox.SetLabelText(constraintMessages)
                self.constraintsBox.Show()
            else:
                self.__inputsEditable('disabled')
                self.numberGeneratorBtn.Disable()
                self.newBtn.Enable()
                self.constraintsBox.Hide()

                result = control.getRandomNumbers(x0, a, c, m)
                values = result.doubleValues  # Números aleatorios ##
                period = result.period  # Periodo
                self.tInput.SetValue(str(period[1] - period[0]))
                ################################################
                rows = math.ceil(len(values) / 8)
                table = Table(self.riPanel, rows, 8, "columns", 29)

                row, col = 0, 0
                for i in range(0, len(values)):
                    if(i >= period[0] and i < period[1]):
                        table.SetCellBackgroundColour(row, col, tCellBG)
                
                    table.SetCellValue(row, col, "{:.4f}".format(values[i]))
                    if(col == 7):
                        row += 1
                        col = 0
                    else:
                        col += 1

                self.kolmogorovBtn.Bind(wx.EVT_BUTTON, lambda event: self.applyKolmogorovSmirnov(e, values))
                self.__setCellsReadonly(table, rows, 8)

                self.riPanel.Validate()
                self.riPanel.Update()
                self.riPanel.Show()

        else:
            self.constraintsBox.SetLabelText('¡Error! Alguno de los campos esta vacío...')
            self.constraintsBox.Show()

    def __deleteWidgets(self, e):
        self.x0Input.SetFocus()
        self.alpha.Enable()
        self.numberGeneratorBtn.Enable()
        self.kolmogorovBtn.Enable()
        self.newBtn.Disable()
        self.__inputsEditable('enabled')

        if(self.kolmogorovPanel.IsShown()):
            self.kolmogorovPanel.Hide()

        if(len(self.riPanel.GetChildren()) > 4):
            self.riPanel.GetChildren()[4].Destroy()
            self.riPanel.Hide()
            self.conclusionPanel.Hide()
            self.alpha.SetSelection(0)
            self.__cleanDataInputs()

    def __cleanDataInputs(self):
        self.x0Input.SetValue('')
        self.aInput.SetValue('')
        self.cInput.SetValue('')
        self.tInput.SetValue('')
        self.mInput.SetValue('')

    def __inputsEditable(self, option):
        if(option == 'disabled'):
            self.x0Input.SetEditable(False)
            self.aInput.SetEditable(False)
            self.cInput.SetEditable(False)
            self.mInput.SetEditable(False)
        else:
            self.x0Input.SetEditable(True)
            self.aInput.SetEditable(True)
            self.cInput.SetEditable(True)
            self.mInput.SetEditable(True)

    def applyKolmogorovSmirnov(self, e, values):
        if(self.alpha.GetSelection()> 0):
            self.alpha.Disable()
            self.kolmogorovBtn.Disable()
            self.comboSelectionAlert.Hide()

            control = Control()
            matrix = control.getKolmogorovSmirnovRes(values)  # Tabla solución

            roundedColPositions = [0,1]
            ############# SETTING DATA ############
            for i in range(0, np.shape(matrix)[0]):
                for j in range(0, np.shape(matrix)[1]):
                    if(j in roundedColPositions):
                        self.kolmogorovTable.SetCellValue(i, j + 2, "{:.0f}".format(matrix[i][j]))
                    else:
                        self.kolmogorovTable.SetCellValue(i, j + 2, "{:.3f}".format(round(matrix[i][j],3)))
            ####################################################
            maxValue = control.getDifferenceMaxValue(matrix)

            for i in range(0,np.shape(matrix)[0]):
                if(matrix[i][np.shape(matrix)[1] - 1] == maxValue):
                    self.kolmogorovTable.SetCellBackgroundColour(i,np.shape(matrix)[1] + 1, tCellBG)

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
            self.conclusionPanel.Validate()
            self.conclusionPanel.Update()
            self.conclusionPanel.Show()
            ####################################################
            self.kolmogorovPanel.Validate()
            self.kolmogorovPanel.Update()
            self.kolmogorovPanel.Show()
    
        else:
            self.alpha.Popup()
            self.comboSelectionAlert.Show()

    def __setCellsReadonly(self, table, rows, cols):
        for i in range(0, rows):
            for j in range(0, cols):
                table.SetReadOnly(i,j, True)

    def __exit(self, e):
        sys.exit(0)

def runProgram():
    app = wx.App()
    frame = MainView(None, 'Congruential Mixed Method | Kolmogorov-Smirnov Test').Show()
    app.MainLoop()
