from .utils import ask_socket, create_instrument, _HOST, _PORT

class Instrument(object):
    '''
    Instrument base class
    '''
    def __init__(self, name, *args, **kwargs):
        params = []
        for key in vars(self).keys():
            if key[0]=='_':
                params.append(key[1:])
        self.params = params
        self.name = name
        super(Instrument, self).__init__()
        
    def _repr_html_(self):
        '''
        Show a pretty HTML representation of the object for ipynb.
        '''
        html = ["<b>",self.name,"</b> - "]
        html.append(self.__doc__)
        html.append("<table width=100%>")
        for key in self.params:
            html.append("<tr>")
            html.append("<td>{0}</td>".format(key))
            html.append("<td>{0}</td>".format(getattr(self,key)))
            html.append("</tr>")
        html.append("</table>")
        return ''.join(html)

class PPMS(Instrument):
    '''
    Wrapper for talking to the C# library for controlling the Quantum Design PPMS.
    Make sure to run QDInstrument server .exe on the control PC.
    host, port = remote IP address and port.
    '''
    def __init__(self, host=_HOST, port=_PORT):
        self._temperature = 300
        self._temperature_status = ''
        self.temperature_rate = 10
        self.temperature_approach = 0 #FastSettle (0), NoOvershoot (1)
        self._field = 0
        self._field_status = ''
        self.field_rate = 100
        self.field_approach = 0 #Linear (0), NoOvershoot (1), Oscillate (2)
        self.field_mode = 0 #Driven (1), Persistent (0)
        self._chamber = ''
        self.ins = create_instrument(host, port)
        super(PPMS, self).__init__('ppms')

    @property
    def temperature(self):
        ret = self.ins.GetTemperature(0,0)
        self._temperature = ret[1]
        self._temperature_status = str(ret[2])
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self.ins.SetTemperature(value, self.temperature_rate, self.temperature_approach)

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
        self.ins.SetField(value, self.field_rate, self.field_approach, self.field_mode)

    @property
    def field_status(self):
        self.field
        return self._field_status

    @property
    def chamber(self):
        self._chamber = str(self.ins.GetChamber(0)[1])
        return self._chamber