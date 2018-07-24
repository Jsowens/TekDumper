Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:06:47) [MSC v.1914 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> 
 RESTART: C:\Users\knotw\AppData\Local\Programs\Python\Python37-32\Scripts\tekTrace.py 
Available Scopes
('USB::0x0699::0x0401::C001256::INSTR',)
TEKTRONIX,MSO4034,C001256,CF:91.1CT FV:v2.68 
CONNECTED

File Name: Multichannel_Test	RUN #: 1

CHANNEL 1: ACTIVE
ERROR: Visa Timeout Exeption
Details: w(SELECT:CH1 on)
>>> 
 RESTART: C:\Users\knotw\AppData\Local\Programs\Python\Python37-32\Scripts\tekTrace.py 
Available Scopes
('USB::0x0699::0x0401::C001256::INSTR',)
TEKTRONIX,MSO4034,C001256,CF:91.1CT FV:v2.68 
CONNECTED

File Name: Multichannel_Test	RUN #: 1

CHANNEL 1: ACTIVE
ERROR: Visa Timeout Exeption
Details: w(:SELECT:CH1 on)
>>> import visa
>>> rm = visa.ResourceManager()
>>> inst = rm.open_resource(rm.list_resources()[0])
>>> message = inst.query("HSNE:ENE?")
Traceback (most recent call last):
  File "<pyshell#3>", line 1, in <module>
    message = inst.query("HSNE:ENE?")
  File "C:\Users\knotw\AppData\Local\Programs\Python\Python37-32\lib\site-packages\pyvisa\resources\messagebased.py", line 564, in query
    return self.read()
  File "C:\Users\knotw\AppData\Local\Programs\Python\Python37-32\lib\site-packages\pyvisa\resources\messagebased.py", line 413, in read
    message = self._read_raw().decode(enco)
  File "C:\Users\knotw\AppData\Local\Programs\Python\Python37-32\lib\site-packages\pyvisa\resources\messagebased.py", line 386, in _read_raw
    chunk, status = self.visalib.read(self.session, size)
  File "C:\Users\knotw\AppData\Local\Programs\Python\Python37-32\lib\site-packages\pyvisa\ctwrapper\functions.py", line 1584, in read
    ret = library.viRead(session, buffer, count, byref(return_count))
  File "C:\Users\knotw\AppData\Local\Programs\Python\Python37-32\lib\site-packages\pyvisa\ctwrapper\highlevel.py", line 188, in _return_handler
    raise errors.VisaIOError(ret_value)
pyvisa.errors.VisaIOError: VI_ERROR_TMO (-1073807339): Timeout expired before operation completed.
>>> message
Traceback (most recent call last):
  File "<pyshell#4>", line 1, in <module>
    message
NameError: name 'message' is not defined
>>> 
 RESTART: C:\Users\knotw\AppData\Local\Programs\Python\Python37-32\Scripts\tekTrace.py 
Available Scopes
('USB::0x0699::0x0401::C001256::INSTR',)
TEKTRONIX,MSO4034,C001256,CF:91.1CT FV:v2.68 
CONNECTED

File Name: Multichannel_Test	RUN #: 1

CHANNEL 1: ACTIVE
ERROR: Visa Timeout Exeption
Details: w(:SELECT:CH1 on)
>>> inst.close()
>>> inst.session()
Traceback (most recent call last):
  File "<pyshell#6>", line 1, in <module>
    inst.session()
  File "C:\Users\knotw\AppData\Local\Programs\Python\Python37-32\lib\site-packages\pyvisa\resources\resource.py", line 100, in session
    raise errors.InvalidSession()
pyvisa.errors.InvalidSession: Invalid session handle. The resource might be closed.
>>> 
 RESTART: C:\Users\knotw\AppData\Local\Programs\Python\Python37-32\Scripts\tekTrace.py 
Available Scopes
('USB::0x0699::0x0401::C001256::INSTR',)
TEKTRONIX,MSO4034,C001256,CF:91.1CT FV:v2.68 
Traceback (most recent call last):
  File "C:\Users\knotw\AppData\Local\Programs\Python\Python37-32\Scripts\tekTrace.py", line 85, in <module>
    print(inst.session())
TypeError: 'int' object is not callable
>>> 
 RESTART: C:\Users\knotw\AppData\Local\Programs\Python\Python37-32\Scripts\tekTrace.py 
Available Scopes
('USB::0x0699::0x0401::C001256::INSTR',)
TEKTRONIX,MSO4034,C001256,CF:91.1CT FV:v2.68 
Traceback (most recent call last):
  File "C:\Users\knotw\AppData\Local\Programs\Python\Python37-32\Scripts\tekTrace.py", line 85, in <module>
    print(str(inst.session()))
TypeError: 'int' object is not callable
>>> 
 RESTART: C:\Users\knotw\AppData\Local\Programs\Python\Python37-32\Scripts\tekTrace.py 
Available Scopes
('USB::0x0699::0x0401::C001256::INSTR',)
TEKTRONIX,MSO4034,C001256,CF:91.1CT FV:v2.68 
130319080
CONNECTED

File Name: Multichannel_Test	RUN #: 1

CHANNEL 1: ACTIVE
ERROR: Visa Timeout Exeption
Details: w(:SELECT:CH1 on)
>>> inst.session
130319080
>>> 
 RESTART: C:\Users\knotw\AppData\Local\Programs\Python\Python37-32\Scripts\tekTrace.py 
Available Scopes
('USB::0x0699::0x0401::C001256::INSTR',)
TEKTRONIX,MSO4034,C001256,CF:91.1CT FV:v2.68 
129270504
CONNECTED

File Name: Multichannel_Test	RUN #: 1

CHANNEL 1: ACTIVE
ERROR: Visa Timeout Exeption
Details: w(:SELECT:CH1 on)
>>> inst.session
Traceback (most recent call last):
  File "<pyshell#8>", line 1, in <module>
    inst.session
  File "C:\Users\knotw\AppData\Local\Programs\Python\Python37-32\lib\site-packages\pyvisa\resources\resource.py", line 100, in session
    raise errors.InvalidSession()
pyvisa.errors.InvalidSession: Invalid session handle. The resource might be closed.
>>> inst = rm.open_resource(rm.list_resources()[0])
>>> isnt.session
Traceback (most recent call last):
  File "<pyshell#10>", line 1, in <module>
    isnt.session
NameError: name 'isnt' is not defined
>>> inst.session
129270504
>>> inst.write_termination
'\r\n'
>>> inst.CR
'\r'
>>> inst.LF
'\n'
>>> inst.read_termination
>>> print(inst.read_termination)
None
>>> inst.read_termination = '\r\n'
>>> print(inst.read_termination)


>>> 
 RESTART: C:\Users\knotw\AppData\Local\Programs\Python\Python37-32\Scripts\tekTrace.py 
Available Scopes
('USB::0x0699::0x0401::C001256::INSTR',)
TEKTRONIX,MSO4034,C001256,CF:91.1CT FV:v2.68 
145654504
CONNECTED

File Name: Multichannel_Test	RUN #: 1

CHANNEL 1: ACTIVE
ERROR: Visa Timeout Exeption
Details: w(:SELECT:CH1 on)
>>> 
 RESTART: C:\Users\knotw\AppData\Local\Programs\Python\Python37-32\Scripts\tekTrace.py 
Available Scopes
('USB::0x0699::0x0401::C001256::INSTR',)
TEKTRONIX,MSO4034,C001256,CF:91.1CT FV:v2.68 

141918952
CONNECTED

File Name: Multichannel_Test	RUN #: 1

CHANNEL 1: ACTIVE
ERROR: Visa Timeout Exeption
Details: w(:SELECT:CH1 on)
>>> 
