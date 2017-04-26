from .utils import connect_socket, ask_socket, create_instrument, _HOST, _PORT
import socket

class PPMS(object):
    '''
    Wrapper for talking to the C# library for controlling the Quantum Design PPMS.
    Make sure to run QDInstrument_Server.exe on the control PC.
    host, port = IP address and port of the control PC.
    '''
    def __init__(self, host=_HOST, port=_PORT):
        super(PPMS, self).__init__()
        self._temperature = 300
        self._temperature_status = ''
        self.temperature_rate = 10
        self.temperature_approach = 'FastSettle'
        self._field = 0
        self._field_status = '' #Charging (6), CoolingSwitch (3), CurrentError (8), Discharging (7), Iterating (5), MagnetFailure (15), MagnetUnknown (0), StableDriven (4), StablePersistent (1), Unused10 (10), Unused11 (11), Unused12 (12), Unused13 (13), Unused14 (14), Unused9 (9), WarmingSwitch (2)
        self.field_rate = 100
        self.field_approach = 'Linear'
        self.field_mode = 'Persistent'
        self._position = 0
        self.position_approach = 0 # 0 is go to setpoint
        self.position_speed = 0 # 0 is fastest, 14 is slowest
        self._chamber = ''
        self.ins = create_instrument(host, port)
        self._temperature_approach_dict = {'FastSettle': self.ins.TemperatureApproach.FastSettle, 'NoOvershoot': self.ins.TemperatureApproach.NoOvershoot}
        self._field_approach_dict = {'Linear': self.ins.FieldApproach.Linear, 'NoOvershoot': self.ins.FieldApproach.NoOvershoot, 'Oscillate': self.ins.FieldApproach.Oscillate}
        self._field_mode_dict = {'Driven': self.ins.FieldMode.Driven, 'Persistent': self.ins.FieldMode.Persistent}

    @property
    def temperature(self):
        ret = self.ins.GetTemperature(0,0)
        self._temperature = ret[1]
        self._temperature_status = str(ret[2])
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self.ins.SetTemperature(value, self.temperature_rate, self._temperature_approach_dict[self.temperature_approach])

    @property
    def temperature_status(self):
        self.temperature
        return self._temperature_status
    
    @property
    def field(self):
        ret = self.ins.GetField(0,0)
        self._field = ret[1]
        self._field_status = str(ret[2])
        return self._field

    @field.setter
    def field(self, value):
        self.ins.SetField(value, self.field_rate, self._field_approach_dict[self.field_approach], self._field_mode_dict[self.field_mode])

    @property
    def field_status(self):
        self.field
        return self._field_status

    @property
    def chamber(self):
        self._chamber = str(self.ins.GetChamber(0)[1])
        return self._chamber

    @property
    def position(self):
        ret = self.ins.GetPPMSItem(3,0,True)
        self._position = ret[1]
        return self._position

    @position.setter
    def position(self,angle):
        if self.position_speed>14 :
            self.position_speed = 14
        if self.position_speed < 0 :
            self.position_speed = 0
        commandstring = 'MOVE '+str(angle)+' 0 '+ str(self.position_speed)
        self.ins.SendPPMSCommand(commandstring,"","",0,0)

class RemotePPMS(object):
    '''
    For remote operation of the Quantum Design PPMS.
    Make sure to run PyQDInstrument.run_server() in an IronPython console on a machine that can connect to the PPMS control PC's QDInstrument_Server.exe program.
    Attributes represent the system control parameters:
    'temperature', 'temperature_rate', 'temperature_approach', 'field', 'field_rate', 'field_approach', 'field_mode', 'temperature_status', 'field_status', 'chamber',
    'position', 'position_speed'
    '''
    def __init__(self, host, port, s=None, name='ppms'):
        self._name = name
        if s == None:
            self._s = connect_socket(host, port)
        else:
            self._s = s
        for param in ['temperature', 'temperature_rate', 'field', 'field_rate', 'temperature_approach', 'field_approach', 'field_mode', 'position', 'position_speed']:
            setattr(RemotePPMS,param,property(fget=eval("lambda self: self._get_param('%s')" %param),
                                                fset=eval("lambda self, value: self._set_param('%s',value)" %param)))
        for param in ['temperature_status', 'field_status', 'chamber']:
            setattr(RemotePPMS,param,property(fget=eval("lambda self: self._get_param('%s')" %param)))
        self._params = ['temperature', 'temperature_rate', 'temperature_approach', 'field', 'field_rate', 'field_approach', 'field_mode', 'position', 'position_speed', 'temperature_status', 'field_status', 'chamber']

    def _get_param(self, param):
        return ask_socket(self._s, param)

    def _set_param(self, param, value):
        if type(value) == str:
            cmd = "%s = '%s'" %(param, value)
        else:
            cmd = '%s = %s' %(param, value)
        return ask_socket(self._s, cmd)

    def _repr_html_(self):
        '''
        Show a pretty HTML representation of the object for ipynb.
        '''
        html = ["<b>",self._name,"</b> - "]
        html.append(self.__doc__)
        html.append("<table width=100%>")
        for key in self._params:
            html.append("<tr>")
            html.append("<td>{0}</td>".format(key))
            html.append("<td>{0}</td>".format(getattr(self,key)))
            html.append("</tr>")
        html.append("</table>")
        return ''.join(html)