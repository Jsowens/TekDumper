#SETUP

import visa
import numpy as np
import time
from struct import unpack
import pylab

#FUNCTIONS
def getCurve(channel,yoff,ymult,yzero,inst):
    #print("\tgetCurve():START")
    #inst.write(":DAT:SOU " + channel)
    #inst.write("DAT:STAR 1")
    #inst.write("DAT:STOP 10000")
    #inst.write("DAT:ENC RPB")
    #inst.write('CURVE?')
    Send(inst, "w", ":DAT:SOU " + channel, 10)
    Send(inst, "w", "DAT:STAR 1", 10)
    Send(inst, "w", "DAT:STOP 10000", 10)
    Send(inst, "w", "DAT:ENC RPB", 10)
    Send(inst, "w", "CURVE?", 10)
    data = inst.read_raw()
    headerlen = 2 + int(data[1])
    header = data[:headerlen]
    ADC_wave = data[headerlen:-1]

    ADC_wave = np.array(unpack('%sB' % len(ADC_wave),ADC_wave))
    Volts = (ADC_wave - yoff) * ymult + yzero
    #print("\tgetCurve():END\n")
    return Volts;

def writeFile(spice, gfile, sp, gf, Volts, xincr, toff):
    #print("\twriteFile():START")
    Time = np.arange(0, xincr* len(Volts), xincr) + toff
    toff = Time[len(Time)-1]

    for i in range(0,len(Volts)):
        if sp:
            #SPICE
            spice.write(str(Time[i]))
            spice.write(",")
            spice.write(str(Volts[i]))
            spice.write(",")

        if gf:
            #GFILE
            gfile.write(str(Volts[i]))
            gfile.write(",")

    if gf:
        gfile.write("0\n")
    #print("\twriteFile():END\n")
    return;

def Send(inst, commandType, command, tries):
    waittime = .1; #In Seconds
    exCount = 0
    #errorResp = ""
    time.sleep(waittime)
    while 1:
        try:
            if commandType == "q":
                resp = inst.query(command)
                #errorResp = resp
            if commandType == "w":
                resp = inst.write(command)
                #errorResp = resp
            if commandType == "r":
                resp = inst.read()
                #errorResp = resp
            break
        except visa.VisaIOError as e:
            exCount += 1
            if exCount >= tries:
                print("ERROR: VisaIOError\nDetails: " +str(e.args)+ "\n\nERRORED COMMAND: "+ commandType + "(" + command + ")")
                print("ERROR CYCLES: " + str(exCount))
                #print("DEVICE RESPONSE: " + str(errorResp))
                inst.close()
                quit()
                
        else:
            exCount = 0
            break
    return resp;

#MAIN
rm = visa.ResourceManager()
print("Available Scopes")
print(rm.list_resources())
inst = rm.open_resource(rm.list_resources()[0])
inst.baud_rate = 57600
#print(inst.query("*IDN?"))
print(Send(inst, "q", "*IDN?", 10))
print(str(inst.session))
print("CONNECTED\n")

FILENAME = "Multichannel_Test"
spiceExt = ".pwl"
genericExt = ".dat"
Run = 2

print("File Name: " + FILENAME + "\tRUN #: " + str(Run) + "\n")

CH1 = 1
CH2 = 1
CH3 = 0
CH4 = 0

if CH1:
    print("CHANNEL 1: ACTIVE")
    Send(inst, "w", ":SELECT:CH1 ON", 10)
else:
    print("CHANNEL 1: INACTIVE")
    Send(inst, "w", ":SELECT:CH1 OFF", 10)
if CH2:
    print("CHANNEL 2: ACTIVE")
    Send(inst, "w", ":SELECT:CH2 ON", 10)
else:
    print("CHANNEL 2: INACTIVE")
    Send(inst, "w", ":SELECT:CH2 OFF", 10)
if CH3:
    print("CHANNEL 3: ACTIVE")
    Send(inst, "w", ":SELECT:CH3 ON", 10)
else:
    print("CHANNEL 3: INACTIVE")
    Send(inst, "w", ":SELECT:CH3 OFF", 10)
if CH4:
    print("CHANNEL 4: ACTIVE")
    Send(inst, "w", ":SELECT:CH4 ON", 10)
else:
    print("CHANNEL 4: INACTIVE")
    Send(inst, "w", ":SELECT:CH4 OFF", 10)


plot = 0
count = 0
TraceCount = 10
sp = 1
gf = 1
toff = 0

#SET ACQ
#inst.write("ACQ:STATE RUN")

#TAKE TRACE
#ymult = float(inst.query('WFMPRE:YMULT?'))
#yzero = float(inst.query('WFMPRE:YZERO?'))
#yoff = float(inst.query('WFMPRE:YOFF?'))
#xincr = float(inst.query('WFMPRE:XINCR?'))
ymult = float(Send(inst, "q", "WFMPRE:YMULT?", 10))
yzero = float(Send(inst, "q", "WFMPRE:YZERO?", 10))
yoff = float(Send(inst, "q", "WFMPRE:YOFF?", 10))
xincr = float(Send(inst, "q", "WFMPRE:XINCR?", 10))

if sp:
    if CH1:
        spice1 = open(FILENAME + "_CH1_" + str(Run) + spiceExt, "w")
    if CH2:
        spice2 = open(FILENAME + "_CH2_" + str(Run) + spiceExt, "w")
    if CH3:
        spice3 = open(FILENAME + "_CH3_" + str(Run) + spiceExt, "w")
    if CH4:
        spice4 = open(FILENAME + "_CH4_" + str(Run) + spiceExt, "w")
if gf:
    if CH1:
        gfile1 = open(FILENAME + "_CH1_" + str(Run) + genericExt, "w")
        gfile1.write("XINCR=" + str(xincr) + "\tTRACELENGTH=" + str(int(inst.query("DAT:STOP?"))-int(inst.query("DAT:STAR?")) - 47) + "\n")
    if CH2:
        gfile2 = open(FILENAME + "_CH2_" + str(Run) + genericExt, "w")
        gfile2.write("XINCR=" + str(xincr) + "\tTRACELENGTH=" + str(int(inst.query("DAT:STOP?"))-int(inst.query("DAT:STAR?")) - 47) + "\n")
    if CH3:
        gfile3 = open(FILENAME + "_CH3_" + str(Run) + genericExt, "w")
        gfile3.write("XINCR=" + str(xincr) + "\tTRACELENGTH=" + str(int(inst.query("DAT:STOP?"))-int(inst.query("DAT:STAR?")) - 47) + "\n")
    if CH4:
        gfile4 = open(FILENAME + "_CH4_" + str(Run) + genericExt, "w")
        gfile4.write("XINCR=" + str(xincr) + "\tTRACELENGTH=" + str(int(inst.query("DAT:STOP?"))-int(inst.query("DAT:STAR?")) - 47) + "\n")

print("Files Open\nHeaders Writen")
print("START ACQ")
#Send(inst, "w", "ACQ:STATUS RUN", 10)
Send(inst, "w", "ACQ:STATE ON", 10)
Send(inst, "w", "ACQ:STOPA SEQ", 10)
while count < TraceCount:
    count += 1
    #inst.write("ACQ:STOPA SEQ")
    while Send(inst, "q", "BUSY?", 10) == 1:
            #Wait until not busy
            print("BUSY: " + str(Send(inst, "q", "BUSY?", 10)))
            print("BUSY... STATUS ON")
    Send(inst, "w", "ACQ:STATE ON", 10)
    #print("TRACE COUNT: " +str(count))
    if CH1:
        #print("CALL: getCurve(CH1)")
        while Send(inst, "q", "BUSY?", 10) == 1:
            #Wait until not busy
            print("BUSY: " + str(Send(inst, "q", "BUSY?", 10)))
            print("BUSY... CH1")
        V1 = getCurve("CH1",yoff,ymult,yzero,inst)        
        writeFile(spice1, gfile1, sp, gf, V1, xincr, toff)
        #print("CALL: writeFile(CH1)")
    if CH2:
        while Send(inst, "q", "BUSY?", 10) == 1:
            #Wait until not busy
            print("BUSY: " + str(Send(inst, "q", "BUSY?", 10)))
            print("BUSY... CH2")
        V2 = getCurve("CH2",yoff,ymult,yzero,inst)
        #print("CALL: getCurve(CH2)")
        writeFile(spice2, gfile2, sp, gf, V2, xincr, toff)
        #print("CALL: writeFile(CH2)")
    if CH3:
        while Send(inst, "q", "BUSY?", 10) == 1:
            #Wait until not busy
            print("BUSY: " + str(Send(inst, "q", "BUSY?", 10)))
            print("BUSY... CH3")
        V3 = getCurve("CH3",yoff,ymult,yzero,inst)
        #print("CALL: getCurve(CH3)")
        writeFile(spice3, gfile3, sp, gf, V3, xincr, toff)
        #print("CALL: writeFile(CH3)")
    if CH4:
        while Send(inst, "q", "BUSY?", 10) == 1:
            #Wait until not busy
            print("BUSY: " + str(Send(inst, "q", "BUSY?", 10)))
            print("BUSY... CH1")
        V4 = getCurve("CH4",yoff,ymult,yzero,inst)
        #print("CALL: getCurve(CH4)")
        writeFile(spice4, gfile4, sp, gf, V4, xincr, toff)
        #print("CALL: writeFile(CH4)")
    #inst.write("ACQ:STATUS RUN")
    #inst.write("ACQ:STOPA RUNST")      

print("STOP ACQ")
if sp:
    if CH1:
        spice1.close()
    if CH2:
        spice2.close()
    if CH3:
        spice3.close()
    if CH4:
        spice4.close()
if gf:
    if CH1:
        gfile1.close()
    if CH2:
        gfile2.close()
    if CH3:
        gfile3.close()
    if CH4:
        gfile4.close()

inst.close()
print("FILES CLOSED")



