'''
Author: Kyle Yang
Creation Date: 2/1/2022
Last Modified: 3/23/2022
Project Description: Shows graphs of age specific birth rate in New Zealand.
Instructions: Click on the buttons or press on the space key to switch between the graphs.
Credits: Mr. Keel and Aaditya Khurana
Updates: Added a citation and added some comments to the program.
Citation: CSV files for download: Stats NZ. (n.d.). Retrieved February 21, 2022
from https://www.stats.govt.nz/large-datasets/csv-files-for-download/
Rubric Item:
    Data is properly cited in header comment block: Line 9, Line 10
    Data is properly cleaned to prevent errors: Line 399, Line 403
    Data is properly parsed into a dictionary or 2D list: Line 394
    A dataset is pasted into a string with 3 single quotes: Line 490
    Use PlotManager & Plot classes to create 3 different plots: Line 423, Line 438, Line 452
    Select a particular plot: Line 467
    Cycle from plot to plot: Line 479
'''

from cmu_graphics import *

# classes
class PlotManager(object):
    '''
    Creates methods for the manager.
    '''
    def __init__(self, left=85, bottom=345, width=300, height=300, title='', xLabel='', yLabel=''):
        self.left = left
        self.bottom = bottom
        self.width = width
        self.height = height

        self.xRange = [ 0, 0 ]
        self.yRange = [ 0, 0 ]

        self.plots = [ ]

        self.tickDrawings = Group()
        self.drawing = Group(self.tickDrawings)
        self.drawAxes(title, xLabel, yLabel)

    def drawAxes(self, title, xLabel, yLabel):
        l, b, w, h = self.left, self.bottom, self.width, self.height
        self.title = Label(title, l + (w / 2), b - h - 10, size=14)
        self.xLabel = Label(xLabel, l + w / 2, b + 30)
        self.yLabel = Label(yLabel, l - 40, b - h / 2, rotateAngle=-90)
        self.drawing.add(
            Line(l, b - h, l, b + 5, fill='silver', lineWidth=3),
            Line(l - 5, b, l + w, b, fill='silver', lineWidth=3),
            self.title, self.xLabel, self.yLabel
            )

    def getKDecimalPlaces(self, num, k):
        num = ((num * (10 ** k)) // 1) / (10 ** k)
        if (k <= 0):
            return int(num)
        else:
            return num

    def drawTicks(self, xPositions=None, xLabels=None, yPositions=None, yLabels=None, precision=[1,1], offsetX=False, offsetY=False):
        xPosDefaults, xLabDefaults, yPosDefaults, yLabDefaults = [], [], [], []
        xLen = 11 if xLabels == None else len(xLabels)
        yLen = 11 if yLabels == None else len(yLabels)
        xOffset = 0 if offsetX == False else 0.5
        yOffset = 0 if offsetY == False else 0.5

        for i in range(xLen):
            xVal = self.xRange[0] + (i + xOffset) * (self.xRange[1] - self.xRange[0]) / (xLen - 2 * (0.5 - xOffset))
            xPos, yPos = self.getPositionFromData(xVal, 0)
            xPosDefaults.append(xPos)
            xLabDefaults.append(xVal)

        for i in range(yLen-1, -1, -1):
            yVal = self.yRange[0] + (i + yOffset) * (self.yRange[1] - self.yRange[0]) / (yLen - 2 * (0.5 - yOffset))
            xPos, yPos = self.getPositionFromData(0, yVal)
            yPosDefaults.append(yPos)
            yLabDefaults.append(yVal)

        if (xPositions == None):
            xPositions = xPosDefaults
        if (xLabels == None):
            xLabels = xLabDefaults
        if (yPositions == None):
            yPositions = yPosDefaults
        if (yLabels == None):
            yLabels = yLabDefaults

        l, b = self.left, self.bottom
        self.tickDrawings.clear()

        for ind in range(len(xPositions)):
            xPos = xPositions[ind]
            xLab = xLabels[ind]
            if (isinstance(xLab, int) or isinstance(xLab, float)):
                xLab = self.getKDecimalPlaces(xLab, precision[0])
            self.tickDrawings.add(
                Line(xPos, b - 3, xPos, b + 3, fill='silver'),
                Label(xLab, xPos, b + 5, rotateAngle=-20, align='top'),
                )

        for ind in range(len(yPositions)):
            yPos = yPositions[ind]
            yLab = yLabels[ind]
            if (isinstance(yLab, int) or isinstance(yLab, float)):
                yLab = self.getKDecimalPlaces(yLab, precision[1])
            self.tickDrawings.add(
                Line(l - 3, yPos, l + 3, yPos, fill='silver'),
                Label(yLab, l - 7, yPos, align='right'),
                )

    def getPositionFromData(self, dataXVal, dataYVal):
        xMin, xMax = self.xRange[0], self.xRange[1]
        yMin, yMax = self.yRange[0], self.yRange[1]

        xPos = self.left + ((dataXVal - xMin) * self.width) / (xMax - xMin)
        yPos = self.bottom - ((dataYVal - yMin) * self.height) / (yMax - yMin)
        return xPos, yPos

    def getDataFromPosition(self, xPos, yPos):
        xMin, xMax = self.xRange[0], self.xRange[1]
        yMin, yMax = self.yRange[0], self.yRange[1]

        dataXVal = ((xPos - self.left) * (xMax - xMin)) / self.width + xMin
        dataYVal = ((self.bottom - yPos) * (yMax - yMin)) / self.height + yMin
        return dataXVal, dataYVal

    def updateRanges(self, xMin=None, xMax=None, yMin=None, yMax=None):
        if (xMin != None):
            self.xRange[0] = xMin
        if (xMax != None):
            self.xRange[1] = xMax
        if (yMin != None):
            self.yRange[0] = yMin
        if (yMax != None):
            self.yRange[1] = yMax

        for plot in self.plots:
            plot.updateDrawing()
        self.drawTicks()

    def removePlot(self, plot):
        if (plot not in self.plots):
            print('Plot does not exist')
            return
        self.plots.remove(plot)
        plot.drawing.visible = False

    def createPlot(self, xData, yData, plotType, color, resizeToNewPlot):
        if (len(xData) != len(yData)):
            print('Data lists were not the same length. Cannot plot!')
            return
        if ((isinstance(color, list) == True) and (len(color) != len(xData))):
            print('Color list and data were not the same length. Using default color!')
            color = 'black'

        newPlot = Plot(self, plotType, xData, yData)

        if (resizeToNewPlot == True):
            self.updateRanges(xMin=newPlot.xRange[0], xMax=newPlot.xRange[1],
                            yMin=newPlot.yRange[0], yMax=newPlot.yRange[1])

        newPlot.draw(color=color)
        self.plots.append(newPlot)
        self.drawing.toFront()
        return newPlot

    def plotPoints(self, xData, yData, color='black', resizeToNewPlot=True):
        return self.createPlot(xData, yData, 'scatter', color, resizeToNewPlot)

    def plotLines(self, xData, yData, color='black', resizeToNewPlot=True):
        return self.createPlot(xData, yData, 'line', color, resizeToNewPlot)

    def plotHorizontalBars(self, xData, yPositions=None, color='black', resizeToNewPlot=True):
        if (yPositions == None):
            yPositions = [ ]
            numBars = len(xData)
            top = self.bottom - self.height
            for i in range(numBars):
                yPositions.append(top + (i + 0.5) * (self.height / numBars))

        return self.createPlot(xData, yPositions, 'horiz bar', color, resizeToNewPlot)

    def plotVerticalBars(self, yData, xPositions=None, color='black', resizeToNewPlot=True):
        if (xPositions == None):
            xPositions = [ ]
            numBars = len(yData)
            for i in range(numBars):
                xPositions.append(self.left + (i + 0.5) * (self.width / numBars))

        return self.createPlot(xPositions, yData, 'vert bar', color, resizeToNewPlot)
    
    def updateLabels(self, title, xLabel, yLabel):
        # Updates the labels for the plot.
        self.drawing.remove(self.title)
        self.drawing.remove(self.xLabel)
        self.drawing.remove(self.yLabel)
        l, b, w, h = self.left, self.bottom, self.width, self.height
        self.title = Label(title, l + (w / 2), b - h - 20, size=14)
        self.xLabel = Label(xLabel, l + w / 2, b + 30)
        self.yLabel = Label(yLabel, l - 40, b - h / 2, rotateAngle=-90)
        self.drawing.add(self.title, self.xLabel, self.yLabel)

class Plot(object):
    '''
    Creates methods for the plot.
    '''
    def __init__(self, manager, plotType, xData, yData):
        self.manager = manager
        self.plotType = plotType

        self.xData = xData
        self.yData = yData

        self.getDataRanges()
        self.drawing = Group()

    def getDataRanges(self):
        # Used in Graph.updateRanges()
        self.xRange = [ 10 ** 10, -10 ** 10 ]
        self.yRange = [ 10 ** 10, -10 ** 10 ]

        for xVal in self.xData:
            if (xVal < self.xRange[0]):
                self.xRange[0] = xVal
            if (xVal > self.xRange[1]):
                self.xRange[1] = xVal
        for yVal in self.yData:
            if (yVal < self.yRange[0]):
                self.yRange[0] = yVal
            if (yVal > self.yRange[1]):
                self.yRange[1] = yVal

        if (self.xData == [ ]):
            self.xRange = [ 0, 1 ]
        if (self.yData == [ ]):
            self.yRange = [ 0, 1 ]

    def getDatapointColor(self, index):
        if (isinstance(self.color, list) == True):
            if (index < len(self.color)):
                color = self.color[index]
            else:
                color = 'black'
        else:
            color = self.color
        return color

    def updateColor(self, newColor):
        self.color = newColor
        for ind in range(len(self.drawing.children)):
            shape = self.drawing.children[ind]
            shape.fill = self.getDatapointColor(ind)

    def updateData(self, newXData=None, newYData=None, resizeRanges=False):
        if (newXData != None):
            self.xData = newXData
        elif (self.plotType == 'vert bar'):
            newXData = [ ]
            numBars = len(newYData)
            for i in range(numBars):
                newXData.append(self.manager.left + (i + 0.5) * (self.manager.width / numBars))
            self.xData = newXData
        if (newYData != None):
            self.yData = newYData
        elif (self.plotType == 'horiz bar'):
            newYData = [ ]
            numBars = len(newXData)
            top = self.manager.bottom - self.manager.height
            for i in range(numBars):
                newYData.append(top + (i + 0.5) * (self.manager.height / numBars))
            self.yData = newYData
        if (len(newXData) != len(newYData)):
            print('Data lists were not the same length. Cannot plot!')
            return
        if (len(newXData) == 0):
            return

        self.getDataRanges()
        if (resizeRanges == True):
            self.manager.updateRanges(xMin=self.xRange[0], xMax=self.xRange[1],
                                    yMin=self.yRange[0], yMax=self.yRange[1])

        prevXVal, prevYVal = newXData[0], newYData[0]
        for ind in range(len(newXData)):
            xVal, yVal = newXData[ind], newYData[ind]
            if (ind < len(self.drawing.children)):
                shape = self.drawing.children[ind]
                if (self.plotType == 'scatter'):
                    shape.datapoint = [ xVal, yVal ]
                elif (self.plotType =='line'):
                    shape.datapoint = [ [ prevXVal, prevYVal ], [ xVal, yVal ] ]
                elif (self.plotType == 'horiz bar'):
                    shape.datapoint = [ xVal, yVal ]
                elif (self.plotType == 'vert bar'):
                    shape.datapoint = [ xVal, yVal ]
                self.updateDatapointShape(shape)
            else:
                color = self.getDatapointColor(ind)
                self.drawDatapoint(xVal, yVal, prevXVal, prevYVal, color)

            prevXVal, prevYVal = xVal, yVal

        if (len(newXData) < len(self.drawing.children)):
            for i in range(ind, len(self.drawing.children)):
                shape = self.drawing.children[i]
                self.drawing.remove(shape)

    def updateDatapointShape(self, shape):
        if (self.plotType == 'scatter'):
            xVal, yVal = shape.datapoint
            newXPos, newYPos = self.manager.getPositionFromData(xVal, yVal)
            shape.centerX, shape.centerY = newXPos, newYPos
        elif (self.plotType =='line'):
            pt1, pt2 = shape.datapoint
            shape.x1, shape.y1 = self.manager.getPositionFromData(pt1[0], pt1[1])
            shape.x2, shape.y2 = self.manager.getPositionFromData(pt2[0], pt2[1])
        elif (self.plotType == 'horiz bar'):
            xVal, yVal = shape.datapoint
            shape.x2, y = self.manager.getPositionFromData(xVal, yVal)
            shape.centerY = yVal
        elif (self.plotType == 'vert bar'):
            xVal, yVal = shape.datapoint
            x, shape.y2 = self.manager.getPositionFromData(0, yVal)
            shape.centerX = xVal

    def updateDrawing(self):
        for shape in self.drawing:
            self.updateDatapointShape(shape)

    def drawDatapoint(self, xVal, yVal, prevXVal, prevYVal, color):
        graphX, graphY = self.manager.getPositionFromData(xVal, yVal)
        if (self.plotType == 'scatter'):
            shape = Circle(graphX, graphY, 5, fill=color, opacity=40)
            shape.datapoint = [ xVal, yVal ]
        elif (self.plotType == 'line'):
            prevGraphX, prevGraphY = self.manager.getPositionFromData(prevXVal, prevYVal)
            shape = Line(prevGraphX, prevGraphY, graphX, graphY, fill=color)
            shape.datapoint = [ [ prevXVal, prevYVal ], [ xVal, yVal ] ]
            prevXVal = xVal
            prevYVal = yVal
        elif (self.plotType == 'horiz bar'):
            height = self.manager.height / (len(self.xData) * 1.5)
            shape = Line(self.manager.left, yVal, graphX, yVal, fill=color, lineWidth=height)
            shape.datapoint = [ xVal, yVal ]
        elif (self.plotType == 'vert bar'):
            width = self.manager.width / (len(self.yData) + 1)
            shape = Line(xVal, self.manager.bottom, xVal, graphY, fill=color, lineWidth=width)
            shape.datapoint = [ xVal, yVal ]
        else:
            print('Invalid plot type!')

        self.drawing.add(shape)
        return prevXVal, prevYVal

    def draw(self, color):
        self.color = color
        if (len(self.xData) == 0):
            return

        prevXVal = self.xData[0]
        prevYVal = self.yData[0]
        for index in range(len(self.xData)):
            xVal = self.xData[index]
            yVal = self.yData[index]
            color = self.getDatapointColor(index)
            prevXVal, prevYVal = self.drawDatapoint(xVal, yVal, prevXVal, prevYVal, color)

manager = PlotManager(left=100,bottom=300,width=200,height=200,
                    title="Birth Rate In New Zealand",
                    xLabel="Period",
                    yLabel="Births Per 1000 Women")

# objects
lineGraph = Rect(50,350,80,30)
lineGraphLabel = Label('Line Graph',90,365,fill='white')

barGraph = Rect(150,350,80,30)
barGraphLabel = Label('Bar Graph',190,365,fill='white')

histogram = Rect(250,350,80,30)
histogramLabel = Label('Histogram',290,365,fill='white')

# groups
legend = Group()

# lists
app.colors = ['red','orange','yellow','green','blue','indigo','violet','black']

# dictionaries
app.data = {}

def main():
    # Calls other functions.
    parseData()
    drawLegend()
    drawLineGraph()

def parseData():
    # Turns the csv into a dictionary with lists in it.
    lines = app.csv.split('\n')
    for lineString in lines:
        line = lineString.split(',')
        if line[0] != 'Period':
            app.data[line[1].replace('–','-')] = []
    for lineString in lines:
        line = lineString.split(',')
        if line[0] != 'Period':
            app.data[line[1].replace('–','-')].append([int(line[0]),float(line[2])])

def drawLegend():
    # Draws the legend for the plot.
    legend.add(Label("Mother's Age",200,30,size=10))
    index=0
    for age in app.data:
        legend.add(Label(age,50+40*index,50,size=8),Circle(50+40*index,60,5,fill=app.colors[index]))
        index+=1

def getXAndYData(age):
    # Gets the x and y data for the plot.
    xData = []
    yData = []
    for point in app.data[age]:
        xData.append(point[0])
        yData.append(point[1])
    return xData, yData

def drawLineGraph():
    # Draws the line graph using the plotLines method from the manager.
    lineGraph.border='gold'
    barGraph.border=None
    histogram.border=None
    legend.visible=True
    index = 0
    for age in app.data:
        xData, yData = getXAndYData(age)
        app.plot = manager.plotLines(xData,yData,color=app.colors[index])
        index += 1
    manager.updateRanges(yMax=150)
    manager.drawTicks(xLabels=[2005,2008,2011,2014,2017,2020],precision=[0,0])
    manager.updateLabels("Birth Rate In New Zealand","Period","Births Per 1000 Women")

def drawBarGraph():
    # Draws the bar graph using the plotVerticalBars method from the manager.
    barGraph.border='gold'
    lineGraph.border=None
    histogram.border=None
    legend.visible=True
    yData = []
    for age in app.data:
        yData.append(app.data[age][-1][-1])
    app.plot = manager.plotVerticalBars(yData,color=app.colors)
    manager.updateRanges(yMax=150)
    manager.drawTicks(xLabels=[],precision=[0,0])
    manager.updateLabels("New Zealand Birth Rate In 2020","","Births Per 1000 Women")

def drawHistogram():
    # Draws the histogram using the plotVerticalBars method from the manager.
    histogram.border='gold'
    lineGraph.border=None
    barGraph.border=None
    legend.visible=False
    yData = []
    for i in range(len(app.data['45 and over'])):
        yData.append(app.data['45 and over'][i][1])
    app.plot = manager.plotVerticalBars(yData,color=app.colors*2)
    manager.updateRanges(yMin=0.5,yMax=1)
    manager.drawTicks(xLabels=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],yLabels=[1.0,0.9,0.8,0.7,0.6,0.5],precision=[0,1])
    manager.updateLabels("New Zealand Birth Rate For Mothers Ages 45 And Older","Years Since 2005","Births Per 1000 Women")

def onMousePress(mouseX,mouseY):
    # This function is called when you left click the screen. Click on the button to switch between the graphs.
    if lineGraph.hits(mouseX,mouseY):
        manager.removePlot(app.plot)
        drawLineGraph()
    if barGraph.hits(mouseX,mouseY):
        manager.removePlot(app.plot)
        drawBarGraph()
    if histogram.hits(mouseX,mouseY):
        manager.removePlot(app.plot)
        drawHistogram()

def onKeyPress(key):
    # This function is called when you press the space key. Press the space key to switch between the graphs.
    if key == 'space':
        manager.removePlot(app.plot)
        if lineGraph.border == 'gold':
            drawBarGraph()
        elif barGraph.border == 'gold':
            drawHistogram()
        elif histogram.border == 'gold':
            drawLineGraph()

app.csv = '''Period,Mothers_Age,Age_specific_birth_rate
2005,Under 15,0.2
2005,15–19,27.2
2005,20–24,67.6
2005,25–29,104.9
2005,30–34,117.1
2005,35–39,62.3
2005,40–44,12
2005,45 and over,0.6
2006,Under 15,0.2
2006,15–19,28.1
2006,20–24,70.9
2006,25–29,105.2
2006,30–34,119.3
2006,35–39,63.7
2006,40–44,12.3
2006,45 and over,0.7
2007,Under 15,0.3
2007,15–19,31.4
2007,20–24,76.5
2007,25–29,114.2
2007,30–34,126.9
2007,35–39,70.3
2007,40–44,13.7
2007,45 and over,0.7
2008,Under 15,0.3
2008,15–19,33.1
2008,20–24,79.5
2008,25–29,113.4
2008,30–34,125.3
2008,35–39,71.6
2008,40–44,13.9
2008,45 and over,0.7
2009,Under 15,0.2
2009,15–19,29.6
2009,20–24,78.7
2009,25–29,109.7
2009,30–34,123.1
2009,35–39,69.4
2009,40–44,14.4
2009,45 and over,0.6
2010,Under 15,0.2
2010,15–19,29
2010,20–24,78.9
2010,25–29,112.7
2010,30–34,126.5
2010,35–39,70.7
2010,40–44,15.2
2010,45 and over,0.8
2011,Under 15,0.2
2011,15–19,25.8
2011,20–24,74.4
2011,25–29,109.1
2011,30–34,122.7
2011,35–39,70.2
2011,40–44,14.6
2011,45 and over,0.8
2012,Under 15,0.1
2012,15–19,24.6
2012,20–24,73.1
2012,25–29,110.7
2012,30–34,124.4
2012,35–39,69.5
2012,40–44,15.1
2012,45 and over,0.7
2013,Under 15,0.1
2013,15–19,21.6
2013,20–24,68.5
2013,25–29,106.8
2013,30–34,118.1
2013,35–39,69.8
2013,40–44,14.6
2013,45 and over,0.9
2014,Under 15,0.2
2014,15–19,19
2014,20–24,62.4
2014,25–29,102.3
2014,30–34,118.6
2014,35–39,66.4
2014,40–44,14.2
2014,45 and over,0.7
2015,Under 15,0.2
2015,15–19,18.6
2015,20–24,64.7
2015,25–29,103.8
2015,30–34,124.1
2015,35–39,70.8
2015,40–44,14.6
2015,45 and over,1
2016,Under 15,0.1
2016,15–19,16
2016,20–24,58.9
2016,25–29,97.3
2016,30–34,118.6
2016,35–39,67.8
2016,40–44,14.3
2016,45 and over,0.8
2017,Under 15,0.1
2017,15–19,14.9
2017,20–24,57.3
2017,25–29,94.6
2017,30–34,115.1
2017,35–39,65.3
2017,40–44,14.7
2017,45 and over,0.9
2018,Under 15,0.1
2018,15–19,13.4
2018,20–24,53.2
2018,25–29,89.1
2018,30–34,109.3
2018,35–39,63.7
2018,40–44,13.9
2018,45 and over,0.9
2019,Under 15,0.1
2019,15–19,12.8
2019,20–24,52.4
2019,25–29,89
2019,30–34,110.6
2019,35–39,64.8
2019,40–44,14.7
2019,45 and over,0.9
2020,Under 15,0.1
2020,15–19,12.2
2020,20–24,48.8
2020,25–29,83.9
2020,30–34,104.1
2020,35–39,60.7
2020,40–44,13.4
2020,45 and over,0.9'''
main()

cmu_graphics.run()
