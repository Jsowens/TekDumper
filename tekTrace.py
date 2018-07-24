#SETUP

import visa
import numpy as np
from struct import unpack
import pylab

rm = visa.ResourceManager()
print("Available Scopes")
print(rm.list_resources())
inst = rm.open_resource(rm.list_resources()[0])
print(inst.query("*IDN"))
print("CONNECTED\n")

FILENAME = "SINGLE_TEST"
spiceExt = ".pwl"
genericExt = ".dat"
Run = 1

print("File Name: " + FILENAME + "\tRun #: " + str(Run) = "\n")

plot = 0
count = 0
TraceCount = 10
sp = 1
gf = 1
toff = 0

#Scope needs to be in normal trigger mode and running
inst.write("DAT:SOU CH1")
inst.write("DAT:STAR 1")
inst.write("DAT:STOP 10000")
inst.write("DAT:ENC RPB")

ymult = float(inst.query("WFMPRE:YMULT?"))
yzero = float(inst.query("WFMPRE:YZERO?"))
yoff = float(inst.query("WFMPRE:YOFF?"))
xincr = float(inst.query("WFMPRE:XINCR?"))

if sp:
    spice = open(FILENAME + "_" + str(Run) + spiceExt, "w")
if gf:

    gfile = open(FILENAME + "_" + str(Run) + genericExt, "w")
    gfile.write("XINCR=" + str(xincr) + "\tTRACELENGTH=" + str(int(inst.query("DAT:STOP?"))-int(inst.query("DAT:STAR?")) - 47) + "\n")

print("Files Open\nHeaders Writen")
print("START ACQ")

while count < TraceCount:
    inst.write("CURVE?")
    data = inst.read_raw()
    headerlen = 2 + int(data[1])
    header = data[:headerlen]
    ADC_wave = data[headerlen:-1]

    ADC_wave = np.array(unpack('%sB' % len(ADC_wave),ADC_wave))
    Volts = (ADC_wave - yoff) * ymult + yzero

    Time = np.arrange(0, xincr * len(Volts), xincr) + toff
    toff = Time[len(Time)-1]

    for i in range(0, len(Volts)):
        if sp:
            #SPICE
            spice.write(str(Time[i]) + "," + str(Volts[i]) + ",")
        if gf:
            #GFILE
            gfile.write(str(Volts[i]) + ",")

    gfile.write("0\n") #Adds a zero to the end of the trace

print("STOP ACQ")
spice.close()
gfile.close()
inst.close()
print("FILES & SCOPE CLOSED")
