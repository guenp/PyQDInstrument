# PyQDInstrument #

Python driver for the Quantum Design Physical Property Measurement System (PPMS®) cryostat.

# Requirements #

- IronPython
- PPMS C# library from [here](https://www.qdusa.com/sitedocs/appNotes/general/QDInstrument_LabView.zip)

# Usage #

- Run the QDInstrument_Server.exe program on the PPMS control PC.
- Copy the `QDInstrument.DLL` file to the IronPython DLL folder.
- Open an IronPython console on a measurement PC (Windows) that can access the control PC's port on which the server can be contacted.
- Add PyQDInstrument to the pythonpath or add an `pqi\__init__.py` file with 

```python
import sys
sys.path.append('C:\whatever\My-PyQDInstrument-directory')
from PyQDInstrument import *
```
- Then start a QDInstrument server:

```python
import pqi
pqi.run_server(HOST, PORT, PPMS_IP, PPMS_PORT)
```
you can find the PPMS_PORT in the ```QDInstrument_Server.exe``` program.

- Open your favorite Python distribution on a (remote) PC/Mac and run e.g.

```python
import PyQDInstrument as pqi
ppms = pqi.RemotePPMS(HOST, PORT)
#get temperature
ppms.temperature
#set temperature
ppms.temperature_rate = 20
ppms.temperature = 200
```

...etcetera. Attributes represent the system control parameters:

- ```temperature```: get/set the system temperature.
- ```temperature_rate```: get/set the temperature ramp rate. Default = 10.
- ```temperature_approach```: get/set the temperature ramp method. Options are: 'FastSettle' (default), 'NoOverShoot'.
- ```field```: get/set the system magnetic field.
- ```field_rate```: get/set the field ramp rate. Default = 100.
- ```field_approach```: get/set the field ramp method. Options are: 'Linear' (default), 'NoOverShoot', 'Oscillate'.
- ```field_mode```: get/set the field ramp mode. Options are: 'Persistent' (default), 'Driven'.
- ```temperature_status```: get the temperature status message.
- ```field_status```: get the field status message.
- ```chamber```: get the chamber status message.

Or, if you really wish, connect to the socket via your own data acquisition software.
Send string commands to the socket in the form ```"temperature"``` or ```"temperature = 200"```.

Pull requests are welcome.

Please cite this repo if used in academia.

Have fun!
