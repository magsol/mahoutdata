import sys
import xml.parsers.expat
import matplotlib.pyplot as plot
import numpy as np
from scipy import stats

inRunningActivity = False
isDistance = False
isTime = False
isTrack = False
avg_paces = []
mileages = []
current_seconds = 0.0
current_meters = 0.0
num_runs = 0

def start_element(name, attrs):
    global inRunningActivity, isDistance, isTime, num_runs, isTrack
    if name == "Activity" and attrs['Sport'] == "Running":
        inRunningActivity = True
        num_runs += 1
    elif inRunningActivity and name == "TotalTimeSeconds":
        isTime = True
    elif inRunningActivity and name == "DistanceMeters":
        isDistance = True
    elif inRunningActivity and name == "Track":
        isTrack = True

def end_element(name):
    global inRunningActivity, isDistance, isTime, avg_paces, current_seconds, current_meters, isTrack, mileages
    if name == "Activity" and inRunningActivity:
        # Tabulate an average pace.
        minutes = current_seconds / 60.0
        miles = current_meters / 1609.0
        pace = minutes / miles
        #print '%s / %s = %s' % (minutes, miles, pace) 
        avg_paces.append(pace)
        mileages.append(miles)

        # Next!
        inRunningActivity = False
        current_seconds = 0.0
        current_meters = 0.0

    elif name == "TotalTimeSeconds":
        isTime = False
    elif name == "DistanceMeters":
        isDistance = False
    elif name == "Track":
        isTrack = False

def char_data(data):
    global isTime, isDistance, current_seconds, current_meters, isTrack
    if isTime:
        current_seconds += float(data)
    elif isDistance and not isTrack:
        current_meters += float(data)

def kde(x, y, h):
    '''
    Arguments
    =========
    x: 1D array of mileages for each run
    y: 1D array of paces for each run
    h: bandwidth

    Returns
    =======
    mhat: 1D array of smoothed race paces (for a linear regression?)
    '''
    mhat = np.zeros(np.size(x))
    for i in range(0, np.size(x)):
        the_x = x[i]
        denominator = 0.0
        numerator = 0.0
        for j in range(0, np.size(x)):
            xi = x[j]
            yi = y[j]
            k = kernel(i, j, h)
            denominator += (k * xi)
            numerator += (k * xi * yi)
        mhat[i] = numerator / denominator
    return mhat

def kernel(xi, x, h):
    '''
    Gaussian kernel.
    '''
    return (1.0 / (np.sqrt(2.0 * np.pi))) * np.exp(-((np.abs(xi - x) / h) ** 2) / 2.0)

# Set up the parser.
p = xml.parsers.expat.ParserCreate()
p.buffer_text = True
p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.CharacterDataHandler = char_data

# Do the parsing.
f = open(sys.argv[1])
p.ParseFile(f)
f.close()

# Do some calculations.
y = np.array(avg_paces)
mileages = np.array(mileages)
mhat = kde(mileages, y, 0.25)
x = np.arange(0, np.size(y))
A = np.vstack([x, np.ones(len(x))]).T
m1, c1 = np.linalg.lstsq(A, y)[0]
m2, c2 = np.linalg.lstsq(A, mhat)[0]
linreg_raw = (m1 * x) + c1
linreg_kde = (m2 * x) + c2

# All done.
plot.figure(0)
plot.title('Average Running Pace from Raw Garmin Data')
plot.xlabel('Runs (earliest to most recent)')
plot.ylabel('Average Pace (minutes)')
plot.ylim([5, 13])
plot.plot(y)

plot.figure(1)
plot.title('Kernel Smoothing, Weighted by Distance (h = 0.25)')
plot.xlabel('Runs (earliest to most recent)')
plot.ylabel('Average Pace (minutes)')
plot.ylim([5, 13])
plot.plot(mhat)

plot.figure(2)
plot.title('Linear Regression on Smoothed Paces')
plot.xlabel('Runs (earliest to most recent)')
plot.ylabel('Average Pace (minutes)')
plot.ylim([5, 13])
plot.plot(linreg_kde)

plot.figure(3)
plot.title('Linear Regression on Raw Data')
plot.xlabel('Runs (earliest to most recent)')
plot.ylabel('Average Pace (minutes)')
plot.ylim([5, 13])
plot.plot(linreg_raw)

plot.figure(4)
plot.title('Average Paces (all)')
plot.xlabel('Runs (earliest to most recent)')
plot.ylabel('Average Pace (minutes)')
plot.ylim([5, 13])
plot.plot(y, label = 'Raw Garmin Data')
#plot.plot(mhat, label = 'Kernel Smoothing')
#plot.plot(linreg_kde, label = 'Linear Regression (kernel)')
plot.plot(linreg_raw, label = 'Linear Regression (raw)')
plot.legend(loc = 1)
plot.show()
