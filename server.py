import clr
import socket

def run_server(host='192.168.0.103', port=50008, instrument_host='192.168.0.101', instrument_port=11000, verbose=True):
	server = Server(host, port, instrument_host, instrument_port)
	server.run(verbose)

class Server():
	def __init__(self, host, port, instrument_host, instrument_port):
		self.host = host
		self.port = port
		self.ins = self.create_instrument(instrument_host,instrument_port)

	def create_instrument(self, host, port):
		'''Create remote QDInstrument'''
		import clr
		clr.AddReference('QDInstrument')
		from QuantumDesign import QDInstrument
		ppms = QDInstrument.QDInstrumentBase.QDInstrumentType.PPMS
		ins = QDInstrument.QDInstrumentFactory.GetQDInstrument(ppms, True, host, port)
		return ins

	def run(self, verbose=False):
	    '''Run a measurement server for remote communication.'''
	    ins = self.ins

	    HOST = self.host                 # Symbolic name meaning all available interfaces
	    PORT = self.port              # Arbitrary non-privileged port
	    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	    s.bind((HOST, PORT))
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