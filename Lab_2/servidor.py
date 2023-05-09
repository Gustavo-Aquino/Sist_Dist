#servidor de echo: lado servidor
#com finalizacao do lado do servidor
#com multithreading (usa join para esperar as threads terminarem apos digitar 'fim' no servidor)
import socket
import select
import sys
import threading
import json

# define a localizacao do servidor
HOST = '' # vazio indica que podera receber requisicoes a partir de qq interface de rede da maquina
PORT = 8000  # porta de acesso

#define a lista de I/O de interesse (jah inclui a entrada padrao)
entradas = [sys.stdin]
#armazena historico de conexoes 
conexoes = {}
#lock para acesso do dicionario 'conexoes'
lock = threading.Lock()
#armazena o dicionario utilizado
try:
    with open("server_dict.txt", "r") as file:
        server_dict = json.load(file)
except json.JSONDecodeError:
    server_dict = {}
except FileNotFoundError:
    server_dict = {}

def iniciaServidor():
	'''Cria um socket de servidor e o coloca em modo de espera por conexoes
	Saida: o socket criado'''
	# cria o socket 
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet( IPv4 + TCP) 

	# vincula a localizacao do servidor
	sock.bind((HOST, PORT))

	# coloca-se em modo de espera por conexoes
	sock.listen(5) 

	# configura o socket para o modo nao-bloqueante
	sock.setblocking(False)

	# inclui o socket principal na lista de entradas de interesse
	entradas.append(sock)

	return sock

def aceitaConexao(sock):
	'''Aceita o pedido de conexao de um cliente
	Entrada: o socket do servidor
	Saida: o novo socket da conexao e o endereco do cliente'''

	# estabelece conexao com o proximo cliente
	clisock, endr = sock.accept()

	# registra a nova conexao
	conexoes[clisock] = endr 

	return clisock, endr

def atendeRequisicoes(clisock, endr):
	while True:
		#recebe dados do cliente
		data = str(clisock.recv(1024), encoding='utf-8').split()
		if not data: # dados vazios: cliente encerrou
			print(str(endr) + '-> encerrou')
			clisock.close() # encerra a conexao com o cliente
			return
		elif (data[0] == 'consult'):
			if not len(data) == 2:
				clisock.send('Erro da instrucao, atente a apenas informar uma chave (sem espacos)'.encode())
				continue
			# acesso a area de dados
			lock.acquire()
			try:
				values = sorted(server_dict[data[1]])
			except KeyError:
				values = ['']
			lock.release()
			# envia os valores da chave ('' se nao houver a chave)
			clisock.send(str(values).encode())
			continue
		elif (data[0] == 'write'):
			if not len(data) == 3:
				clisock.send('Erro da instrucao, atente a apenas informar uma chave e seu valor (com um espaco entre eles)'.encode())
				continue
			# acesso a area de dados
			lock.acquire()
			if (data[1] in server_dict):
				server_dict[data[1]].append(data[2])
				clisock.send('Atualizada a lista de valores da chave'.encode())
			else:
				server_dict[data[1]] = []
				server_dict[data[1]].append(data[2])
				clisock.send('Criada um novo par de chave e valores'.encode())
			lock.release()
			continue
        
def atendeAdmin(sock, clientes):
	cmd = input()

	if cmd == 'fim': #solicitacao de finalizacao do servidor
		for c in clientes: #aguarda todas as threads terminarem
			c.join()
		sock.close()
		with open("server_dict.txt", "w") as file:
			json.dump(server_dict, file)
		sys.exit()
	elif cmd == 'hist':
		print(str(conexoes.values()))
	elif cmd == 'remove':
		lock.acquire()
		key = input('Chave a ser removida do dicionario: ')
		if(key in server_dict): 
			del server_dict[key]
			print('Chave removida com sucesso')
		else:
			print('Chave inexistente, as chaves atuais sao: {}'.format(list(server_dict.keys())))
			print('(digite remove novamente para tentar outra opcao)')
		lock.release()

def print_admin_welcome():
	print("Bem vindo, voce e o administrador desde sistema\nSeus possiveis comandos sao os seguintes:\n-fim (espera os clientes ativos encerrarem e fecha o servidor)\n-remove (entra na interface para a remocao de uma chave)\n-hist (historico de conecxoes estabelecidas)")
	
def main():
	'''Inicializa e implementa o loop principal (infinito) do servidor'''
	clientes=[] #armazena as threads criadas para fazer join
	sock = iniciaServidor()
	print_admin_welcome()
	while True:
		#espera por qualquer entrada de interesse
		leitura, escrita, excecao = select.select(entradas, [], [])
		#tratar todas as entradas prontas
		for pronto in leitura:
			if pronto == sock:  #pedido novo de conexao
				clisock, endr = aceitaConexao(sock)
				print ('Conectado com: ', endr)
				#cria nova thread para atender o cliente
				cliente = threading.Thread(target=atendeRequisicoes, args=(clisock,endr))
				cliente.start()
				clientes.append(cliente) #armazena a referencia da thread para usar com join()
			elif pronto == sys.stdin: #entrada padrao
				atendeAdmin(sock, clientes)



main()