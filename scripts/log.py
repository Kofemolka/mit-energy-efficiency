import ina226_driver_aardvark as ina226
import time
import datetime
import csv
import sys

driver = ina226.ina226(i2c_driver_type = 'SBC_LINUX_SMBUS', i2c_bus_number=1)
driver.configure(avg = ina226.ina226_averages_t['INA226_AVERAGES_128'],
  busConvTime = ina226.ina226_busConvTime_t['INA226_BUS_CONV_TIME_332US'],
  shuntConvTime = ina226.ina226_shuntConvTime_t['INA226_SHUNT_CONV_TIME_332US'])
driver.calibrate(rShuntValue = 0.1, iMaxExcepted = 1)

print "Mode: "+str(hex(driver.getMode()))
print "Max Possible Current: " + str(round(driver.getMaxPossibleCurrent(), 4))

filename = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.csv")
if len(sys.argv) >= 2:
    filename = sys.argv[1] + "/" + filename
print "Writing to " + filename

now_ms = lambda: int(round(time.time() * 1000))

start_ms = now_ms()
last_reading = 0

with open(filename, mode='w') as output_file:
    output = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    output.writerow(['timestamp', 'Vb', 'Vs', 'Is', 'P', 'Ph'])

    try:                             
        while True:
            timestamp = now_ms() - start_ms             # ms from start
            Vb = round(driver.readBusVoltage(),4)       # V
            Vs = round(driver.readShuntVoltage(),4)     # V
            Is = round(driver.readShuntCurrent(),4)     # A
            P = round(driver.readBusPower(),4)          # W
            Ph = round(P * (timestamp-last_reading), 4) # Wms

            last_reading = timestamp

            output.writerow([timestamp, Vb, Vs, Is, P, Ph]);

            print str(timestamp) + ": " + str(Vb) + "\t" + str(Vs) + "\t" + str(Is) + "\t" \
                + str(P) + "\t" + str(Ph)
                    
            time.sleep(0.1)

    except KeyboardInterrupt as e:
            print '\nCTRL^C received, Terminating..'                
            driver.close()
        
    except Exception as e:
        print "There has been an exception, Find detais below:"
        print str(e)
        driver.close()