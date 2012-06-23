import sys
import xml.parsers.expat
import matplotlib.pyplot as plot
import numpy as np
from scipy import stats

class ThreeRunsParser:

    def __init__(self, filename):
        self.parser = xml.parsers.expat.ParserCreate()
        self.parser.buffer_text = True
        self.parser.StartElementHandler = self._startElement
        self.parser.EndElementHandler = self._endElement
        self.parser.CharacterDataHandler = self._characterData

        self.f = open(filename)

        self.isRunning = False
        self.isDistance = False
        self.isTime = False
        self.isTrack = False
        self.splits = []
        self.times = []
        self.numRuns = 0

        # Kick it off.
        self.parser.ParseFile(self.f)

    def close(self):
        self.f.close()

    def plotData(self):
        # First: post-process the run data (in case some splits are != 1mi).
        y = self._postProcess()

        # Second: plot the data.
        x = np.arange(0, np.size(y))
        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y)[0]
        linreg = (m * x) + c
        plot.figure(0)
        plot.title('Average 1mi split paces')
        plot.xlabel('1mi splits (earliest to most recent)')
        plot.ylabel('Average Pace (minutes)')
        plot.ylim([5, 13])
        plot.plot(y, label = 'Garmin Data')
        plot.plot(linreg, label = 'Linear Regression')
        plot.legend(loc = 0)
        
        # All done!
        plot.show()

    def _startElement(self, name, attrs):
        if name == 'Activity' and attrs['Sport'] == 'Running':
            self.isRunning = True
            self.numRuns += 1
        elif self.isRunning and name == 'TotalTimeSeconds':
            self.isTime = True
        elif self.isRunning and name == 'DistanceMeters':
            self.isDistance = True
        elif self.isRunning and name == 'Track':
            self.isTrack = True

    def _endElement(self, name):
        if name == 'Activity' and self.isRunning:
            # Clean up.
            self.isRunning = False
        elif name == 'TotalTimeSeconds':
            self.isTime = False
        elif name == 'DistanceMeters':
            self.isDistance = False
        elif name == 'Track':
            self.isTrack = False

    def _characterData(self, data):
        if self.isTime:
            self.times.append(float(data))
        elif self.isDistance and not self.isTrack:
            self.splits.append(float(data))

    def _postProcess(self):
        # Convert to NumPy arrays.
        self.splits = np.array(self.splits)
        self.times = np.array(self.times)
        paces = []

        # Record all the splits.
        for i in range(0, np.size(self.splits)):
            distance = self.splits[i]
            time = self.times[i]
            if distance == 0.0:
                print 'Split %s has a distance of 0' % i
                continue
            mileage = distance / 1609.0
            pace = (time / mileage) / 60
            paces.append(pace)
        return np.array(paces)

if __name__ == '__main__':
    analyze = ThreeRunsParser(sys.argv[1])
    analyze.close()
    analyze.plotData()