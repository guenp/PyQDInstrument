import socket
from .pqdinstrument import PPMS

def run_server(host='', port=0, instrument_host='', instrument_port=11000, verbose=True):
    server = Server(host, port, instrument_host, instrument_port)
    server.run(verbose)

class Server():
    '''
    Server for connecting remotely to the IronPython console.
    '''
    def __init__(self, remote_host, remote_port, instrument_host, instrument_port):
        self.HOST = remote_host
        self.PORT = remote_port
        self.ppms = PPMS(instrument_host, instrument_port)

    def run(self, verbose=False):
        '''Run a measurement server for remote communication.'''
        ppms = self.ppms
        while True:
        	print('Creating socket at %s:%s...' %(self.HOST, self.PORT))
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
	                cmd = b'ppms.' + cmd
	                if verbose: print(cmd.decode())
	                if b'=' in cmd:
	                    exec(cmd)
	                    response = 'True'
	                else:
	                    response = str(eval(cmd))
	                conn.sendall(response.encode())
	            except (SyntaxError, NameError, AttributeError):
	                conn.sendall(b'Command not recognized.')
	        conn.close()