import clr
import socket

def run_server(host='', port=50008, instrument_host='192.168.0.101', instrument_port=11000, verbose=True):
	server = Server(host, port, instrument_host, instrument_port)
	server.run(verbose)

def create_instrument(host, port):
		'''Create remote QDInstrument'''
		import clr
		clr.AddReference('QDInstrument')
		from QuantumDesign import QDInstrument
		ppms = QDInstrument.QDInstrumentBase.QDInstrumentType.PPMS
		ins = QDInstrument.QDInstrumentFactory.GetQDInstrument(ppms, True, host, port)
		return ins

class Server():
	def __init__(self, host, port, instrument_host, instrument_port):
		self.HOST = host
		self.PORT = port
		self.ins = create_instrument(instrument_host,instrument_port)	

	def run(self, verbose=False):
	    '''Run a measurement server for remote communication.'''
	    ins = self.ins
	    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	    s.bind((self.HOST, self.PORT))
	    s.listen(1)
	    conn, addr = s.accept()
	    print('Connected by', addr)
	    while True:
	        cmd = conn.recv(1024)
	        if not cmd: break
	        try:
	            if verbose: print(cmd.decode())
	            conn.sendall(str(eval(cmd)).encode())
	        except (SyntaxError, NameError, AttributeError):
	            conn.sendall(b'Command not recognized.')
	    conn.close()