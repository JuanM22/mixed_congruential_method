import wx.grid as grid
import wx
import view.colors as colors

class Table(grid.Grid):
    def __init__(self, parent, rows, cols, rowsOrCols, tableHeigth, width, height):

        colSize = ((width*5)/100) if(rowsOrCols == 'rows' or rowsOrCols == 'columns') else ((width*9.5)/100)

        grid.Grid.__init__(self, parent, name='riData', size=wx.Size((cols) * (colSize + 12), (height * tableHeigth) / 100), pos=wx.Point(0, 0))

        self.CreateGrid(rows, cols)
        self.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_DEFAULT)
        self.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.SetLabelBackgroundColour(colors.tableLabelsBG)
        self.SetLabelTextColour(colors.white)
        self.SetDefaultCellBackgroundColour(colors.darkGray)
        self.SetDefaultCellTextColour(colors.white)

        for i in range(0, cols):
            self.SetColSize(i, colSize)

        if(rowsOrCols == 'columns'):
            for i in range(0, rows):
                self.SetRowLabelValue(i, "Ri")
            self.HideColLabels()

        self.DisableDragColSize()
        self.DisableDragRowSize()
        self.EnableEditing(False)