#servidor de echo: lado cliente
import socket

HOST = 'localhost' # maquina onde esta o servidor
PORT = 8000       # porta que o servidor esta escutando

information_interface = 'Bem vindo, voce e um cliente nesse sistema\nSuas possiveis interacoes sao as seguintes:\n- consult (entra na interface de consulta)\n- write (entra na interface de escrita)\n- fim (encerra a conexao com o servidor)\n- help (mostra novamente esta mensagem)\n'

def iniciaCliente():
	'''Cria um socket de cliente e conecta-se ao servidor.
	Saida: socket criado'''
	# cria socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet (IPv4 + TCP) 

	# conecta-se com o servidor
	sock.connect((HOST, PORT)) 

	return sock

def fazRequisicoes(sock):
	'''Faz requisicoes ao servidor e exibe o resultado.
	Entrada: socket conectado ao servidor'''
	# le as mensagens do usuario ate ele digitar 'fim'
	while True: 
		comando = input("Digite um comando:")
		if comando == 'fim': break 
		elif (len(comando.encode('utf-8')) > 1024):
			print('Mensagem passou o limite do sistema (1024 bytes)')
			continue
		elif (comando == 'consult'):
			key = input('Digite a chave a ser consultada (apenas a chave):\n')
			msg = 'consult '+key
			sock.send(msg.encode())
		elif (comando == 'write'):
			key_value = input('Digite o par chave valor (apenas uma chave e um valor com um espaco entre eles)\n')
			msg = 'write '+key_value
			sock.send(msg.encode())
		elif (comando == 'help'):
			print(information_interface)
			continue
		else: 
			print('Comando nao reconhecido')
			continue

		#espera a resposta do servidor
		msg = sock.recv(1024) 
		# imprime a mensagem recebida
		print(str(msg, encoding='utf-8'))

	# encerra a conexao
	sock.close()

def main():
	'''Funcao principal do cliente'''
	#inicia o cliente
	sock = iniciaCliente()
	print(information_interface)
	#interage com o servidor ate encerrar
	fazRequisicoes(sock)

main()