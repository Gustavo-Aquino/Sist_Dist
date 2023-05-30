# Servidor de echo usando RPC 
import rpyc
import threading
import json

#servidor que dispara um processo filho a cada conexao
from rpyc.utils.server import ForkingServer 

# porta de escuta do servidor de echo
PORTA = 10000

lock = threading.Lock()

def server_dictionary():
	try:
		with open('server_dict.txt', 'r') as file:
			server_dict = json.load(file)
	except json.JSONDecodeError:
		server_dict = {}
	except FileNotFoundError:
		server_dict = {}
	
	return server_dict
		

# classe que implementa o servico de echo
class Echo(rpyc.Service):
	# executa quando uma conexao eh criada
	def on_connect(self, conn):
		print("Conexao iniciada:")

	# executa quando uma conexao eh fechada
	def on_disconnect(self, conn):
		print("Conexao finalizada:")
	
	def exposed_consult(self, key):
		lock.acquire()
		try:
			values = sorted(server_dictionary()[key])
		except KeyError:
			values = ['']
		lock.release()

		return values
	
	def exposed_remove(self, key):
		lock.acquire()
		dictionary = server_dictionary()
		if(key in dictionary): 
			del dictionary[key]
			msg = 'Chave removida com sucesso'
			with open("server_dict.txt", "w") as file:
				json.dump(dictionary, file)
		else:
			msg = 'Chave inexistente, as chaves atuais sao: {}'.format(list(dictionary.keys()))
		lock.release()
		return msg
	
	def exposed_write(self, key, value):
		lock.acquire()
		dictionary = server_dictionary()
		if (key in dictionary):
			dictionary[key].append(value)
			msg = 'Atualizada a lista de valores da chave'
		else:
			dictionary[key] = []
			dictionary[key].append(value)
			msg = 'Criada um novo par de chave e valores'
		with open("server_dict.txt", "w") as file:
			json.dump(dictionary, file)
		lock.release()
		
		return msg
	
  
# dispara o servidor
if __name__ == "__main__":
	srv = ForkingServer(Echo, port = PORTA)
	srv.start()



