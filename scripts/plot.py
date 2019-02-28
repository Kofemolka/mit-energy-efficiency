from csv import reader
from matplotlib import pyplot
import sys

with open(sys.argv[1], 'r') as f:
    data = list(reader(f))

    #startTime = int(data[1][0])
    T = [(int(i[0]))/1000 for i in data[1:]]    # seconds
    P = [float(i[4])*1000 for i in data[1:]]    # mW
    I = [float(i[3])*1000 for i in data[1:]]    # mA
    Ph = [float(i[5])*1000 for i in data[1:]]   # mWms

    Imax = max(I)
    Tall = T[-1] - T[0]                         # seconds
    Pavr = round(sum(P) / len(P), 2)            # mW
    Ptotal = round(sum(Ph)/(1000*3600), 2)      # mWh
    Pcon = round(Ptotal * Tall / 3600, 2)       # mWh

    pyplot.plot(T, P)
    pyplot.title('Power consumption over time (' + str(Tall) + "s).  \nMax I:" + str(Imax)\
         + "mA  Average Power: " + str(Pavr)\
         + "mW  Total Power: " + str(Ptotal) + "mWh" \
         + "  Consumption: " + str(Pcon) + "mWh")
    pyplot.xlabel('Time (sec)')
    pyplot.ylabel('Power (mW)')
    pyplot.show()