#SETUP

import visa
import numpy as np
from struct import unpack
import pylab
import ROOT as root
from ROOT import gROOT, TCanvas

#FUNCTIONS
def getCurve(channel,inst):
    #This function read a trace from a channel. Both the channel number in a string format ("CH1"), and the instrument object must be passed in.

    #Sets data acquisition parameters
    Send(inst, "w", ":DAT:SOU " + channel, 10)
    Send(inst, "w", "DAT:STAR 1", 10)
    Send(inst, "w", "DAT:STOP 10000", 10)
    Send(inst, "w", "DAT:ENC RPB", 10)    

    #Gets curve scaling and positioning
    ymult = float(Send(inst, "q", "WFMPRE:YMULT?", 10))
    yzero = float(Send(inst, "q", "WFMPRE:YZERO?", 10))
    yoff = float(Send(inst, "q", "WFMPRE:YOFF?", 10))
    
    #Gets waveform data (Most of this is borrowed code)
    Send(inst, "w", "CURVE?", 10)    
    data = inst.read_raw()
    headerlen = 2 + int(data[1])
    header = data[:headerlen]
    ADC_wave = data[headerlen:-1]

    ADC_wave = np.array(unpack('%sB' % len(ADC_wave),ADC_wave))
    Volts = (ADC_wave - yoff) * ymult + yzero
    
    return Volts;

def writeFile(spice, gfile, sp, gf, Volts, xincr, toff):
    #This function writes the trace to a file. spice and gfile are file objects. sp and gf are boolean values that indicate which file formats should be used. Volts is the curve. xincr and toff are time position and scaling variables.

    #Calculates the time axis
    Time = np.arange(0, xincr* len(Volts), xincr) + toff
    toff = Time[len(Time)-1]

    for i in range(0,len(Volts)):
        if sp:
            #Creates a file formate readable by LTspice
            spice.write(str(Time[i]) + "," + str(Volts[i]) + ",")
            
        if gf:
            #Creates a general purpose file without the time axis, but includes xincr in the header. This is used to create ROOT files with FillTree.C.
            gfile.write(str(Volts[i]) + ",")

    if gf:
        gfile.write("0\n") #Adds an extra point to the back of each trace. This is an easy way to take care of any errors produced by the trailing ",". This point is not included in the total points in the header, so it should not be read with standard indexing.
    
    return;

def Send(inst, commandType, command, tries):
    #This function is a wraper for sending and recieving commands and data from the device. It encases the commands in while try structure to protect the user from random errors. If too many errors occur it will print out an error message.
    #The instrument must be passed (inst). The command type can be "w" for write, "r" for read, or "q" for query (aka ask). command is the command to be passed to the scope. tries is how many time to attempt passing the command until an error is thrown.

    exCount = 0
    while 1:
        try:
            while inst.query("BUSY?") == 1: #Waits until the instrument is not busy to issue the next command 
                print("BUSY: " + inst.query("BUSY?"))
                print("BUSY...")
                
            if commandType == "q":
                resp = inst.query(command)
                
            else if commandType == "w":
                resp = inst.write(command)

            else if commandType == "r":
                resp = inst.read()

            else:
                resp = "ERROR: Incorrect commandType input. Use \"w\" for write, \"r\" for read, and \"q\" for query (aka ask)"

            break #If no error occur, break out of the while loop.
        except visa.VisaIOError as e:
            exCount += 1
            if exCount >= tries:
                print("ERROR: VisaIOError\nDetails: " +str(e.args)+ "\n\nERRORED COMMAND: "+ commandType + "(" + command + ")")
                print("ERROR CYCLES: " + str(exCount))
                
                inst.close()
                quit()
                
        else:
            exCount = 0
            break
    return resp;

def 


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

###################################################################################################################
##############################################FILENAME AND SETTINGS################################################
###################################################################################################################

#File Settings
FILENAME = "NoOpAmp_Co60_EJ276_5in_Teflon_CH1PMT_CH2SiPM"
Run = 3

#Channel settings: 1 - on, 0 - off
CH1 = 1
CH2 = 1
CH3 = 0
CH4 = 0

#Plot settings
TraceCount = 10 #The number of traces to record
sp = 0          #Output LTspice format file: 1 - yes, 0 - no
gf = 1          #Output general format file: 1 - yes, 0 - no
rf = 1          #Output ROOT format file: 1 - yes, 0 - no
dataSize = 16   #The number of bits each data point value is sent in 
###################################################################################################################
###################################################################################################################
###################################################################################################################

#Counting variables and file extensions. It is NOT advisable to change these values
#########################
toff = 0                #
count = 0               #
spiceExt = ".pwl"       #
genericExt = ".dat"     #
rootExt = ".root"       #
#########################


print("File Name: " + FILENAME + "\tRUN #: " + str(Run) + "\n")

#Turns on and off specified channels
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

#Get time increment of trace
xincr = float(Send(inst, "q", "WFMPRE:XINCR?", 10))

#Creats the proper file formats for each active channel
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

#Sets up acquisition
inst.write("WFMI:BIT_N " + str(dataSize))
Send(inst, "w", "ACQ:STATE ON", 10)
Send(inst, "w", "ACQ:STOPA SEQ", 10)
while count < TraceCount:
    count += 1
    Send(inst, "w", "ACQ:STATE ON", 10) #Trigger and freezes on next input trace

    #Gets the waveform for each active channel and saves it to its file 
    if CH1:
        V1 = getCurve("CH1",inst)        
        writeFile(spice1, gfile1, sp, gf, V1, xincr, toff)
        
    if CH2:
        V2 = getCurve("CH2",inst)
        writeFile(spice2, gfile2, sp, gf, V2, xincr, toff)
        
    if CH3:
        V3 = getCurve("CH3",inst)
        writeFile(spice3, gfile3, sp, gf, V3, xincr, toff)
        
    if CH4:
        V4 = getCurve("CH4",inst)
        writeFile(spice4, gfile4, sp, gf, V4, xincr, toff)     

print("STOP ACQ")

#Closes all open files and instruments
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



