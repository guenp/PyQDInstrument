_HOST = ''
_PORT = 50008
_REMOTE_HOST = ''
_REMOTE_PORT = 11000

def connect_socket(HOST, PORT):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s

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
    except (IndentationError, SyntaxError, NameError):
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