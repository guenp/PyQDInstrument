import ConfigParser

config = ConfigParser.SafeConfigParser()
config.readfp(open('example.cfg'))
_HOST = config.get('PyQDInstrument', 'host')
_PORT = int(config.get('PyQDInstrument', 'port'))
_REMOTE_HOST = config.get('PyQDInstrument', 'remote_host')
_REMOTE_PORT = int(config.get('PyQDInstrument', 'remote_port'))

def ask_socket(s, cmd):
    '''query socket and return response'''
    import select
    #empty socket buffer
    inputready, o, e = select.select([s],[],[], 0.0)
    if len(inputready)>0:
        for s in inputready: s.recv(1)
    s.sendall(cmd.encode())
    data = s.recv(1024)
    try:
        ans = eval(data)
    except (IndentationError, SyntaxError):
        ans = data.decode()
    return ans

def create_instrument(host, port):
    '''Create remote QDInstrument'''
    import clr
    clr.AddReference('QDInstrument')
    from QuantumDesign import QDInstrument
    ppms = QDInstrument.QDInstrumentBase.QDInstrumentType.PPMS
    ins = QDInstrument.QDInstrumentFactory.GetQDInstrument(ppms, True, host, port)
    return ins