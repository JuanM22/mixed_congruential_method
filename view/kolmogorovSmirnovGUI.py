import wx, math, pygame, sys
import wx.lib
import numpy as np
from controller.main import Control
from view.tableUI import Table
from view.alphaBox import AlphaComboBox
import view.colors as colors

pygame.display.init()
resolution = pygame.display.Info()

width = resolution.current_w
height = resolution.current_h - 50

class MainView(wx.Frame):

    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, title = title, name="riTable", pos=wx.Point(0, 0), size=wx.Size(width, height), style = wx.CAPTION)

        self.labelFont = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        self.mainPanel = wx.Panel(self)
        self.mainPanel.SetBackgroundColour(colors.mainBG)

        self.kolmogorovDPos = []
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
        self.alpha = AlphaComboBox(self.riPanel, width, height)
        self.position = [(width * 48.5)/100, (height * 5) / 100]
        self.alphaLabel = wx.StaticText(self.riPanel, -1, "ALPHA: ", pos = self.position)
        self.alphaLabel.SetForegroundColour(colors.white)
        self.alphaLabel.SetFont(self.labelFont)
        self.position = [(width * 53)/100, (height*1.5)/100]
        self.riSelectionAlert = wx.StaticText(self.riPanel, -1, pos = self.position)
        self.riSelectionAlert.SetForegroundColour(colors.red)
        self.riSelectionAlert.Hide()
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
        self.dataPanel.SetBackgroundColour(colors.panelBackGround)
        ###########################################################
        self.position = [(width * 3)/100, (height * 17.2) / 100]
        self.constraintsBox = wx.StaticText(self.dataPanel,-1, pos = self.position)
        self.constraintsBox.SetForegroundColour(colors.red)
        self.constraintsBox.Hide()
        ###########################################################
        self.size = [(width * 25)/100, (height * 3) / 100]
        self.position = [0 ,0]
        titlePanel = wx.Panel(self.dataPanel, size= self.size, pos= self.position)
        titlePanel.SetBackgroundColour((colors.tableLabelsBG))

        self.position = [(width * 8.2)/100, (height * 0.5) / 100]
        dataPanelTitle = wx.StaticText(titlePanel, -1, "VALORES INICIALES", pos = self.position)
        dataPanelTitle.SetForegroundColour(colors.white)
        dataPanelTitle.SetFont(self.labelFont)

        labels = ["X0", "a", "c", "m", "Periodo (T)"]

        self.position = [(width * 2)/100, (height * 5) / 100]

        x0Label = wx.StaticText(self.dataPanel, -1, labels[0], pos= self.position)
        x0Label.SetForegroundColour(colors.black)
        x0Label.SetFont(self.labelFont)
        
        self.position = [(width * 8.5)/100, (height * 5) / 100]

        aLabel = wx.StaticText(self.dataPanel, -1, labels[1], pos= self.position)
        aLabel.SetForegroundColour(colors.black)
        aLabel.SetFont(self.labelFont)

        self.position = [(width * 2.5)/100, (height * 9) / 100]

        cLabel = wx.StaticText(self.dataPanel, -1, labels[2], pos= self.position)
        cLabel.SetForegroundColour(colors.black)
        cLabel.SetFont(self.labelFont)

        self.position = [(width * 8)/100, (height * 9) / 100]

        mLabel = wx.StaticText(self.dataPanel, -1, labels[3], pos= self.position)
        mLabel.SetForegroundColour(colors.black)
        mLabel.SetFont(self.labelFont)

        self.position = [(width * 14.5)/100, (height * 5) / 100]

        tLabel = wx.StaticText(self.dataPanel, -1, labels[4], pos = self.position)
        tLabel.SetForegroundColour(colors.black)
        tLabel.SetFont(self.labelFont)
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
        ##################################################################################

    def __onlyNumbers(self, e):
        key_code = e.GetKeyCode()
        if (ord('0') <= key_code <= ord('9') or key_code == 8):
            e.Skip()
            return

    def __createRiPanel(self):
        self.riPanel = wx.Panel(self.mainPanel, pos= self.position, size= self.size, style = wx.BORDER_DOUBLE)
        self.riPanel.SetBackgroundColour(colors.panelBackGround)
        #########################################
        self.position = [(width* 50.8)/100, (height* 10) / 100]
        nLabel = wx.StaticText(self.riPanel, -1, 'n: ',pos = self.position)
        nLabel.SetForegroundColour(colors.white)
        nLabel.SetFont(self.labelFont)
        #########################################
        self.position = [(width* 53)/100, (height * 9.5) / 100]
        self.nInput = wx.TextCtrl(self.riPanel, size=[(width * 4)/100, (height * 3) / 100], style=wx.TE_CENTER, pos= self.position)
        self.nInput.Bind(wx.EVT_CHAR, self.__onlyNumbers)
        #########################################
        self.position = [(width* 48.5)/100, (height* 15) / 100]
        self.kolmogorovBtn = wx.Button(self.riPanel, -1, label="Aplicar prueba de Kolmogorov-Smirnov", pos= self.position)
        self.riPanel.Hide()

    def __createKolmogorovPanel(self):
        self.kolmogorovPanel = wx.Panel(self.mainPanel, pos= self.position, size= self.size, style = wx.BORDER_DOUBLE)
        self.kolmogorovPanel.SetBackgroundColour(colors.darkGray)
        self.kolmogorovPanel.Hide()        

    def __createKolmogorovTable(self):
        self.kolmogorovTable = Table(self.kolmogorovPanel, 10, 9, "", 33.5, width, height)
        self.kolmogorovTable.SetColLabelSize(50)
        ####################### HEADER ###########################
        colLabels = ['Rango o intervalo','Significa','Frecuencia obtenida','Frecuencia obtenida \nacumulada', 
                     'Probabilidad obtenida \nacumulada', 'Frecuencia esperada \n(n/N° Intervalos)',
                     'Frecuencia esperada \nacumulada','Probabilidad esperada \nacumulada', 'Diferencia (D)']

        for i in range(0, len(colLabels)):
            self.kolmogorovTable.SetColLabelValue(i, colLabels[i])

        #################### INTERVALS ####################
        rowLabels = ['[ 0 a 0.1 )','[ 0.1 a 0.2 )','[ 0.2 a 0.3 )','[ 0.3 a 0.4 )','[ 0.4 a 0.5 )','[ 0.5 a 0.6 )',
                     '[ 0.6 a 0.7 )','[ 0.7 a 0.8 )','[ 0.8 a 0.9 )','[ 0.9 a 1.0 )']

        for i in range(0, len(rowLabels)):
            self.kolmogorovTable.SetCellValue(i,0, rowLabels[i])

        ############### MEANINGS COLUMN DATA ###############
        meaningsColumn = ['0 <= n < 0.1','0.1 <= n < 0.2', '0.2 <= n < 0.3','0.3 <= n < 0.4','0.4 <= n < 0.5',
                          '0.5 <= n < 0.6','0.6 <= n < 0.7', '0.7 <= n < 0.8','0.8 <= n < 0.9','0.9 <= n < 1.0']
        
        for i in range(0, len(meaningsColumn)):
                self.kolmogorovTable.SetCellValue(i,1, meaningsColumn[i])    

    def __createConclusionPanel(self):
        self.conclusionPanel = wx.Panel(self.mainPanel, pos= self.position, size= self.size, style = wx.BORDER_DOUBLE)
        self.conclusionPanel.SetBackgroundColour(colors.darkGray)
        self.conclusionPanel.Hide()
        ###############################
        self.position = [(width * 0.5)/100, (height * 3.3) / 100]
        conclusionLabel = wx.StaticText(self.conclusionPanel, -1, "CONCLUSIÓN: ", pos = self.position)
        conclusionLabel.SetForegroundColour(colors.white)
        conclusionLabel.SetFont(self.labelFont)
        ###############################
        self.size = [(width * 55)/100, (height * 7) / 100]
        self.position = [(width * 6.5)/100, (height * 1) / 100]
        self.conclusionText = wx.TextCtrl(self.conclusionPanel, size= self.size, pos= self.position)
        self.conclusionText.SetEditable(False)
        ###############################
        self.position = [(width * 63)/100, (height * 3.3) / 100]
        kologorovLabel = wx.StaticText(self.conclusionPanel, -1, "VALOR CRÍTICO: ", pos = self.position)
        kologorovLabel.SetForegroundColour(colors.white)
        kologorovLabel.SetFont(self.labelFont)
        ###############################
        self.size = [(width * 10)/100, (height * 7) / 100]
        self.position = [(width * 70)/100, (height * 1) / 100]
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

            if(m <= 2500000):

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
                    table = Table(self.riPanel, rows, 8, "columns", 29, width, height)
                    row, col = 0, 0
                    focusIndex = 0
                    for i in range(0, len(values)):
                        if(i >= period[0] and i < period[1]):
                            if(values[i] == values[period[0]] and focusIndex==0):
                                focusIndex = row
                            table.SetCellBackgroundColour(row, col, colors.tCellBG)
                    
                        table.SetCellValue(row, col, "{:.4f}".format(values[i]))
                        if(col == 7):
                            row += 1
                            col = 0
                        else:
                            col += 1

                    table.GoToCell(focusIndex,0)
                    self.kolmogorovBtn.Bind(wx.EVT_BUTTON, lambda event: self.applyKolmogorovSmirnov(e, values, period))
                    self.riPanel.Validate()
                    self.riPanel.Update()
                    self.riPanel.Show()
            else:
                self.constraintsBox.SetLabelText('El valor de m no puede ser superior a\n2.5 millones (2500000) !!!')
                self.constraintsBox.Show()    
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
        self.riSelectionAlert.Hide()

        if(self.kolmogorovPanel.IsShown()):
            self.kolmogorovPanel.Hide()

        if(len(self.riPanel.GetChildren()) > 6):
            self.riPanel.GetChildren()[6].Destroy()
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
        self.nInput.SetValue('')

    def __inputsEditable(self, option):
        if(option == 'disabled'):
            self.x0Input.SetEditable(False)
            self.aInput.SetEditable(False)
            self.cInput.SetEditable(False)
            self.mInput.SetEditable(False)
            self.nInput.SetEditable(True)
        else:
            self.x0Input.SetEditable(True)
            self.aInput.SetEditable(True)
            self.cInput.SetEditable(True)
            self.mInput.SetEditable(True)
            self.nInput.SetEditable(False)

    def applyKolmogorovSmirnov(self, e, values, period):
        empty = ['',' ']
        n = int(self.nInput.GetValue()) if (not(self.nInput.GetValue() in empty)) else 0
        if(n <= len(values)):
            if(self.alpha.GetSelection()> 0):

                if(len(self.kolmogorovDPos) > 0):
                    self.kolmogorovTable.SetCellBackgroundColour(self.kolmogorovDPos[0], self.kolmogorovDPos[1], colors.darkGray)

                self.nInput.SetEditable(False)
                self.alpha.Disable()
                self.kolmogorovBtn.Disable()
                self.riSelectionAlert.Hide()

                control = Control()
                values = values[period[0]:period[1]] if(n == 0) else values[period[0]: (period[0] + n)]
                matrix = control.getKolmogorovSmirnovRes(values)  # Tabla solución

                roundedColPositions = [0,1]
                formater = ""
                ############# SETTING DATA ############
                for i in range(0, np.shape(matrix)[0]):
                    for j in range(0, np.shape(matrix)[1]):
                        if(j in roundedColPositions):
                            formater = "{:.0f}"
                        else:
                            formater = "{:.4f}"
                        self.kolmogorovTable.SetCellValue(i, j + 2, formater.format(matrix[i][j]))
                
                ####################################################
                maxValue = control.getDifferenceMaxValue(matrix)
                maxValuePos = self.__getMaxValuePos(matrix, maxValue)
                self.kolmogorovDPos = [maxValuePos, self.kolmogorovTable.GetNumberCols()-1]
                self.kolmogorovTable.SetCellBackgroundColour(self.kolmogorovDPos[0],self.kolmogorovDPos[1], colors.tCellBG)
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
                self.riSelectionAlert.SetLabel("Seleccione un valor para alpha")
                self.riSelectionAlert.Show()
        else:
            self.riSelectionAlert.SetLabel("n debe ser menor o igual que m")
            self.riSelectionAlert.Show()

    def __getMaxValuePos(self, matrix, maxValue):
        for i in range(0,np.shape(matrix)[0]):
            if(matrix[i][np.shape(matrix)[1] - 1] == maxValue):
                return i

    def __exit(self, e):
        sys.exit(0)

def runProgram():
    app = wx.App()
    frame = MainView(None, 'Congruential Mixed Method | Kolmogorov-Smirnov Test').Show()
    app.MainLoop()
