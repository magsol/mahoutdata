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
        self.speedRuns = []
        self.easyRuns = []
        self.tempoRuns = []
        self.splitDistances = []
        self.splitTimes = []
        self.numRuns = 0

        # Kick it off.
        self.parser.ParseFile(self.f)

    def close(self):
        self.f.close()

    def plotData(self):
        # First: the easy run data.
        paces1 = []
        for item in self.easyRuns:
            paces1.append(item[0] / item[1])
        y1 = np.array(paces1)
        x1 = np.arange(0, np.size(y1))
        A1 = np.vstack([x1, np.ones(len(x1))]).T
        m1, c1 = np.linalg.lstsq(A1, y1)[0]
        linreg1 = (m1 * x1) + c1
        plot.figure(0)
        plot.title('Long Runs and Races')
        plot.xlabel('Runs (earliest to most recent)')
        plot.ylabel('Average Pace (minutes)')
        plot.ylim([5, 13])
        plot.plot(y1, label = 'Garmin Data')
        plot.plot(linreg1, label = 'Linear Regression')
        plot.legend(loc = 0)
        
        # Second: tempo run data.
        paces2 = []
        for item in self.tempoRuns:
            paces2.append(item[0] / item[1])
        y2 = np.array(paces2)
        x2 = np.arange(0, np.size(y2))
        A2 = np.vstack([x2, np.ones(len(x2))]).T
        m2, c2 = np.linalg.lstsq(A2, y2)[0]
        linreg2 = (m2 * x2) + c2
        plot.figure(1)
        plot.title('Tempo Runs')
        plot.xlabel('Runs (earliest to most recent)')
        plot.ylabel('Average Pace (minutes)')
        plot.ylim([5, 13])
        plot.plot(y2, label = 'Garmin Data')
        plot.plot(linreg2, label = 'Linear Regression')
        plot.legend(loc = 0)

        # Third: speed work.
        paces3 = []
        for item in self.speedRuns:
            paces3.append(item[0] / item[1])
        y3 = np.array(paces3)
        x3 = np.arange(0, np.size(y3))
        A3 = np.vstack([x3, np.ones(len(x3))]).T
        m3, c3 = np.linalg.lstsq(A3, y3)[0]
        linreg3 = (m3 * x3) + c3
        plot.figure(2)
        plot.title('Speed Work')
        plot.xlabel('Runs (earliest to most recent)')
        plot.ylabel('Average Pace (minutes)')
        plot.ylim([5, 13])
        plot.plot(y3, label = 'Garmin Data')
        plot.plot(linreg3, label = 'Linear Regression')
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
            # Do all the interesting stuff.
            thetype = self._determineRunType()
            totaltime = np.sum(self.splitTimes)
            totaldist = np.sum(self.splitDistances)
            toadd = [totaltime / 60.0, totaldist / 1609.0]
            if thetype == 'speed':
                self.speedRuns.append(toadd)
            elif thetype == 'tempo':
                self.tempoRuns.append(toadd)
            else:
                self.easyRuns.append(toadd)

            # Clean up.
            self.isRunning = False
            self.splitDistances = []
            self.splitTimes = []

        elif name == 'TotalTimeSeconds':
            self.isTime = False
        elif name == 'DistanceMeters':
            self.isDistance = False
        elif name == 'Track':
            self.isTrack = False

    def _characterData(self, data):
        if self.isTime:
            self.splitTimes.append(float(data))
        elif self.isDistance and not self.isTrack:
            self.splitDistances.append(float(data))

    def _determineRunType(self):
        # Easier to work with NumPy arrays.
        distances = np.array(self.splitDistances)
        times = np.array(self.splitTimes)

        # Speed work: the 2nd and 4th laps should be nearly the same, but
        # very different from the 3rd lap.
        if np.size(distances) >= 5:
            second = distances[1]
            third = distances[2]
            fourth = distances[3]
            ratio1 = np.min([second, fourth]) / np.max([second, fourth])
            ratio2 = third / np.max([second, fourth])
            # Ratio1 should be very close to 1; Ratio2 should be close to 0.5
            if ratio1 - ratio2 > 0.4:
                return 'speed'

        # Tempo work: the first and last laps should be similar, and the middle
        # laps should be similar, but the two groups should be different.
        if np.size(times) >= 3:
            first = times[0]
            last = times[-1]
            middle = times[1:-1]
            # Let's say tempo pace is, on average, a half-minute faster.
            if np.mean([first, last]) - 30 > np.median(middle):
                return 'tempo'

        # Easy runs: everything else.
        return 'easy'

if __name__ == '__main__':
    analyze = ThreeRunsParser(sys.argv[1])
    analyze.close()
    analyze.plotData()
