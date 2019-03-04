from csv import reader
from matplotlib import pyplot
import numpy as np
import sys

with open(sys.argv[1], 'r') as f:
    data = list(reader(f))

    Tbegin = 1
    Tend = len(data)

    if len(sys.argv) >= 3:
         Tbegin = np.searchsorted([row[0] for row in data[1:]], int(sys.argv[2]))
    if Tbegin == 0:
         Tbegin = 1

    if len(sys.argv) >= 4:
         Tend = np.searchsorted([row[0] for row in data[1:]], int(sys.argv[3]))

    print "T=(" + str(Tbegin) + "-" + str(Tend) + ")"

    #startTime = int(data[1][0])
    T = [(int(i[0]))/1000 for i in data[Tbegin:Tend]]    # seconds
    P = [float(i[4])*1000 for i in data[Tbegin:Tend]]    # mW
    I = [float(i[3])*1000 for i in data[Tbegin:Tend]]    # mA
    Ph = [float(i[5])*1000 for i in data[Tbegin:Tend]]   # mWms

    Imax = max(I)
    Tall = T[-1] - T[0]                         # seconds
    Pavr = round(sum(P) / len(P), 2)            # mW
    Ptotal = round(sum(Ph)/(1000*3600), 2)      # mWh
    Pcon = round(Ptotal * 3600 / Tall , 2)      # mWh

    pyplot.plot(T, P)
    pyplot.title('Power consumption over time (' + str(Tall) + "s).  \nMax I:" + str(Imax)\
         + "mA  Average Power: " + str(Pavr)\
         + "mW  Total Power: " + str(Ptotal) + "mWh" \
         + "  Consumption: " + str(Pcon) + "mWh")
    pyplot.xlabel('Time (sec)')
    pyplot.ylabel('Power (mW)')
    pyplot.show()